# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import make_group, run_action, setup
from jupyter_releaser.util import CHECKOUT_NAME, get_latest_tag, log

setup()

run_action("jupyter-releaser prep-git")


# Capture the "since" argument in case we add tags befor checking changelog
# Do this before bumping the version
with make_group("Handle RH_SINCE"):
    if not os.environ.get("RH_SINCE"):
        curr_dir = os.getcwd()
        os.chdir(CHECKOUT_NAME)
        since_last_stable_env = os.environ.get("RH_SINCE_LAST_STABLE")
        since_last_stable = since_last_stable_env == "true"
        since = get_latest_tag(os.environ.get("RH_BRANCH"), since_last_stable)
        if since:
            log(f"Capturing {since} in RH_SINCE variable")
            os.environ["RH_SINCE"] = since
        os.chdir(curr_dir)

run_action("jupyter-releaser bump-version")
run_action("jupyter-releaser build-changelog")
run_action("jupyter-releaser draft-changelog")
