import os
import sys
from pathlib import Path

from jupyter_releaser.changelog import get_version_entry

target = sys.argv[-1]
branch = os.environ.get("INPUT_BRANCH")
since = os.environ.get("INPUT_SINCE")
until = os.environ.get("INPUT_UNTIL")
convert_to_rst = os.environ.get("INPUT_CONVERT_TO_RST", "")

print("Generating changelog")
print("target:", target)
print("branch:", branch)
print("convert to rst:", convert_to_rst)

output = get_version_entry(branch, target, "current", since=since, until=until)
if convert_to_rst.lower() == "true":
    from pypandoc import convert_text

    output = convert_text(output, "rst", "markdown")
print("\n\n------------------------------")
print(output, "------------------------------\n\n")
Path("changelog.md").write_text(output, encoding="utf-8")
