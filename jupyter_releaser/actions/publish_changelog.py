"""Remove silent placeholder entries in the changelog."""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import run_action, setup
from jupyter_releaser.util import CHECKOUT_NAME, get_default_branch

setup(False)

run_action("jupyter-releaser prep-git")

# Handle the branch.
if not os.environ.get("RH_BRANCH"):
    cur_dir = os.getcwd()
    os.chdir(CHECKOUT_NAME)
    os.environ["RH_BRANCH"] = get_default_branch() or ""
    os.chdir(cur_dir)

run_action("jupyter-releaser publish-changelog")
