# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_releaser.actions.common import run_action, setup

setup()

run_action("jupyter-releaser prep-git")
run_action("jupyter-releaser bump-version")

# TODO: make this compare files changed since the sha in the metadata.
run_action("jupyter-releaser check-changelog")

# Make sure npm comes before python in case it produces
# files for the python package
run_action("jupyter-releaser build-npm")
run_action("jupyter-releaser check-npm")
run_action("jupyter-releaser build-python")
run_action("jupyter-releaser check-python")
run_action("jupyter-releaser check-manifest")
run_action("jupyter-releaser check-links")
run_action("jupyter-releaser tag-release")

run_action("jupyter-releaser check-changelog")
run_action("jupyter-releaser draft-release")
