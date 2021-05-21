# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import os.path as osp
import traceback
from pathlib import Path
from urllib.request import OpenerDirector

from click.testing import CliRunner
from pytest import fixture

from jupyter_releaser import changelog
from jupyter_releaser import cli
from jupyter_releaser import util
from jupyter_releaser.tests import util as testutil
from jupyter_releaser.util import run


@fixture(autouse=True)
def mock_env(mocker):
    """Clear unwanted environment variables"""
    # Anything that starts with RH_ or GITHUB_
    prefixes = ["GITHUB_", "RH_"]
    env = os.environ.copy()
    for key in list(env):
        for prefix in prefixes:
            if key.startswith(prefix):
                del env[key]

    mocker.patch.dict(os.environ, env, clear=True)

    try:
        run("git config --global user.name")
    except Exception:
        run("git config --global user.name snuffy")
        run("git config --global user.email snuffy@sesame.com")

    yield


@fixture
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

    readme = tmp_path / "README.md"
    readme.write_text("Hello from foo project\n", encoding="utf-8")

    run("git add .")
    run('git commit -m "foo"')
    run(f"git remote add origin {util.normalize_path(tmp_path)}")
    run("git push origin foo")
    run("git remote set-head origin foo")
    run("git checkout -b bar foo")
    run("git fetch origin")
    yield tmp_path
    os.chdir(prev_dir)


@fixture
def py_package(git_repo):
    return testutil.create_python_package(git_repo)


@fixture
def npm_package(git_repo):
    return testutil.create_npm_package(git_repo)


@fixture
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
        run("npm init -y")
        index = new_dir / "index.js"
        index.write_text('console.log("hello")', encoding="utf-8")
        if name == "foo":
            pkg_json = new_dir / "package.json"
            sub_data = json.loads(pkg_json.read_text(encoding="utf-8"))
            sub_data["dependencies"] = dict(bar="*")
            sub_data["main"] = "index.js"
            pkg_json.write_text(json.dumps(sub_data), encoding="utf-8")
        elif name == "baz":
            pkg_json = new_dir / "package.json"
            sub_data = json.loads(pkg_json.read_text(encoding="utf-8"))
            sub_data["dependencies"] = dict(foo="*")
            sub_data["main"] = "index.js"
            pkg_json.write_text(json.dumps(sub_data), encoding="utf-8")
    os.chdir(prev_dir)
    util.run("git add .")
    util.run('git commit -a -m "Add workspaces"')
    return npm_package


@fixture
def py_dist(py_package, runner, mocker, build_mock, git_prep):
    changelog_entry = testutil.mock_changelog_entry(py_package, runner, mocker)

    # Create the dist files
    util.run("python -m build .", cwd=util.CHECKOUT_NAME)

    # Finalize the release
    runner(["tag-release"])

    return py_package


@fixture
def npm_dist(workspace_package, runner, mocker, git_prep):
    changelog_entry = testutil.mock_changelog_entry(workspace_package, runner, mocker)

    # Create the dist files
    runner(["build-npm"])

    # Finalize the release
    runner(["tag-release"])

    return workspace_package


@fixture()
def runner():
    cli_runner = CliRunner()

    def run(*args, **kwargs):
        result = cli_runner.invoke(cli.main, *args, **kwargs)
        if result.exit_code != 0:
            if result.stderr_bytes:
                print("Captured stderr\n", result.stderr, "\n\n")
            print("Catpured stdout\n", result.stdout, "\n\n")
            raise result.exception

        return result

    return run


@fixture()
def git_prep(runner, git_repo):
    runner(["prep-git", "--git-url", git_repo])


@fixture
def open_mock(mocker):
    open_mock = mocker.patch.object(OpenerDirector, "open", autospec=True)
    open_mock.return_value = testutil.MockHTTPResponse()
    yield open_mock


@fixture
def build_mock(mocker):
    orig_run = util.run

    def wrapped(cmd, **kwargs):
        if cmd == "python -m build .":
            if osp.exists(util.CHECKOUT_NAME):
                dist_dir = Path(f"{util.CHECKOUT_NAME}/dist")
            else:
                dist_dir = Path("dist")
            os.makedirs(dist_dir, exist_ok=True)
            Path(f"{dist_dir}/foo-0.0.2a0.tar.gz").write_text("hello", encoding="utf-8")
            Path(f"{dist_dir}/foo-0.0.2a0-py3-none-any.whl").write_text(
                "hello", encoding="utf-8"
            )
            return ""
        return orig_run(cmd, **kwargs)

    mock_run = mocker.patch("jupyter_releaser.util.run", wraps=wrapped)
