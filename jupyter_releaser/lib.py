# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import os.path as osp
import re
import shutil
import uuid
from datetime import datetime
from glob import glob
from pathlib import Path
from subprocess import CalledProcessError
from tempfile import TemporaryDirectory

import requests
from ghapi.core import GhApi
from pkg_resources import parse_version

from jupyter_releaser import changelog
from jupyter_releaser import npm
from jupyter_releaser import python
from jupyter_releaser import util


def bump_version(version_spec, version_cmd):
    """Bump the version and verify new version"""
    util.bump_version(version_spec, version_cmd=version_cmd)

    version = util.get_version()

    # A properly parsed version will have a "major" attribute
    parsed = parse_version(version)

    if util.SETUP_PY.exists() and not hasattr(parsed, "major"):
        raise ValueError(f"Invalid version {version}")

    # Bail if tag already exists
    tag_name = f"v{version}"
    if tag_name in util.run("git --no-pager tag").splitlines():
        msg = f"Tag {tag_name} already exists!"
        msg += " To delete run: `git push --delete origin {tag_name}`"
        raise ValueError(msg)

    return version


def check_links(ignore_glob, ignore_links, cache_file, links_expire):
    """Check URLs for HTML-containing files."""
    cache_dir = osp.expanduser(cache_file).replace(os.sep, "/")
    os.makedirs(cache_dir, exist_ok=True)
    cmd = "pytest --noconftest --check-links --check-links-cache "
    cmd += f"--check-links-cache-expire-after {links_expire} "
    cmd += f"--check-links-cache-name {cache_dir}/check-release-links "

    ignored = []
    for spec in ignore_glob:
        cmd += f' --ignore-glob "{spec}"'
        ignored.extend(glob(spec, recursive=True))

    ignore_links = list(ignore_links) + [
        "https://github.com/.*/(pull|issues)/.*",
        "https://github.com/search?",
        "http://localhost.*",
    ]

    for spec in ignore_links:
        cmd += f' --check-links-ignore "{spec}"'

    cmd += " --ignore-glob node_modules"

    # Gather all of the markdown, RST, and ipynb files
    files = []
    for ext in [".md", ".rst", ".ipynb"]:
        matched = glob(f"**/*{ext}", recursive=True)
        files.extend(m for m in matched if not m in ignored and "node_modules" not in m)

    for f in files:
        file_cmd = cmd + f' "{f}"'
        try:
            util.run(file_cmd)
        except Exception as e:
            # Return code 5 means no tests were run (no links found)
            if e.returncode != 5:
                util.run(file_cmd + " --lf")


def draft_changelog(version_spec, branch, repo, since, auth, changelog_path, dry_run):
    """Create a changelog entry PR"""
    repo = repo or util.get_repo()
    branch = branch or util.get_branch()
    version = util.get_version()

    tags = util.run("git --no-pager tag")
    if f"v{version}" in tags.splitlines():
        raise ValueError(f"Tag v{version} already exists")

    # Check out any unstaged files from version bump
    # If this is an automated changelog PR, there may be no effective changes
    try:
        util.run("git checkout -- .")
    except CalledProcessError as e:
        util.log(str(e))
        return

    current = changelog.extract_current(changelog_path)
    util.log(f"\n\nCurrent Changelog Entry:\n{current}")

    title = f"{changelog.PR_PREFIX} for {version} on {branch}"
    commit_message = f'git commit -a -m "{title}"'
    body = title

    # Check for multiple versions
    if util.PACKAGE_JSON.exists():
        body += npm.get_package_versions(version)

    body += '\n\nAfter merging this PR run the "Draft Release" Workflow on your fork of `jupyter_releaser` with the following inputs'
    body += f"""
| Input  | Value |
| ------------- | ------------- |
| Target | {repo}  |
| Branch  | {branch}  |
| Version Spec | {version_spec} |
"""
    if since:
        body += f"| Since | {since} |"
    util.log(body)

    make_changelog_pr(auth, branch, repo, title, commit_message, body, dry_run=dry_run)


