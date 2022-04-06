# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.actions.common import run_action

release_url = os.environ["release_url"]

if release_url:
    run_action(f"jupyter-releaser extract-release {release_url}")

run_action(f"jupyter-releaser publish-assets {release_url}")

if release_url:
    run_action(f"jupyter-releaser forwardport-changelog {release_url}")
    run_action(f"jupyter-releaser publish-release {release_url}")
