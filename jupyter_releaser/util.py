# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Of the form:
# https://github.com/{owner}/{repo}/releases/tag/{tag}
import atexit
import hashlib
import json
import os
import os.path as osp
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import warnings
from datetime import datetime
from glob import glob
from io import BytesIO
from pathlib import Path
from subprocess import PIPE, CalledProcessError, check_output
from urllib.parse import urlparse

import requests
import toml
from ghapi import core
from importlib_resources import files
from jsonschema import Draft4Validator as Validator
from packaging.version import Version
from packaging.version import parse as parse_version
from pkginfo import Wheel

from jupyter_releaser.tee import run as tee

PYPROJECT = Path("pyproject.toml")
SETUP_PY = Path("setup.py")
SETUP_CFG = Path("setup.cfg")
PACKAGE_JSON = Path("package.json")
MANIFEST = Path("MANIFEST.in")
YARN_LOCK = Path("yarn.lock")
JUPYTER_RELEASER_CONFIG = Path(".jupyter-releaser.toml")
METADATA_JSON = Path("metadata.json")

BUF_SIZE = 65536
TBUMP_CMD = "pipx run tbump --non-interactive --only-patch"

CHECKOUT_NAME = ".jupyter_releaser_checkout"
RELEASE_HTML_PATTERN = (
    "(?:https://github.com|%s)/(?P<owner>[^/]+)/(?P<repo>[^/]+)/releases/tag/(?P<tag>.*)"
)
RELEASE_API_PATTERN = (
    "https://api.github.com/repos/(?P<owner>[^/]+)/(?P<repo>[^/]+)/releases/tags/(?P<tag>.*)"
)

SCHEMA = files("jupyter_releaser").joinpath("schema.json").read_text()
SCHEMA = json.loads(SCHEMA)

GIT_FETCH_CMD = "git fetch origin --filter=blob:none --quiet"


def run(cmd, **kwargs):
    """Run a command as a subprocess and get the output as a string"""
    quiet_error = kwargs.pop("quiet_error", False)
    show_cwd = kwargs.pop("show_cwd", False)
    quiet = kwargs.get("quiet", False)
    echo = kwargs.pop("echo", False)

    if echo:
        prefix = "COMMAND"
        if show_cwd:
            prefix += f" (in '{os.getcwd()}')"
        prefix += ":"
        log(f"{prefix} {cmd}")

    if sys.platform.startswith("win"):
        # Async subprocesses do not work well on Windows, use standard
        # subprocess methods
        return _run_win(cmd, **kwargs)

    kwargs.setdefault("check", True)

    try:
        process = tee(cmd, **kwargs)
        return (process.stdout or "").strip()
    except CalledProcessError as e:
        if quiet and not quiet_error:
            if e.stderr:
                log("stderr:\n", e.stderr.strip(), "\n\n")
            if e.stdout:
                log("stdout:\n", e.stdout.strip(), "\n\n")
        raise e


def _run_win(cmd, **kwargs):
    """Run a command as a subprocess and get the output as a string"""
    quiet = kwargs.pop("quiet", False)

    if not quiet:
        kwargs.setdefault("stderr", PIPE)

    kwargs.setdefault("shell", True)

    parts = shlex.split(cmd)
    if "/" not in parts[0]:
        executable = shutil.which(parts[0])
        if not executable:
            raise CalledProcessError(1, f'Could not find executable "{parts[0]}"')
        parts[0] = normalize_path(executable)

    check = kwargs.pop("check", True)

    try:
        output = check_output(parts, **kwargs).decode("utf-8").strip()
        log(output)
        return output
    except CalledProcessError as e:
        e.output = e.output.decode("utf-8")
        if quiet:
            e.stderr = e.stderr.decode("utf-8")
            log("stderr:\n", e.stderr.strip(), "\n\n")
        log("stdout:\n", e.output.strip(), "\n\n")
        if check:
            raise e


