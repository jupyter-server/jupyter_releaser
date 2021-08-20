# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import os.path as osp
import re
import shutil
import sys
from glob import glob
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import call

import pytest

from jupyter_releaser import changelog
from jupyter_releaser import util
from jupyter_releaser.tests.util import CHANGELOG_ENTRY
from jupyter_releaser.tests.util import get_log
from jupyter_releaser.tests.util import HTML_URL
from jupyter_releaser.tests.util import mock_changelog_entry
from jupyter_releaser.tests.util import MockHTTPResponse
from jupyter_releaser.tests.util import MockRequestResponse
from jupyter_releaser.tests.util import PR_ENTRY
from jupyter_releaser.tests.util import REPO_DATA
from jupyter_releaser.tests.util import VERSION_SPEC
from jupyter_releaser.util import bump_version
from jupyter_releaser.util import normalize_path
from jupyter_releaser.util import run


def test_prep_git_simple(py_package, runner):
    """Standard local run with no env variables."""
    result = runner(["prep-git", "--git-url", py_package], env=dict(GITHUB_ACTIONS=""))

    log = get_log()
    assert "before-prep-git" not in log
    assert "after-prep-git" in log

    os.chdir(util.CHECKOUT_NAME)
    assert util.get_branch() == "bar", util.get_branch()


def test_prep_git_pr(py_package, runner):
    """With RH_BRANCH"""
    env = dict(RH_BRANCH="foo", GITHUB_ACTIONS="")
    result = runner(["prep-git", "--git-url", py_package], env=env)
    os.chdir(util.CHECKOUT_NAME)
    assert util.get_branch() == "foo", util.get_branch()


def test_prep_git_tag(py_package, runner):
    tag = "v0.1"
    util.run(f"git tag {tag}")
    result = runner(
        ["prep-git", "--git-url", py_package],
        env=dict(GITHUB_ACTIONS="", RH_REF=f"refs/tags/{tag}", RH_BRANCH=tag),
    )

    log = get_log()
    assert "before-prep-git" not in log
    assert "after-prep-git" in log

    os.chdir(util.CHECKOUT_NAME)
    assert util.get_branch() == tag, util.get_branch()


def test_prep_git_slashes(py_package, runner):
    branch = "a/b/c"
    util.run(f"git checkout -b {branch} foo")
    result = runner(
        ["prep-git", "--git-url", py_package],
        env=dict(GITHUB_ACTIONS="", RH_REF=f"refs/heads/{branch}", RH_BRANCH=branch),
    )

    log = get_log()
    assert "before-prep-git" not in log
    assert "after-prep-git" in log

    os.chdir(util.CHECKOUT_NAME)
    assert util.get_branch() == branch, util.get_branch()


def test_prep_git_full(py_package, tmp_path, mocker, runner):
    """Full GitHub Actions simulation (Push)"""

    env = dict(
        RH_REF="refs/pull/42",
        RH_BRANCH="foo",
        GITHUB_ACTIONS="true",
        RH_REPOSITORY="baz/bar",
        GITHUB_ACTOR="snuffy",
        GITHUB_ACCESS_TOKEN="abc123",
    )

    # Fake out the runner
    mock_run = mocker.patch("jupyter_releaser.util.run")
    mock_run.return_value = ""
    os.mkdir(util.CHECKOUT_NAME)

    runner(["prep-git"], env=env)
    mock_run.assert_has_calls(
        [
            call("git config --global user.email"),
            call(
                'git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"'
            ),
            call('git config --global user.name "GitHub Action"'),
            call("git init .jupyter_releaser_checkout"),
            call("git remote add origin https://snuffy:abc123@github.com/baz/bar.git"),
            call("git fetch origin --tags --force --quiet"),
            call("git fetch origin +refs/pull/42:refs/pull/42"),
            call("git fetch origin refs/pull/42"),
            call("git checkout -B foo refs/pull/42"),
        ]
    )


def test_bump_version(npm_package, runner):
    runner(["prep-git", "--git-url", npm_package])
    runner(["bump-version", "--version-spec", "1.0.1-rc0"])

    log = get_log()
    assert "before-bump-version" in log
    assert "after-bump-version" in log

    os.chdir(util.CHECKOUT_NAME)
    version = util.get_version()
    assert version == "1.0.1-rc0"


def test_bump_version_bad_version(py_package, runner):
    runner(["prep-git", "--git-url", py_package])
    with pytest.raises(CalledProcessError):
        runner(
            ["bump-version", "--version-spec", "a1.0.1"], env=dict(GITHUB_ACTIONS="")
        )


