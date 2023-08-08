"""Finalize a release."""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import run_action, setup

setup()

release_url = os.environ["RH_RELEASE_URL"]

if release_url:
    run_action("jupyter-releaser extract-release")

run_action("jupyter-releaser publish-assets")

if release_url:
    if not bool(os.environ.get('RH_DRY_RUN', False)):
        run_action("jupyter-releaser prep-git")
    run_action("jupyter-releaser tag-release")
    run_action("jupyter-releaser forwardport-changelog")
    run_action("jupyter-releaser publish-release")
