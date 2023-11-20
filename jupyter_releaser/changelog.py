"""Changelog utilities for Jupyter Releaser."""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import re
from pathlib import Path
from typing import Optional

import mdformat
from fastcore.net import HTTP404NotFoundError  # type:ignore[import-untyped]
from github_activity import generate_activity_md  # type:ignore[import-untyped]

from jupyter_releaser import util

START_MARKER = "<!-- <START NEW CHANGELOG ENTRY> -->"
END_MARKER = "<!-- <END NEW CHANGELOG ENTRY> -->"
START_SILENT_MARKER = "<!-- START SILENT CHANGELOG ENTRY -->"
END_SILENT_MARKER = "<!-- END SILENT CHANGELOG ENTRY -->"
PR_PREFIX = "Automated Changelog Entry"
PRECOMMIT_PREFIX = "[pre-commit.ci] pre-commit autoupdate"


def format_pr_entry(target, number, auth=None, dry_run=False):
    """Format a PR entry in the style used by our changelogs.

    Parameters
    ----------
    target : str
        The GitHub owner/repo
    number : int
        The PR number to resolve
    auth : str, optional
        The GitHub authorization token
    dry_run: bool, optional
        Whether this is a dry run.

    Returns
    -------
    str
        A formatted PR entry
    """
    owner, repo = target.split("/")
    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo, token=auth)
    pull = gh.pulls.get(number)
    title = pull.title
    url = pull.html_url
    user_name = pull.user.login
    user_url = pull.user.html_url
    return f"- {title} [#{number}]({url}) ([@{user_name}]({user_url}))"


def get_version_entry(
    ref,
    branch,
    repo,
    version,
    *,
    since=None,
    since_last_stable=None,
    until=None,
    auth=None,
    resolve_backports=False,
    dry_run=False,
):
    """Get a changelog for the changes since the last tag on the given branch.

    Parameters
    ----------
    branch : str
        The target branch
    ref: str
        The source reference
    repo : str
        The GitHub owner/repo
    version : str
        The new version
    since: str
        Use PRs with activity since this date or git reference
    since_last_stable:
        Use PRs with activity since the last stable git tag
    until: str, optional
        Use PRs until this date or git reference
    auth : str, optional
        The GitHub authorization token
    resolve_backports: bool, optional
        Whether to resolve backports to the original PR
    dry_run: bool, optional
        Whether this is a dry run.

    Returns
    -------
    str
        A formatted changelog entry with markers
    """
    branch = branch or util.get_branch()
    since = since or util.get_latest_tag(ref or branch, since_last_stable)

    if since == "":
        since = util.get_first_commit(ref or branch)

    util.log(f"Getting changes to {repo} since {since} on branch {branch}...")

    until = until.replace("%", "") if until else None

    md = generate_activity_md(
        repo,
        since=since,
        until=until,
        kind="pr",
        heading_level=2,
        auth=auth,
        branch=branch,
    )

    if not md:
        util.log("No PRs found")
        return f"## {version}\n\nNo merged PRs"

    entry = md.replace("[full changelog]", "[Full Changelog]")

    entry = entry.replace("...None", f"...{until}") if until else entry.replace("...None", "")

    entry = entry.splitlines()[2:]

    for ind, line in enumerate(entry):
        # Look for a backport, either manual or automatic.
        match = re.search(r"Backport PR #(\d+) on branch", line)
        if match:
            entry[ind] = format_pr_entry(repo, match.groups()[0], auth=auth, dry_run=dry_run)

    # Remove github actions PRs
    gh_actions = "[@github-actions](https://github.com/github-actions)"
    entry = [e for e in entry if gh_actions not in e]

    # Remove automated changelog PRs
    entry = [e for e in entry if PR_PREFIX not in e]

    # Remove Pre-Commit PRs
    entry = [e for e in entry if PRECOMMIT_PREFIX not in e]

    entry = "\n".join(entry).strip()

    # Remove empty documentation entry if only automated changelogs were there
    if "# Documentation improvements" in entry and "# Documentation improvements\n\n-" not in entry:
        entry = re.sub(r"#+ Documentation improvements\n\n", "", entry)

    output = f"""
## {version}

{entry}
""".strip()

    return output


