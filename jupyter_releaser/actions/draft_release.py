# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from jupyter_releaser.util import run

run("jupyter-releaser prep-git")
run("jupyter-releaser bump-version")
run("jupyter-releaser check-changelog")
run("jupyter-releaser check-links")
# Make sure npm comes before python in case it produces
# files for the python package
run("jupyter-releaser build-npm")
run("jupyter-releaser check-npm")
run("jupyter-releaser build-python")
run("jupyter-releaser check-python")
run("jupyter-releaser check-manifest")
run("jupyter-releaser tag-release")
run("jupyter-releaser draft-release")
