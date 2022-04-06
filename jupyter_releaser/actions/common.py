import os
from contextlib import contextmanager

from jupyter_releaser.util import run as _run


@contextmanager
def make_group(name):
    print(f"::group::{name}")
    yield
    print("::endgroup::")


def setup():
    with make_group("Common Setup"):
        # Set up env variables
        os.environ.setdefault("RH_REPOSITORY", os.environ["GITHUB_REPOSITORY"])
        os.environ.setdefault("RH_REF", os.environ["GITHUB_REF"])

        check_release = os.environ.get("RH_IS_CHECK_RELEASE", "").lower() == "true"
        if not os.environ.get("RH_BRANCH") and check_release:
            if os.environ.get("GITHUB_BASE_REF"):
                base_ref = os.environ.get("GITHUB_BASE_REF", "")
                print(f"Using GITHUB_BASE_REF: ${base_ref}")
                os.environ["RH_BRANCH"] = base_ref

            else:
                # e.g refs/head/foo or refs/tag/bar
                ref = os.environ["GITHUB_REF"]
                print(f"Using GITHUB_REF: {ref}")
                os.environ["RH_BRANCH"] = "/".join(ref.split("/")[2:])


def run_action(target, *args, **kwargs):
    with make_group(target):
        _run(target, *args, **kwargs)