def build_entry(
    ref, branch, repo, auth, changelog_path, since, since_last_stable, resolve_backports
):
    """Build a python version entry"""
    branch = branch or util.get_branch()
    repo = repo or util.get_repo()

    # Get the new version
    version = util.get_version()

    # Get changelog entry
    entry = get_version_entry(
        ref,
        branch,
        repo,
        version,
        since=since,
        since_last_stable=since_last_stable,
        auth=auth,
        resolve_backports=resolve_backports,
    )
    update_changelog(changelog_path, entry)


def update_changelog(changelog_path, entry, silent=False):
    """Update a changelog with a new entry."""
    # Get the new version
    version = util.get_version()

    # Get the existing changelog and run some validation
    changelog = Path(changelog_path).read_text(encoding="utf-8")

    if START_MARKER not in changelog or END_MARKER not in changelog:
        msg = "Missing insert marker for changelog"
        raise ValueError(msg)

    if changelog.find(START_MARKER) != changelog.rfind(START_MARKER):
        msg = "Insert marker appears more than once in changelog"
        raise ValueError(msg)

    changelog = insert_entry(changelog, entry, version=version, silent=silent)
    Path(changelog_path).write_text(changelog, encoding="utf-8")


def remove_placeholder_entries(
    repo: str,
    auth: Optional[str],
    changelog_path: str,
    dry_run: bool,
) -> int:
    """Replace any silent marker with the GitHub release body
    if the release has been published.

    Parameters
    ----------
    repo : str
        The GitHub owner/repo
    auth : str
        The GitHub authorization token
    changelog_path : str
        The changelog file path
    dry_run: bool

    Returns
    -------
    int
        Number of placeholders removed
    """

    changelog = Path(changelog_path).read_text(encoding="utf-8")
    start_count = changelog.count(START_SILENT_MARKER)
    end_count = changelog.count(END_SILENT_MARKER)
    if start_count != end_count:
        msg = ""
        raise ValueError(msg)

    repo = repo or util.get_repo()
    owner, repo_name = repo.split("/")
    gh = util.get_gh_object(dry_run=dry_run, owner=owner, repo=repo_name, token=auth)

    # Replace silent placeholder by release body if it has been published
    previous_index = None
    changes_count = 0
    for _ in range(start_count):
        start = changelog.index(START_SILENT_MARKER, previous_index)
        end = changelog.index(END_SILENT_MARKER, start)

        version = _extract_version(changelog[start + len(START_SILENT_MARKER) : end])
        try:
            util.log(f"Getting release for tag '{version}'...")
            release = gh.repos.get_release_by_tag(owner=owner, repo=repo_name, tag=f"v{version}")
        except HTTP404NotFoundError:
            # Skip this version
            pass
        else:
            if not release.draft:
                changelog_text = mdformat.text(release.body)
                changelog = (
                    changelog[:start]
                    + f"\n\n{changelog_text}\n\n"
                    + changelog[end + len(END_SILENT_MARKER) :]
                )
                changes_count += 1

        previous_index = end

    # Write back the new changelog
    Path(changelog_path).write_text(format(changelog), encoding="utf-8")
    return changes_count


def insert_entry(
    changelog: str, entry: str, version: Optional[str] = None, silent: bool = False
) -> str:
    """Insert the entry into the existing changelog."""
    # Test if we are augmenting an existing changelog entry (for new PRs)
    # Preserve existing PR entries since we may have formatted them
    if silent:
        entry = f"{START_SILENT_MARKER}\n\n## {version}\n\n{END_SILENT_MARKER}"

    new_entry = f"{START_MARKER}\n\n{entry}\n\n{END_MARKER}"
    prev_entry = changelog[
        changelog.index(START_MARKER) : changelog.index(END_MARKER) + len(END_MARKER)
    ]

    if f"# {version}\n" in prev_entry:
        lines = new_entry.splitlines()
        old_lines = prev_entry.splitlines()
        for ind, line in enumerate(lines):
            pr = re.search(r"\[#\d+\]", line)
            if not pr:
                continue
            for old_line in old_lines:
                if pr.group() in old_line:
                    lines[ind] = old_line
        changelog = changelog.replace(prev_entry, "\n".join(lines))
    else:
        changelog = changelog.replace(END_MARKER, "")
        changelog = changelog.replace(START_MARKER, new_entry)

    return format(changelog)


