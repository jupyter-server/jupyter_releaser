# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import os.path as osp
import re
import shutil
import tempfile
import uuid
from datetime import datetime
from glob import glob
from pathlib import Path
from subprocess import CalledProcessError

import mdformat
from packaging.version import parse as parse_version
from pkginfo import SDist, Wheel

from jupyter_releaser import changelog, npm, python, util


def bump_version(version_spec, version_cmd, changelog_path):
    """Bump the version and verify new version"""
    util.bump_version(version_spec, version_cmd=version_cmd, changelog_path=changelog_path)

    version = util.get_version()

    # A properly parsed version will have a "major" attribute
    parsed = parse_version(version)

    if util.SETUP_PY.exists() and not hasattr(parsed, "major"):
        raise ValueError(f"Invalid version {version}")

    # Bail if tag already exists
    tag_name = f"v{version}"
    if tag_name in util.run("git --no-pager tag", quiet=True).splitlines():
        msg = f"Tag {tag_name} already exists!"
        msg += " To delete run: `git push --delete origin {tag_name}`"
        raise ValueError(msg)

    return version


def draft_changelog(
    version_spec,
    ref,
    branch,
    repo,
    since,
    since_last_stable,
    auth,
    changelog_path,
    dry_run,
    post_version_spec,
    post_version_message,
):
    """Create a changelog entry PR"""
    repo = repo or util.get_repo()
    branch = branch or util.get_branch()
    version = util.get_version()
    prerelease = util.is_prerelease(version)

    current_sha = util.run("git rev-parse HEAD")

    # Check for multiple versions
    npm_versions = None
    if util.PACKAGE_JSON.exists():
        npm_versions = npm.get_package_versions(version)
        util.log(npm_versions)

    tags = util.run("git --no-pager tag", quiet=True)
    if f"v{version}" in tags.splitlines():
        raise ValueError(f"Tag v{version} already exists")

    current = changelog.extract_current(changelog_path)
    util.log(f"\n\nCurrent Changelog Entry:\n{current}")

    # Check out all changed files.
    try:
        util.run("git checkout .", echo=True)
    except CalledProcessError as e:
        util.log(str(e))
        return

    util.run("git status", echo=True)
    util.log(f"\n\nCreating draft GitHub release for {version}")
    owner, repo_name = repo.split("/")
    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo_name, token=auth)

    data = {
        "version_spec": version_spec,
        "ref": ref,
        "branch": branch,
        "repo": repo,
        "since": since,
        "since_last_stable": since_last_stable,
        "version": version,
        "post_version_spec": post_version_spec,
        "post_version_message": post_version_message,
        "expected_sha": current_sha,
    }
    with tempfile.TemporaryDirectory() as d:
        metadata_path = Path(d) / util.METADATA_JSON
        with open(metadata_path, "w") as fid:
            json.dump(data, fid)

        release = gh.create_release(
            f"v{version}", branch, f"v{version}", current, True, prerelease, files=[metadata_path]
        )

    # Remove draft releases over a day old
    if bool(os.environ.get("GITHUB_ACTIONS")):
        for rel in gh.repos.list_releases():
            if str(rel.draft).lower() == "false":
                continue
            created = rel.created_at
            d_created = datetime.strptime(created, r"%Y-%m-%dT%H:%M:%SZ")
            delta = datetime.utcnow() - d_created
            if delta.days > 0:
                gh.repos.delete_release(rel.id)

    # Set the GitHub action output for the release url.
    util.actions_output("release_url", release.html_url)


def make_changelog_pr(auth, branch, repo, title, commit_message, body, dry_run=False):
    repo = repo or util.get_repo()
    branch = branch or util.get_branch()

    # Make a new branch with a uuid suffix
    pr_branch = f"changelog-{uuid.uuid1().hex}"

    if not dry_run:
        dirty = util.run("git --no-pager diff --stat") != ""
        if dirty:
            util.run("git stash")
        util.run(f"{util.GIT_FETCH_CMD} {branch}")
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
    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo_name, token=auth)

    base = branch
    head = pr_branch
    maintainer_can_modify = True

    if not dry_run:
        util.run(f"git push origin {pr_branch}", echo=True)

    #  title, head, base, body, maintainer_can_modify, draft, issue
    pull = gh.pulls.create(title, head, base, body, maintainer_can_modify, False, None)

    # Try to add the documentation label to the PR.
    number = pull.number
    try:
        gh.issues.add_labels(number, ["documentation"])
    except Exception as e:
        print(e)

    util.actions_output("pr_url", pull.html_url)


def tag_release(dist_dir, release_message, tag_format, tag_message, no_git_tag_workspace):
    """Create release commit and tag"""
    # Get the new version
    version = util.get_version()

    # Create the release commit
    util.create_release_commit(version, release_message, dist_dir)

    # Create the annotated release tag
    tag_name = tag_format.format(version=version)
    tag_message = tag_message.format(tag_name=tag_name, version=version)
    util.run(f'git tag {tag_name} -a -m "{tag_message}"')

    # Create release tags for workspace packages if given
    if not no_git_tag_workspace:
        npm.tag_workspace_packages()