def test_bump_version_tag_exists(py_package, runner):
    runner(["prep-git", "--git-url", py_package])
    run("git tag v1.0.1", cwd=util.CHECKOUT_NAME)
    with pytest.raises(ValueError):
        runner(["bump-version", "--version-spec", "1.0.1"], env=dict(GITHUB_ACTIONS=""))


def test_list_envvars(runner):
    result = runner(["list-envvars"])
    assert (
        result.output.strip()
        == """
auth: GITHUB_ACCESS_TOKEN
branch: RH_BRANCH
cache-file: RH_CACHE_FILE
changelog-path: RH_CHANGELOG
dist-dir: RH_DIST_DIR
dry-run: RH_DRY_RUN
links-expire: RH_LINKS_EXPIRE
npm-cmd: RH_NPM_COMMAND
npm-install-options: RH_NPM_INSTALL_OPTIONS
npm-token: NPM_TOKEN
output: RH_CHANGELOG_OUTPUT
post-version-message: RH_POST_VERSION_MESSAGE
post-version-spec: RH_POST_VERSION_SPEC
ref: RH_REF
release-message: RH_RELEASE_MESSAGE
repo: RH_REPOSITORY
resolve-backports: RH_RESOLVE_BACKPORTS
since: RH_SINCE
tag-message: RH_TAG_MESSAGE
twine-cmd: TWINE_COMMAND
username: GITHUB_ACTOR
version-cmd: RH_VERSION_COMMAND
version-spec: RH_VERSION_SPEC
""".strip()
    )


def test_build_changelog(py_package, mocker, runner):
    run("pre-commit run -a")

    changelog_path = "CHANGELOG.md"

    runner(["prep-git", "--git-url", py_package])
    runner(["bump-version", "--version-spec", VERSION_SPEC])

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_path])

    log = get_log()
    assert "before-build-changelog" in log
    assert "after-build-changelog" in log

    changelog_path = Path(util.CHECKOUT_NAME) / "CHANGELOG.md"
    text = changelog_path.read_text(encoding="utf-8")
    assert changelog.START_MARKER in text
    assert changelog.END_MARKER in text
    assert PR_ENTRY in text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a")


def test_build_changelog_existing(py_package, mocker, runner):
    changelog_file = "CHANGELOG.md"
    changelog_path = Path(util.CHECKOUT_NAME) / changelog_file

    runner(["prep-git", "--git-url", py_package])
    runner(["bump-version", "--version-spec", VERSION_SPEC])

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_file])

    text = changelog_path.read_text(encoding="utf-8")
    text = text.replace("defining contributions", "Definining contributions")
    changelog_path.write_text(text, encoding="utf-8")

    # Commit the change
    run('git commit -a -m "commit changelog"', cwd=util.CHECKOUT_NAME)

    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_file])

    text = changelog_path.read_text(encoding="utf-8")
    assert "Definining contributions" in text, text
    assert not "defining contributions" in text, text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a", cwd=util.CHECKOUT_NAME)


def test_build_changelog_backport(py_package, mocker, runner, open_mock):
    changelog_file = "CHANGELOG.md"
    changelog_path = Path(util.CHECKOUT_NAME) / changelog_file

    data = dict(title="foo", html_url="bar", user=dict(login="snuffy", html_url="baz"))
    open_mock.return_value = MockHTTPResponse(data)

    runner(["prep-git", "--git-url", py_package])
    runner(["bump-version", "--version-spec", VERSION_SPEC])

    entry = CHANGELOG_ENTRY.replace("consideRatio", "meeseeksmachine")
    entry = entry.replace(
        "Support git references etc.", "Backport PR #50 (original title"
    )

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = entry
    runner(["build-changelog", "--changelog-path", changelog_file])
    text = changelog_path.read_text(encoding="utf-8")
    assert changelog.START_MARKER in text
    assert changelog.END_MARKER in text

    assert "- foo [#50](bar) ([@snuffy](baz))" in text, text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a")


def test_build_changelog_slashes(py_package, mocker, runner, open_mock):
    branch = "a/b/c"
    util.run(f"git checkout -b {branch} foo")
    env = dict(RH_REF=f"refs/heads/{branch}", RH_BRANCH=branch)
    run("pre-commit run -a")

    changelog_path = "CHANGELOG.md"

    runner(["prep-git", "--git-url", py_package], env=env)
    runner(["bump-version", "--version-spec", VERSION_SPEC], env=env)

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_path], env=env)

    log = get_log()
    assert "before-build-changelog" in log
    assert "after-build-changelog" in log

    changelog_path = Path(util.CHECKOUT_NAME) / "CHANGELOG.md"
    text = changelog_path.read_text(encoding="utf-8")
    assert changelog.START_MARKER in text
    assert changelog.END_MARKER in text
    assert PR_ENTRY in text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a")


