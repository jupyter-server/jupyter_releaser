# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import sys

from jupyter_releaser.actions.common import run_action, setup
from jupyter_releaser.util import actions_output, get_gh_object, log, release_for_url

setup()

# Skip if we already have asset shas.
release_url = os.environ["RH_RELEASE_URL"]
owner, repo = os.environ["RH_REPOSITORY"].split("/")
auth = os.environ["GITHUB_ACCESS_TOKEN"]
gh = get_gh_object(False, owner=owner, repo=repo, token=auth)
release = release_for_url(gh, release_url)
for asset in release.assets:
    if asset.name == "asset_shas.json":
        log("Skipping populate assets")
        actions_output("release_url", release_url)
        sys.exit(0)

dry_run = os.environ.get("RH_DRY_RUN", "").lower() == "true"

if not os.environ.get("RH_RELEASE_URL"):
    raise RuntimeError("Cannot complete Draft Release, no draft GitHub release url found!")

run_action("jupyter-releaser prep-git")
run_action("jupyter-releaser ensure-sha")
run_action("jupyter-releaser bump-version")
run_action("jupyter-releaser extract-changelog")

# Make sure npm comes before python in case it produces
# files for the python package
run_action("jupyter-releaser build-npm")
run_action("jupyter-releaser check-npm")
run_action("jupyter-releaser build-python")
run_action("jupyter-releaser check-python")
run_action("jupyter-releaser tag-release")
run_action("jupyter-releaser ensure-sha")
run_action("jupyter-releaser populate-release")
