from jupyter_releaser.actions.common import run_action, setup

setup()

run_action("jupyter-releaser prep-git")

run_action("jupyter-releaser check-links --force")
