# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import os.path as osp
import tempfile
import time
import uuid
from pathlib import Path

import pytest
from click.testing import CliRunner
from ghapi.core import GhApi

from jupyter_releaser import cli, util
from jupyter_releaser.util import ensure_mock_github, run
from tests import util as testutil


@pytest.fixture(autouse=True)
def github_port(worker_id):
    # The worker id will be of the form "gw123" unless xdist is disabled,
    # in which case it will be "master".
    if worker_id == "master":
        return
    os.environ["MOCK_GITHUB_PORT"] = str(8000 + int(worker_id[2:]))


@pytest.fixture(autouse=True)
def mock_env(mocker):
    """Clear unwanted environment variables"""
    # Anything that starts with RH_ or GITHUB_ or PIP
    # Also clear HATCH_ENV_ACTIVE to prevent hatch 1.16+ from inheriting
    # the parent environment when running hatch version in subprocesses
    prefixes = ["GITHUB_", "RH_", "PIP_", "HATCH_ENV"]
    env = os.environ.copy()
    for key in list(env):
        for prefix in prefixes:
            if key.startswith(prefix):
                del env[key]

    mocker.patch.dict(os.environ, env, clear=True)
    return


@pytest.fixture()
def git_repo(tmp_path):
    prev_dir = os.getcwd()
    os.chdir(tmp_path)

    run("git init")
    run("git config user.name snuffy")
    run("git config user.email snuffy@sesame.com")

    run("git checkout -b foo")
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(f"dist/*\nbuild/*\n{util.CHECKOUT_NAME}\n", encoding="utf-8")

    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")

    config = Path(util.JUPYTER_RELEASER_CONFIG)
    config.write_text(testutil.TOML_CONFIG, encoding="utf-8")

    run("git add .")
    run('git commit -m "foo"')
    run(f"git remote add origin {util.normalize_path(tmp_path)}")
    run("git push origin foo")
    run("git remote set-head origin foo")
    run("git checkout -b bar foo")
    run("git fetch origin")
    yield tmp_path
    os.chdir(prev_dir)


@pytest.fixture()
def py_package(git_repo):
    return testutil.create_python_package(git_repo)


@pytest.fixture()
def py_multipackage(git_repo):
    return testutil.create_python_package(git_repo, multi=True)


@pytest.fixture()
def py_package_different_names(git_repo):
    return testutil.create_python_package(git_repo, not_matching_name=True)


@pytest.fixture()
def npm_package(git_repo):
    return testutil.create_npm_package(git_repo)


@pytest.fixture()
def workspace_package(npm_package):
    pkg_file = npm_package / "package.json"
    data = json.loads(pkg_file.read_text(encoding="utf-8"))
    data["workspaces"] = dict(packages=["packages/*"])
    data["private"] = True
    pkg_file.write_text(json.dumps(data), encoding="utf-8")

    prev_dir = Path(os.getcwd())
    for name in ["foo", "bar", "baz"]:
        new_dir = prev_dir / "packages" / name
        os.makedirs(new_dir)
        os.chdir(new_dir)
        run("npm init -y", quiet=True)
        index = new_dir / "index.js"
        index.write_text('console.log("hello")', encoding="utf-8")
        if name == "foo":
            pkg_json = new_dir / "package.json"
            sub_data = json.loads(pkg_json.read_text(encoding="utf-8"))
            sub_data["dependencies"] = dict(bar="*")
            sub_data["main"] = "index.js"
            sub_data["repository"] = dict(url=str(npm_package))
            pkg_json.write_text(json.dumps(sub_data), encoding="utf-8")
        elif name == "baz":
            pkg_json = new_dir / "package.json"
            sub_data = json.loads(pkg_json.read_text(encoding="utf-8"))
            sub_data["dependencies"] = dict(foo="*")
            sub_data["main"] = "index.js"
            sub_data["repository"] = dict(url=str(npm_package))
            pkg_json.write_text(json.dumps(sub_data), encoding="utf-8")
        elif name == "bar":
            pkg_json = new_dir / "package.json"
            sub_data = json.loads(pkg_json.read_text(encoding="utf-8"))
            sub_data["repository"] = dict(url=str(npm_package))
            pkg_json.write_text(json.dumps(sub_data), encoding="utf-8")
    os.chdir(prev_dir)
    util.run("git add .")
    util.run('git commit -a -m "Add workspaces"')
    return npm_package


