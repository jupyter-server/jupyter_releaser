# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.util import run


os.environ.setdefault("TWINE_USERNAME", "__token__")

if os.environ.get("RH_DRY_RUN") == "true":
    os.environ.setdefault("TWINE_COMMAND", "twine upload --skip-existing")
    os.environ.setdefault("TWINE_REPOSITORY_URL", "https://test.pypi.org/legacy/")
    os.environ.setdefault("RH_NPM_COMMAND", "npm publish --dry-run")

release_url = os.environ["release_url"]
run(f"jupyter-releaser extract-release {release_url}")
run(f"jupyter-releaser forwardport-changelog {release_url}")
run(f"jupyter-releaser publish-release {release_url}")
