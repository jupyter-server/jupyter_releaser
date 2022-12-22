# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import os.path as osp
import typing as t
from glob import glob
from pathlib import Path

import click

from jupyter_releaser import changelog, lib, npm, python, util


class ReleaseHelperGroup(click.Group):
    """Click group tailored to jupyter-releaser"""

    _needs_checkout_dir: t.Dict[str, bool] = {}

    def invoke(self, ctx):
        """Handle jupyter-releaser config while invoking a command"""
        # Get the command name and make sure it is valid
        cmd_name = ctx.protected_args[0]
        if cmd_name not in self.commands:
            super().invoke(ctx)

        if cmd_name == "list-envvars":
            envvars: t.Dict[str, str] = {}
            for cmd_name in self.commands:
                for param in self.commands[cmd_name].params:
                    if isinstance(param, click.Option):
                        if param.envvar:
                            envvars[str(param.name)] = str(param.envvar)

            for key in sorted(envvars):
                util.log(f"{key.replace('_', '-')}: {envvars[key]}")

            return

        orig_dir = os.getcwd()

        if cmd_name.replace("-", "_") in self._needs_checkout_dir:
            if not osp.exists(util.CHECKOUT_NAME):
                raise ValueError("Please run prep-git first")
            os.chdir(util.CHECKOUT_NAME)

        # Read in the config
        config = util.read_config()
        hooks = config.get("hooks", {})
        options = config.get("options", {})
        skip = config.get("skip", [])

        if "--force" in ctx.args:
            skip = []
            ctx.args.remove("--force")

        skip += os.environ.get("RH_STEPS_TO_SKIP", "").split(",")

        # Print a separation header
        util.log(f'\n\n{"-" * 50}')
        util.log(f"\n\n{cmd_name}\n\n")
        util.log(f'\n\n{"-" * 50}')

        if cmd_name in skip or cmd_name.replace("-", "_") in skip:
            util.log("*** Skipping based on skip config")
            util.log(f'{"-" * 50}\n\n')
            return

        # Handle all of the parameters
        for param in self.commands[cmd_name].get_params(ctx):
            name = param.name
            assert name is not None

            # Defer to env var overrides
            if param.envvar and os.environ.get(str(param.envvar)):
                value = os.environ[str(param.envvar)]
                if "token" in name.lower():
                    value = "***"
                util.log(f"Using env value for {name}: '{value}'")
                continue

            # Handle cli and options overrides.
            if name in options or name.replace("_", "-") in options:
                arg = f"--{name.replace('_', '-')}"
                # Defer to cli overrides
                if arg not in ctx.args:
                    val = options.get(name, options.get(name.replace("_", "-")))
                    if "token" in arg.lower():
                        val = "***"
                    util.log(f"Adding option override for {arg}: '{val}")
                    if isinstance(val, list):
                        for v in val:
                            ctx.args.append(arg)
                            ctx.args.append(v)
                    else:
                        ctx.args.append(arg)
                        ctx.args.append(val)
                    continue
                else:
                    val = ctx.args[ctx.args.index(arg) + 1]
                    if "token" in name.lower():
                        val = "***"
                    util.log(f"Using cli arg for {name}: '{val}'")
                    continue

            util.log(f"Using default value for {name}: '{param.default}'")

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
        super().invoke(ctx)

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

        os.chdir(orig_dir)

    def list_commands(self, ctx):
        """List commands in insertion order"""
        return self.commands.keys()


@click.group(cls=ReleaseHelperGroup)
@click.option("--force", default=False, help="Force a command to run even when skipped by config")
def main(force):
    """Jupyter Releaser scripts"""
    pass


# Extracted common options
version_spec_options = [
    click.option(
        "--version-spec",
        envvar="RH_VERSION_SPEC",
        default="",
        help="The new version specifier",
    )
]


post_version_spec_options = [
    click.option(
        "--post-version-spec",
        envvar="RH_POST_VERSION_SPEC",
        default="",
        help="The post release version (usually dev)",
    ),
    click.option(
        "--post-version-message",
        default="Bumped version to {post_version}",
        envvar="RH_POST_VERSION_MESSAGE",
        help="The post release message",
    ),
]

version_cmd_options = [
    click.option("--version-cmd", envvar="RH_VERSION_COMMAND", help="The version command")
]


