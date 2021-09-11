# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.util import run

# First extract the pypi token
twine_pwd = os.environ.get("PYPI_TOKEN")
pypi_token_map = os.environ.get("PYPI_TOKEN_MAP", "").replace(r"\n", "\n")
if pypi_token_map:
    for line in pypi_token_map.splitlines():
        name, _, token = line.partition(",")
        if name == os.environ["RH_REPOSITORY"]:
            twine_pwd = token
os.environ["TWINE_PASSWORD"] = token


release_url = os.environ["release_url"]
run(f"jupyter-releaser extract-release {release_url}")
run(f"jupyter-releaser forwardport-changelog {release_url}")
run("jupyter-releaser publish-assets")
run(f"jupyter-releaser publish-release {release_url}")