def test_draft_changelog_full(py_package, mocker, runner, open_mock, git_prep):
    mock_changelog_entry(py_package, runner, mocker)
    runner(["draft-changelog", "--version-spec", VERSION_SPEC])

    log = get_log()
    assert "before-draft-changelog" in log
    assert "after-draft-changelog" in log

    open_mock.assert_called_once()


def test_draft_changelog_skip(py_package, mocker, runner, open_mock, git_prep):
    mock_changelog_entry(py_package, runner, mocker)

    config_path = Path(util.CHECKOUT_NAME) / util.JUPYTER_RELEASER_CONFIG
    config = util.toml.loads(config_path.read_text(encoding="utf-8"))
    config["skip"] = ["draft-changelog"]
    config_path.write_text(util.toml.dumps(config), encoding="utf-8")

    runner(["draft-changelog", "--version-spec", VERSION_SPEC])
    open_mock.assert_not_called()


def test_draft_changelog_dry_run(npm_package, mocker, runner, git_prep):
    mock_changelog_entry(npm_package, runner, mocker)
    runner(["draft-changelog", "--dry-run", "--version-spec", VERSION_SPEC])


def test_draft_changelog_lerna(workspace_package, mocker, runner, open_mock, git_prep):
    mock_changelog_entry(workspace_package, runner, mocker)
    runner(["draft-changelog", "--version-spec", VERSION_SPEC])
    open_mock.assert_called_once()


def test_check_links(py_package, runner):
    readme = Path("README.md")
    text = readme.read_text(encoding="utf-8")
    text += "\nhttps://apod.nasa.gov/apod/astropix.html"
    readme.write_text(text, encoding="utf-8")

    config = Path(util.JUPYTER_RELEASER_CONFIG)
    config_data = util.toml.loads(config.read_text(encoding="utf-8"))
    config_data["options"] = {"ignore-glob": ["FOO.md"]}
    config.write_text(util.toml.dumps(config_data), encoding="utf-8")

    util.run("git commit -a -m 'update files'")

    runner(["prep-git", "--git-url", py_package])
    runner(["check-links"])

    log = get_log()
    assert "before-check-links" in log
    assert "after-check-links" in log

    foo = Path(util.CHECKOUT_NAME) / "FOO.md"
    foo.write_text("http://127.0.0.1:5555")

    bar = Path(util.CHECKOUT_NAME) / "BAR BAZ.md"
    bar.write_text("")

    runner(["check-links"])


def test_check_changelog(py_package, tmp_path, mocker, runner, git_prep):
    changelog_entry = mock_changelog_entry(py_package, runner, mocker)
    output = "output.md"

    # prep the release
    bump_version(VERSION_SPEC)

    runner(
        ["check-changelog", "--changelog-path", changelog_entry, "--output", output],
    )

    log = get_log()
    assert "before-check-changelog" in log
    assert "after-check-changelog" in log

    output = Path(util.CHECKOUT_NAME) / output
    assert PR_ENTRY in output.read_text(encoding="utf-8")
    changelog_entry = Path(util.CHECKOUT_NAME) / changelog_entry
    text = changelog_entry.read_text(encoding="utf-8")
    assert f"{changelog.START_MARKER}\n\n## {VERSION_SPEC}" in text
    assert changelog.END_MARKER in text


def test_build_python(py_package, runner, build_mock, git_prep):
    runner(["build-python"])

    log = get_log()
    assert "before-build-python" in log
    assert "after-build-python" in log


def test_build_python_setup(py_package, runner, git_prep):
    Path(util.CHECKOUT_NAME).joinpath("pyproject.toml").unlink()
    runner(["build-python"])


def test_build_python_npm(npm_package, runner, build_mock, git_prep):
    runner(["build-python"])


def test_check_python(py_package, runner, build_mock, git_prep):
    runner(["build-python"])
    runner(["check-python"])

    log = get_log()
    assert "before-check-python" in log
    assert "after-check-python" in log


