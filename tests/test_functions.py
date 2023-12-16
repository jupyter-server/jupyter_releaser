# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import shutil
import time
from pathlib import Path

import toml
from ghapi.core import GhApi

from jupyter_releaser import changelog, npm, util
from jupyter_releaser.tests import util as testutil
from jupyter_releaser.util import run


def test_get_branch(git_repo):
    assert util.get_branch() == "bar"
    run("git checkout foo")
    assert util.get_branch() == "foo"


def test_get_repo(git_repo, mocker):
    repo = f"{git_repo.parent.name}/{git_repo.name}"
    assert util.get_repo() == repo


def test_get_version_pyproject_hatch(py_package):
    assert util.get_version() == "0.0.1"
    util.bump_version("0.0.2a0")
    assert util.get_version() == "0.0.2a0"


def test_get_version_multipython(py_multipackage):
    prev_dir = os.getcwd()
    for package in py_multipackage:
        os.chdir(package["rel_path"])
        assert util.get_version() == "0.0.1"
        util.bump_version("0.0.2a0")
        assert util.get_version() == "0.0.2a0"
        os.chdir(prev_dir)


def test_get_version_npm(npm_package):
    assert util.get_version() == "1.0.0"
    npm = util.normalize_path(shutil.which("npm"))
    run(f"{npm} version patch")
    assert util.get_version() == "1.0.1"


def test_format_pr_entry(mock_github):
    gh = GhApi(owner="snuffy", repo="foo")
    info = gh.pulls.create("title", "head", "base", "body", True, False, None)
    resp = changelog.format_pr_entry("snuffy/foo", info["number"], auth="baz")
    assert resp.startswith("- ")


