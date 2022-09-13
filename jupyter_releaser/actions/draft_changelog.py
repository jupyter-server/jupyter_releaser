# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import make_group, run_action, setup
from jupyter_releaser.util import CHECKOUT_NAME, get_default_branch, handle_since

setup(False)

run_action("jupyter-releaser prep-git")

# Handle the branch.
if not os.environ.get("RH_BRANCH"):
    cur_dir = os.getcwd()
    os.chdir(CHECKOUT_NAME)
    os.environ["RH_BRANCH"] = get_default_branch() or ""
    os.chdir(cur_dir)

# Capture the "since" variable in case we add tags before checking changelog
# Do this before bumping the version.
with make_group("Handle RH_SINCE"):
    handle_since()

run_action("jupyter-releaser bump-version")
run_action("jupyter-releaser build-changelog")
run_action("jupyter-releaser draft-changelog")
