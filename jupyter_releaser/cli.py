# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import os.path as osp
from glob import glob
from pathlib import Path

import click

from jupyter_releaser import changelog
from jupyter_releaser import lib
from jupyter_releaser import npm
from jupyter_releaser import python
from jupyter_releaser import util


class ReleaseHelperGroup(click.Group):
    """Click group tailored to jupyter-releaser"""

    _needs_checkout_dir = dict()

    def invoke(self, ctx):
        """Handle jupyter-releaser config while invoking a command"""
        # Get the command name and make sure it is valid
        cmd_name = ctx.protected_args[0]
        if not cmd_name in self.commands:
            super().invoke(ctx)

        if cmd_name == "list-envvars":
            envvars = dict()
            for cmd_name in self.commands:
                for param in self.commands[cmd_name].params:
                    if isinstance(param, click.Option):
                        if param.envvar:
                            envvars[param.name] = param.envvar

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

        # Print a separation header
        util.log(f'\n\n{"-" * 50}')
        util.log(cmd_name)
        util.log(f'{"-" * 50}\n\n')

        if cmd_name in skip or cmd_name.replace("-", "_") in skip:
            util.log("*** Skipping based on skip config")
            return

        # Handle all of the parameters
        for param in self.commands[cmd_name].get_params(ctx):
            # Defer to env var overrides
            if param.envvar and os.environ.get(param.envvar):
                continue
            name = param.name
            if name in options or name.replace("_", "-") in options:
                arg = f"--{name.replace('_', '-')}"
                # Defer to cli overrides
                if arg not in ctx.args:
                    val = options.get(name, options.get(name.replace("_", "-")))
                    if isinstance(val, list):
                        for v in val:
                            ctx.args.append(arg)
                            ctx.args.append(v)
                    else:
                        ctx.args.append(arg)
                        ctx.args.append(val)

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
        if cmd_name == "prep-git":
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
@click.option(
    "--force", default=False, help="Force a command to run even when skipped by config"
)
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

version_cmd_options = [
    click.option(
        "--version-cmd", envvar="RH_VERSION_COMMAND", help="The version command"
    )
]


branch_options = [
    click.option("--ref", envvar="RH_REF", help="The source reference"),
    click.option("--branch", envvar="RH_BRANCH", help="The target branch"),
    click.option("--repo", envvar="RH_REPOSITORY", help="The git repo"),
]

auth_options = [
    click.option("--auth", envvar="GITHUB_ACCESS_TOKEN", help="The GitHub auth token"),
]

username_options = [
    click.option("--username", envvar="GITHUB_ACTOR", help="The git username")
]

dist_dir_options = [
    click.option(
        "--dist-dir",
        envvar="RH_DIST_DIR",
        default="dist",
        help="The folder to use for dist files",
    )
]

dry_run_options = [
    click.option(
        "--dry-run", is_flag=True, envvar="RH_DRY_RUN", help="Run as a dry run"
    )
]


git_url_options = [
    click.option("--git-url", help="A custom url for the git repository")
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
    )
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
@use_checkout_dir()
def bump_version(version_spec, version_cmd):
    """Prep git and env variables and bump version"""
    lib.bump_version(version_spec, version_cmd)


@main.command()
@add_options(changelog_options)
@use_checkout_dir()
def build_changelog(ref, branch, repo, auth, changelog_path, since, resolve_backports):
    """Build changelog entry"""
    changelog.build_entry(branch, repo, auth, changelog_path, since, resolve_backports)


@main.command()
@add_options(version_spec_options)
@add_options(branch_options)
@add_options(since_options)
@add_options(auth_options)
@add_options(changelog_path_options)
@add_options(dry_run_options)
@use_checkout_dir()
def draft_changelog(
    version_spec, ref, branch, repo, since, auth, changelog_path, dry_run
):
    """Create a changelog entry PR"""
    lib.draft_changelog(
        version_spec, branch, repo, since, auth, changelog_path, dry_run
    )


@main.command()
@add_options(changelog_options)
@click.option(
    "--output", envvar="RH_CHANGELOG_OUTPUT", help="The output file for changelog entry"
)
@use_checkout_dir()
def check_changelog(
    ref, branch, repo, auth, changelog_path, since, resolve_backports, output
):
    """Check changelog entry"""
    changelog.check_entry(
        branch, repo, auth, changelog_path, since, resolve_backports, output
    )


@main.command()
@add_options(dist_dir_options)
@use_checkout_dir()
def build_python(dist_dir):
    """Build Python dist files"""
    if not util.PYPROJECT.exists() and not util.SETUP_PY.exists():
        util.log("Skipping build-python since there are no python package files")
        return
    python.build_dist(dist_dir)


