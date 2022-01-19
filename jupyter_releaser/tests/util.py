# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import shutil
from pathlib import Path

from jupyter_releaser import changelog
from jupyter_releaser import cli
from jupyter_releaser import util
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


def setup_cfg_template(package_name="foo", module_name=None):
    return f"""
[metadata]
name = {package_name}
version = attr: {module_name or package_name}.__version__
description = My package description
long_description = file: README.md
long_description_content_type = text/markdown
license = BSD 3-Clause License
author = foo
author_email = foo@foo.com
url = https://foo.com

[options]
zip_safe = False
include_package_data = True
py_modules = {module_name or package_name}
"""


SETUP_PY_TEMPLATE = """__import__("setuptools").setup()\n"""


def pyproject_template(sub_packages=[]):
    res = """
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
"""
    if sub_packages:
        res += f"""
[tools.jupyter-releaser.options]
python_packages = {sub_packages}
"""
    return res


PY_MODULE_TEMPLATE = '__version__ = "0.0.1"\n'


TBUMP_BASE_TEMPLATE = r"""
[version]
current = "0.0.1"
regex = '''
  (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)
  ((?P<channel>a|b|rc|.dev)(?P<release>\d+))?
'''

[git]
message_template = "Bump to {new_version}"
tag_template = "v{new_version}"
"""


def tbump_py_template(package_name="foo"):
    return f"""
[[file]]
src = "{package_name}.py"
"""


TBUMP_NPM_TEMPLATE = """
[[file]]
src = "package.json"
search = '"version": "{current_version}"'
"""

MANIFEST_TEMPLATE = """
include *.md
include *.toml
include *.yaml
"""

CHANGELOG_TEMPLATE = f"""# Changelog

{changelog.START_MARKER}

## 0.0.1

Initial commit

{changelog.END_MARKER}
"""

HTML_URL = "https://github.com/snuffy/test/releases/tag/bar"
URL = "https://api.gihub.com/repos/snuffy/test/releases/tags/bar"
REPO_DATA = dict(
    body="bar",
    tag_name=f"v{VERSION_SPEC}",
    target_commitish="bar",
    name="foo",
    prerelease=False,
    draft=True,
    created_at="2013-02-27T19:35:32Z",
)


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
    git_repo.joinpath("index.js").write_text('console.log("hello")', encoding="utf-8")
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
    def write_files(git_repo, sub_packages=[], package_name="foo", module_name=None):

        module_name = module_name or package_name

        setuppy = git_repo / "setup.py"
        setuppy.write_text(SETUP_PY_TEMPLATE, encoding="utf-8")

        setuppy = git_repo / "setup.cfg"
        setuppy.write_text(
            setup_cfg_template(package_name, module_name), encoding="utf-8"
        )

        tbump = git_repo / "tbump.toml"
        tbump.write_text(
            TBUMP_BASE_TEMPLATE + tbump_py_template(package_name),
            encoding="utf-8",
        )

        pyproject = git_repo / "pyproject.toml"
        pyproject.write_text(pyproject_template(sub_packages), encoding="utf-8")

        foopy = git_repo / f"{module_name}.py"
        foopy.write_text(PY_MODULE_TEMPLATE, encoding="utf-8")

        manifest = git_repo / "MANIFEST.in"
        manifest.write_text(MANIFEST_TEMPLATE, encoding="utf-8")

        here = Path(__file__).parent
        text = here.parent.parent.joinpath(".pre-commit-config.yaml").read_text(
            encoding="utf-8"
        )

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


class MockHTTPResponse:
    header = {}
    status = 200

    def __init__(self, data=None):
        self.url = ""
        data = data or {}
        defaults = dict(id="foo", html_url=HTML_URL, url=URL, upload_url=URL)
        if isinstance(data, list):
            for datum in data:
                for key in defaults:
                    datum.setdefault(key, defaults[key])
        else:
            for key in defaults:
                data.setdefault(key, defaults[key])
        self.data = json.dumps(data).encode("utf-8")
        self.headers = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def read(self, amt=None):
        return self.data

    @property
    def status(self):
        return self.code


class MockRequestResponse:
    def __init__(self, filename, status_code=200):
        self.filename = filename
        self.status_code = status_code

    def raise_for_status(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def iter_content(self, *args, **kwargs):
        with open(self.filename, "rb") as fid:
            return [fid.read()]