def log(*outputs, **kwargs):
    """Log an output to stderr"""
    kwargs.setdefault("file", sys.stderr)
    print(*outputs, **kwargs)


def get_branch():
    """Get the appropriate git branch"""
    return run("git branch --show-current")


def get_default_branch():
    """Get the default remote branch"""
    info = run("git remote show origin")
    for line in info.splitlines():
        if line.strip().startswith("HEAD branch:"):
            return line.strip().split()[-1]


def get_repo():
    """Get the remote repo owner and name"""
    url = run("git remote get-url origin")
    url = normalize_path(url)
    parts = url.split("/")[-2:]
    if ":" in parts[0]:
        parts[0] = parts[0].split(":")[-1]
    parts[1] = parts[1].replace(".git", "")
    return "/".join(parts)


def get_version():
    """Get the current package version"""
    # Prefer to get a static version from pyproject.toml.
    if PYPROJECT.exists():
        text = PYPROJECT.read_text(encoding="utf-8")
        data = toml.loads(text)
        project = data.get("project", {})
        version = project.get("version")
        if version:
            return version

        # If this is a hatchling project, use hatch to get
        # the dynamic version.
        if data.get("build-system", {}).get("build-backend") == "hatchling.build":
            cmd = _get_hatch_version_cmd()
            return run(cmd).split("\n")[-1]

    if SETUP_PY.exists():
        warnings.warn("Using deprecated setup.py invocation")
        try:
            return run("python setup.py --version").split("\n")[-1]
        except CalledProcessError as e:
            log(e)

    # Build the wheel and extract the version.
    if PYPROJECT.exists():
        with tempfile.TemporaryDirectory() as tempdir:
            run(f"pipx run build --wheel --outdir {tempdir}")
            wheel_path = glob(f"{tempdir}/*.whl")[0]
            wheel = Wheel(wheel_path)
            version = wheel.version
            return version

    if PACKAGE_JSON.exists():
        return json.loads(PACKAGE_JSON.read_text(encoding="utf-8")).get("version", "")

    raise ValueError("No version identifier could be found!")


def normalize_path(path):
    """Normalize a path to use backslashes"""
    return str(path).replace(os.sep, "/")


def compute_sha256(path):
    """Compute the sha256 of a file"""
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def create_release_commit(version, release_message=None, dist_dir="dist"):
    """Generate a release commit that has the sha256 digests for the release files"""
    release_message = release_message or "Publish {version}"
    release_message = release_message.format(version=version)
    cmd = f'git commit -am "{release_message}"'

    shas = {}

    files = glob(f"{dist_dir}/*")
    if files:  # pragma: no cover
        cmd += ' -m "SHA256 hashes:"'

    for path in sorted(files):
        path = normalize_path(path)
        sha256 = compute_sha256(path)
        shas[path] = sha256
        name = osp.basename(path)
        cmd += f' -m "{name}: {sha256}"'

    run(cmd)

    return shas


def _get_hatch_version_cmd():
    if shutil.which("hatch"):
        return "hatch version"
    return "pipx run hatch version"


