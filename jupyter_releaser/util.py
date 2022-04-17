# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Of the form:
# https://github.com/{owner}/{repo}/releases/tag/{tag}
import hashlib
import json
import os
import os.path as osp
import re
import shlex
import shutil
import sys
import tempfile
import time
import warnings
from datetime import datetime
from glob import glob
from pathlib import Path
from subprocess import PIPE, CalledProcessError, check_output

import toml
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

BUF_SIZE = 65536
TBUMP_CMD = "tbump --non-interactive --only-patch"

CHECKOUT_NAME = ".jupyter_releaser_checkout"

RELEASE_HTML_PATTERN = (
    "https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/releases/tag/(?P<tag>.*)"
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
    quiet = kwargs.pop("quiet", False)
    echo = kwargs.pop("echo", False)

    if echo:
        prefix = "COMMAND"
        if show_cwd:
            prefix += f" (in '{os.getcwd()}')"
        prefix += ":"
        print(f"{prefix} {cmd}", file=sys.stderr)

    if sys.platform.startswith("win"):
        # Async subprocesses do not work well on Windows, use standard
        # subprocess methods
        return _run_win(cmd, **kwargs)

    quiet = kwargs.get("quiet")
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
    if SETUP_PY.exists():
        warnings.warn("Using deprecated setup.py invocation")
        try:
            return run("python setup.py --version").split("\n")[-1]
        except CalledProcessError as e:
            print(e)

    if PYPROJECT.exists():
        text = PYPROJECT.read_text(encoding="utf-8")
        data = toml.loads(text)
        project = data.get("project", {})
        version = project.get("version")
        if not version:
            with tempfile.TemporaryDirectory() as tempdir:
                run(f"{sys.executable} -m build --wheel --outdir {tempdir}")
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
            if "tbump" in PYPROJECT.read_text(encoding="utf-8"):
                version_cmd = version_cmd or TBUMP_CMD

        if SETUP_CFG.exists():
            if "bumpversion" in SETUP_CFG.read_text(encoding="utf-8"):
                version_cmd = version_cmd or "bump2version"

    if not version_cmd and PACKAGE_JSON.exists():
        version_cmd = "npm version --git-tag-version false"

    if not version_cmd:  # pragma: no cover
        raise ValueError("Please specify a version bump command to run")

    # Assign default values if no version spec was given
    if not version_spec:
        if "tbump" in version_cmd:
            version_spec = "next"
        else:
            version_spec = "patch"

    # Add some convenience options on top of "tbump"
    if "tbump" in version_cmd:
        v = parse_version(get_version())
        assert isinstance(v, Version)

        if v.is_devrelease:
            # bump from the version in the changelog.
            if version_spec in ["patch", "next"]:
                from jupyter_releaser.changelog import extract_current_version

                v = parse_version(extract_current_version(changelog_path))
                assert isinstance(v, Version)
                version_spec = f"{v.major}.{v.minor}.{v.micro + 1}"

            # Drop the dev portion and move to the minor release.
            elif version_spec == "minor":
                version_spec = f"{v.major}.{v.minor}.{v.micro}"

            # Bump to the next dev version.
            elif version_spec == "dev":
                assert v.dev is not None
                version_spec = f"{v.major}.{v.minor}.{v.micro}.dev{v.dev + 1}"

        else:
            # Bump to next minor for dev.
            if version_spec == "dev":
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
    run(f"{version_cmd} {version_spec}")

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


def lastest_draft_release(gh):
    """Get the latest draft release for a given repo"""
    newest_time = None
    newest_release = None
    for release in gh.repos.list_releases():
        if str(release.draft).lower() == "false":
            continue
        created = release.created_at
        d_created = datetime.strptime(created, r"%Y-%m-%dT%H:%M:%SZ")
        if newest_time is None or d_created > newest_time:
            newest_time = d_created
            newest_release = release
    if not newest_release:
        raise ValueError("No draft releases found")
    return newest_release


def actions_output(name, value):
    "Print the special GitHub Actions `::set-output` line for `name::value`"
    log(f"\n\nSetting output {name}={value}")
    if "GITHUB_ACTIONS" in os.environ:
        print(f"::set-output name={name}::{value}")


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

    if not config and PYPROJECT.exists():
        data = toml.loads(PYPROJECT.read_text(encoding="utf-8"))
        pyproject_config = data.get("tool", {}).get("jupyter-releaser")
        if pyproject_config:
            config = pyproject_config

    if not config and PACKAGE_JSON.exists():
        data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        if "jupyter-releaser" in data:
            config = data["jupyter-releaser"]

    config = config or {}
    validator = Validator(SCHEMA)
    validator.validate(config)
    return config
