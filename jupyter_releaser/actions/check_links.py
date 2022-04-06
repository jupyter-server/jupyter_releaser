from jupyter_releaser.actions.common import run_action
from jupyter_releaser.actions.common import setup

setup()

run_action("jupyter-releaser prep-git")

run_action("jupyter-releaser check-links --force")
