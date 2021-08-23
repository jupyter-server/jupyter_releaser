import os
from pathlib import Path

from jupyter_releaser.changelog import get_version_entry
from jupyter_releaser.util import CHECKOUT_NAME
from jupyter_releaser.util import run

target = os.environ.get("RH_REPOSITORY")
branch = os.environ.get("RH_BRANCH")
ref = os.environ.get("RH_REF")
since = os.environ.get("RH_SINCE")
until = os.environ.get("INPUT_UNTIL")
convert_to_rst = os.environ.get("INPUT_CONVERT_TO_RST", "")

print("Generating changelog")
print("target:", target)
print("branch:", branch)
print("convert to rst:", convert_to_rst)

run("jupyter-releaser prep-git")
orig_dir = os.getcwd()
os.chdir(CHECKOUT_NAME)
output = get_version_entry(ref, branch, target, "current", since=since, until=until)

if convert_to_rst.lower() == "true":
    from pypandoc import convert_text

    output = convert_text(output, "rst", "markdown")
print("\n\n------------------------------")
print(output, "------------------------------\n\n")
os.chdir(orig_dir)
Path("CHANGELOG_ENTRY.md").write_text(output, encoding="utf-8")