def populate_release(
    ref,
    branch,
    repo,
    version_cmd,
    auth,
    changelog_path,
    dist_dir,
    dry_run,
    release_url,
    post_version_spec,
    post_version_message,
    assets,
):
    """Populate release assets and push tags and commits"""
    branch = branch or util.get_branch()
    assets = assets or glob(f"{dist_dir}/*")
    body = changelog.extract_current(changelog_path)

    match = util.parse_release_url(release_url)
    owner, repo_name = match["owner"], match["repo"]

    # Bump to post version if given.
    if post_version_spec:
        post_version = bump_version(
            post_version_spec, version_cmd=version_cmd, changelog_path=changelog_path
        )
        util.log(post_version_message.format(post_version=post_version))
        util.run(f'git commit -a -m "Bump to {post_version}"')

    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo_name, token=auth)
    release = util.release_for_url(gh, release_url)

    remote_name = util.get_remote_name(dry_run)
    remote_url = util.run(f"git config --get remote.{remote_name}.url")
    if not os.path.exists(remote_url):
        util.run(f"git push {remote_name} HEAD:{branch} --follow-tags --tags")

    # Set the body of the release with the changelog contents.
    # Get the new release since the draft release might change urls.
    release = gh.repos.update_release(
        release.id,
        release.tag_name,
        release.target_commitish,
        release.name,
        body,
        True,
        release.prerelease,
    )

    # Upload the assets to the draft release.
    release = util.upload_assets(gh, assets, release, auth)

    # Set the GitHub action output
    util.actions_output("release_url", release.html_url)


def delete_release(auth, release_url, dry_run=False):
    """Delete a draft GitHub release by url to the release page"""
    pattern = util.RELEASE_HTML_PATTERN % util.get_mock_github_url()
    match = re.match(pattern, release_url)
    match = match or re.match(util.RELEASE_API_PATTERN, release_url)
    if not match:
        raise ValueError(f"Release url is not valid: {release_url}")

    gh = util.get_gh_object(dry_run=dry_run, owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)
    for asset in release.assets:
        gh.repos.delete_release_asset(asset.id)

    gh.repos.delete_release(release.id)


def extract_release(auth, dist_dir, dry_run, release_url):
    """Download and verify assets from a draft GitHub release"""
    match = util.parse_release_url(release_url)
    owner, repo = match["owner"], match["repo"]

    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo, token=auth)
    release = util.release_for_url(gh, release_url)
    branch = release.target_commitish
    assets = release.assets

    # Prepare a git checkout
    prep_git(None, branch, f"{owner}/{repo}", auth, None, None)

    orig_dir = os.getcwd()
    os.chdir(util.CHECKOUT_NAME)

    # Clean the dist folder
    dist = Path(dist_dir)
    if dist.exists():
        shutil.rmtree(dist, ignore_errors=True)
    os.makedirs(dist)

    # Fetch, validate, and publish assets
    for asset in assets:
        util.fetch_release_asset(dist_dir, asset, auth)

    # Validate the shas of all the files
    asset_shas_file = dist / "asset_shas.json"
    with open(asset_shas_file) as fid:
        asset_shas = json.load(fid)
    asset_shas_file.unlink()

    for asset in assets:
        if asset.name.endswith(".json"):
            continue
        if asset.name not in asset_shas:
            raise ValueError(f"{asset.name} was not found in asset_shas file")
        if util.compute_sha256(dist / asset.name) != asset_shas[asset.name]:
            raise ValueError(f"sha for {asset.name} does not match asset_shas file")

    os.chdir(orig_dir)


