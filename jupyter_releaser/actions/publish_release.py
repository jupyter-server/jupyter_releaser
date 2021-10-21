# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.util import get_default_branch, run

release_url = os.environ["release_url"]
default_branch = get_default_branch()

if release_url:
    run(f"jupyter-releaser extract-release {release_url}")
    run(
        f"jupyter-releaser forwardport-changelog {release_url} --branch {default_branch}"
    )

run(f"jupyter-releaser publish-assets {release_url}")

if release_url:
    run(f"jupyter-releaser publish-release {release_url}")
