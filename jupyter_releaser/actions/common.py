"""Common functions for actions."""
from contextlib import contextmanager

from jupyter_releaser.util import prepare_environment
from jupyter_releaser.util import run as _run


@contextmanager
def make_group(name):
    """Make a collapsed group in the GitHub Actions log."""
    print(f"::group::{name}")
    yield
    print("::endgroup::")


def setup(fetch_draft_release=True):
    """Common setup tasks for actions."""
    with make_group("Prepare Environment"):
        return prepare_environment(fetch_draft_release=fetch_draft_release)


def run_action(target, *args, **kwargs):
    """Run an action."""
    with make_group(target):
        _run(target, *args, **kwargs)
