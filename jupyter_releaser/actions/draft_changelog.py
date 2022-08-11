# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from jupyter_releaser.actions.common import make_group, run_action, setup
from jupyter_releaser.util import handle_since

setup()

run_action("jupyter-releaser prep-git")

# Capture the "since" variable in case we add tags before checking changelog
# Do this before bumping the version.
with make_group("Handle RH_SINCE"):
    handle_since()

run_action("jupyter-releaser bump-version")
run_action("jupyter-releaser build-changelog")
run_action("jupyter-releaser draft-changelog")
