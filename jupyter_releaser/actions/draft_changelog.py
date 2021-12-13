# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import setup
from jupyter_releaser.util import CHECKOUT_NAME
from jupyter_releaser.util import get_latest_tag
from jupyter_releaser.util import log
from jupyter_releaser.util import run

setup()
run("jupyter-releaser prep-git")

# Capture the "since" argument in case we add tags befor checking changelog
# Do this before bumping the version
if not os.environ.get("RH_SINCE"):
    curr_dir = os.getcwd()
    os.chdir(CHECKOUT_NAME)
    since_last_stable = os.environ.get("RH_SINCE_LAST_STABLE")
    since = get_latest_tag(os.environ.get("RH_BRANCH"), since_last_stable)
    if since:
        log(f"Capturing {since} in RH_SINCE variable")
        os.environ["RH_SINCE"] = since
    os.chdir(curr_dir)

run("jupyter-releaser bump-version")
run("jupyter-releaser build-changelog")
run("jupyter-releaser draft-changelog")