branch_options = [
    click.option("--ref", envvar="RH_REF", help="The source reference"),
    click.option("--branch", envvar="RH_BRANCH", help="The target branch"),
    click.option("--repo", envvar="RH_REPOSITORY", help="The git repo"),
]

auth_options = [
    click.option("--auth", envvar="GITHUB_ACCESS_TOKEN", help="The GitHub auth token"),
]

username_options = [click.option("--username", envvar="GITHUB_ACTOR", help="The git username")]

dist_dir_options = [
    click.option(
        "--dist-dir",
        envvar="RH_DIST_DIR",
        default="dist",
        help="The folder to use for dist files",
    )
]

python_packages_options = [
    click.option(
        "--python-packages",
        envvar="RH_PYTHON_PACKAGES",
        default=["."],
        multiple=True,
        help='The list of strings of the form "path_to_package:name_of_package"',
    )
]

check_imports_options = [
    click.option(
        "--check-imports",
        envvar="RH_CHECK_IMPORTS",
        default=[],
        multiple=True,
        help="The Python packages import to check for; default to the Python package name.",
    )
]

dry_run_options = [
    click.option("--dry-run", is_flag=True, envvar="RH_DRY_RUN", help="Run as a dry run")
]


git_url_options = [click.option("--git-url", help="A custom url for the git repository")]


release_url_options = [
    click.option("--release-url", envvar="RH_RELEASE_URL", help="A draft GitHub release url")
]


changelog_path_options = [
    click.option(
        "--changelog-path",
        envvar="RH_CHANGELOG",
        default="CHANGELOG.md",
        help="The path to changelog file",
    ),
]

since_options = [
    click.option(
        "--since",
        envvar="RH_SINCE",
        default=None,
        help="Use PRs with activity since this date or git reference",
    ),
    click.option(
        "--since-last-stable",
        is_flag=True,
        envvar="RH_SINCE_LAST_STABLE",
        help="Use PRs with activity since the last stable git tag",
    ),
]

changelog_options = (
    branch_options
    + auth_options
    + changelog_path_options
    + since_options
    + [
        click.option(
            "--resolve-backports",
            envvar="RH_RESOLVE_BACKPORTS",
            default=True,
            help="Resolve backport PRs to their originals",
        ),
    ]
)

npm_install_options = [
    click.option(
        "--npm-install-options",
        envvar="RH_NPM_INSTALL_OPTIONS",
        default="",
        help="Options to pass when calling npm install",
    )
]

pydist_check_options = [
    click.option(
        "--pydist-check-cmd",
        envvar="RH_PYDIST_CHECK_CMD",
        default="pipx run twine check --strict {dist_file}",
        help="The command to use to check a python distribution file",
    ),
    click.option(
        "--pydist-extra-check-cmds",
        envvar="RH_EXTRA_PYDIST_CHECK_CMDS",
        default=[
            "pipx run 'validate-pyproject[all]' pyproject.toml",
            "pipx run check-wheel-contents --ignore W002 {dist_dir}",
        ],
        multiple=True,
        help="Extra checks to run against the pydist file",
    ),
    click.option(
        "--pydist-resource-paths",
        envvar="RH_PYDIST_RESOURCE_PATHS",
        multiple=True,
        help="Resource paths that should be available when installed",
    ),
]


def add_options(options):
    """Add extracted common options to a click command"""
    # https://stackoverflow.com/a/40195800
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def use_checkout_dir():
    """Use the checkout dir created by prep-git"""

    def inner(func):
        ReleaseHelperGroup._needs_checkout_dir[func.__name__] = True
        return func

    return inner


@main.command()
def list_envvars():
    """List the environment variables"""
    # This is implemented in ReleaseHelperGroup.invoke
    pass


@main.command()
@add_options(branch_options)
@add_options(auth_options)
@add_options(username_options)
@add_options(git_url_options)
def prep_git(ref, branch, repo, auth, username, git_url):
    """Prep git and env variables and bump version"""
    lib.prep_git(ref, branch, repo, auth, username, git_url)


@main.command()
@add_options(version_spec_options)
@add_options(version_cmd_options)
@add_options(changelog_path_options)
@add_options(python_packages_options)
@use_checkout_dir()
def bump_version(version_spec, version_cmd, changelog_path, python_packages):
    """Prep git and env variables and bump version"""
    prev_dir = os.getcwd()
    for python_package in [p.split(":")[0] for p in python_packages]:
        os.chdir(python_package)
        lib.bump_version(version_spec, version_cmd, changelog_path)
        os.chdir(prev_dir)


