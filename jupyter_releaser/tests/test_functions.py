# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import shutil
from pathlib import Path

import toml

from jupyter_releaser import changelog
from jupyter_releaser import util
from jupyter_releaser.tests import util as testutil
from jupyter_releaser.util import run


def test_get_branch(git_repo):
    assert util.get_branch() == "bar"
    run("git checkout foo")
    assert util.get_branch() == "foo"


def test_get_repo(git_repo, mocker):
    repo = f"{git_repo.parent.name}/{git_repo.name}"
    assert util.get_repo() == repo


def test_get_version_python(py_package):
    assert util.get_version() == "0.0.1"
    util.bump_version("0.0.2a0")
    assert util.get_version() == "0.0.2a0"


def test_get_version_npm(npm_package):
    assert util.get_version() == "1.0.0"
    npm = util.normalize_path(shutil.which("npm"))
    run(f"{npm} version patch")
    assert util.get_version() == "1.0.1"


def test_format_pr_entry(mocker, open_mock):
    data = dict(title="foo", user=dict(login="bar", html_url=testutil.HTML_URL))
    open_mock.return_value = testutil.MockHTTPResponse(data)
    resp = changelog.format_pr_entry("snuffy/foo", 121, auth="baz")
    open_mock.assert_called_once()

    assert resp.startswith("- ")


def test_get_changelog_version_entry(py_package, mocker):
    version = util.get_version()

    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    branch = "foo"
    resp = changelog.get_version_entry(branch, "bar/baz", version)
    mocked_gen.assert_called_with(
        "bar/baz", since=None, kind="pr", branch=branch, heading_level=2, auth=None
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp

    mocked_gen.return_value = testutil.CHANGELOG_ENTRY
    resp = changelog.get_version_entry(
        branch, "bar/baz", version, resolve_backports=True, auth="bizz"
    )
    mocked_gen.assert_called_with(
        "bar/baz",
        since=None,
        kind="pr",
        branch=branch,
        heading_level=2,
        auth="bizz",
    )

    assert f"## {version}" in resp
    assert testutil.PR_ENTRY in resp


def test_compute_sha256(py_package):
    assert len(util.compute_sha256(py_package / "CHANGELOG.md")) == 64


def test_create_release_commit(py_package, build_mock):
    util.bump_version("0.0.2a0")
    version = util.get_version()
    util.run("python -m build .")
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
    txt = (py_package / "tbump.toml").read_text(encoding="utf-8")
    txt += testutil.TBUMP_NPM_TEMPLATE
    (py_package / "tbump.toml").write_text(txt, encoding="utf-8")

    util.run("python -m build .")
    shas = util.create_release_commit(version)
    assert len(shas) == 2
    assert util.normalize_path("dist/foo-0.0.2a0.tar.gz") in shas


def test_bump_version(py_package):
    for spec in ["1.0.1", "1.0.1.dev1", "1.0.3a4"]:
        util.bump_version(spec)
        util.run("git commit -a -m 'bump version'")
        assert util.get_version() == spec


def test_get_config_python(py_package):
    text = util.PYPROJECT.read_text(encoding="utf-8")
    text = testutil.TOML_CONFIG.replace("\n[", "\n[tool.jupyter-releaser.")
    util.PYPROJECT.write_text(text, encoding="utf-8")
    config = util.read_config()
    assert config["hooks"]["before-build-python"] == "python setup.py --version"
    assert config["options"]["dist_dir"] == "foo"


def test_get_config_npm(npm_package):
    package_json = util.PACKAGE_JSON
    data = json.loads(package_json.read_text(encoding="utf-8"))
    data["jupyter-releaser"] = toml.loads(testutil.TOML_CONFIG)
    package_json.write_text(json.dumps(data))
    config = util.read_config()
    assert config["hooks"]["after-build-python"] == [
        "python setup.py --version",
        "python setup.py --name",
    ]
    assert config["options"]["dist_dir"] == "foo"


def test_get_config_file(git_repo):
    config = util.JUPYTER_RELEASER_CONFIG
    config.write_text(testutil.TOML_CONFIG, encoding="utf-8")
    config = util.read_config()
    assert config["hooks"]["before-build-python"] == "python setup.py --version"
    assert config["options"]["dist_dir"] == "foo"