def bump_version(version_spec, *, changelog_path="", version_cmd=""):
    """Bump the version"""
    # Look for config files to determine version command if not given
    if not version_cmd:
        for name in "bumpversion", ".bumpversion", "bump2version", ".bump2version":
            if osp.exists(name + ".cfg"):
                version_cmd = "bump2version"

        if osp.exists("tbump.toml"):
            version_cmd = version_cmd or TBUMP_CMD

        if PYPROJECT.exists():
            pyproject_text = PYPROJECT.read_text(encoding="utf-8")
            if "tool.tbump" in pyproject_text:
                version_cmd = version_cmd or TBUMP_CMD
            elif "hatchling.build" in pyproject_text:
                version_cmd = version_cmd or _get_hatch_version_cmd()

        if SETUP_CFG.exists():
            if "bumpversion" in SETUP_CFG.read_text(encoding="utf-8"):
                version_cmd = version_cmd or "bump2version"

    if not version_cmd and PACKAGE_JSON.exists():
        version_cmd = "npm version --git-tag-version false"

    if not version_cmd:  # pragma: no cover
        raise ValueError("Please specify a version bump command to run")

    # Assign default values if no version spec was given
    if not version_spec:
        if "tbump" in version_cmd or "hatch" in version_cmd:
            version_spec = "next"
        else:
            version_spec = "patch"

    # Add some convenience options on top of "tbump" and "hatch"
    if "tbump" in version_cmd or "hatch" in version_cmd:

        v = parse_version(get_version())
        log(f"Current version was: {v}")
        assert isinstance(v, Version)

        if v.is_devrelease:
            # bump from the version in the changelog unless the spec is dev.
            # Import here to avoid circular import.
            from jupyter_releaser.changelog import extract_current_version

            try:
                vc = parse_version(extract_current_version(changelog_path))
                log(f"Changelog version was: {vc}")
                assert isinstance(vc, Version)
            except ValueError:
                vc = v

            if version_spec in ["patch", "next"]:
                if vc.is_prerelease:
                    if vc.is_devrelease:
                        # Bump to the next dev release.
                        assert vc.dev is not None
                        version_spec = f"{vc.major}.{vc.minor}.{vc.micro}.dev{vc.dev + 1}"
                    else:
                        assert vc.pre is not None
                        # Bump to the next prerelease.
                        version_spec = f"{vc.major}.{vc.minor}.{vc.micro}{vc.pre[0]}{vc.pre[1] + 1}"

                else:
                    # Bump to the next micro.
                    version_spec = f"{vc.major}.{vc.minor}.{vc.micro + 1}"

            # Move to the minor release
            elif version_spec == "minor":
                version_spec = f"{vc.major}.{vc.minor+1}.0"

            # Bump to the next dev version.
            elif version_spec == "dev":
                assert v.dev is not None
                version_spec = f"{v.major}.{v.minor}.{v.micro}.dev{v.dev + 1}"

        else:
            # Handle dev version spec.
            if version_spec == "dev":
                if v.pre:
                    version_spec = f"{v.major}.{v.minor}.{v.micro}.dev0"
                # Bump to next minor dev.
                else:
                    version_spec = f"{v.major}.{v.minor + 1}.0.dev0"

            # For next, go to next prerelease or patch if it is a final version.
            elif version_spec == "next":
                if v.is_prerelease:
                    assert v.pre is not None
                    version_spec = f"{v.major}.{v.minor}.{v.micro}{v.pre[0]}{v.pre[1] + 1}"
                else:
                    version_spec = f"{v.major}.{v.minor}.{v.micro + 1}"

            # For patch, always patch.
            elif version_spec == "patch":
                version_spec = f"{v.major}.{v.minor}.{v.micro + 1}"

            # For minor, always minor.
            elif version_spec == "minor":
                version_spec = f"{v.major}.{v.minor + 1}.0"

    # Bump the version
    run(f"{version_cmd} {version_spec}", echo=True)

    return get_version()


def is_prerelease(version):
    """Test whether a version is a prerelease version"""
    match = re.match("([0-9]+.[0-9]+.[0-9]+)", version)
    assert match is not None
    final_version = match.groups()[0]
    return final_version != version


def release_for_url(gh, url):
    """Get release response data given a release url"""
    release = None
    for rel in gh.repos.list_releases():
        if rel.html_url == url or rel.url == url:
            release = rel
    if not release:
        raise ValueError(f"No release found for url {url}")
    return release


