# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shutil
import tempfile
from pathlib import Path

from ghapi.core import GhApi

from jupyter_releaser import changelog, cli, util
from jupyter_releaser.util import run

VERSION_SPEC = "1.0.1"

TOML_CONFIG = """
[hooks]
"""

for name in cli.main.commands:
    TOML_CONFIG += f"'before-{name}' = \"echo before-{name} >> 'log.txt'\"\n"
    TOML_CONFIG += f"'after-{name}' = \"echo after-{name} >> 'log.txt'\"\n"

PR_ENTRY = "Mention the required GITHUB_ACCESS_TOKEN [#1](https://github.com/executablebooks/github-activity/pull/1) ([@consideRatio](https://github.com/consideRatio))"

CHANGELOG_ENTRY = f"""
## master@{{2019-09-01}}...master@{{2019-11-01}}

([full changelog](https://github.com/executablebooks/github-activity/compare/479cc4b2f5504945021e3c4ee84818a10fabf810...ed7f1ed78b523c6b9fe6b3ac29e834087e299296))

### Merged PRs

- defining contributions [#14](https://github.com/executablebooks/github-activity/pull/14) ([@choldgraf](https://github.com/choldgraf))
- updating CLI for new tags [#12](https://github.com/executablebooks/github-activity/pull/12) ([@choldgraf](https://github.com/choldgraf))
- fixing link to changelog with refs [#11](https://github.com/executablebooks/github-activity/pull/11) ([@choldgraf](https://github.com/choldgraf))
- adding contributors list [#10](https://github.com/executablebooks/github-activity/pull/10) ([@choldgraf](https://github.com/choldgraf))
- some improvements to `since` and opened issues list [#8](https://github.com/executablebooks/github-activity/pull/8) ([@choldgraf](https://github.com/choldgraf))
- Support git references etc. [#6](https://github.com/executablebooks/github-activity/pull/6) ([@consideRatio](https://github.com/consideRatio))
- adding authentication information [#2](https://github.com/executablebooks/github-activity/pull/2) ([@choldgraf](https://github.com/choldgraf))
- {PR_ENTRY}

### Contributors to this release

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2019-09-01&to=2019-11-01&type=c))

[@betatim](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Abetatim+updated%3A2019-09-01..2019-11-01&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2019-09-01..2019-11-01&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2019-09-01..2019-11-01&type=Issues)
"""

EMPTY_CHANGELOG_ENTRY = """
## main@{2021-09-15}...main@{2022-01-18}

([Full Changelog](https://github.com/QuantStack/jupyterlab-js-logs/compare/v0.2.4...None))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/QuantStack/jupyterlab-js-logs/graphs/contributors?from=2021-09-15&to=2022-01-18&type=c))

"""

GITHUB_CHANGELOG_ENTRY = """
## What's Changed
* Some improvements to `since` and opened issues list @choldgraf in https://github.com/executablebooks/github-activity/pull/8
* Defining contributions by @choldgraf in https://github.com/executablebooks/github-activity/pull/14
* Fixing link to changelog with refs by @choldgraf in https://github.com/executablebooks/github-activity/pull/11


**Full Changelog**: https://github.com/executablebooks/github-activity/compare/479cc4b2f5504945021e3c4ee84818a10fabf810...ed7f1ed78b523c6b9fe6b3ac29e834087e299296
"""


def setup_cfg_template(package_name="foo", module_name=None):
    return f"""
[metadata]
name = {package_name}
version = attr: {module_name or package_name}.__version__

[options]
zip_safe = False
include_package_data = True
py_modules = {module_name or package_name}
"""


SETUP_PY_TEMPLATE = """__import__("setuptools").setup()\n"""

LICENSE_TEMPLATE = "A fake license\n"

README_TEMPLATE = "A fake readme\n"


def pyproject_template(project_name="foo", module_name="foo", sub_packages=None):
    sub_packages = sub_packages or []
    res = f"""
[build-system]
requires = ["hatchling>=1.11"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
dynamic = ["version"]
description = "My package description"
readme = "README.md"
license = {{file = "LICENSE"}}
authors = [
  {{email = "foo@foo.com"}},
  {{name = "foo"}}
]

[tool.hatch.version]
path = "{module_name}.py"
validate-bump = false

[project.urls]
homepage = "https://foo.com"
"""
    if sub_packages:
        res += f"""
[tools.jupyter-releaser.options]
python_packages = {sub_packages}
"""
    return res