def test_handle_npm(npm_package, runner, git_prep):
    runner(["build-npm"])

    log = get_log()
    assert "before-build-npm" in log
    assert "after-build-npm" in log

    runner(["check-npm"])

    log = get_log()
    assert "before-check-npm" in log
    assert "after-check-npm" in log


def test_handle_npm_lerna(workspace_package, runner, git_prep):
    runner(["build-npm"])
    runner(["check-npm"])


def test_check_manifest(py_package, runner, git_prep):
    runner(["check-manifest"])

    log = get_log()
    assert "before-check-manifest" in log
    assert "after-check-manifest" in log


def test_check_manifest_npm(npm_package, runner, git_prep):
    runner(["check-manifest"])


def test_tag_release(py_package, runner, build_mock, git_prep):
    # Bump the version
    runner(["bump-version", "--version-spec", VERSION_SPEC])
    # Create the dist files
    util.run("python -m build .", cwd=util.CHECKOUT_NAME)
    # Tag the release
    runner(
        [
            "tag-release",
            "--release-message",
            "hi {version}",
            "--tag-message",
            "no thanks",
        ]
    )

    log = get_log()
    assert "before-tag-release" in log
    assert "after-tag-release" in log


def test_draft_release_dry_run(py_dist, mocker, runner, open_mock, git_prep):
    # Publish the release - dry run
    runner(
        [
            "draft-release",
            "--dry-run",
            "--post-version-spec",
            "1.1.0.dev0",
            "--post-version-message",
            "haha",
        ]
    )
    open_mock.assert_not_called()

    log = get_log()
    assert "before-draft-release" in log
    assert "after-draft-release" in log


def test_draft_release_final(npm_dist, runner, mocker, open_mock, git_prep):
    open_mock.side_effect = [
        MockHTTPResponse([REPO_DATA]),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
    ]

    # Publish the release
    os.environ["GITHUB_ACTIONS"] = "true"
    runner(["draft-release"])
    assert len(open_mock.call_args) == 2


def test_delete_release(npm_dist, runner, mocker, open_mock, git_prep):
    # Publish the release
    # Mimic being on GitHub actions so we get the magic output
    os.environ["GITHUB_ACTIONS"] = "true"
    open_mock.side_effect = [
        MockHTTPResponse([REPO_DATA]),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
        MockHTTPResponse(),
    ]
    result = runner(["draft-release"])

    assert len(open_mock.call_args) == 2

    url = ""
    for line in result.output.splitlines():
        match = re.match(r"::set-output name=release_url::(.*)", line)
        if match:
            url = match.groups()[0]

    # Delete the release
    data = dict(assets=[dict(id="bar")])
    open_mock.side_effect = [
        MockHTTPResponse([data]),
        MockHTTPResponse(),
        MockHTTPResponse(),
    ]
    runner(["delete-release", url])
    assert len(open_mock.call_args) == 2

    log = get_log()
    assert "before-delete-release" in log
    assert "after-delete-release" in log


@pytest.mark.skipif(
    os.name == "nt" and sys.version_info.major == 3 and sys.version_info.minor < 8,
    reason="See https://bugs.python.org/issue26660",
)
def test_extract_dist_py(py_package, runner, mocker, open_mock, tmp_path, git_prep):
    changelog_entry = mock_changelog_entry(py_package, runner, mocker)

    # Create the dist files
    run("python -m build .", cwd=util.CHECKOUT_NAME)

    # Finalize the release
    runner(["tag-release"])

    os.makedirs("staging")
    shutil.move(f"{util.CHECKOUT_NAME}/dist", "staging")

    def helper(path, **kwargs):
        return MockRequestResponse(f"{py_package}/staging/dist/{path}")

    get_mock = mocker.patch("requests.get", side_effect=helper)

    tag_name = f"v{VERSION_SPEC}"

    dist_names = [osp.basename(f) for f in glob("staging/dist/*.*")]
    releases = [
        dict(
            tag_name=tag_name,
            target_commitish=util.get_branch(),
            assets=[dict(name=dist_name, url=dist_name) for dist_name in dist_names],
        )
    ]
    sha = run("git rev-parse HEAD", cwd=util.CHECKOUT_NAME)

    tags = [dict(ref=f"refs/tags/{tag_name}", object=dict(sha=sha))]
    url = normalize_path(osp.join(os.getcwd(), util.CHECKOUT_NAME))
    open_mock.side_effect = [
        MockHTTPResponse(releases),
        MockHTTPResponse(tags),
        MockHTTPResponse(dict(html_url=url)),
    ]

    runner(["extract-release", HTML_URL])
    assert len(open_mock.mock_calls) == 2
    assert len(get_mock.mock_calls) == len(dist_names) == 2

    log = get_log()
    assert "before-extract-release" not in log
    assert "after-extract-release" in log