@main.command()
@add_options(dist_dir_options)
@use_checkout_dir()
def check_python(dist_dir):
    """Check Python dist files"""
    for dist_file in glob(f"{dist_dir}/*"):
        if Path(dist_file).suffix not in [".gz", ".whl"]:
            util.log(f"Skipping non-python dist file {dist_file}")
            continue
        python.check_dist(dist_file)


@main.command()
@add_options(dist_dir_options)
@click.argument("package", default=".")
@use_checkout_dir()
def build_npm(package, dist_dir):
    """Build npm package"""
    if not osp.exists("./package.json"):
        util.log("Skipping check-npm since there is no package.json file")
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
@use_checkout_dir()
def check_manifest():
    """Check the project manifest"""
    if util.PYPROJECT.exists() or util.SETUP_PY.exists():
        util.run("check-manifest -v")
    else:
        util.log("Skipping check-manifest since there are no python package files")


@main.command()
@click.option(
    "--ignore-glob",
    default=[],
    multiple=True,
    help="Ignore test file paths based on glob pattern",
)
@click.option(
    "--ignore-links",
    multiple=True,
    help="Ignore links based on regex pattern(s)",
)
@click.option(
    "--cache-file",
    envvar="RH_CACHE_FILE",
    default="~/.cache/pytest-link-check",
    help="The cache file to use",
)
@click.option(
    "--links-expire",
    default=604800,
    envvar="RH_LINKS_EXPIRE",
    help="Duration in seconds for links to be cached (default one week)",
)
@use_checkout_dir()
def check_links(ignore_glob, ignore_links, cache_file, links_expire):
    """Check URLs for HTML-containing files."""
    lib.check_links(ignore_glob, ignore_links, cache_file, links_expire)


@main.command()
@add_options(dist_dir_options)
@click.option(
    "--no-git-tag-workspace",
    is_flag=True,
    help="Whether to skip tagging npm workspace packages",
)
@use_checkout_dir()
def tag_release(dist_dir, no_git_tag_workspace):
    """Create release commit and tag"""
    lib.tag_release(dist_dir, no_git_tag_workspace)


@main.command()
@add_options(branch_options)
@add_options(auth_options)
@add_options(changelog_path_options)
@add_options(version_cmd_options)
@add_options(dist_dir_options)
@add_options(dry_run_options)
@click.option(
    "--post-version-spec",
    envvar="RH_POST_VERSION_SPEC",
    help="The post release version (usually dev)",
)
@click.argument("assets", nargs=-1)
@use_checkout_dir()
def draft_release(
    ref,
    branch,
    repo,
    auth,
    changelog_path,
    version_cmd,
    dist_dir,
    dry_run,
    post_version_spec,
    assets,
):
    """Publish Draft GitHub release"""
    lib.draft_release(
        ref,
        branch,
        repo,
        auth,
        changelog_path,
        version_cmd,
        dist_dir,
        dry_run,
        post_version_spec,
        assets,
    )


@main.command()
@add_options(auth_options)
@click.argument("release-url", nargs=1)
def delete_release(auth, release_url):
    """Delete a draft GitHub release by url to the release page"""
    lib.delete_release(auth, release_url)


@main.command()
@add_options(auth_options)
@add_options(dist_dir_options)
@add_options(dry_run_options)
@add_options(npm_install_options)
@click.argument("release-url", nargs=1)
def extract_release(auth, dist_dir, dry_run, release_url, npm_install_options):
    """Download and verify assets from a draft GitHub release"""
    lib.extract_release(auth, dist_dir, dry_run, release_url, npm_install_options)


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
    default="twine upload",
)
@click.option("--use-checkout-dir", help="Use the checkout directory", is_flag=True)
@add_options(dry_run_options)
def publish_assets(dist_dir, npm_token, npm_cmd, twine_cmd, dry_run, use_checkout_dir):
    """Publish release asset(s)"""
    lib.publish_assets(
        dist_dir, npm_token, npm_cmd, twine_cmd, dry_run, use_checkout_dir
    )


@main.command()
@add_options(auth_options)
@click.argument("release-url", nargs=1)
def publish_release(auth, release_url):
    """Publish GitHub release"""
    lib.publish_release(auth, release_url)


@main.command()
@add_options(auth_options)
@add_options(branch_options)
@add_options(username_options)
@add_options(changelog_path_options)
@add_options(dry_run_options)
@add_options(git_url_options)
@click.argument("release-url")
def forwardport_changelog(
    auth, ref, branch, repo, username, changelog_path, dry_run, git_url, release_url
):
    """Forwardport Changelog Entries to the Default Branch"""
    lib.forwardport_changelog(
        auth, ref, branch, repo, username, changelog_path, dry_run, git_url, release_url
    )


if __name__ == "__main__":  # pragma: no cover
    main()