PY_MODULE_TEMPLATE = '__version__ = "0.0.1"\n'

TBUMP_NPM_TEMPLATE = """
[[file]]
src = "package.json"
search = '"version": "{current_version}"'
"""

MANIFEST_TEMPLATE = """
include *.md
include *.toml
include *.yaml
include LICENSE
"""

CHANGELOG_TEMPLATE = f"""# Changelog

{changelog.START_MARKER}

## 0.0.2

Second commit

{changelog.END_MARKER}

## 0.0.1

Initial commit
"""


def mock_changelog_entry(package_path, runner, mocker, version_spec=VERSION_SPEC):
    runner(["bump-version", "--version-spec", version_spec])
    changelog_file = "CHANGELOG.md"
    changelog = Path(util.CHECKOUT_NAME) / changelog_file
    mocked_gen = mocker.patch("jupyter_releaser.changelog.generate_activity_md")
    mocked_gen.return_value = CHANGELOG_ENTRY
    runner(["build-changelog", "--changelog-path", changelog_file])
    return changelog_file


def create_npm_package(git_repo):
    npm = util.normalize_path(shutil.which("npm"))
    run(f"{npm} init -y")

    git_repo.joinpath("index.js").write_text('console.log("hello");\n', encoding="utf-8")

    run("git add .")
    run('git commit -m "initial npm package"')

    run("git checkout foo")
    run("git pull origin bar", quiet=True)
    run("git checkout bar")
    return git_repo


def get_log():
    log = Path(util.CHECKOUT_NAME) / "log.txt"
    return log.read_text(encoding="utf-8").splitlines()


def create_python_package(git_repo, multi=False, not_matching_name=False):
    def write_files(git_repo, sub_packages=None, package_name="foo", module_name=None):

        sub_packages = sub_packages or []

        module_name = module_name or package_name

        pyproject = git_repo / "pyproject.toml"
        pyproject.write_text(
            pyproject_template(package_name, module_name, sub_packages), encoding="utf-8"
        )

        foopy = git_repo / f"{module_name}.py"
        foopy.write_text(PY_MODULE_TEMPLATE, encoding="utf-8")

        license = git_repo / "LICENSE"
        license.write_text(LICENSE_TEMPLATE, encoding="utf-8")

        here = Path(__file__).parent
        text = here.parent.parent.joinpath(".pre-commit-config.yaml").read_text(encoding="utf-8")

        readme = git_repo / "README.md"
        readme.write_text(README_TEMPLATE, encoding="utf-8")

        pre_commit = git_repo / ".pre-commit-config.yaml"
        pre_commit.write_text(text, encoding="utf-8")

    sub_packages = []
    if multi:
        packages = [{"abs_path": git_repo, "rel_path": "."}]
        for i in range(2):
            sub_package = Path(f"sub_package{i}")
            sub_packages.append(str(sub_package))
            packages.append(
                {
                    "abs_path": git_repo / sub_package,
                    "rel_path": sub_package,
                }
            )
            sub_package.mkdir()
            package_name = f"foo{i}"
            module_name = f"foo{i}bar" if not_matching_name else None
            write_files(
                git_repo / sub_package,
                package_name=package_name,
                module_name=module_name,
            )
            run(f"git add {sub_package}")
            run(f'git commit -m "initial python {sub_package}"')

    package_name = "foo"
    module_name = "foobar" if not_matching_name else None
    write_files(
        git_repo,
        sub_packages=sub_packages,
        package_name=package_name,
        module_name=module_name,
    )
    run("git add .")
    run('git commit -m "initial python package"')

    run("git checkout foo")
    run("git pull origin bar", quiet=True)
    run("git checkout bar")

    if multi:
        return packages
    else:
        return git_repo


def create_draft_release(ref="bar", files=None):
    gh = GhApi("foo", "bar")
    release = gh.create_release(ref, "bar", ref, "body", True, True)
    if files:
        with tempfile.TemporaryDirectory() as td:
            metadata_file = os.path.join(td, "metadata.json")
            with open(metadata_file, "w") as fid:
                fid.write("{}")
            gh.upload_file(release, metadata_file)
            release = util.release_for_url(gh, release.url)
        util.upload_assets(gh, files, release, "foo")
    return release