@pytest.mark.skipif(
    os.name == "nt" and sys.version_info.major == 3 and sys.version_info.minor < 8,
    reason="See https://bugs.python.org/issue26660",
)
def test_extract_dist_npm(npm_dist, runner, mocker, open_mock, tmp_path):

    os.makedirs("staging")
    shutil.move(f"{util.CHECKOUT_NAME}/dist", "staging")

    def helper(path, **kwargs):
        return MockRequestResponse(f"{npm_dist}/staging/dist/{path}")

    get_mock = mocker.patch("requests.get", side_effect=helper)

    dist_names = [osp.basename(f) for f in glob("staging/dist/*.tgz")]
    url = normalize_path(osp.join(os.getcwd(), util.CHECKOUT_NAME))
    tag_name = f"v{VERSION_SPEC}"
    releases = [
        dict(
            tag_name=tag_name,
            target_commitish="foo",
            assets=[dict(name=dist_name, url=dist_name) for dist_name in dist_names],
        )
    ]
    sha = run("git rev-parse HEAD", cwd=util.CHECKOUT_NAME)
    tags = [dict(ref=f"refs/tags/{tag_name}", object=dict(sha=sha))]
    open_mock.side_effect = [
        MockHTTPResponse(releases),
        MockHTTPResponse(tags),
        MockHTTPResponse(dict(html_url=url)),
    ]

    runner(["extract-release", HTML_URL])
    assert len(open_mock.mock_calls) == 2
    assert len(get_mock.mock_calls) == len(dist_names) == 3

    log = get_log()
    assert "before-extract-release" not in log
    assert "after-extract-release" in log


@pytest.mark.skipif(
    os.name == "nt", reason="pypiserver does not start properly on Windows"
)
def test_publish_assets_py(py_package, runner, mocker, git_prep):
    # Create the dist files
    changelog_entry = mock_changelog_entry(py_package, runner, mocker)
    run("python -m build .", cwd=util.CHECKOUT_NAME)

    orig_run = util.run
    called = 0

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("twine upload"):
            called += 1
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    dist_dir = py_package / util.CHECKOUT_NAME / "dist"
    runner(["publish-assets", "--dist-dir", dist_dir, "--dry-run"])
    assert called == 2, called

    log = get_log()
    assert "before-publish-assets" in log
    assert "after-publish-assets" in log


def test_publish_assets_npm(npm_dist, runner, mocker):
    dist_dir = npm_dist / util.CHECKOUT_NAME / "dist"
    orig_run = util.run
    called = 0

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("npm publish --dry-run"):
            called += 1
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    runner(
        [
            "publish-assets",
            "--npm-cmd",
            "npm publish --dry-run",
            "--dist-dir",
            dist_dir,
        ]
    )

    assert called == 3, called


def test_publish_assets_npm_exists(npm_dist, runner, mocker):
    dist_dir = npm_dist / util.CHECKOUT_NAME / "dist"
    called = 0

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("npm publish --dry-run"):
            called += 1
            if called == 0:
                err = CalledProcessError(1, "foo")
                err.stderr = "EPUBLISHCONFLICT"
                raise err

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    runner(
        [
            "publish-assets",
            "--npm-token",
            "abc",
            "--npm-cmd",
            "npm publish --dry-run",
            "--dist-dir",
            dist_dir,
        ]
    )

    assert called == 3, called


def test_publish_assets_npm_all_exists(npm_dist, runner, mocker):
    dist_dir = npm_dist / util.CHECKOUT_NAME / "dist"
    called = 0

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("npm publish --dry-run"):
            called += 1
            err = CalledProcessError(1, "foo")
            err.stderr = "previously published versions"
            raise err

    mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    with pytest.raises(ValueError):
        runner(
            [
                "publish-assets",
                "--npm-token",
                "abc",
                "--npm-cmd",
                "npm publish --dry-run",
                "--dist-dir",
                dist_dir,
            ]
        )

    assert called == 3, called


def test_publish_release(npm_dist, runner, mocker, open_mock):
    open_mock.side_effect = [MockHTTPResponse([REPO_DATA]), MockHTTPResponse()]
    dist_dir = npm_dist / util.CHECKOUT_NAME / "dist"
    runner(["publish-release", HTML_URL])

    log = get_log()
    assert "before-publish-release" in log
    assert "after-publish-release" in log

    assert len(open_mock.call_args) == 2


