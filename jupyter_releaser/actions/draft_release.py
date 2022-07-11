# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shutil
from pathlib import Path
from subprocess import CalledProcessError

from jupyter_releaser.actions.common import make_group, run_action, setup
from jupyter_releaser.changelog import extract_current
from jupyter_releaser.util import CHECKOUT_NAME, get_latest_tag, log, run

setup()

changelog_location = None
changelog_text = ""

with make_group("Handle Check Release"):
    check_release = os.environ.get("RH_IS_CHECK_RELEASE", "").lower() == "true"

    if check_release:
        log("Handling Check Release action")

        # Extract the changelog
        changelog_location_str = os.environ.get("RH_CHANGELOG", "CHANGELOG.md")
        changelog_location = Path(CHECKOUT_NAME) / changelog_location_str
        changelog_text = changelog_location.read_text(encoding="utf-8")

        # Remove the checkout
        shutil.rmtree(CHECKOUT_NAME)

        # Re-install jupyter-releaser if it was overshadowed
        try:
            run("jupyter-releaser --help", quiet=True, quiet_error=True)
        except CalledProcessError:
            run("pip install -q -e .")


run_action("jupyter-releaser prep-git")


with make_group("Handle RH_SINCE"):
    # Capture the "since" argument in case we add tags befor checking changelog
    # Do this before bumping the version
    if not os.environ.get("RH_SINCE"):
        curr_dir = os.getcwd()
        os.chdir(CHECKOUT_NAME)
        since_last_stable_env = os.environ.get("RH_SINCE_LAST_STABLE")
        since_last_stable = since_last_stable_env == "true"
        since = get_latest_tag(os.environ.get("RH_BRANCH"), since_last_stable)
        if since:
            log(f"Capturing {since} in RH_SINCE variable")
            os.environ["RH_SINCE"] = since
        os.chdir(curr_dir)


run_action("jupyter-releaser bump-version")

with make_group("Handle Check Release"):
    if check_release:
        # Override the changelog
        log("Patching the changelog")
        assert changelog_location is not None
        Path(changelog_location).write_text(changelog_text)
        log(extract_current(changelog_location))

run_action("jupyter-releaser check-changelog")

# Make sure npm comes before python in case it produces
# files for the python package
run_action("jupyter-releaser build-npm")
run_action("jupyter-releaser check-npm")
run_action("jupyter-releaser build-python")
run_action("jupyter-releaser check-python")
run_action("jupyter-releaser check-manifest")
run_action("jupyter-releaser check-links")
run_action("jupyter-releaser tag-release")

# Run check changelog again to make sure no new PRs have been merged
# Skip if this is a check_release job
if not check_release:
    run_action("jupyter-releaser check-changelog")

run_action("jupyter-releaser draft-release")
