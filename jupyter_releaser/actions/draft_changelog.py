# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from jupyter_releaser.util import run

run("jupyter-releaser prep-git")
run("jupyter-releaser bump-version")
run("jupyter-releaser build-changelog")
run("jupyter-releaser draft-changelog")