@main.command()
@add_options(dry_run_options)
@add_options(auth_options)
@add_options(changelog_path_options)
@add_options(release_url_options)
@use_checkout_dir()
def extract_changelog(dry_run, auth, changelog_path, release_url):
    lib.extract_changelog(dry_run, auth, changelog_path, release_url)


@main.command()
@add_options(changelog_options)
@use_checkout_dir()
def build_changelog(
    ref, branch, repo, auth, changelog_path, since, since_last_stable, resolve_backports
):
    """Build changelog entry"""
    changelog.build_entry(
        ref,
        branch,
        repo,
        auth,
        changelog_path,
        since,
        since_last_stable,
        resolve_backports,
    )


@main.command()
@add_options(version_spec_options)
@add_options(branch_options)
@add_options(since_options)
@add_options(auth_options)
@add_options(changelog_path_options)
@add_options(dry_run_options)
@add_options(post_version_spec_options)
@use_checkout_dir()
def draft_changelog(
    version_spec,
    ref,
    branch,
    repo,
    since,
    since_last_stable,
    auth,
    changelog_path,
    dry_run,
    post_version_spec,
    post_version_message,
):
    """Create a changelog entry PR"""
    lib.draft_changelog(
        version_spec,
        ref,
        branch,
        repo,
        since,
        since_last_stable,
        auth,
        changelog_path,
        dry_run,
        post_version_spec,
        post_version_message,
    )


@main.command()
@add_options(dist_dir_options)
@add_options(python_packages_options)
@use_checkout_dir()
def build_python(dist_dir, python_packages):
    """Build Python dist files"""
    prev_dir = os.getcwd()
    clean = True
    for python_package in [p.split(":")[0] for p in python_packages]:
        os.chdir(python_package)
        if not util.PYPROJECT.exists() and not util.SETUP_PY.exists():
            util.log(
                f"Skipping build-python in {python_package} since there are no python package files"
            )
        else:
            python.build_dist(Path(os.path.relpath(".", python_package)) / dist_dir, clean=clean)
            clean = False
        os.chdir(prev_dir)


@main.command()
@add_options(dist_dir_options)
@add_options(check_imports_options)
@add_options(pydist_check_options)
@use_checkout_dir()
def check_python(
    dist_dir, check_imports, pydist_check_cmd, pydist_extra_check_cmds, pydist_resource_paths
):
    """Check Python dist files"""
    for dist_file in glob(f"{dist_dir}/*"):
        if Path(dist_file).suffix not in [".gz", ".whl"]:
            util.log(f"Skipping non-python dist file {dist_file}")
            continue

        python.check_dist(
            dist_file,
            python_imports=check_imports,
            check_cmd=pydist_check_cmd,
            extra_check_cmds=pydist_extra_check_cmds,
            resource_paths=pydist_resource_paths,
        )


@main.command()
@add_options(dist_dir_options)
@click.argument("package", default=".")
@use_checkout_dir()
def build_npm(package, dist_dir):
    """Build npm package"""
    if not osp.exists("./package.json"):
        util.log("Skipping build-npm since there is no package.json file")
        return
    npm.build_dist(package, dist_dir)


@main.command()
@add_options(dist_dir_options)
@add_options(npm_install_options)
@use_checkout_dir()
def check_npm(dist_dir, npm_install_options):
    """Check npm package"""
    if not osp.exists("./package.json"):
        util.log("Skipping check-npm since there is no package.json file")
        return
    npm.check_dist(dist_dir, npm_install_options)


@main.command()
@add_options(dist_dir_options)
@click.option(
    "--release-message",
    envvar="RH_RELEASE_MESSAGE",
    default="Publish {version}",
    help="The message to use for the release commit",
)
@click.option(
    "--tag-format",
    envvar="RH_TAG_FORMAT",
    default="v{version}",
    help="The format to use for the release tag",
)
@click.option(
    "--tag-message",
    envvar="RH_TAG_MESSAGE",
    default="Release {tag_name}",
    help="The message to use for the release tag",
)
@click.option(
    "--no-git-tag-workspace",
    is_flag=True,
    help="Whether to skip tagging npm workspace packages",
)
@use_checkout_dir()
def tag_release(dist_dir, release_message, tag_format, tag_message, no_git_tag_workspace):
    """Create release commit and tag"""
    lib.tag_release(dist_dir, release_message, tag_format, tag_message, no_git_tag_workspace)