def test_config_file(py_package, runner, mocker, git_prep):

    config = Path(util.CHECKOUT_NAME) / util.JUPYTER_RELEASER_CONFIG
    config_data = util.toml.loads(config.read_text(encoding="utf-8"))
    config_data["options"] = {"dist-dir": "foo"}
    config.write_text(util.toml.dumps(config_data), encoding="utf-8")

    orig_run = util.run
    called = False

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("python -m build --outdir foo"):
            called = True
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    runner(["build-python"])
    assert called

    log = get_log()
    assert "before-build-python" in log
    assert "after-build-python" in log


def test_config_file_env_override(py_package, runner, mocker, git_prep):

    orig_run = util.run
    called = False

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("python -m build --outdir bar"):
            called = True
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    os.environ["RH_DIST_DIR"] = "bar"
    runner(["build-python"])
    assert called

    log = get_log()
    assert "before-build-python" in log
    assert "after-build-python" in log


def test_config_file_cli_override(py_package, runner, mocker, git_prep):
    orig_run = util.run
    called = False

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("python -m build --outdir bar"):
            called = True
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    runner(["build-python", "--dist-dir", "bar"])
    assert called

    log = get_log()
    assert "before-build-python" in log
    assert "after-build-python" in log


def test_forwardport_changelog_no_new(npm_package, runner, mocker, open_mock, git_prep):

    open_mock.side_effect = [MockHTTPResponse([REPO_DATA]), MockHTTPResponse()]

    # Create a branch with a changelog entry
    util.run("git checkout -b backport_branch", cwd=util.CHECKOUT_NAME)
    util.run("git push origin backport_branch", cwd=util.CHECKOUT_NAME)
    mock_changelog_entry(npm_package, runner, mocker)
    util.run('git commit -a -m "Add changelog entry"', cwd=util.CHECKOUT_NAME)
    util.run(f"git tag v{VERSION_SPEC}", cwd=util.CHECKOUT_NAME)

    # Run the forwardport workflow against default branch
    runner(["forwardport-changelog", HTML_URL])

    assert len(open_mock.mock_calls) == 2

    log = get_log()
    assert "before-forwardport-changelog" in log
    assert "after-forwardport-changelog" in log


def test_forwardport_changelog_has_new(
    npm_package, runner, mocker, open_mock, git_prep
):

    open_mock.side_effect = [MockHTTPResponse([REPO_DATA]), MockHTTPResponse()]
    current = util.run("git branch --show-current")

    # Create a branch with a changelog entry
    util.run("git checkout -b backport_branch", cwd=util.CHECKOUT_NAME)
    util.run("git push origin backport_branch", cwd=util.CHECKOUT_NAME)
    util.run(f"git checkout {current}")
    mock_changelog_entry(npm_package, runner, mocker)
    util.run(
        f'git commit -a -m "Add changelog entry {VERSION_SPEC}"', cwd=util.CHECKOUT_NAME
    )
    util.run(f"git tag v{VERSION_SPEC}", cwd=util.CHECKOUT_NAME)
    util.run(f"git checkout {current}", cwd=util.CHECKOUT_NAME)
    util.run("git push origin backport_branch --tags", cwd=util.CHECKOUT_NAME)

    # Add a new changelog entry in main branch
    util.run("git checkout backport_branch", cwd=str(npm_package))
    util.run(f"git checkout {current}", cwd=util.CHECKOUT_NAME)
    mock_changelog_entry(npm_package, runner, mocker, version_spec="2.0.0")
    util.run('git commit -a -m "Add changelog entry v2.0.0"', cwd=util.CHECKOUT_NAME)
    util.run("git tag v2.0.0", cwd=util.CHECKOUT_NAME)
    util.run("git checkout backport_branch", cwd=npm_package)
    util.run(f"git push origin {current} --tags", cwd=util.CHECKOUT_NAME)

    # Run the forwardport workflow against default branch
    url = osp.abspath(npm_package)
    os.chdir(npm_package)
    runner(["forwardport-changelog", HTML_URL, "--branch", current])

    assert len(open_mock.call_args) == 2
    util.run(f"git checkout {current}", cwd=npm_package)

    expected = """
<!-- <START NEW CHANGELOG ENTRY> -->

## 2.0.0
"""
    text = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert expected in text, text

    expect = """
<!-- <END NEW CHANGELOG ENTRY> -->

## 1.0.1
"""
    assert expected in text, text