@pytest.fixture()
def py_dist(py_package, runner, mocker, build_mock, git_prep):
    changelog_entry = testutil.mock_changelog_entry(py_package, runner, mocker)

    # Create the dist files
    util.run("pipx run build .", cwd=util.CHECKOUT_NAME, quiet=True)

    # Finalize the release
    runner(["tag-release"])

    return py_package


@pytest.fixture()
def npm_dist(workspace_package, runner, mocker, git_prep):
    changelog_entry = testutil.mock_changelog_entry(workspace_package, runner, mocker)

    # Create the dist files
    runner(["build-npm"])

    # Finalize the release
    runner(["tag-release"])

    return workspace_package


@pytest.fixture()
def npm_dist_prerelease(workspace_package, runner, mocker, git_prep):
    """Fixture for npm packages with a prerelease version (e.g., 1.0.0-alpha.0).

    To test npm 11+ behavior which requires --tag for prereleases.
    """
    prerelease_version = "1.0.0-alpha.0"

    changelog_entry = testutil.mock_changelog_entry(
        workspace_package, runner, mocker, version_spec=prerelease_version
    )

    # Manually update workspace package versions
    checkout_dir = Path(util.CHECKOUT_NAME)
    for pkg_dir in (checkout_dir / "packages").iterdir():
        if pkg_dir.is_dir():
            pkg_json = pkg_dir / "package.json"
            if pkg_json.exists():
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                data["version"] = prerelease_version
                pkg_json.write_text(json.dumps(data), encoding="utf-8")

    # Create the dist files
    runner(["build-npm"])

    # Finalize the release
    runner(["tag-release"])

    return workspace_package


@pytest.fixture()
def runner():
    cli_runner = CliRunner()

    def run(*args, **kwargs):
        result = cli_runner.invoke(cli.main, *args, **kwargs)
        if result.exit_code != 0:
            if result.stderr_bytes:
                print("Captured stderr\n", result.stderr, "\n\n")
            print("Captured stdout\n", result.stdout, "\n\n")
            assert result.exception is not None
            raise result.exception

        return result

    return run


@pytest.fixture()
def git_prep(runner, git_repo):
    runner(["prep-git", "--git-url", git_repo])


@pytest.fixture()
def build_mock(mocker):
    orig_run = util.run

    def wrapped(cmd, **kwargs):
        if cmd == "pipx run build .":
            if osp.exists(util.CHECKOUT_NAME):
                dist_dir = Path(f"{util.CHECKOUT_NAME}/dist")
            else:
                dist_dir = Path("dist")
            os.makedirs(dist_dir, exist_ok=True)
            Path(f"{dist_dir}/foo-0.0.2a0.tar.gz").write_text("hello", encoding="utf-8")
            Path(f"{dist_dir}/foo-0.0.2a0-py3-none-any.whl").write_text("hello", encoding="utf-8")
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)


@pytest.fixture()
def mock_github():
    proc = ensure_mock_github()
    yield proc

    if proc:
        proc.kill()
        proc.wait()


@pytest.fixture()
def release_metadata():
    return dict(
        [(k, v) for k, v in testutil.BASE_RELEASE_METADATA.items() if k != "version"]
        + [("version", uuid.uuid4().hex)]
    )


@pytest.fixture()
def draft_release(mock_github, release_metadata):
    gh = GhApi(owner="foo", repo="bar")
    data = release_metadata
    tag = "v" + data["version"]

    with tempfile.TemporaryDirectory() as d:
        metadata_path = Path(d) / "metadata.json"
        with open(metadata_path, "w") as fid:
            json.dump(data, fid)

        # Ensure this is the latest release.
        time.sleep(1)
        release = gh.create_release(tag, "bar", tag, "hi", True, True, files=[metadata_path])
    yield release.html_url
    try:
        gh.repos.delete_release(release.id)
    except Exception as e:
        print(e)
