from jupyter_releaser.actions.common import setup
from jupyter_releaser.util import run

setup()
run("jupyter-releaser prep-git")
run("jupyter-releaser check-links --force")
