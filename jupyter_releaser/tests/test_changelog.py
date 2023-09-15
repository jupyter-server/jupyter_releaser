# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import subprocess

from pytest import fixture

from jupyter_releaser.changelog import (
    END_MARKER,
    END_SILENT_MARKER,
    START_MARKER,
    START_SILENT_MARKER,
    update_changelog,
)
from jupyter_releaser.tests import util as testutil


@fixture
def mock_py_package(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(testutil.pyproject_template(), encoding="utf-8")

    foopy = tmp_path / "foo.py"
    foopy.write_text(testutil.PY_MODULE_TEMPLATE, encoding="utf-8")


def test_update_changelog(tmp_path, mock_py_package):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")

    os.chdir(tmp_path)
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY)

    new_changelog = changelog.read_text(encoding="utf-8")

    assert f"{START_MARKER}\n{testutil.CHANGELOG_ENTRY}\n{END_MARKER}" in new_changelog


def test_silent_update_changelog(tmp_path, mock_py_package):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")
    os.chdir(tmp_path)
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY, True)

    new_changelog = changelog.read_text(encoding="utf-8")

    assert (
        f"{START_MARKER}\n\n{START_SILENT_MARKER}\n\n## 0.0.1\n\n{END_SILENT_MARKER}\n\n{END_MARKER}"
        in new_changelog
    )


def test_update_changelog_with_silent_entry(tmp_path, mock_py_package):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")
    os.chdir(tmp_path)

    # Update changelog for current version
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY, True)
    # Bump version
    subprocess.check_call(["pipx", "run", "hatch", "version", "patch"], cwd=tmp_path)  # noqa S603
    # Update changelog for the new version
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY)

    new_changelog = changelog.read_text(encoding="utf-8")

    assert f"{START_SILENT_MARKER}\n\n## 0.0.1\n\n{END_SILENT_MARKER}" in new_changelog
    assert (
        f"{START_MARKER}\n\n{START_SILENT_MARKER}\n\n## 0.0.1\n\n{END_SILENT_MARKER}\n\n{END_MARKER}"
        not in new_changelog
    )


# @pytest.mark.parametrize('release_metadata', [testutil.BASE_RELEASE_METADATA | {"version": "0.0.0"}])
# def test_remove_placeholder_entries(tmp_path, release_metadata, draft_release):

#     changelog = tmp_path / "CHANGELOG.md"
#     placeholder = f"\n{START_SILENT_MARKER}\n\n## {release_metadata['version']}\n\n{END_SILENT_MARKER}\n"
#     changelog.write_text(testutil.CHANGELOG_TEMPLATE + placeholder, encoding="utf-8")
#     os.chdir(tmp_path)

#     remove_placeholder_entries("foo/bar", None, changelog, False)

#     new_changelog = changelog.read_text(encoding="utf-8")
#     assert placeholder not in new_changelog
#     assert "hi" in new_changelog


# @pytest.mark.parametrize('release_metadata', [testutil.BASE_RELEASE_METADATA | {"version": "0.0.0", "silent": True}])
# def test_dont_remove_placeholder_entries(tmp_path, release_metadata, draft_release):

#     changelog = tmp_path / "CHANGELOG.md"
#     placeholder = f"\n{START_SILENT_MARKER}\n\n## {release_metadata['version']}\n\n{END_SILENT_MARKER}\n"
#     changelog.write_text(testutil.CHANGELOG_TEMPLATE + placeholder, encoding="utf-8")
#     os.chdir(tmp_path)

#     remove_placeholder_entries("foo/bar", None, changelog, False)

#     new_changelog = changelog.read_text(encoding="utf-8")
#     assert placeholder in new_changelog
#     assert "hi" not in new_changelog
