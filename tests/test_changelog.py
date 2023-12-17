# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import subprocess

import pytest
from ghapi.core import GhApi

from jupyter_releaser.changelog import (
    END_MARKER,
    END_SILENT_MARKER,
    START_MARKER,
    START_SILENT_MARKER,
    remove_placeholder_entries,
    update_changelog,
)
from jupyter_releaser.util import release_for_url
from tests import util as testutil


@pytest.fixture()
def module_template():
    return testutil.PY_MODULE_TEMPLATE


@pytest.fixture()
def mock_py_package(tmp_path, module_template):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(testutil.pyproject_template(), encoding="utf-8")

    foopy = tmp_path / "foo.py"
    foopy.write_text(module_template, encoding="utf-8")


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


def test_update_changelog_with_old_silent_entry(tmp_path, mock_py_package):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")
    os.chdir(tmp_path)

    # Update changelog for current version
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY, True)
    # Bump version
    subprocess.check_call(["pipx", "run", "hatch", "version", "patch"], cwd=tmp_path)  # noqa: S603, S607
    # Update changelog for the new version
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY)

    new_changelog = changelog.read_text(encoding="utf-8")

    assert f"{START_SILENT_MARKER}\n\n## 0.0.1\n\n{END_SILENT_MARKER}" in new_changelog
    assert (
        f"{START_MARKER}\n\n{START_SILENT_MARKER}\n\n## 0.0.1\n\n{END_SILENT_MARKER}\n\n{END_MARKER}"
        not in new_changelog
    )


@pytest.mark.parametrize("module_template", ['__version__ = "0.0.3"\n'])
def test_silence_existing_changelog_entry(tmp_path, mock_py_package):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(testutil.CHANGELOG_TEMPLATE, encoding="utf-8")
    os.chdir(tmp_path)
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY)

    new_changelog = changelog.read_text(encoding="utf-8")
    assert f"{START_MARKER}\n{testutil.CHANGELOG_ENTRY}\n{END_MARKER}" in new_changelog

    # Should silent the current entry
    update_changelog(str(changelog), testutil.CHANGELOG_ENTRY, True)

    new_changelog = changelog.read_text(encoding="utf-8")
    assert (
        f"{START_MARKER}\n\n{START_SILENT_MARKER}\n\n## 0.0.3\n\n{END_SILENT_MARKER}\n\n{END_MARKER}"
        in new_changelog
    )
    assert f"{START_MARKER}\n{testutil.CHANGELOG_ENTRY}\n{END_MARKER}" not in new_changelog


@pytest.mark.parametrize(
    "release_metadata",
    [
        dict(
            [(k, v) for k, v in testutil.BASE_RELEASE_METADATA.items() if k != "version"]
            + [("version", "0.0.0")]
        )
    ],
)
def test_remove_placeholder_entries(tmp_path, release_metadata, draft_release):
    # Create changelog with silent placeholder
    changelog = tmp_path / "CHANGELOG.md"
    placeholder = (
        f"\n{START_SILENT_MARKER}\n\n## {release_metadata['version']}\n\n{END_SILENT_MARKER}\n"
    )
    changelog.write_text(testutil.CHANGELOG_TEMPLATE + placeholder, encoding="utf-8")
    os.chdir(tmp_path)

    # Publish the release (as it is a draft from `draft_release`)
    gh = GhApi(owner="foo", repo="bar")
    release = release_for_url(gh, draft_release)
    published_changelog = "Published body"
    gh.repos.update_release(
        release["id"],
        release["tag_name"],
        release["target_commitish"],
        release["name"],
        published_changelog,
        False,
        release["prerelease"],
    )

    remove_placeholder_entries("foo/bar", None, changelog, False)

    new_changelog = changelog.read_text(encoding="utf-8")
    assert placeholder not in new_changelog
    assert published_changelog in new_changelog


@pytest.mark.parametrize(
    "release_metadata",
    [
        dict(
            [
                (k, v)
                for k, v in testutil.BASE_RELEASE_METADATA.items()
                if k not in ("version", "silent")
            ]
            + [("version", "0.0.0"), ("silent", True)]
        )
    ],
)
def test_dont_remove_placeholder_entries(tmp_path, release_metadata, draft_release):
    changelog = tmp_path / "CHANGELOG.md"
    placeholder = (
        f"\n{START_SILENT_MARKER}\n\n## {release_metadata['version']}\n\n{END_SILENT_MARKER}\n"
    )
    changelog.write_text(testutil.CHANGELOG_TEMPLATE + placeholder, encoding="utf-8")
    os.chdir(tmp_path)

    # Release is not published, so this is a no-op
    remove_placeholder_entries("foo/bar", None, changelog, False)

    new_changelog = changelog.read_text(encoding="utf-8")
    assert placeholder in new_changelog
    assert "hi" not in new_changelog