def test_get_changelog_version_entry(py_package, mocker):
    version = util.get_version()

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    branch = "foo"
    util.run("git branch baz/bar")
    util.run("git tag v1.0 baz/bar")
    ref = "heads/baz/bar"
    resp = changelog.get_version_entry(ref, branch, "baz/bar", version)
    mocked_gen.assert_called_with(
        "baz/bar",
        since="v1.0",
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth=None,
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp

    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    resp = changelog.get_version_entry(
        ref, branch, "baz/bar", version, resolve_backports=True, auth="bizz"
    )
    mocked_gen.assert_called_with(
        "baz/bar",
        since="v1.0",
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth="bizz",
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp


def test_get_changelog_version_entry_no_tag(py_package, mocker):
    version = util.get_version()

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    branch = "foo"
    util.run("git branch baz/bar")
    commit = run("git rev-list --max-parents=0 HEAD", quiet=True)
    ref = "heads/baz/bar"
    resp = changelog.get_version_entry(ref, branch, "baz/bar", version)
    mocked_gen.assert_called_with(
        "baz/bar",
        since=commit,
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth=None,
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp

    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    resp = changelog.get_version_entry(
        ref, branch, "baz/bar", version, resolve_backports=True, auth="bizz"
    )
    mocked_gen.assert_called_with(
        "baz/bar",
        since=commit,
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth="bizz",
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp


def test_get_changelog_version_entry_since_last_stable(py_package, mocker):
    version = util.get_version()

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    branch = "foo"
    util.run("git branch baz/bar")
    util.run("git tag v1.0.0 baz/bar")
    util.run("git tag v1.1.0a0 baz/bar")
    ref = "heads/baz/bar"
    resp = changelog.get_version_entry(ref, branch, "baz/bar", version, since_last_stable=True)
    mocked_gen.assert_called_with(
        "baz/bar",
        since="v1.0.0",
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth=None,
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp


def test_get_empty_changelog(py_package, mocker):
    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.EMPTY_CHANGELOG_ENTRY
    branch = "foo"
    util.run("git branch baz/bar")
    ref = "heads/baz/bar"
    resp = changelog.get_version_entry(ref, branch, "baz/bar", "0.2.5", since="v0.2.4")
    mocked_gen.assert_called_with(
        "baz/bar",
        since="v0.2.4",
        until=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth=None,
    )

    assert "...None" not in resp


def test_splice_github_entry(py_package, mocker):
    version = util.get_version()

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    branch = "foo"
    util.run("git branch baz/bar")
    util.run("git tag v1.0.0 baz/bar")
    util.run("git tag v1.1.0a0 baz/bar")
    ref = "heads/baz/bar"
    resp = changelog.get_version_entry(ref, branch, "baz/bar", version, since_last_stable=True)

    updated = changelog.splice_github_entry(resp, testutil.GITHUB_CHANGELOG_ENTRY)

    assert "Defining contributions" in updated

    preamble = "# My title\nmy content\n"
    updated = changelog.splice_github_entry(resp, preamble + testutil.GITHUB_CHANGELOG_ENTRY)

    assert "Defining contributions" in updated
    assert preamble in updated


def test_compute_sha256(py_package):
    assert len(util.compute_sha256(py_package / "CHANGELOG.md")) == 64


def test_create_release_commit(py_package, build_mock):
    util.bump_version("0.0.2a0")
    version = util.get_version()
    util.run("pipx run build .")
    shas = util.create_release_commit(version)
    assert util.normalize_path("dist/foo-0.0.2a0.tar.gz") in shas
    assert util.normalize_path("dist/foo-0.0.2a0-py3-none-any.whl") in shas


def test_create_release_commit_hybrid(py_package, build_mock):
    # Add an npm package and test with that
    util.bump_version("0.0.2a0")
    version = util.get_version()
    testutil.create_npm_package(py_package)
    pkg_json = py_package / "package.json"
    data = json.loads(pkg_json.read_text(encoding="utf-8"))
    data["version"] = version
    pkg_json.write_text(json.dumps(data, indent=4), encoding="utf-8")
    util.run("pre-commit run --all-files", check=False)
    txt = testutil.TBUMP_NPM_TEMPLATE
    (py_package / "tbump.toml").write_text(txt, encoding="utf-8")

    util.run("pipx run build .")
    shas = util.create_release_commit(version)
    assert len(shas) == 2
    assert util.normalize_path("dist/foo-0.0.2a0.tar.gz") in shas


def test_handle_npm_config(npm_package):
    npmrc = Path("~/.npmrc").expanduser()
    existed = npmrc.exists()
    if existed:
        npmrc_text = npmrc.read_text(encoding="utf-8")
    npm.handle_npm_config("abc")
    text = npmrc.read_text(encoding="utf-8")
    assert "_authToken=abc" in text

    if existed:
        npmrc.write_text(npmrc_text, encoding="utf-8")


def test_bump_version_reg(py_package):
    for spec in ["1.0.1", "1.0.3a4"]:
        util.bump_version(spec)
        util.run("git commit -a -m 'bump version'")
        assert util.get_version() == spec
    util.bump_version("1.0.2")
    util.bump_version("next")
    assert util.get_version() == "1.0.3"
    util.bump_version("patch")
    assert util.get_version() == "1.0.4"
    util.bump_version("1.0.3a5")
    util.bump_version("next")
    assert util.get_version() == "1.0.3a6"
    util.bump_version("minor")
    assert util.get_version() == "1.1.0"


def test_bump_version_dev(py_package):
    util.bump_version("dev", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.1.0.dev0"
    util.bump_version("dev", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.1.0.dev1"
    util.bump_version("next", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.0.3"
    util.bump_version("dev", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.1.0.dev0"
    util.bump_version("patch", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.0.3"
    util.bump_version("dev", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.1.0.dev0"
    util.bump_version("minor", changelog_path="CHANGELOG.md")
    assert util.get_version() == "0.1.0"


def test_get_config_python(py_package):
    Path(util.JUPYTER_RELEASER_CONFIG).unlink()
    text = util.PYPROJECT.read_text(encoding="utf-8")
    text = testutil.TOML_CONFIG.replace("\n[", "\n[tool.jupyter-releaser.")
    util.PYPROJECT.write_text(text, encoding="utf-8")
    config = util.read_config()
    assert "before-build-python" in config["hooks"]["before-build-python"]


def test_get_config_npm(npm_package):
    Path(util.JUPYTER_RELEASER_CONFIG).unlink()
    package_json = util.PACKAGE_JSON
    data = json.loads(package_json.read_text(encoding="utf-8"))
    data["jupyter-releaser"] = toml.loads(testutil.TOML_CONFIG)
    package_json.write_text(json.dumps(data), encoding="utf-8")
    config = util.read_config()
    assert "before-build-npm" in config["hooks"]["before-build-npm"]


def test_get_config_file(git_repo):
    config = util.read_config()
    assert "before-build-python" in config["hooks"]["before-build-python"]


def test_get_latest_draft_release(mock_github):
    gh = GhApi(owner="foo", repo="bar")
    gh.create_release(
        "v1.0.0",
        "main",
        "v1.0.0",
        "body",
        True,
        True,
        files=[],
    )
    latest = util.latest_draft_release(gh)
    assert latest.name == "v1.0.0"

    # Ensure a different timestamp.
    time.sleep(1)
    gh.create_release(
        "v1.1.0",
        "bob",
        "v1.1.0",
        "body",
        True,
        True,
        files=[],
    )
    latest = util.latest_draft_release(gh)
    assert latest.name == "v1.1.0"
    latest = util.latest_draft_release(gh, "main")
    assert latest.name == "v1.0.0"


def test_parse_release_url():
    match = util.parse_release_url("https://github.com/foo/bar/releases/tag/fizz")
    assert match.groupdict() == {"owner": "foo", "repo": "bar", "tag": "fizz"}
    match = util.parse_release_url("https://api.github.com/repos/fizz/buzz/releases/tags/foo")
    assert match.groupdict() == {"owner": "fizz", "repo": "buzz", "tag": "foo"}
    match = util.parse_release_url(
        "https://github.com/foo/bar/releases/tag/untagged-8a3c19f85a0a51d3ea66"
    )
    assert match.groupdict() == {
        "owner": "foo",
        "repo": "bar",
        "tag": "untagged-8a3c19f85a0a51d3ea66",
    }


def test_extract_metadata_from_release_url(mock_github, draft_release):
    gh = GhApi(owner="foo", repo="bar")
    data = util.extract_metadata_from_release_url(gh, draft_release, "")
    assert os.environ["RH_BRANCH"] == data["branch"]


def test_prepare_environment(mock_github, draft_release):
    os.environ["GITHUB_REPOSITORY"] = "foo/bar"
    tag = draft_release.split("/")[-1]
    os.environ["RH_BRANCH"] = "bar"
    os.environ["GITHUB_REF"] = f"refs/tag/{tag}"
    os.environ["RH_DRY_RUN"] = "true"
    data = util.prepare_environment()
    assert os.environ["RH_RELEASE_URL"] == draft_release
    assert data["version_spec"] == os.environ["RH_VERSION_SPEC"]


def test_handle_since(npm_package, runner):
    runner(["prep-git", "--git-url", npm_package])
    since = util.handle_since()
    assert not since

    run("git tag v1.0.1", cwd=util.CHECKOUT_NAME)
    since = util.handle_since()
    assert since == "v1.0.1"