def latest_draft_release(gh, branch=None):
    """Get the latest draft release for a given repo"""
    newest_time = None
    newest_release = None
    if branch:
        log(f"Getting latest draft release on branch {branch}")
    else:
        log("Getting latest draft release")
    for release in gh.repos.list_releases():
        if str(release.draft).lower() == "false":
            continue
        if branch and release.target_commitish != branch:
            continue
        created = release.created_at
        d_created = datetime.strptime(created, r"%Y-%m-%dT%H:%M:%SZ")
        if newest_time is None or d_created > newest_time:
            newest_time = d_created
            newest_release = release
    if not newest_release:
        log("No draft release found!")
    else:
        log(f"Found draft release at {newest_release.html_url}")
    return newest_release


def actions_output(name, value):
    """Handle setting an action output on GitHub"""
    log(f"\n\nSetting output {name}={value}")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as fid:
            fid.write(f"{name}={value}\n")


def get_latest_tag(source, since_last_stable=False):
    """Get the default 'since' value for a branch"""
    source = source or get_branch()
    tags = run(f"git --no-pager tag --sort=-creatordate --merged {source}", quiet=True)
    if not tags:
        return ""

    tags = tags.splitlines()

    if since_last_stable:
        stable_tag = re.compile(r"\d\.\d\.\d$")
        tags = [t for t in tags if re.search(stable_tag, t)]
        if not tags:
            return ""
        return tags[0]

    return tags[0]


def get_first_commit(source):
    """Get the default 'since' value for a branch"""
    source = source or get_branch()
    commit = run("git rev-list --max-parents=0 HEAD", quiet=True)
    return commit


def retry(cmd, **kwargs):
    """Run a command with retries"""
    attempt = 0
    while True:
        time.sleep(attempt)
        try:
            run(cmd, **kwargs)
            return
        except Exception as e:
            attempt += 1
            if attempt == 3:
                raise e


def read_config():
    """Read the jupyter-releaser config data"""
    config = None

    if JUPYTER_RELEASER_CONFIG.exists():
        config = toml.loads(JUPYTER_RELEASER_CONFIG.read_text(encoding="utf-8"))
        log(f"jupyter-releaser configuration loaded from {JUPYTER_RELEASER_CONFIG}.")

    if PYPROJECT.exists():
        data = toml.loads(PYPROJECT.read_text(encoding="utf-8"))
        pyproject_config = data.get("tool", {}).get("jupyter-releaser")
        if pyproject_config:
            if not config:
                config = pyproject_config
                log(f"jupyter-releaser configuration loaded from {PYPROJECT}.")
            else:
                log(f"Ignoring jupyter-releaser configuration from {PYPROJECT}.")

    if PACKAGE_JSON.exists():
        data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        if "jupyter-releaser" in data:
            if not config:
                config = data["jupyter-releaser"]
                log(f"jupyter-releaser configuration loaded from {PACKAGE_JSON}.")
            else:
                log(f"Ignoring jupyter-releaser configuration from {PACKAGE_JSON}.")

    config = config or {}
    validator = Validator(SCHEMA)
    validator.validate(config)
    return config


def parse_release_url(release_url):
    """Parse a release url into a regex match"""
    pattern = RELEASE_HTML_PATTERN % get_mock_github_url()
    match = re.match(pattern, release_url)
    match = match or re.match(RELEASE_API_PATTERN, release_url)
    if not match:
        raise ValueError(f"Release url is not valid: {release_url}")
    return match


def fetch_release_asset(target_dir, asset, auth):
    """Fetch a release asset into a target directory."""
    log(f"Fetching {asset.name}...")
    url = asset.url
    headers = {"Authorization": f"token {auth}", "Accept": "application/octet-stream"}
    path = Path(target_dir) / asset.name
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return path


def fetch_release_asset_data(asset, auth):
    """Fetch the data for a release asset."""
    log(f"Fetching data for {asset.name}...")
    url = asset.url
    headers = {"Authorization": f"token {auth}", "Accept": "application/octet-stream"}

    sink = BytesIO()
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            sink.write(chunk)
    sink.seek(0)
    return json.loads(sink.read().decode("utf-8"))