def format(changelog: str) -> str:  # noqa A001
    """Clean up changelog formatting"""
    changelog = re.sub(r"\n\n+", r"\n\n", changelog)
    return re.sub(r"\n\n+$", r"\n", changelog)


def check_entry(  # noqa
    ref,
    branch,
    repo,
    auth,
    changelog_path,
    since,
    since_last_stable,
    resolve_backports,
    output,
):
    """Check changelog entry"""
    branch = branch or util.get_branch()

    # Get the new version
    version = util.get_version()

    # Finalize changelog
    changelog = Path(changelog_path).read_text(encoding="utf-8")

    start = changelog.find(START_MARKER)
    end = changelog.find(END_MARKER)

    if start == -1 or end == -1:  # pragma: no cover
        msg = "Missing new changelog entry delimiter(s)"
        raise ValueError(msg)

    if start != changelog.rfind(START_MARKER):  # pragma: no cover
        msg = "Insert marker appears more than once in changelog"
        raise ValueError(msg)

    final_entry = changelog[start + len(START_MARKER) : end]

    repo = repo or util.get_repo()

    raw_entry = get_version_entry(
        ref,
        branch,
        repo,
        version,
        since=since,
        since_last_stable=since_last_stable,
        auth=auth,
        resolve_backports=resolve_backports,
    )

    if f"# {version}" not in final_entry:  # pragma: no cover
        util.log(final_entry)
        msg = f"Did not find entry for {version}"
        raise ValueError(msg)

    final_prs = re.findall(r"\[#(\d+)\]", final_entry)
    raw_prs = re.findall(r"\[#(\d+)\]", raw_entry)

    for pr in raw_prs:
        # Allow for changelog PR to not be in changelog itself
        skip = False
        for line in raw_entry.splitlines():
            if f"[#{pr}]" in line and "changelog" in line.lower():
                skip = True
                break
        if skip:
            continue
        if f"[#{pr}]" not in final_entry:  # pragma: no cover
            msg = f"Missing PR #{pr} in changelog"
            raise ValueError(msg)
    for pr in final_prs:
        if f"[#{pr}]" not in raw_entry:  # pragma: no cover
            msg = f"PR #{pr} does not belong in changelog for {version}"
            raise ValueError(msg)

    if output:
        Path(output).write_text(final_entry, encoding="utf-8")


def splice_github_entry(orig_entry, github_entry):
    """Splice an entry created on GitHub into one created by build_entry"""

    # Override PR titles
    gh_regex = re.compile(r"^\* (.*?) by @.*?/pull/(\d+)$", flags=re.MULTILINE)
    cl_regex = re.compile(r"^- (.*?) \[#(\d+)\]")

    lut = {}
    for title, pr in re.findall(gh_regex, github_entry):
        lut[pr] = title

    lines = orig_entry.splitlines()
    for ind, line in enumerate(lines):
        match = re.match(cl_regex, line)
        if not match:
            continue
        title, pr = re.findall(cl_regex, line)[0]
        if pr in lut:
            lines[ind] = line.replace(title, lut[pr])

    # Handle preamble
    preamble_index = github_entry.index("## What's Changed")
    if preamble_index > 0:
        preamble = github_entry[:preamble_index]
        if preamble.startswith("# "):
            preamble = preamble.replace("# ", "## ")
        if preamble.startswith("## "):
            preamble = preamble.replace("## ", "### ")

        lines = [*preamble.splitlines(), "", *lines]

    return "\n".join(lines)


def extract_current(changelog_path):
    """Extract the current changelog entry"""
    body = ""
    if changelog_path and Path(changelog_path).exists():
        changelog = Path(changelog_path).read_text(encoding="utf-8")

        start = changelog.find(START_MARKER)
        end = changelog.find(END_MARKER)
        if start != -1 and end != -1:
            body = changelog[start + len(START_MARKER) : end]
    return body


def extract_current_version(changelog_path):
    """Extract the current released version from the changelog"""
    body = extract_current(changelog_path)
    return _extract_version(body)


def _extract_version(entry: str) -> str:
    """Extract version from entry"""
    match = re.match(r"#+ (\d\S+)", entry.strip())
    if not match:
        msg = "Could not find previous version"
        raise ValueError(msg)
    return match.groups()[0]
