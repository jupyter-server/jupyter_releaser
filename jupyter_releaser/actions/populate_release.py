# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os

from jupyter_releaser.actions.common import run_action, setup
from jupyter_releaser.util import ensure_sha, log

data = setup()

if len(data.get("asset_shas", [])):
    log("Skipping populate assets")

dry_run = os.environ.get("RH_DRY_RUN", "").lower() == "true"

if not dry_run:
    ensure_sha()

if not os.environ.get("RH_RELEASE_URL"):
    raise RuntimeError("Cannot complete Draft Release, no draft GitHub release url found!")

run_action("jupyter-releaser prep-git")
run_action("jupyter-releaser bump-version")

# Make sure npm comes before python in case it produces
# files for the python package
run_action("jupyter-releaser build-npm")
run_action("jupyter-releaser check-npm")
run_action("jupyter-releaser build-python")
run_action("jupyter-releaser check-python")
run_action("jupyter-releaser tag-release")

if not dry_run:
    ensure_sha()
run_action("jupyter-releaser populate-release")