def publish_assets(
    dist_dir,
    npm_token,
    npm_cmd,
    twine_cmd,
    npm_registry,
    twine_repository_url,
    dry_run,
    release_url,
    python_package,
):
    """Publish release asset(s)"""
    os.environ["NPM_REGISTRY"] = npm_registry
    os.environ["TWINE_REPOSITORY_URL"] = twine_repository_url
    twine_token = ""

    if len(glob(f"{dist_dir}/*.tgz")):
        npm.handle_npm_config(npm_token)
        if npm_token:
            util.run("npm whoami")

    res = python_package.split(":")
    python_package_path = res[0]
    if len(res) == 2:
        python_package_name = res[1].replace("-", "_")
    else:
        python_package_name = ""

    if release_url and len(glob(f"{dist_dir}/*.whl")):
        twine_token = python.get_pypi_token(release_url, python_package_path)

    if dry_run:
        # Start local pypi server with no auth, allowing overwrites,
        # in a temporary directory
        if len(glob(f"{dist_dir}/*.whl")):
            python.start_local_pypi()
            twine_cmd = "pipx run twine upload --repository-url=http://0.0.0.0:8081"
            os.environ["TWINE_USERNAME"] = "foo"
            twine_token = twine_token or "bar"
        npm_cmd = "npm publish --dry-run"
    else:
        os.environ.setdefault("TWINE_USERNAME", "__token__")

    found = False
    for path in sorted(glob(f"{dist_dir}/*.*")):
        name = Path(path).name
        util.log(f"Handling dist file {path}")
        suffix = Path(path).suffix
        if suffix in [".gz", ".whl"]:
            if suffix == ".gz":
                dist = SDist
            else:
                dist = Wheel
            pkg = dist(path)
            if not python_package_name or python_package_name == pkg.name:
                env = os.environ.copy()
                env["TWINE_PASSWORD"] = twine_token
                # NOTE: Do not print the env since a twine token extracted from
                # a PYPI_TOKEN_MAP will not be sanitized in output
                util.retry(f"{twine_cmd} {name}", cwd=dist_dir, env=env, echo=True)
                found = True
        elif suffix == ".tgz":
            # Ignore already published versions
            try:
                util.run(f"{npm_cmd} {name}", cwd=dist_dir, quiet=True, quiet_error=True, echo=True)
            except CalledProcessError as e:
                stderr = e.stderr
                if "EPUBLISHCONFLICT" in stderr or "previously published versions" in stderr:
                    continue
                raise e
            found = True
        else:
            util.log(f"Nothing to upload for {name}")
    if not found:
        util.log("No files to upload")


def publish_release(auth, dry_run, release_url):
    """Publish GitHub release"""
    util.log(f"Publishing {release_url}")

    match = util.parse_release_url(release_url)

    # Take the release out of draft
    gh = util.get_gh_object(dry_run=dry_run, owner=match["owner"], repo=match["repo"], token=auth)
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


def prep_git(ref, branch, repo, auth, username, url):
    """Set up git"""
    repo = repo or util.get_repo()

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
    util.run(f"{util.GIT_FETCH_CMD} --tags --force")

    # Handle the ref
    if ref.startswith("refs/pull/"):
        pull = ref[len("refs/pull/") :]
        ref_alias = f"refs/pull/{pull}"
    else:
        ref = None

    # Reuse existing branch if possible
    if ref:
        util.run(f"{util.GIT_FETCH_CMD} +{ref}:{ref_alias}")
        util.run(f"{util.GIT_FETCH_CMD} {ref}")
        checkout_cmd = f"git checkout -B {branch} {ref_alias}"
    else:
        util.run(f"{util.GIT_FETCH_CMD} {branch}")
        checkout_cmd = f"git checkout {branch}"

    if checkout_exists:
        try:
            util.run(f"git checkout {branch}")
        except Exception:
            util.run(checkout_cmd)
    else:
        util.run(checkout_cmd)

    # Check for detached head state, create branch if needed
    try:
        util.run("git symbolic-ref -q HEAD")
    except Exception:
        util.run(f"git switch -c {branch}")

    try:
        has_git_config = util.run("git config user.email").strip()
    except Exception:
        has_git_config = False

    if not has_git_config:
        # Default to the GitHub Actions bot
        # https://github.community/t/github-actions-bot-email-address/17204/6
        git_user_name = username or "41898282+github-actions[bot]"
        util.run(f'git config user.email "{git_user_name}@users.noreply.github.com"', echo=True)
        util.run(f'git config user.name "{git_user_name}"', echo=True)

    os.chdir(orig_dir)

    return branch


def extract_changelog(dry_run, auth, changelog_path, release_url):
    """Extract the changelog from the draft GH release body and update it."""
    match = util.parse_release_url(release_url)
    gh = util.get_gh_object(dry_run=dry_run, owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)
    changelog_text = mdformat.text(release.body)
    changelog.update_changelog(changelog_path, changelog_text)


def forwardport_changelog(auth, ref, branch, repo, username, changelog_path, dry_run, release_url):
    """Forwardport Changelog Entries to the Default Branch"""
    # Set up the git repo with the branch
    match = util.parse_release_url(release_url)

    gh = util.get_gh_object(dry_run=dry_run, owner=match["owner"], repo=match["repo"], token=auth)
    release = util.release_for_url(gh, release_url)
    tag = release.tag_name
    source_branch = release.target_commitish

    repo = f'{match["owner"]}/{match["repo"]}'

    # switch to main branch here
    branch = branch or util.get_default_branch()
    util.run(f"{util.GIT_FETCH_CMD} {branch}")
    util.run(f"git checkout {branch}")

    # Bail if the tag has been merged to the branch
    tags = util.run(f"git --no-pager tag --merged {branch}", quiet=True)
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
    if prev_header not in default_log:
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

    make_changelog_pr(auth, branch, repo, title, commit_message, body, dry_run=dry_run)

    # Clean up after ourselves
    util.run(f"git checkout {source_branch}")
