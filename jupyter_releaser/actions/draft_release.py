# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shutil
from pathlib import Path
from subprocess import CalledProcessError

from jupyter_releaser.actions.common import setup
from jupyter_releaser.changelog import extract_current
from jupyter_releaser.util import CHECKOUT_NAME
from jupyter_releaser.util import get_latest_tag
from jupyter_releaser.util import log
from jupyter_releaser.util import run

setup()

check_release = os.environ.get("RH_IS_CHECK_RELEASE", "").lower() == "true"

if check_release:
    log("Handling Check Release action")

    # Extract the changelog
    changelog_location = os.environ.get("RH_CHANGELOG", "CHANGELOG.md")
    changelog_location = Path(CHECKOUT_NAME) / changelog_location
    changelog_text = changelog_location.read_text(encoding="utf-8")

    # Remove the checkout
    shutil.rmtree(CHECKOUT_NAME)

    # Re-install jupyter-releaser if it was overshadowed
    try:
        run("jupyter-releaser --help", quiet=True, quiet_error=True)
    except CalledProcessError:
        run("pip install -q -e .")

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

if check_release:
    # Override the changelog
    log("Patching the changelog")
    Path(changelog_location).write_text(changelog_text)
    log(extract_current(changelog_location))

run("jupyter-releaser check-changelog")

# Make sure npm comes before python in case it produces
# files for the python package
run("jupyter-releaser build-npm")
run("jupyter-releaser check-npm")
run("jupyter-releaser build-python")
run("jupyter-releaser check-python")
run("jupyter-releaser check-manifest")
run("jupyter-releaser check-links")
run("jupyter-releaser tag-release")

# Run check changelog again to make sure no new PRs have been merged
# Skip if this is a check_release job
if not check_release:
    run("jupyter-releaser check-changelog")

run("jupyter-releaser draft-release")