def make_changelog_pr(auth, branch, repo, title, commit_message, body, dry_run=False):
    repo = repo or util.get_repo()

    # Make a new branch with a uuid suffix
    pr_branch = f"changelog-{uuid.uuid1().hex}"

    if not dry_run:
        dirty = util.run("git --no-pager diff --stat") != ""
        if dirty:
            util.run("git stash")
        util.run(f"git fetch origin {branch}")
        util.run(f"git checkout -b {pr_branch} origin/{branch}")
        if dirty:
            util.run("git stash apply")

    # Add a commit with the message
    try:
        util.run(commit_message)
    except CalledProcessError as e:
        util.log(str(e))
        return

    # Create the pull
    owner, repo_name = repo.split("/")
    gh = GhApi(owner=owner, repo=repo_name, token=auth)

    base = branch
    head = pr_branch
    maintainer_can_modify = True

    if dry_run:
        util.log("Skipping pull request due to dry run")
        return

    util.run(f"git push origin {pr_branch}")

    #  title, head, base, body, maintainer_can_modify, draft, issue
    pull = gh.pulls.create(title, head, base, body, maintainer_can_modify, False, None)

    util.actions_output("pr_url", pull.html_url)


def tag_release(dist_dir, no_git_tag_workspace):
    """Create release commit and tag"""
    # Get the new version
    version = util.get_version()

    # Create the release commit
    util.create_release_commit(version, dist_dir)

    # Create the annotated release tag
    tag_name = f"v{version}"
    util.run(f'git tag {tag_name} -a -m "Release {tag_name}"')

    # Create annotated release tags for workspace packages if given
    if not no_git_tag_workspace:
        npm.tag_workspace_packages()


def draft_release(
    ref,
    branch,
    repo,
    auth,
    changelog_path,
    version_cmd,
    dist_dir,
    dry_run,
    post_version_spec,
    assets,
):
    """Publish Draft GitHub release and handle post version bump"""
    branch = branch or util.get_branch()
    repo = repo or util.get_repo()
    assets = assets or glob(f"{dist_dir}/*")
    version = util.get_version()
    body = changelog.extract_current(changelog_path)
    prerelease = util.is_prerelease(version)

    # Bump to post version if given
    if post_version_spec:
        post_version = bump_version(post_version_spec, version_cmd)

        util.log(f"Bumped version to {post_version}")
        util.run(f'git commit -a -m "Bump to {post_version}"')

    if dry_run:
        return

    owner, repo_name = repo.split("/")
    gh = GhApi(owner=owner, repo=repo_name, token=auth)

    # Remove draft releases over a day old
    if bool(os.environ.get("GITHUB_ACTIONS")):
        for release in gh.repos.list_releases():
            if str(release.draft).lower() == "false":
                continue
            created = release.created_at
            d_created = datetime.strptime(created, r"%Y-%m-%dT%H:%M:%SZ")
            delta = datetime.utcnow() - d_created
            if delta.days > 0:
                gh.repos.delete_release(release.id)

    remote_url = util.run("git config --get remote.origin.url")
    if not os.path.exists(remote_url):
        util.run(f"git push origin HEAD:{branch} --follow-tags --tags")

    util.log(f"Creating release for {version}")
    util.log(f"With assets: {assets}")
    release = gh.create_release(
        f"v{version}",
        branch,
        f"Release v{version}",
        body,
        True,
        prerelease,
        files=assets,
    )

    # Set the GitHub action output
    util.actions_output("release_url", release.html_url)


def delete_release(auth, release_url):
    """Delete a draft GitHub release by url to the release page"""
    match = re.match(util.RELEASE_HTML_PATTERN, release_url)
    match = match or re.match(util.RELEASE_API_PATTERN, release_url)
    if not match:
        raise ValueError(f"Release url is not valid: {release_url}")

    gh = GhApi(owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)
    for asset in release.assets:
        gh.repos.delete_release_asset(asset.id)

    gh.repos.delete_release(release.id)