@main.command()
@add_options(branch_options)
@add_options(version_cmd_options)
@add_options(auth_options)
@add_options(changelog_path_options)
@add_options(dist_dir_options)
@add_options(dry_run_options)
@add_options(release_url_options)
@add_options(post_version_spec_options)
@click.argument("assets", nargs=-1)
@use_checkout_dir()
def populate_release(
    ref,
    branch,
    repo,
    version_cmd,
    auth,
    changelog_path,
    dist_dir,
    dry_run,
    release_url,
    post_version_spec,
    post_version_message,
    assets,
):
    lib.populate_release(
        ref,
        branch,
        repo,
        version_cmd,
        auth,
        changelog_path,
        dist_dir,
        dry_run,
        release_url,
        post_version_spec,
        post_version_message,
        assets,
    )


@main.command()
@add_options(auth_options)
@add_options(dry_run_options)
@add_options(release_url_options)
@use_checkout_dir()
def delete_release(auth, dry_run, release_url):
    """Delete a draft GitHub release by url to the release page"""
    lib.delete_release(auth, release_url, dry_run)


@main.command()
@add_options(auth_options)
@add_options(dist_dir_options)
@add_options(dry_run_options)
@add_options(release_url_options)
def extract_release(auth, dist_dir, dry_run, release_url):
    """Download and verify assets from a draft GitHub release"""
    lib.extract_release(
        auth,
        dist_dir,
        dry_run,
        release_url,
    )


@main.command()
@add_options(dist_dir_options)
@click.option("--npm-token", help="A token for the npm release", envvar="NPM_TOKEN")
@click.option(
    "--npm-cmd",
    help="The command to run for npm release",
    envvar="RH_NPM_COMMAND",
    default="npm publish",
)
@click.option(
    "--twine-cmd",
    help="The twine to run for Python release",
    envvar="TWINE_COMMAND",
    default="pipx run twine upload",
)
@click.option(
    "--npm-registry",
    help="The npm registry to target for publishing",
    envvar="NPM_REGISTRY",
    default="https://registry.npmjs.org/",
)
@click.option(
    "--twine-repository-url",
    help="The pypi registry to target for publishing",
    envvar="TWINE_REPOSITORY_URL",
    default="https://upload.pypi.org/legacy/",
)
@add_options(dry_run_options)
@add_options(python_packages_options)
@add_options(release_url_options)
@use_checkout_dir()
def publish_assets(
    dist_dir,
    npm_token,
    npm_cmd,
    twine_cmd,
    npm_registry,
    twine_repository_url,
    dry_run,
    release_url,
    python_packages,
):
    """Publish release asset(s)"""
    for python_package in python_packages:
        lib.publish_assets(
            dist_dir,
            npm_token,
            npm_cmd,
            twine_cmd,
            npm_registry,
            twine_repository_url,
            dry_run,
            release_url,
            python_package,
        )


@main.command()
@add_options(auth_options)
@add_options(dry_run_options)
@add_options(release_url_options)
@use_checkout_dir()
def publish_release(auth, dry_run, release_url):
    """Publish GitHub release"""
    lib.publish_release(auth, dry_run, release_url)


@main.command()
@add_options(branch_options)
@add_options(dry_run_options)
@click.option(
    "--expected-sha", help="The expected sha of the branch HEAD", envvar="RH_EXPECTED_SHA"
)
@use_checkout_dir()
def ensure_sha(ref, branch, repo, dry_run, expected_sha):
    util.ensure_sha(dry_run, expected_sha, branch)


@main.command()
@add_options(auth_options)
@add_options(branch_options)
@add_options(username_options)
@add_options(changelog_path_options)
@add_options(dry_run_options)
@add_options(release_url_options)
@use_checkout_dir()
def forwardport_changelog(auth, ref, branch, repo, username, changelog_path, dry_run, release_url):
    """Forwardport Changelog Entries to the Default Branch"""
    lib.forwardport_changelog(
        auth, ref, branch, repo, username, changelog_path, dry_run, release_url
    )


if __name__ == "__main__":  # pragma: no cover
    main()
