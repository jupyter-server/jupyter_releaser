# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shutil
from pathlib import Path

from jupyter_releaser.util import CHECKOUT_NAME
from jupyter_releaser.util import log
from jupyter_releaser.util import run

check_release = os.environ.get("RH_IS_CHECK_RELEASE").lower() == "true"

if check_release:
    log("Handling Check Release action")

    # Extract the changelog
    changelog_location = os.environ.get("RH_CHANGELOG", "CHANGELOG.md")
    changelog_location = Path(CHECKOUT_NAME) / changelog_location
    changelog_text = changelog_location.read_text(encoding="utf-8")

    # Remove the checkout
    shutil.rmtree(CHECKOUT_NAME)

    # Re-install the parent dir in case it was overshadowed
    run("pip install -e .")

run("jupyter-releaser prep-git")
run("jupyter-releaser bump-version")

if check_release:
    # Override the changelog
    log("Patching the changelog")
    log(changelog_text)
    Path(changelog_location).write_text(changelog_text)

run("jupyter-releaser check-changelog")
run("jupyter-releaser check-links")
# Make sure npm comes before python in case it produces
# files for the python package
run("jupyter-releaser build-npm")
run("jupyter-releaser check-npm")
run("jupyter-releaser build-python")
run("jupyter-releaser check-python")
run("jupyter-releaser check-manifest")
run("jupyter-releaser tag-release")
run("jupyter-releaser draft-release")
