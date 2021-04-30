# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyter_releaser.util import run

release_url = os.environ["release_url"]
run(f"jupyter-releaser extract-release {release_url}")
run(f"jupyter-releaser forwardport-changelog {release_url}")
run("jupyter-releaser publish-assets")
run(f"jupyter-releaser publish-release {release_url}")