def upload_assets(gh, assets, release, auth):
    """Upload assets to a release."""
    log(f"Uploading assets: {assets}")
    asset_shas = {}
    for fpath in assets:
        gh.upload_file(release, fpath)
        asset_shas[os.path.basename(fpath)] = compute_sha256(fpath)

    # Create an asset_shas file.
    with tempfile.TemporaryDirectory() as td:
        asset_shas_file = os.path.join(td, "asset_shas.json")
        with open(asset_shas_file, "w") as fid:
            json.dump(asset_shas, fid)
        gh.upload_file(release, asset_shas_file)

    return release


def extract_metadata_from_release_url(gh, release_url, auth):
    log(f"Extracting metadata for release: {release_url}")
    release = release_for_url(gh, release_url)

    data = None
    for asset in release.assets:
        if asset.name != METADATA_JSON.name:
            continue

        data = fetch_release_asset_data(asset, auth)

    if data is None:
        raise ValueError(
            f'Could not find "{METADATA_JSON.name}" file in draft release {release_url}'
        )

    # Update environment variables.
    for key, value in data.items():
        if value is not None:
            env_name = f"RH_{key.upper()}"
            os.environ[env_name] = str(value)

    return data


def prepare_environment(fetch_draft_release=True):
    """Prepare the environment variables, for use when running one of the
    action scripts."""
    # Set up env variables
    if not os.environ.get("RH_REPOSITORY"):
        if os.environ.get("RH_RELEASE_URL"):
            match = parse_release_url(os.environ["RH_RELEASE_URL"])
            owner, repo = match["owner"], match["repo"]
            os.environ["RH_REPOSITORY"] = f"{owner}/{repo}"
        else:
            os.environ["RH_REPOSITORY"] = os.environ["GITHUB_REPOSITORY"]
    if not os.environ.get("RH_REF"):
        os.environ["RH_REF"] = os.environ["GITHUB_REF"]

    dry_run = os.environ.get("RH_DRY_RUN", "").lower() == "true"

    # Set the branch when using check release.
    if not os.environ.get("RH_BRANCH") and dry_run:
        if os.environ.get("GITHUB_BASE_REF"):
            base_ref = os.environ.get("GITHUB_BASE_REF", "")
            log(f"Using GITHUB_BASE_REF: ${base_ref}")
            os.environ["RH_BRANCH"] = base_ref

        else:
            # e.g refs/head/foo or refs/tag/bar
            ref = os.environ["GITHUB_REF"]
            log(f"Using GITHUB_REF: {ref}")
            os.environ["RH_BRANCH"] = "/".join(ref.split("/")[2:])

    # Start the mock GitHub server if in a dry run.
    if dry_run:
        static_dir = os.path.join(tempfile.gettempdir(), "gh_static")
        os.makedirs(static_dir, exist_ok=True)
        os.environ["RH_GITHUB_STATIC_DIR"] = static_dir
        ensure_mock_github()

    # Set up GitHub object.
    branch = os.environ.get("RH_BRANCH")
    log(f"Getting GitHub connection for {os.environ['RH_REPOSITORY']}")
    owner, repo_name = os.environ["RH_REPOSITORY"].split("/")
    auth = os.environ.get("GITHUB_ACCESS_TOKEN", "")
    gh = get_gh_object(dry_run=dry_run, owner=owner, repo=repo_name, token=auth)

    # Ensure the user is an admin.
    if not dry_run:
        user = os.environ["GITHUB_ACTOR"]
        log(f"Getting permission level for {user}")
        try:
            collab_level = gh.repos.get_collaborator_permission_level(user)
            if not collab_level["permission"] == "admin":
                raise RuntimeError(f"User {user} does not have admin permission")
            log("User was admin!")
        except Exception as e:
            log(str(e))
            raise RuntimeError(
                "Could not get user permission level, assuming user was not admin!"
            ) from None

    # Get the latest draft release if none is given.
    release_url = os.environ.get("RH_RELEASE_URL")
    log(f"Environment release url was {release_url}")
    if not release_url and fetch_draft_release:
        release = latest_draft_release(gh, branch)
        if release:
            release_url = release.html_url

    if release_url:
        os.environ["RH_RELEASE_URL"] = release_url

        # Extract the metadata from the release url.
        return extract_metadata_from_release_url(gh, release_url, auth)
    return release_url


