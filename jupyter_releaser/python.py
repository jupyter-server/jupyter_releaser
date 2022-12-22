# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import atexit
import os
import os.path as osp
import re
import shlex
from glob import glob
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen
from tempfile import TemporaryDirectory

from jupyter_releaser import util

PYPROJECT = util.PYPROJECT
SETUP_PY = util.SETUP_PY


def build_dist(dist_dir, clean=True):
    """Build the python dist files into a dist folder"""
    # Clean the dist folder of existing npm tarballs
    os.makedirs(dist_dir, exist_ok=True)
    dest = Path(dist_dir)
    if clean:
        for pkg in glob(f"{dest}/*.gz") + glob(f"{dest}/*.whl"):
            os.remove(pkg)

    util.run(f"pipx run build --outdir {dest} .", quiet=True, show_cwd=True)


def check_dist(
    dist_file,
    test_cmd="",
    python_imports=None,
    check_cmd="pipx run twine check --strict {dist_file}",
    extra_check_cmds=None,
    resource_paths=None,
):
    """Check a Python package locally (not as a cli)"""
    resource_paths = resource_paths or []
    dist_file = util.normalize_path(dist_file)
    dist_dir = os.path.dirname(dist_file)  # used for check cmds.

    for cmd in [check_cmd] + list(extra_check_cmds or []):
        util.run(cmd.format(**locals()))

    test_commands = []

    if test_cmd:
        test_commands.append(test_cmd)
    elif python_imports is not None:
        test_commands.extend([f'python -c "import {name}"' for name in python_imports])
    else:
        # Get the package name from the dist file name
        match = re.match(r"(\S+)-\d", osp.basename(dist_file))
        assert match is not None
        name = match.groups()[0]
        name = name.replace("-", "_")
        test_commands.append(f'python -c "import {name}"')

    # Create venvs to install dist file
    # run the test command in the venv
    with TemporaryDirectory() as td:
        env_path = util.normalize_path(osp.abspath(td))
        if os.name == "nt":  # pragma: no cover
            bin_path = f"{env_path}/Scripts/"
        else:
            bin_path = f"{env_path}/bin"

        # Create the virtual env, upgrade pip,
        # install, and run test command
        util.run(f"python -m venv {env_path}")
        util.run(f"{bin_path}/python -m pip install -q -U pip")
        util.run(f"{bin_path}/pip install -q {dist_file}")
        try:
            for cmd in test_commands:
                util.run(f"{bin_path}/{cmd}")
        except CalledProcessError as e:
            if test_cmd == "":
                util.log(
                    'You may need to set "check_imports" to appropriate Python package names in the config file.'
                )
            raise e
        for resource_path in resource_paths:
            name, _, _ = resource_path.partition("/")
            test_file = Path(td) / "test_path.py"
            test_text = f"""
from importlib.metadata import PackagePath, files
assert PackagePath('{resource_path}') in files('{name}')
"""
            test_file.write_text(test_text, encoding="utf-8")
            test_file = util.normalize_path(test_file)
            cmd = f"{bin_path}/python {test_file}"
            util.run(cmd)


def get_pypi_token(release_url, python_package):
    """Get the PyPI token

    Note: Do not print the token in CI since it will not be sanitized
    if it comes from the PYPI_TOKEN_MAP"""
    twine_pwd = os.environ.get("PYPI_TOKEN", "")
    pypi_token_map = os.environ.get("PYPI_TOKEN_MAP", "").replace(r"\n", "\n")
    if pypi_token_map and release_url:
        parts = (
            release_url.replace(util.get_mock_github_url() + "/", "")
            .replace("https://github.com/", "")
            .split("/")
        )
        repo_name = f"{parts[0]}/{parts[1]}"
        if python_package != ".":
            repo_name += f"/{python_package}"
        util.log(f"Looking for PYPI token for {repo_name} in token map")
        for line in pypi_token_map.splitlines():
            name, _, token = line.partition(",")
            if name == repo_name:
                twine_pwd = token.strip()
                util.log(f"Found PYPI token in map ending in {twine_pwd[-5:]}")
    elif twine_pwd:
        util.log("Using PYPI token from PYPI_TOKEN")
    else:
        util.log("PYPI token not found")

    return twine_pwd


def start_local_pypi():
    """Start a local PyPI server"""
    temp_dir = TemporaryDirectory()
    cmd = f"pypi-server run -p 8081  -P . -a . -o  -v {temp_dir.name}"
    proc = Popen(shlex.split(cmd), stdout=PIPE)
    # Wait for the server to start
    while True:
        assert proc.stdout is not None
        line = proc.stdout.readline().decode("utf-8").strip()
        util.log(line)
        if "Listening on" in line:
            break
    atexit.register(proc.kill)
    atexit.register(temp_dir.cleanup)
