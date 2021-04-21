# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import shutil
from pathlib import Path

from jupyter_releaser import changelog
from jupyter_releaser import util
from jupyter_releaser.util import run


VERSION_SPEC = "1.0.1"

TOML_CONFIG = """
[hooks]
before-build-python = "python setup.py --version"
after-build-python = ["python setup.py --version", "python setup.py --name"]

[options]
dist_dir = "foo"
"""

PR_ENTRY = "Mention the required GITHUB_ACCESS_TOKEN [#1](https://github.com/executablebooks/github-activity/pull/1) ([@consideRatio](https://github.com/consideRatio))"

CHANGELOG_ENTRY = f"""
## master@{{2019-09-01}}...master@{{2019-11-01}}

([full changelog](https://github.com/executablebooks/github-activity/compare/479cc4b2f5504945021e3c4ee84818a10fabf810...ed7f1ed78b523c6b9fe6b3ac29e834087e299296))

### Merged PRs

* defining contributions [#14](https://github.com/executablebooks/github-activity/pull/14) ([@choldgraf](https://github.com/choldgraf))
* updating CLI for new tags [#12](https://github.com/executablebooks/github-activity/pull/12) ([@choldgraf](https://github.com/choldgraf))
* fixing link to changelog with refs [#11](https://github.com/executablebooks/github-activity/pull/11) ([@choldgraf](https://github.com/choldgraf))
* adding contributors list [#10](https://github.com/executablebooks/github-activity/pull/10) ([@choldgraf](https://github.com/choldgraf))
* some improvements to `since` and opened issues list [#8](https://github.com/executablebooks/github-activity/pull/8) ([@choldgraf](https://github.com/choldgraf))
* Support git references etc. [#6](https://github.com/executablebooks/github-activity/pull/6) ([@consideRatio](https://github.com/consideRatio))
* adding authentication information [#2](https://github.com/executablebooks/github-activity/pull/2) ([@choldgraf](https://github.com/choldgraf))
* {PR_ENTRY}

### Contributors to this release

([GitHub contributors page for this release](https://github.com/executablebooks/github-activity/graphs/contributors?from=2019-09-01&to=2019-11-01&type=c))

[@betatim](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Abetatim+updated%3A2019-09-01..2019-11-01&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3Acholdgraf+updated%3A2019-09-01..2019-11-01&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Aexecutablebooks%2Fgithub-activity+involves%3AconsideRatio+updated%3A2019-09-01..2019-11-01&type=Issues)
"""

SETUP_CFG_TEMPLATE = """
[metadata]
name = foo
version = attr: foo.__version__
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
py_modules = foo
"""

SETUP_PY_TEMPLATE = """__import__("setuptools").setup()\n"""


PYPROJECT_TEMPLATE = """
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
"""

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

TBUMP_PY_TEMPLATE = """
[[file]]
src = "foo.py"
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
    run("git pull origin bar")
    run("git checkout bar")
    return git_repo


def create_python_package(git_repo):
    setuppy = git_repo / "setup.py"
    setuppy.write_text(SETUP_PY_TEMPLATE, encoding="utf-8")

    setuppy = git_repo / "setup.cfg"
    setuppy.write_text(SETUP_CFG_TEMPLATE, encoding="utf-8")

    tbump = git_repo / "tbump.toml"
    tbump.write_text(TBUMP_BASE_TEMPLATE + TBUMP_PY_TEMPLATE, encoding="utf-8")

    pyproject = git_repo / "pyproject.toml"
    pyproject.write_text(PYPROJECT_TEMPLATE, encoding="utf-8")

    foopy = git_repo / "foo.py"
    foopy.write_text(PY_MODULE_TEMPLATE, encoding="utf-8")

    manifest = git_repo / "MANIFEST.in"
    manifest.write_text(MANIFEST_TEMPLATE, encoding="utf-8")

    here = Path(__file__).parent
    text = here.parent.parent.joinpath(".pre-commit-config.yaml").read_text(
        encoding="utf-8"
    )

    pre_commit = git_repo / ".pre-commit-config.yaml"
    pre_commit.write_text(text, encoding="utf-8")

    run("git add .")
    run('git commit -m "initial python package"')

    run("git checkout foo")
    run("git pull origin bar")
    run("git checkout bar")

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