def handle_since() -> str:
    """Capture the "since" argument in case we add tags before checking changelog."""
    since = os.environ.get("RH_SINCE", "")
    if since:
        log(f"Using RH_SINCE from env: {since}")
        return since
    curr_dir = os.getcwd()
    os.chdir(CHECKOUT_NAME)
    since_last_stable_env = os.environ.get("RH_SINCE_LAST_STABLE", "")
    since_last_stable = since_last_stable_env.lower() == "true"
    log(f"Since last stable? {since_last_stable}")
    since = get_latest_tag(os.environ.get("RH_BRANCH"), since_last_stable)
    if since:
        log(f"Capturing {since} in RH_SINCE variable")
        os.environ["RH_SINCE"] = since
    else:
        log("No last stable found!")
    os.chdir(curr_dir)
    return since


def ensure_sha(dry_run, expected_sha, branch):
    """Ensure the sha of the remote branch matches the expected sha"""
    log("Ensuring sha...")
    remote_name = get_remote_name(False)
    run("git remote -v", echo=True)
    run(f"git fetch {remote_name} {branch}", echo=True)
    sha = run(f"git rev-parse {remote_name}/{branch}", echo=True)
    if sha != expected_sha:
        msg = f"{branch} current sha {sha} is not equal to expected sha {expected_sha}"
        if dry_run:
            log(msg)
        else:
            raise RuntimeError(msg)


def get_gh_object(dry_run=False, **kwargs):
    """Get a properly configured GhAPi object"""
    if dry_run:
        ensure_mock_github()

    return core.GhApi(**kwargs)


_local_remote = None


def get_remote_name(dry_run):
    """Get the appropriate remote git name."""
    global _local_remote
    if not dry_run:
        return "origin"

    if _local_remote:
        try:
            run(f"git remote add test {_local_remote}")
        except Exception:
            pass
        return "test"

    tfile = tempfile.NamedTemporaryFile(suffix=".git")
    tfile.close()
    _local_remote = tfile.name.replace(os.sep, "/")
    run(f"git init --bare {_local_remote}")
    run(f"git remote add test {_local_remote}")
    return "test"


def get_mock_github_url():
    port = os.environ.get("MOCK_GITHUB_PORT", "8000")
    return f"http://127.0.0.1:{port}"


def ensure_mock_github():
    """Check for or start a mock github server."""
    core.GH_HOST = host = get_mock_github_url()
    port = urlparse(host).port

    log("Ensuring mock GitHub")
    # First see if it is already running.
    try:
        requests.get(host)
        return
    except requests.ConnectionError:
        pass

    # Next make sure we have the required libraries.
    python = sys.executable.replace(os.sep, "/")
    try:
        import fastapi  # noqa
        import univcorn  # type: ignore  # noqa
    except ImportError:
        run(f"'{python}' -m pip install fastapi uvicorn")

    proc = subprocess.Popen(
        [python, "-m", "uvicorn", "jupyter_releaser.mock_github:app", "--port", str(port)]
    )

    try:
        ret = proc.wait(1)
        if ret > 0:
            raise ValueError(f"mock_github failed with {proc.returncode}")
    except subprocess.TimeoutExpired:
        pass
    log("Mock GitHub started")
    atexit.register(proc.kill)

    while 1:
        try:
            requests.get(host)
            break
        except requests.ConnectionError:
            pass
    return proc