def extract_release(auth, dist_dir, dry_run, release_url, npm_install_options):
    """Download and verify assets from a draft GitHub release"""
    match = parse_release_url(release_url)
    owner, repo = match["owner"], match["repo"]
    gh = GhApi(owner=owner, repo=repo, token=auth)
    release = util.release_for_url(gh, release_url)
    assets = release.assets

    # Clean the dist folder
    dist = Path(dist_dir)
    if dist.exists():
        shutil.rmtree(dist, ignore_errors=True)
    os.makedirs(dist)

    # Fetch, validate, and publish assets
    for asset in assets:
        util.log(f"Fetching {asset.name}...")
        url = asset.url
        headers = dict(Authorization=f"token {auth}", Accept="application/octet-stream")
        path = dist / asset.name
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            suffix = Path(asset.name).suffix
            if suffix in [".gz", ".whl"]:
                python.check_dist(path)
            elif suffix == ".tgz":
                npm.check_dist(path, npm_install_options)
            else:
                util.log(f"Nothing to check for {asset.name}")

    # Skip sha validation for dry runs since the remote tag will not exist
    if dry_run:
        return

    branch = release.target_commitish
    tag_name = release.tag_name

    sha = None
    for tag in gh.list_tags():
        if tag.ref == f"refs/tags/{tag_name}":
            sha = tag.object.sha
    if sha is None:
        raise ValueError("Could not find tag")

    # Run a git checkout
    # Fetch the branch
    # Get the commmit message for the branch
    commit_message = ""
    with TemporaryDirectory() as td:
        url = gh.repos.get().html_url
        util.run(f"git clone {url} local", cwd=td)
        checkout = osp.join(td, "local")
        if not osp.exists(url):
            util.run(f"git fetch origin {branch}", cwd=checkout)
        commit_message = util.run(f"git log --format=%B -n 1 {sha}", cwd=checkout)

    for asset in assets:
        # Check the sha against the published sha
        valid = False
        path = dist / asset.name
        sha = util.compute_sha256(path)

        for line in commit_message.splitlines():
            if asset.name in line:
                if sha in line:
                    valid = True
                else:
                    util.log("Mismatched sha!")

        if not valid:  # pragma: no cover
            raise ValueError(f"Invalid file {asset.name}")


def parse_release_url(release_url):
    """Parse a release url into a regex match"""
    match = re.match(util.RELEASE_HTML_PATTERN, release_url)
    match = match or re.match(util.RELEASE_API_PATTERN, release_url)
    if not match:
        raise ValueError(f"Release url is not valid: {release_url}")
    return match


def publish_assets(dist_dir, npm_token, npm_cmd, twine_cmd, dry_run, use_checkout_dir):
    """Publish release asset(s)"""
    if use_checkout_dir:
        if not osp.exists(util.CHECKOUT_NAME):
            raise ValueError("Please run prep-git first")
        os.chdir(util.CHECKOUT_NAME)

    if dry_run:
        # Start local pypi server with no auth, allowing overwrites,
        # in a temporary directory
        if len(glob(f"{dist_dir}/*.whl")):
            python.start_local_pypi()
            twine_cmd = "twine upload --repository-url=http://localhost:8081"
            os.environ["TWINE_USERNAME"] = "foo"
            os.environ["TWINE_PASSWORD"] = "bar"
        npm_cmd = "npm publish --dry-run"
    else:
        os.environ.setdefault("TWINE_USERNAME", "__token__")

    if len(glob(f"{dist_dir}/*.tgz")):
        npm.handle_npm_config(npm_token, dist_dir)

    found = False
    for path in sorted(glob(f"{dist_dir}/*.*")):
        name = Path(path).name
        suffix = Path(path).suffix
        if suffix in [".gz", ".whl"]:
            util.run(f"{twine_cmd} {name}", cwd=dist_dir)
            found = True
        elif suffix == ".tgz":
            # Ignore already published versions
            try:
                util.run(f"{npm_cmd} {name}", cwd=dist_dir, quiet=True)
            except CalledProcessError as e:
                stderr = e.stderr
                if (
                    "EPUBLISHCONFLICT" in stderr
                    or "previously published versions" in stderr
                ):
                    continue
                raise e
            found = True
        else:
            util.log(f"Nothing to upload for {name}")

    if not found:  # pragma: no cover
        raise ValueError("No assets published, refusing to finalize release")


def publish_release(auth, release_url):
    """Publish GitHub release"""
    util.log(f"Publishing {release_url}")

    match = parse_release_url(release_url)

    # Take the release out of draft
    gh = GhApi(owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)

    release = gh.repos.update_release(
        release.id,
        release.tag_name,
        release.target_commitish,
        release.name,
        release.body,
        False,
        release.prerelease,
    )

    # Set the GitHub action output
    util.actions_output("release_url", release.html_url)


