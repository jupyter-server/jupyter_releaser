# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import shutil
import tempfile
from pathlib import Path

from ghapi.core import GhApi
from ruamel.yaml import YAML

from jupyter_releaser import changelog, cli, util
from jupyter_releaser.util import run

VERSION_SPEC = "1.0.1"

TOML_CONFIG = """
[hooks]
"""

for name in cli.main.commands:
    TOML_CONFIG += f"'before-{name}' = \"echo before-{name} >> 'log.txt'\"\n"
    TOML_CONFIG += f"'after-{name}' = \"echo after-{name} >> 'log.txt'\"\n"

PR_ENTRY = "Add link to the blog post to the documentation [#591](https://github.com/jupyter-server/jupyter_releaser/pull/591) ([@jtpio](https://github.com/jtpio), [@krassowski](https://github.com/krassowski))"

CHANGELOG_ENTRY = f"""
## main@{{2024-10-01}}...main@{{2024-12-01}}

([full changelog](https://github.com/jupyter-server/jupyter_releaser/compare/4fe67ed3f81c41131d231a19696d912bb0abfb14...44e858497e4364a7546b7bd3cd08228b5563d027))

### Maintenance and upkeep improvements

- Fix "test minimum versions" job [#597](https://github.com/jupyter-server/jupyter_releaser/pull/597) ([@krassowski](https://github.com/krassowski), [@brichet](https://github.com/brichet))
- Pin `pypiserver` to v2.2.0 [#596](https://github.com/jupyter-server/jupyter_releaser/pull/596) ([@krassowski](https://github.com/krassowski), [@brichet](https://github.com/brichet))

### Documentation improvements

- {PR_ENTRY}
- Add FAQ section about publish to `npm` only [#590](https://github.com/jupyter-server/jupyter_releaser/pull/590) ([@jtpio](https://github.com/jtpio), [@krassowski](https://github.com/krassowski))
- Add link to GitHub repo in docs navbar [#589](https://github.com/jupyter-server/jupyter_releaser/pull/589) ([@krassowski](https://github.com/krassowski), [@jtpio](https://github.com/jtpio))
- Add more content to the FAQ [#588](https://github.com/jupyter-server/jupyter_releaser/pull/588) ([@jtpio](https://github.com/jtpio), [@krassowski](https://github.com/krassowski))
- Add `hatch` scripts to build, serve and watch the docs + docs improvements [#587](https://github.com/jupyter-server/jupyter_releaser/pull/587) ([@jtpio](https://github.com/jtpio), [@krassowski](https://github.com/krassowski))
- Fix code indentation in README.md [#586](https://github.com/jupyter-server/jupyter_releaser/pull/586) ([@jtpio](https://github.com/jtpio), [@krassowski](https://github.com/krassowski))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2024-10-01&to=2024-12-01&type=c))

@brichet ([activity](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Abrichet+updated%3A2024-10-01..2024-12-01&type=Issues)) | @jtpio ([activity](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2024-10-01..2024-12-01&type=Issues)) | @krassowski ([activity](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Akrassowski+updated%3A2024-10-01..2024-12-01&type=Issues))
"""

EMPTY_CHANGELOG_ENTRY = """
## main@{2024-08-01}...main@{2024-08-15}

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/76ce4aa66e668f50b2f8eb4fe0a02a14659504fa...None))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2024-08-01&to=2024-08-15&type=c))

"""

GITHUB_CHANGELOG_ENTRY = """
## What's Changed
* Fix test minimum versions job by @krassowski in https://github.com/jupyter-server/jupyter_releaser/pull/597
* Pin pypiserver to v2.2.0 by @krassowski in https://github.com/jupyter-server/jupyter_releaser/pull/596
* Add blog post link to the documentation by @jtpio in https://github.com/jupyter-server/jupyter_releaser/pull/591


**Full Changelog**: https://github.com/jupyter-server/jupyter_releaser/compare/4fe67ed3f81c41131d231a19696d912bb0abfb14...44e858497e4364a7546b7bd3cd08228b5563d027
"""


BASE_RELEASE_METADATA = dict(
    version_spec="foo",
    branch="bar",
    repo="fizz",
    since="buzz",
    since_last_stable=False,
    post_version_spec="dev",
    post_version_message="hi",
    silent=False,
)


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

    # Add the npm provenance info.
    pack_json = Path(git_repo / "package.json")
    with pack_json.open() as fid:
        data = json.load(fid)
    data["repository"] = dict(url=str(git_repo))
    with pack_json.open("w") as fid:
        json.dump(data, fid)

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
        text = here.parent.joinpath(".pre-commit-config.yaml").read_text(encoding="utf-8")

        # Remove sp-repo-review and don't check yaml files.
        yaml = YAML(typ="safe")
        table = yaml.load(text)
        for item in list(table["repos"]):
            if item["repo"] == "https://github.com/scientific-python/cookie":
                table["repos"].remove(item)

        pre_commit = git_repo / ".pre-commit-config.yaml"
        with open(str(pre_commit), "w") as fid:
            yaml.dump(table, fid)

        readme = git_repo / "README.md"
        readme.write_text(README_TEMPLATE, encoding="utf-8")

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
