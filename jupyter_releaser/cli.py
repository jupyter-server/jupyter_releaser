"""CLI for Jupyter Releaser."""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import os
import os.path as osp
import sys
from collections.abc import Callable
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import Any

from jupyter_releaser import changelog, lib, npm, python, util

# Registry for commands that need to use checkout directory
_needs_checkout_dir: set[str] = set()


def use_checkout_dir(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to mark a command as needing the checkout directory"""
    _needs_checkout_dir.add(func.__name__.replace("_", "-").replace("cmd-", ""))
    return func


@dataclass
class OptionDef:
    """Definition of a CLI option."""

    name: str
    envvar: str | None = None
    default: Any = None
    help_text: str = ""
    is_flag: bool = False
    multiple: bool = False


# Define all the common options
VERSION_SPEC_OPTIONS = [
    OptionDef(
        "version-spec",
        envvar="RH_VERSION_SPEC",
        default="",
        help_text="The new version specifier",
    )
]

POST_VERSION_SPEC_OPTIONS = [
    OptionDef(
        "post-version-spec",
        envvar="RH_POST_VERSION_SPEC",
        default="",
        help_text="The post release version (usually dev)",
    ),
    OptionDef(
        "post-version-message",
        envvar="RH_POST_VERSION_MESSAGE",
        default="Bumped version to {post_version}",
        help_text="The post release message",
    ),
]

VERSION_CMD_OPTIONS = [
    OptionDef("version-cmd", envvar="RH_VERSION_COMMAND", help_text="The version command")
]

REPO_OPTIONS = [
    OptionDef("repo", envvar="RH_REPOSITORY", help_text="The git repo"),
]

BRANCH_OPTIONS = [
    OptionDef("ref", envvar="RH_REF", help_text="The source reference"),
    OptionDef("branch", envvar="RH_BRANCH", help_text="The target branch"),
    *REPO_OPTIONS,
]

AUTH_OPTIONS = [
    OptionDef("auth", envvar="GITHUB_ACCESS_TOKEN", help_text="The GitHub auth token"),
]

USERNAME_OPTIONS = [OptionDef("username", envvar="GITHUB_ACTOR", help_text="The git username")]

DIST_DIR_OPTIONS = [
    OptionDef(
        "dist-dir",
        envvar="RH_DIST_DIR",
        default="dist",
        help_text="The folder to use for dist files",
    )
]

PYTHON_PACKAGES_OPTIONS = [
    OptionDef(
        "python-packages",
        envvar="RH_PYTHON_PACKAGES",
        default=["."],
        multiple=True,
        help_text='The list of strings of the form "path_to_package:name_of_package"',
    )
]

CHECK_IMPORTS_OPTIONS = [
    OptionDef(
        "check-imports",
        envvar="RH_CHECK_IMPORTS",
        default=[],
        multiple=True,
        help_text="The Python packages import to check for; default to the Python package name.",
    )
]

DRY_RUN_OPTIONS = [
    OptionDef("dry-run", is_flag=True, envvar="RH_DRY_RUN", help_text="Run as a dry run")
]

GIT_URL_OPTIONS = [OptionDef("git-url", help_text="A custom url for the git repository")]

RELEASE_URL_OPTIONS = [
    OptionDef("release-url", envvar="RH_RELEASE_URL", help_text="A draft GitHub release url")
]

CHANGELOG_PATH_OPTIONS = [
    OptionDef(
        "changelog-path",
        envvar="RH_CHANGELOG",
        default="CHANGELOG.md",
        help_text="The path to changelog file",
    ),
]

SILENT_OPTIONS = [
    OptionDef(
        "silent",
        envvar="RH_SILENT",
        default=False,
        is_flag=True,
        help_text="Set a placeholder in the changelog.",
    )
]

SINCE_OPTIONS = [
    OptionDef(
        "since",
        envvar="RH_SINCE",
        default=None,
        help_text="Use PRs with activity since this date or git reference",
    ),
    OptionDef(
        "since-last-stable",
        is_flag=True,
        envvar="RH_SINCE_LAST_STABLE",
        help_text="Use PRs with activity since the last stable git tag",
    ),
]

CHANGELOG_OPTIONS = (
    BRANCH_OPTIONS
    + AUTH_OPTIONS
    + CHANGELOG_PATH_OPTIONS
    + SINCE_OPTIONS
    + [
        OptionDef(
            "resolve-backports",
            envvar="RH_RESOLVE_BACKPORTS",
            default=True,
            help_text="Resolve backport PRs to their originals",
        ),
    ]
)

NPM_INSTALL_OPTIONS = [
    OptionDef(
        "npm-install-options",
        envvar="RH_NPM_INSTALL_OPTIONS",
        default="",
        help_text="Options to pass when calling npm install",
    )
]

PYDIST_CHECK_OPTIONS = [
    OptionDef(
        "pydist-check-cmd",
        envvar="RH_PYDIST_CHECK_CMD",
        default="pipx run twine check --strict {dist_file}",
        help_text="The command to use to check a python distribution file",
    ),
    OptionDef(
        "pydist-extra-check-cmds",
        envvar="RH_EXTRA_PYDIST_CHECK_CMDS",
        default=[
            "pipx run 'validate-pyproject[all]' pyproject.toml",
            "pipx run check-wheel-contents --config pyproject.toml {dist_dir}",
        ],
        multiple=True,
        help_text="Extra checks to run against the pydist file",
    ),
    OptionDef(
        "pydist-resource-paths",
        envvar="RH_PYDIST_RESOURCE_PATHS",
        default=[],
        multiple=True,
        help_text="Resource paths that should be available when installed",
    ),
]

TAG_FORMAT_OPTIONS = [
    OptionDef(
        "tag-format",
        envvar="RH_TAG_FORMAT",
        default="v{version}",
        help_text="The format to use for the release tag",
    )
]

# Command-specific options (extracted to avoid duplication)
RELEASE_MESSAGE_OPTIONS = [
    OptionDef(
        "release-message",
        envvar="RH_RELEASE_MESSAGE",
        default="Publish {version}",
        help_text="The message to use for the release commit",
    ),
]

TAG_MESSAGE_OPTIONS = [
    OptionDef(
        "tag-message",
        envvar="RH_TAG_MESSAGE",
        default="Release {tag_name}",
        help_text="The message to use for the release tag",
    ),
]

NO_GIT_TAG_WORKSPACE_OPTIONS = [
    OptionDef(
        "no-git-tag-workspace",
        is_flag=True,
        help_text="Whether to skip tagging npm workspace packages",
    ),
]

NPM_TOKEN_OPTIONS = [
    OptionDef(
        "npm-token",
        envvar="NPM_TOKEN",
        help_text="A token for the npm release",
    ),
]

NPM_CMD_OPTIONS = [
    OptionDef(
        "npm-cmd",
        envvar="RH_NPM_COMMAND",
        default="npm publish",
        help_text="The command to run for npm release",
    ),
]

TWINE_CMD_OPTIONS = [
    OptionDef(
        "twine-cmd",
        envvar="TWINE_COMMAND",
        default="pipx run twine upload",
        help_text="The twine to run for Python release",
    ),
]

NPM_REGISTRY_OPTIONS = [
    OptionDef(
        "npm-registry",
        envvar="NPM_REGISTRY",
        default="https://registry.npmjs.org/",
        help_text="The npm registry to target for publishing",
    ),
]

TWINE_REPOSITORY_URL_OPTIONS = [
    OptionDef(
        "twine-repository-url",
        envvar="TWINE_REPOSITORY_URL",
        default="https://upload.pypi.org/legacy/",
        help_text="The pypi registry to target for publishing",
    ),
]

NPM_TAG_OPTIONS = [
    OptionDef(
        "npm-tag",
        envvar="NPM_TAG",
        default="",
        help_text="The npm tag. It defaults to 'next' if it is a prerelease otherwise to 'latest'.",
    ),
]

EXPECTED_SHA_OPTIONS = [
    OptionDef(
        "expected-sha",
        envvar="RH_EXPECTED_SHA",
        help_text="The expected sha of the branch HEAD",
    ),
]

# Combined publish options for convenience
PUBLISH_OPTIONS = (
    NPM_TOKEN_OPTIONS
    + NPM_CMD_OPTIONS
    + TWINE_CMD_OPTIONS
    + NPM_REGISTRY_OPTIONS
    + TWINE_REPOSITORY_URL_OPTIONS
    + NPM_TAG_OPTIONS
)

# Combined tag release options
TAG_RELEASE_OPTIONS = RELEASE_MESSAGE_OPTIONS + TAG_MESSAGE_OPTIONS + NO_GIT_TAG_WORKSPACE_OPTIONS


def _convert_to_bool(value: str) -> bool:
    """Convert a string value to boolean, matching Click's behavior.

    Click accepts: true, 1, yes, on, t, y (case-insensitive) as truthy values.
    """
    return value.lower() in ("true", "1", "yes", "on", "t", "y")


def add_option_to_parser(parser: argparse.ArgumentParser, opt: OptionDef) -> None:
    """Add an option definition to an argparse parser."""
    arg_name = f"--{opt.name}"
    kwargs: dict[str, Any] = {}

    if opt.help_text:
        kwargs["help"] = opt.help_text

    if opt.is_flag:
        kwargs["action"] = "store_true"
        kwargs["default"] = False
    elif opt.multiple:
        kwargs["action"] = "append"
        kwargs["default"] = None  # We'll handle defaults later
    else:
        kwargs["default"] = None  # We'll handle defaults later

    parser.add_argument(arg_name, **kwargs)


def add_options_to_parser(parser: argparse.ArgumentParser, options: list[OptionDef]) -> None:
    """Add multiple option definitions to a parser."""
    for opt in options:
        add_option_to_parser(parser, opt)


def get_option_value(
    args: argparse.Namespace,
    opt: OptionDef,
    config_options: dict[str, Any],
) -> Any:
    """Get the value for an option considering CLI, env vars, config, and defaults.

    Priority order (highest to lowest):
    1. Environment variables
    2. CLI arguments
    3. Config file options
    4. Default values
    """
    name = opt.name.replace("-", "_")
    cli_value = getattr(args, name, None)

    # Check environment variable first (highest priority)
    if opt.envvar and os.environ.get(opt.envvar):
        env_value = os.environ[opt.envvar]
        display_value = "***" if "token" in name.lower() else env_value
        util.log(f"Using env value for {name}: '{display_value}'")
        # Convert string env values to boolean for flag/boolean options
        if opt.is_flag or isinstance(opt.default, bool):
            return _convert_to_bool(env_value)
        if opt.multiple:
            return [env_value]  # Environment variable is a single value for multiple
        return env_value

    # Check CLI value
    if cli_value is not None:
        display_value = "***" if "token" in name.lower() else cli_value
        util.log(f"Using cli arg for {name}: '{display_value}'")
        # Convert string CLI values to boolean for non-flag boolean options
        # (flags are already handled by argparse's store_true action)
        if not opt.is_flag and isinstance(opt.default, bool) and isinstance(cli_value, str):
            return _convert_to_bool(cli_value)
        return cli_value

    # Check config options
    config_name = opt.name.replace("_", "-")
    config_name_underscore = opt.name.replace("-", "_")
    if config_name in config_options or config_name_underscore in config_options:
        val = config_options.get(config_name, config_options.get(config_name_underscore))
        display_value = "***" if "token" in name.lower() else val
        util.log(f"Adding option override for --{opt.name}: '{display_value}'")
        # Convert string config values to boolean for flag/boolean options
        if (opt.is_flag or isinstance(opt.default, bool)) and isinstance(val, str):
            return _convert_to_bool(val)
        return val

    # Use default
    util.log(f"Using default value for {name}: '{opt.default}'")
    return opt.default


def collect_all_options() -> dict[str, OptionDef]:
    """Collect all option definitions into a dict keyed by name.

    Used by list-envvars command to show all available environment variables.
    """
    all_opts: dict[str, OptionDef] = {}

    # All option lists (base + command-specific)
    option_lists = [
        VERSION_SPEC_OPTIONS,
        POST_VERSION_SPEC_OPTIONS,
        VERSION_CMD_OPTIONS,
        REPO_OPTIONS,
        BRANCH_OPTIONS,
        AUTH_OPTIONS,
        USERNAME_OPTIONS,
        DIST_DIR_OPTIONS,
        PYTHON_PACKAGES_OPTIONS,
        CHECK_IMPORTS_OPTIONS,
        DRY_RUN_OPTIONS,
        GIT_URL_OPTIONS,
        RELEASE_URL_OPTIONS,
        CHANGELOG_PATH_OPTIONS,
        SILENT_OPTIONS,
        SINCE_OPTIONS,
        CHANGELOG_OPTIONS,
        NPM_INSTALL_OPTIONS,
        PYDIST_CHECK_OPTIONS,
        TAG_FORMAT_OPTIONS,
        # Command-specific options
        RELEASE_MESSAGE_OPTIONS,
        TAG_MESSAGE_OPTIONS,
        NO_GIT_TAG_WORKSPACE_OPTIONS,
        NPM_TOKEN_OPTIONS,
        NPM_CMD_OPTIONS,
        TWINE_CMD_OPTIONS,
        NPM_REGISTRY_OPTIONS,
        TWINE_REPOSITORY_URL_OPTIONS,
        NPM_TAG_OPTIONS,
        EXPECTED_SHA_OPTIONS,
    ]

    for opts in option_lists:
        for opt in opts:
            all_opts[opt.name] = opt

    return all_opts


# Command implementations


def cmd_list_envvars(args: argparse.Namespace) -> None:  # noqa: ARG001
    """List the environment variables."""
    all_opts = collect_all_options()
    envvars: dict[str, str] = {}
    for name, opt in all_opts.items():
        if opt.envvar:
            envvars[name] = opt.envvar

    for key in sorted(envvars):
        util.log(f"{key}: {envvars[key]}")


def cmd_prep_git(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Prep git and env variables and bump version"""
    opts = BRANCH_OPTIONS + AUTH_OPTIONS + USERNAME_OPTIONS + GIT_URL_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.prep_git(
        values["ref"],
        values["branch"],
        values["repo"],
        values["auth"],
        values["username"],
        values["git_url"],
    )


@use_checkout_dir
def cmd_bump_version(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Prep git and env variables and bump version"""
    opts = (
        VERSION_SPEC_OPTIONS
        + VERSION_CMD_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + PYTHON_PACKAGES_OPTIONS
        + TAG_FORMAT_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    prev_dir = os.getcwd()
    python_packages = values["python_packages"] or ["."]
    for package in python_packages:
        package_path, package_name = (
            package.split(":", maxsplit=1) if ":" in package else [package, None]
        )
        os.chdir(package_path)
        lib.bump_version(
            values["version_spec"],
            values["version_cmd"],
            values["changelog_path"],
            values["tag_format"],
            package_name=package_name if len(python_packages) > 1 else None,
        )
        os.chdir(prev_dir)


@use_checkout_dir
def cmd_extract_changelog(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Extract the changelog entry."""
    opts = (
        DRY_RUN_OPTIONS
        + AUTH_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + RELEASE_URL_OPTIONS
        + SILENT_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.extract_changelog(
        values["dry_run"],
        values["auth"],
        values["changelog_path"],
        values["release_url"],
        values["silent"],
    )


@use_checkout_dir
def cmd_build_changelog(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Build changelog entry"""
    opts = CHANGELOG_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    changelog.build_entry(
        values["ref"],
        values["branch"],
        values["repo"],
        values["auth"],
        values["changelog_path"],
        values["since"],
        values["since_last_stable"],
        values["resolve_backports"],
    )


@use_checkout_dir
def cmd_draft_changelog(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Create a changelog entry PR"""
    opts = (
        VERSION_SPEC_OPTIONS
        + BRANCH_OPTIONS
        + SINCE_OPTIONS
        + AUTH_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + DRY_RUN_OPTIONS
        + POST_VERSION_SPEC_OPTIONS
        + SILENT_OPTIONS
        + TAG_FORMAT_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.draft_changelog(
        values["version_spec"],
        values["ref"],
        values["branch"],
        values["repo"],
        values["since"],
        values["since_last_stable"],
        values["auth"],
        values["changelog_path"],
        values["dry_run"],
        values["post_version_spec"],
        values["post_version_message"],
        values["silent"],
        values["tag_format"],
    )


@use_checkout_dir
def cmd_build_python(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Build Python dist files"""
    opts = DIST_DIR_OPTIONS + PYTHON_PACKAGES_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    prev_dir = os.getcwd()
    clean = True
    python_packages = values["python_packages"] or ["."]
    for python_package in [p.split(":")[0] for p in python_packages]:
        os.chdir(python_package)
        if not util.PYPROJECT.exists() and not util.SETUP_PY.exists():
            util.log(
                f"Skipping build-python in {python_package} since there are no python package files"
            )
        else:
            python.build_dist(
                Path(os.path.relpath(".", python_package)) / values["dist_dir"], clean=clean
            )
            clean = False
        os.chdir(prev_dir)


@use_checkout_dir
def cmd_check_python(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Check Python dist files"""
    opts = DIST_DIR_OPTIONS + CHECK_IMPORTS_OPTIONS + PYDIST_CHECK_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    dist_dir = values["dist_dir"]
    for dist_file in glob(f"{dist_dir}/*"):
        if Path(dist_file).suffix not in [".gz", ".whl"]:
            util.log(f"Skipping non-python dist file {dist_file}")
            continue

        python.check_dist(
            dist_file,
            python_imports=values["check_imports"] or [],
            check_cmd=values["pydist_check_cmd"],
            extra_check_cmds=values["pydist_extra_check_cmds"] or [],
            resource_paths=values["pydist_resource_paths"] or [],
        )


@use_checkout_dir
def cmd_build_npm(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Build npm package"""
    opts = DIST_DIR_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    # Handle the positional argument
    package = getattr(args, "package", None) or "."

    if not osp.exists("./package.json"):
        util.log("Skipping build-npm since there is no package.json file")
        return
    npm.build_dist(package, values["dist_dir"])


@use_checkout_dir
def cmd_check_npm(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Check npm package"""
    opts = DIST_DIR_OPTIONS + NPM_INSTALL_OPTIONS + REPO_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    if not osp.exists("./package.json"):
        util.log("Skipping check-npm since there is no package.json file")
        return
    npm.check_dist(values["dist_dir"], values["npm_install_options"], values["repo"])


@use_checkout_dir
def cmd_tag_release(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Create release commit and tag."""
    opts = DIST_DIR_OPTIONS + TAG_FORMAT_OPTIONS + TAG_RELEASE_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.tag_release(
        values["dist_dir"],
        values["release_message"],
        values["tag_format"],
        values["tag_message"],
        values["no_git_tag_workspace"],
    )


@use_checkout_dir
def cmd_populate_release(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Populate a release."""
    opts = (
        BRANCH_OPTIONS
        + VERSION_CMD_OPTIONS
        + AUTH_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + DIST_DIR_OPTIONS
        + DRY_RUN_OPTIONS
        + RELEASE_URL_OPTIONS
        + POST_VERSION_SPEC_OPTIONS
        + SILENT_OPTIONS
        + TAG_FORMAT_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    # Handle assets positional argument
    assets = getattr(args, "assets", None) or []

    lib.populate_release(
        values["ref"],
        values["branch"],
        values["repo"],
        values["version_cmd"],
        values["auth"],
        values["changelog_path"],
        values["dist_dir"],
        values["dry_run"],
        values["release_url"],
        values["post_version_spec"],
        values["post_version_message"],
        assets,
        values["tag_format"],
        values["silent"],
    )


@use_checkout_dir
def cmd_delete_release(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Delete a draft GitHub release by url to the release page"""
    opts = AUTH_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.delete_release(values["auth"], values["release_url"], values["dry_run"])


def cmd_extract_release(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Download and verify assets from a draft GitHub release"""
    opts = AUTH_OPTIONS + DIST_DIR_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.extract_release(
        values["auth"],
        values["dist_dir"],
        values["dry_run"],
        values["release_url"],
    )


@use_checkout_dir
def cmd_publish_assets(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Publish release asset(s)."""
    opts = (
        AUTH_OPTIONS
        + DIST_DIR_OPTIONS
        + PUBLISH_OPTIONS
        + DRY_RUN_OPTIONS
        + PYTHON_PACKAGES_OPTIONS
        + RELEASE_URL_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }

    python_packages = values["python_packages"] or ["."]
    for python_package in python_packages:
        lib.publish_assets(
            values["auth"],
            values["dist_dir"],
            values["npm_token"],
            values["npm_cmd"],
            values["twine_cmd"],
            values["npm_registry"],
            values["twine_repository_url"],
            values["npm_tag"],
            values["dry_run"],
            values["release_url"],
            python_package,
        )


@use_checkout_dir
def cmd_publish_release(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Publish GitHub release"""
    opts = AUTH_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS + SILENT_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.publish_release(values["auth"], values["dry_run"], values["release_url"], values["silent"])


@use_checkout_dir
def cmd_ensure_sha(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Ensure that a sha has not changed."""
    opts = BRANCH_OPTIONS + DRY_RUN_OPTIONS + EXPECTED_SHA_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    util.ensure_sha(values["dry_run"], values["expected_sha"], values["branch"])


@use_checkout_dir
def cmd_forwardport_changelog(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Forwardport Changelog Entries to the Default Branch"""
    opts = (
        AUTH_OPTIONS
        + BRANCH_OPTIONS
        + USERNAME_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + DRY_RUN_OPTIONS
        + RELEASE_URL_OPTIONS
    )
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.forwardport_changelog(
        values["auth"],
        values["ref"],
        values["branch"],
        values["repo"],
        values["username"],
        values["changelog_path"],
        values["dry_run"],
        values["release_url"],
    )


@use_checkout_dir
def cmd_publish_changelog(args: argparse.Namespace, config_options: dict[str, Any]) -> None:
    """Remove changelog placeholder entries."""
    opts = AUTH_OPTIONS + BRANCH_OPTIONS + CHANGELOG_PATH_OPTIONS + DRY_RUN_OPTIONS
    values = {
        opt.name.replace("-", "_"): get_option_value(args, opt, config_options) for opt in opts
    }
    lib.publish_changelog(
        values["branch"],
        values["repo"],
        values["auth"],
        values["changelog_path"],
        values["dry_run"],
    )


# Command registry - maps command names to their handlers and options
COMMANDS: dict[str, dict[str, Any]] = {
    "list-envvars": {
        "func": cmd_list_envvars,
        "help": "List the environment variables",
        "options": [],
        "simple": True,  # Does not need config processing
    },
    "prep-git": {
        "func": cmd_prep_git,
        "help": "Prep git and env variables and bump version",
        "options": BRANCH_OPTIONS + AUTH_OPTIONS + USERNAME_OPTIONS + GIT_URL_OPTIONS,
    },
    "bump-version": {
        "func": cmd_bump_version,
        "help": "Prep git and env variables and bump version",
        "options": VERSION_SPEC_OPTIONS
        + VERSION_CMD_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + PYTHON_PACKAGES_OPTIONS
        + TAG_FORMAT_OPTIONS,
    },
    "extract-changelog": {
        "func": cmd_extract_changelog,
        "help": "Extract the changelog entry",
        "options": DRY_RUN_OPTIONS
        + AUTH_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + RELEASE_URL_OPTIONS
        + SILENT_OPTIONS,
    },
    "build-changelog": {
        "func": cmd_build_changelog,
        "help": "Build changelog entry",
        "options": CHANGELOG_OPTIONS,
    },
    "draft-changelog": {
        "func": cmd_draft_changelog,
        "help": "Create a changelog entry PR",
        "options": (
            VERSION_SPEC_OPTIONS
            + BRANCH_OPTIONS
            + SINCE_OPTIONS
            + AUTH_OPTIONS
            + CHANGELOG_PATH_OPTIONS
            + DRY_RUN_OPTIONS
            + POST_VERSION_SPEC_OPTIONS
            + SILENT_OPTIONS
            + TAG_FORMAT_OPTIONS
        ),
    },
    "build-python": {
        "func": cmd_build_python,
        "help": "Build Python dist files",
        "options": DIST_DIR_OPTIONS + PYTHON_PACKAGES_OPTIONS,
    },
    "check-python": {
        "func": cmd_check_python,
        "help": "Check Python dist files",
        "options": DIST_DIR_OPTIONS + CHECK_IMPORTS_OPTIONS + PYDIST_CHECK_OPTIONS,
    },
    "build-npm": {
        "func": cmd_build_npm,
        "help": "Build npm package",
        "options": DIST_DIR_OPTIONS,
        "positional_args": [("package", {"nargs": "?", "default": "."})],
    },
    "check-npm": {
        "func": cmd_check_npm,
        "help": "Check npm package",
        "options": DIST_DIR_OPTIONS + NPM_INSTALL_OPTIONS + REPO_OPTIONS,
    },
    "tag-release": {
        "func": cmd_tag_release,
        "help": "Create release commit and tag",
        "options": DIST_DIR_OPTIONS + TAG_FORMAT_OPTIONS + TAG_RELEASE_OPTIONS,
    },
    "populate-release": {
        "func": cmd_populate_release,
        "help": "Populate a release",
        "options": (
            BRANCH_OPTIONS
            + VERSION_CMD_OPTIONS
            + AUTH_OPTIONS
            + CHANGELOG_PATH_OPTIONS
            + DIST_DIR_OPTIONS
            + DRY_RUN_OPTIONS
            + RELEASE_URL_OPTIONS
            + POST_VERSION_SPEC_OPTIONS
            + SILENT_OPTIONS
            + TAG_FORMAT_OPTIONS
        ),
        "positional_args": [("assets", {"nargs": "*"})],
    },
    "delete-release": {
        "func": cmd_delete_release,
        "help": "Delete a draft GitHub release by url to the release page",
        "options": AUTH_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS,
    },
    "extract-release": {
        "func": cmd_extract_release,
        "help": "Download and verify assets from a draft GitHub release",
        "options": AUTH_OPTIONS + DIST_DIR_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS,
    },
    "publish-assets": {
        "func": cmd_publish_assets,
        "help": "Publish release asset(s)",
        "options": (
            AUTH_OPTIONS
            + DIST_DIR_OPTIONS
            + PUBLISH_OPTIONS
            + DRY_RUN_OPTIONS
            + PYTHON_PACKAGES_OPTIONS
            + RELEASE_URL_OPTIONS
        ),
    },
    "publish-release": {
        "func": cmd_publish_release,
        "help": "Publish GitHub release",
        "options": AUTH_OPTIONS + DRY_RUN_OPTIONS + RELEASE_URL_OPTIONS + SILENT_OPTIONS,
    },
    "ensure-sha": {
        "func": cmd_ensure_sha,
        "help": "Ensure that a sha has not changed",
        "options": BRANCH_OPTIONS + DRY_RUN_OPTIONS + EXPECTED_SHA_OPTIONS,
    },
    "forwardport-changelog": {
        "func": cmd_forwardport_changelog,
        "help": "Forwardport Changelog Entries to the Default Branch",
        "options": AUTH_OPTIONS
        + BRANCH_OPTIONS
        + USERNAME_OPTIONS
        + CHANGELOG_PATH_OPTIONS
        + DRY_RUN_OPTIONS
        + RELEASE_URL_OPTIONS,
    },
    "publish-changelog": {
        "func": cmd_publish_changelog,
        "help": "Remove changelog placeholder entries",
        "options": AUTH_OPTIONS + BRANCH_OPTIONS + CHANGELOG_PATH_OPTIONS + DRY_RUN_OPTIONS,
    },
}


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands"""
    parser = argparse.ArgumentParser(
        prog="jupyter-releaser",
        description="Jupyter Releaser scripts",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force a command to run even when skipped by config",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    for cmd_name, cmd_info in COMMANDS.items():
        subparser = subparsers.add_parser(cmd_name, help=cmd_info["help"])
        add_options_to_parser(subparser, cmd_info["options"])

        # Add positional arguments if any
        for pos_arg in cmd_info.get("positional_args", []):
            arg_name, arg_kwargs = pos_arg
            subparser.add_argument(arg_name, **arg_kwargs)

    return parser


def run_command(args: argparse.Namespace) -> int:
    """Run the specified command with proper handling"""
    cmd_name = args.command

    if cmd_name is None:
        # No command provided, show help
        create_parser().print_help()
        return 0

    if cmd_name not in COMMANDS:
        util.log(f"Unknown command: {cmd_name}")
        return 1

    cmd_info = COMMANDS[cmd_name]

    # Handle simple commands that don't need config processing
    if cmd_info.get("simple"):
        cmd_info["func"](args)
        return 0

    orig_dir = os.getcwd()

    try:
        # Check if we need to be in checkout directory
        if cmd_name in _needs_checkout_dir:
            if not osp.exists(util.CHECKOUT_NAME):
                msg = "Please run prep-git first"
                raise ValueError(msg)
            os.chdir(util.CHECKOUT_NAME)

        # Read in the config
        config = util.read_config()
        hooks = config.get("hooks", {})
        config_options = config.get("options", {})
        skip = config.get("skip", [])

        if args.force:
            skip = []

        skip += os.environ.get("RH_STEPS_TO_SKIP", "").split(",")

        # Print a separation header
        util.log(f'\n\n{"-" * 50}')
        util.log(f"\n\n{cmd_name}\n\n")
        util.log(f'\n\n{"-" * 50}')

        if cmd_name in skip or cmd_name.replace("-", "_") in skip:
            util.log("*** Skipping based on skip config")
            util.log(f'{"-" * 50}\n\n')
            return 0

        util.log(f'{"~" * 50}\n\n')

        # Handle before hooks
        before = f"before-{cmd_name}"
        if before in hooks:
            before_hooks = hooks[before]
            if isinstance(before_hooks, str):
                before_hooks = [before_hooks]
            if before_hooks:
                util.log(f"\nRunning hooks for {before}")
            for hook in before_hooks:
                util.run(hook)

        # Run the actual command
        cmd_info["func"](args, config_options)

        # Handle after hooks
        # Re-read config if we just did a git checkout
        if cmd_name in ["prep-git", "extract-release"]:
            os.chdir(util.CHECKOUT_NAME)
            config = util.read_config()
            hooks = config.get("hooks", {})

        after = f"after-{cmd_name}"
        if after in hooks:
            after_hooks = hooks[after]
            if isinstance(after_hooks, str):
                after_hooks = [after_hooks]
            if after_hooks:
                util.log(f"\nRunning hooks for {after}")
            for hook in after_hooks:
                util.run(hook)

        return 0

    finally:
        os.chdir(orig_dir)


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    return run_command(parsed_args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
