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

from jupyter_releaser import changelog, util
from jupyter_releaser.tests.util import (
    CHANGELOG_ENTRY,
    PR_ENTRY,
    VERSION_SPEC,
    create_draft_release,
    get_log,
    mock_changelog_entry,
)
from jupyter_releaser.util import GIT_FETCH_CMD, normalize_path, run


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
            call("echo before-prep-git >> 'log.txt'"),
            call("git init .jupyter_releaser_checkout"),
            call("git remote add origin https://snuffy:abc123@github.com/baz/bar.git"),
            call(f"{GIT_FETCH_CMD} --tags --force"),
            call(f"{GIT_FETCH_CMD} +refs/pull/42:refs/pull/42"),
            call(f"{GIT_FETCH_CMD} refs/pull/42"),
            call("git checkout -B foo refs/pull/42"),
            call("git symbolic-ref -q HEAD"),
            call("git config user.email"),
            call('git config user.email "snuffy@users.noreply.github.com"', echo=True),
            call('git config user.name "snuffy"', echo=True),
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
        runner(["bump-version", "--version-spec", "a1.0.1"], env=dict(GITHUB_ACTIONS=""))


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
changelog-path: RH_CHANGELOG
check-imports: RH_CHECK_IMPORTS
dist-dir: RH_DIST_DIR
dry-run: RH_DRY_RUN
expected-sha: RH_EXPECTED_SHA
npm-cmd: RH_NPM_COMMAND
npm-install-options: RH_NPM_INSTALL_OPTIONS
npm-registry: NPM_REGISTRY
npm-token: NPM_TOKEN
post-version-message: RH_POST_VERSION_MESSAGE
post-version-spec: RH_POST_VERSION_SPEC
pydist-check-cmd: RH_PYDIST_CHECK_CMD
pydist-extra-check-cmds: RH_EXTRA_PYDIST_CHECK_CMDS
pydist-resource-paths: RH_PYDIST_RESOURCE_PATHS
python-packages: RH_PYTHON_PACKAGES
ref: RH_REF
release-message: RH_RELEASE_MESSAGE
release-url: RH_RELEASE_URL
repo: RH_REPOSITORY
resolve-backports: RH_RESOLVE_BACKPORTS
since: RH_SINCE
since-last-stable: RH_SINCE_LAST_STABLE
tag-format: RH_TAG_FORMAT
tag-message: RH_TAG_MESSAGE
twine-cmd: TWINE_COMMAND
twine-repository-url: TWINE_REPOSITORY_URL
username: GITHUB_ACTOR
version-cmd: RH_VERSION_COMMAND
version-spec: RH_VERSION_SPEC
""".strip()
    )


def test_build_changelog(py_package, mocker, runner):
    run("pre-commit run -a")

    changelog_path_str = "CHANGELOG.md"

    runner(["prep-git", "--git-url", py_package])
    runner(["bump-version", "--version-spec", VERSION_SPEC])

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_path_str])

    log = get_log()
    assert "before-build-changelog" in log
    assert "after-build-changelog" in log

    changelog_path = Path(util.CHECKOUT_NAME) / changelog_path_str
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
    assert "defining contributions" not in text, text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a", cwd=util.CHECKOUT_NAME)


def test_build_changelog_backport(py_package, mocker, runner, mock_github):
    changelog_file = "CHANGELOG.md"
    changelog_path = Path(util.CHECKOUT_NAME) / changelog_file

    runner(["prep-git", "--git-url", py_package])
    runner(["bump-version", "--version-spec", VERSION_SPEC])

    entry = CHANGELOG_ENTRY.replace(
        "Support git references etc.", "Backport PR #50 on branch (original title"
    )

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = entry
    runner(["build-changelog", "--changelog-path", changelog_file])
    text = changelog_path.read_text(encoding="utf-8")
    assert changelog.START_MARKER in text
    assert changelog.END_MARKER in text

    assert "- foo [#50](http://foo.com) ([@bar](http://bar.com))" in text, text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a")


def test_build_changelog_slashes(py_package, mocker, runner):
    branch = "a/b/c"
    util.run(f"git checkout -b {branch} foo")
    env = dict(RH_REF=f"refs/heads/{branch}", RH_BRANCH=branch)
    run("pre-commit run -a")

    changelog_path_str = "CHANGELOG.md"

    runner(["prep-git", "--git-url", py_package], env=env)
    runner(["bump-version", "--version-spec", VERSION_SPEC], env=env)

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_path_str], env=env)

    log = get_log()
    assert "before-build-changelog" in log
    assert "after-build-changelog" in log

    changelog_path = Path(util.CHECKOUT_NAME) / changelog_path_str
    text = changelog_path.read_text(encoding="utf-8")
    assert changelog.START_MARKER in text
    assert changelog.END_MARKER in text
    assert PR_ENTRY in text

    assert len(re.findall(changelog.START_MARKER, text)) == 1
    assert len(re.findall(changelog.END_MARKER, text)) == 1

    run("pre-commit run -a")


def test_draft_changelog_full(py_package, mocker, runner, git_prep, mock_github):
    mock_changelog_entry(py_package, runner, mocker)
    runner(["draft-changelog", "--version-spec", VERSION_SPEC])

    log = get_log()
    assert "before-draft-changelog" in log
    assert "after-draft-changelog" in log


def test_draft_changelog_skip_config(py_package, mocker, runner, git_prep):
    mock_changelog_entry(py_package, runner, mocker)

    config_path = Path(util.CHECKOUT_NAME) / util.JUPYTER_RELEASER_CONFIG
    config = util.toml.loads(config_path.read_text(encoding="utf-8"))
    config["skip"] = ["draft-changelog"]
    config_path.write_text(util.toml.dumps(config), encoding="utf-8")

    runner(["draft-changelog", "--version-spec", VERSION_SPEC, "--since", "foo"])


def test_draft_changelog_skip_environ(py_package, mocker, runner, git_prep):
    mock_changelog_entry(py_package, runner, mocker)

    config_path = Path(util.CHECKOUT_NAME) / util.JUPYTER_RELEASER_CONFIG
    config = util.toml.loads(config_path.read_text(encoding="utf-8"))
    os.environ["RH_STEPS_TO_SKIP"] = "draft-changelog,other-fake-step"
    config_path.write_text(util.toml.dumps(config), encoding="utf-8")

    runner(["draft-changelog", "--version-spec", VERSION_SPEC, "--since", "foo"])
    del os.environ["RH_STEPS_TO_SKIP"]


def test_draft_changelog_dry_run(npm_package, mocker, runner, git_prep):
    mock_changelog_entry(npm_package, runner, mocker)
    os.environ["RH_SINCE_LAST_STABLE"] = "true"
    runner(
        [
            "draft-changelog",
            "--dry-run",
            "--version-spec",
            VERSION_SPEC,
            "--since-last-stable",
        ]
    )
    del os.environ["RH_SINCE_LAST_STABLE"]


def test_draft_changelog_lerna(workspace_package, mocker, runner, mock_github, git_prep):
    mock_changelog_entry(workspace_package, runner, mocker)
    runner(["draft-changelog", "--version-spec", VERSION_SPEC])


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


def test_check_python_different_names(
    monkeypatch, py_package_different_names, runner, build_mock, git_prep
):
    monkeypatch.setenv("RH_CHECK_IMPORTS", "foobar")


def test_check_python_resource_path(monkeypatch, py_package, runner, build_mock, git_prep):
    monkeypatch.setenv("RH_PYDIST_RESOURCE_PATHS", "foo/bar/baz.txt")

    # Convert the package to use a package dir.
    foo_dir = Path(util.CHECKOUT_NAME) / "foo"
    foo_dir.mkdir()
    shutil.move(Path(util.CHECKOUT_NAME) / "foo.py", foo_dir / "__init__.py")

    bar_dir = foo_dir / "bar"
    bar_dir.mkdir()
    path = bar_dir / "baz.txt"
    path.write_text("hello", encoding="utf-8")

    pyproject = Path(util.CHECKOUT_NAME / util.PYPROJECT)
    pyproject_text = pyproject.read_text('utf-8')
    pyproject_text = pyproject_text.replace("foo.py", "foo/__init__.py")
    pyproject.write_text(pyproject_text, "utf-8")

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


def test_tag_release(py_package, runner, build_mock, git_prep):
    # Bump the version
    runner(["bump-version", "--version-spec", VERSION_SPEC])
    # Create the dist files
    util.run("pipx run build .", cwd=util.CHECKOUT_NAME)
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


def test_populate_release_dry_run(py_dist, mocker, runner, git_prep, draft_release):
    # Publish the release - dry run
    runner(
        [
            "populate-release",
            "--dry-run",
            "--post-version-spec",
            "1.1.0.dev0",
            "--post-version-message",
            "haha",
            "--release-url",
            draft_release,
        ]
    )

    log = get_log()
    assert "before-populate-release" in log
    assert "after-populate-release" in log


def test_populate_release_final(npm_dist, runner, mock_github, git_prep, draft_release):
    # Publish the release
    os.environ["GITHUB_ACTIONS"] = "true"
    os.environ["RH_RELEASE_URL"] = draft_release
    runner(["populate-release"])


def test_delete_release(npm_dist, runner, mock_github, git_prep, draft_release):
    # Publish the release
    # Mimic being on GitHub actions so we get the magic output
    os.environ["GITHUB_ACTIONS"] = "true"
    os.environ["RH_RELEASE_URL"] = draft_release
    result = runner(["populate-release"])

    # Delete the release
    runner(["delete-release"])

    log = get_log()
    assert "before-delete-release" in log
    assert "after-delete-release" in log


@pytest.mark.skipif(
    os.name == "nt" and sys.version_info < (3, 8),
    reason="See https://bugs.python.org/issue26660",
)
def test_extract_dist_py(py_package, runner, mocker, mock_github, tmp_path, git_prep):
    changelog_entry = mock_changelog_entry(py_package, runner, mocker)

    # Create the dist files
    run("pipx run build .", cwd=util.CHECKOUT_NAME)

    # Finalize the release
    runner(["tag-release"])

    # Create the release.
    dist_dir = os.path.join(util.CHECKOUT_NAME, "dist")
    release = create_draft_release("bar", glob(f"{dist_dir}/*.*"))
    shutil.rmtree(dist_dir)

    os.environ["RH_RELEASE_URL"] = release.html_url
    runner(["extract-release"])

    log = get_log()
    assert "before-extract-release" not in log
    assert "after-extract-release" in log


@pytest.mark.skipif(
    os.name == "nt" and sys.version_info < (3, 8),
    reason="See https://bugs.python.org/issue26660",
)
def test_extract_dist_multipy(py_multipackage, runner, mocker, mock_github, tmp_path, git_prep):
    git_repo = py_multipackage[0]["abs_path"]
    changelog_entry = mock_changelog_entry(git_repo, runner, mocker)

    # Create the dist files
    files = []
    dist_dir = normalize_path(Path(util.CHECKOUT_NAME).resolve() / "dist")
    for package in py_multipackage:
        run(
            f"pipx run build . -o {dist_dir}",
            cwd=Path(util.CHECKOUT_NAME) / package["rel_path"],
        )
        files.extend(glob(dist_dir + "/*.*"))

    # Finalize the release
    runner(["tag-release"])

    # Create the release.
    dist_dir = os.path.join(util.CHECKOUT_NAME, "dist")
    release = create_draft_release("bar", glob(f"{dist_dir}/*.*"))
    shutil.rmtree(dist_dir)

    os.environ["RH_RELEASE_URL"] = release.html_url
    runner(["extract-release"])

    log = get_log()
    assert "before-extract-release" not in log
    assert "after-extract-release" in log


@pytest.mark.skipif(
    os.name == "nt" and sys.version_info < (3, 8),
    reason="See https://bugs.python.org/issue26660",
)
def test_extract_dist_npm(npm_dist, runner, mocker, mock_github, tmp_path):
    # Create the release.
    dist_dir = os.path.join(util.CHECKOUT_NAME, "dist")
    release = create_draft_release("bar", glob(f"{dist_dir}/*.*"))
    shutil.rmtree(dist_dir)

    os.environ["RH_RELEASE_URL"] = release.html_url
    runner(["extract-release"])

    log = get_log()
    assert "before-extract-release" not in log
    assert "after-extract-release" in log


@pytest.mark.skipif(os.name == "nt", reason="pypiserver does not start properly on Windows")
def test_publish_assets_py(py_package, runner, mocker, git_prep, mock_github):
    # Create the dist files
    changelog_entry = mock_changelog_entry(py_package, runner, mocker)
    run("pipx run build .", cwd=util.CHECKOUT_NAME)

    orig_run = util.run
    called = 0

    os.environ["PYPI_TOKEN_MAP"] = "foo/bar,foo-token\nfizz/buzz,bar"

    def wrapped(cmd, **kwargs):
        nonlocal called
        if "twine upload" in cmd:
            if kwargs["env"]["TWINE_PASSWORD"] == "foo-token":
                called += 1
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    dist_dir = py_package / util.CHECKOUT_NAME / "dist"
    release = create_draft_release(files=glob(f"{dist_dir}/*.*"))
    os.environ["RH_RELEASE_URL"] = release.html_url
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

    runner(["publish-assets", "--npm-cmd", "npm publish --dry-run", "--dist-dir", dist_dir])

    assert called == 3, called


def test_publish_assets_npm_exists(npm_dist, runner, mocker, mock_github, draft_release):
    os.environ["RH_RELEASE_URL"] = draft_release
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


def test_publish_assets_npm_all_exists(npm_dist, runner, mocker, mock_github, draft_release):
    os.environ["RH_RELEASE_URL"] = draft_release
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


def test_publish_release(npm_dist, runner, mocker, mock_github, draft_release):
    os.environ["RH_RELEASE_URL"] = draft_release
    runner(["publish-release"])

    log = get_log()
    assert "before-publish-release" in log
    assert "after-publish-release" in log


def test_config_file(py_package, runner, mocker, git_prep):

    config = Path(util.CHECKOUT_NAME) / util.JUPYTER_RELEASER_CONFIG
    config_data = util.toml.loads(config.read_text(encoding="utf-8"))
    config_data["options"] = {"dist-dir": "foo"}
    config.write_text(util.toml.dumps(config_data), encoding="utf-8")

    orig_run = util.run
    called = False

    def wrapped(cmd, **kwargs):
        nonlocal called
        if cmd.startswith("pipx run build --outdir foo"):
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
        if cmd.startswith("pipx run build --outdir bar"):
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
        if cmd.startswith("pipx run build --outdir bar"):
            called = True
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)

    runner(["build-python", "--dist-dir", "bar"])
    assert called

    log = get_log()
    assert "before-build-python" in log
    assert "after-build-python" in log


def test_forwardport_changelog_no_new(npm_package, runner, mocker, mock_github, git_prep):
    release = create_draft_release("bar")
    os.environ["RH_RELEASE_URL"] = release.html_url

    # Create a branch with a changelog entry
    util.run("git checkout -b backport_branch", cwd=util.CHECKOUT_NAME)
    util.run("git push origin backport_branch", cwd=util.CHECKOUT_NAME)
    mock_changelog_entry(npm_package, runner, mocker)
    util.run('git commit -a -m "Add changelog entry"', cwd=util.CHECKOUT_NAME)
    util.run(f"git tag v{VERSION_SPEC}", cwd=util.CHECKOUT_NAME)

    # Run the forwardport workflow against default branch
    runner(["forwardport-changelog"])

    log = get_log()
    assert "before-forwardport-changelog" in log
    assert "after-forwardport-changelog" in log


def test_forwardport_changelog_has_new(npm_package, runner, mocker, mock_github, git_prep):
    release = create_draft_release("bar")
    os.environ["RH_RELEASE_URL"] = release.html_url

    current = util.run("git branch --show-current", cwd=util.CHECKOUT_NAME)

    # Create a branch with a changelog entry
    util.run("git checkout -b backport_branch", cwd=util.CHECKOUT_NAME)
    util.run("git push origin backport_branch", cwd=util.CHECKOUT_NAME)
    util.run(f"git checkout {current}")
    mock_changelog_entry(npm_package, runner, mocker)
    util.run(f'git commit -a -m "Add changelog entry {VERSION_SPEC}"', cwd=util.CHECKOUT_NAME)
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
    runner(["forwardport-changelog", "--branch", current])

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


def test_ensure_sha(npm_package, runner, git_prep):
    sha = util.run("git rev-parse HEAD", cwd=util.CHECKOUT_NAME)
    current = util.run("git branch --show-current", cwd=util.CHECKOUT_NAME)
    runner(["ensure-sha", "--branch", current, "--expected-sha", sha])
    runner(["ensure-sha", "--branch", current, "--expected-sha", "abc", "--dry-run"])

    with pytest.raises(RuntimeError):
        runner(["ensure-sha", "--branch", current, "--expected-sha", "abc"])