def prep_git(ref, branch, repo, auth, username, url, install=True):
    """Set up git"""
    repo = repo or util.get_repo()

    user_name = ""
    try:
        user_name = util.run("git config --global user.email")
    except Exception as e:
        pass

    if not user_name:
        # Use email address for the GitHub Actions bot
        # https://github.community/t/github-actions-bot-email-address/17204/6
        util.run(
            'git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"'
        )
        util.run('git config --global user.name "GitHub Action"')

    # Set up the repository
    checkout_dir = os.environ.get("RH_CHECKOUT_DIR", util.CHECKOUT_NAME)
    checkout_exists = False
    if osp.exists(osp.join(checkout_dir, ".git")):
        util.log("Git checkout already exists")
        checkout_exists = True

    if not checkout_exists:
        util.run(f"git init {checkout_dir}")

    orig_dir = os.getcwd()
    os.chdir(checkout_dir)

    if not url:
        if auth:
            url = f"https://{username}:{auth}@github.com/{repo}.git"
        else:
            url = f"https://github.com/{repo}.git"

    if osp.exists(url):
        url = util.normalize_path(url)

    if not checkout_exists:
        util.run(f"git remote add origin {url}")

    branch = branch or util.get_default_branch()
    ref = ref or ""

    # Make sure we have *all* tags
    util.run("git fetch origin --tags --force")

    # Handle the ref
    if ref.startswith("refs/pull/"):
        pull = ref[len("refs/pull/") :]
        ref_alias = f"refs/pull/{pull}"
    else:
        ref = None

    # Reuse existing branch if possible
    if ref:
        util.run(f"git fetch origin +{ref}:{ref_alias}")
        util.run(f"git fetch origin {ref}")
        checkout_cmd = f"git checkout -B {branch} {ref_alias}"
    else:
        util.run(f"git fetch origin {branch}")
        checkout_cmd = f"git checkout {branch}"

    if checkout_exists:
        try:
            util.run(f"git checkout {branch}")
        except Exception:
            util.run(checkout_cmd)
    else:
        util.run(checkout_cmd)

    # Install the package
    if install:
        # install python package in editable mode with test deps
        if util.SETUP_PY.exists():
            util.run('pip install -e ".[test]"')

        # prefer yarn if yarn lock exists
        elif util.YARN_LOCK.exists():
            if not shutil.which("yarn"):
                util.run("npm install -g yarn")
            util.run("yarn")

        # npm install otherwise
        elif util.PACKAGE_JSON.exists():
            util.run("npm install")

    os.chdir(orig_dir)

    return branch


def forwardport_changelog(
    auth, ref, branch, repo, username, changelog_path, dry_run, git_url, release_url
):
    """Forwardport Changelog Entries to the Default Branch"""
    # Set up the git repo with the branch
    match = parse_release_url(release_url)
    gh = GhApi(owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)
    tag = release.tag_name

    repo = f'{match["owner"]}/{match["repo"]}'

    # We want to target the main branch
    orig_dir = os.getcwd()
    branch = prep_git(None, None, repo, auth, username, git_url, install=False)
    os.chdir(util.CHECKOUT_NAME)

    # Bail if the tag has been merged to the branch
    tags = util.run(f"git --no-pager tag --merged {branch}")
    if tag in tags.splitlines():
        util.log(f"Skipping since tag is already merged into {branch}")
        return

    # Get the entry for the tag
    util.run(f"git checkout {tag}")
    entry = changelog.extract_current(changelog_path)

    # Get the previous header for the branch
    full_log = Path(changelog_path).read_text(encoding="utf-8")
    start = full_log.index(changelog.END_MARKER)

    prev_header = ""
    for line in full_log[start:].splitlines():
        if line.strip().startswith("#"):
            prev_header = line
            break

    if not prev_header:
        raise ValueError("No anchor for previous entry")

    # Check out the branch again
    util.run(f"git checkout -B {branch} origin/{branch}")

    default_entry = changelog.extract_current(changelog_path)

    # Look for the previous header
    default_log = Path(changelog_path).read_text(encoding="utf-8")
    if not prev_header in default_log:
        util.log(
            f'Could not find previous header "{prev_header}" in {changelog_path} on branch {branch}'
        )
        return

    # If the previous header is the current entry in the default branch, we need to move the change markers
    if prev_header in default_entry:
        default_log = changelog.insert_entry(default_log, entry)

    # Otherwise insert the new entry ahead of the previous header
    else:
        insertion_point = default_log.index(prev_header)
        default_log = changelog.format(
            default_log[:insertion_point] + entry + default_log[insertion_point:]
        )

    Path(changelog_path).write_text(default_log, encoding="utf-8")

    # Create a forward port PR
    title = f"{changelog.PR_PREFIX} Forward Ported from {tag}"
    commit_message = f'git commit -a -m "{title}"'
    body = title

    pr = make_changelog_pr(
        auth, branch, repo, title, commit_message, body, dry_run=dry_run
    )

    # Clean up after ourselves
    os.chdir(orig_dir)
    shutil.rmtree(util.CHECKOUT_NAME)
