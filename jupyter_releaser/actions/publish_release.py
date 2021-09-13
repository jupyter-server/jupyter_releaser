# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.util import CHECKOUT_NAME
from jupyter_releaser.util import get_repo
from jupyter_releaser.util import run

release_url = os.environ["release_url"]
run(f"jupyter-releaser extract-release {release_url}")
run(f"jupyter-releaser forwardport-changelog {release_url}")

# Extract the pypi token
twine_pwd = os.environ.get("PYPI_TOKEN", "")
pypi_token_map = os.environ.get("PYPI_TOKEN_MAP", "").replace(r"\n", "\n")
if pypi_token_map:
    pwd = os.getcwd()
    os.chdir(CHECKOUT_NAME)
    repo_name = get_repo()
    for line in pypi_token_map.splitlines():
        name, _, token = line.partition(",")
        if name == repo_name:
            twine_pwd = token
    os.chdir(pwd)
os.environ["TWINE_PASSWORD"] = twine_pwd

run("jupyter-releaser publish-assets")
run(f"jupyter-releaser publish-release {release_url}")
