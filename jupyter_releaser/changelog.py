# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import re
from pathlib import Path

from ghapi.core import GhApi
from github_activity import generate_activity_md

from jupyter_releaser import util

START_MARKER = "<!-- <START NEW CHANGELOG ENTRY> -->"
END_MARKER = "<!-- <END NEW CHANGELOG ENTRY> -->"
PR_PREFIX = "Automated Changelog Entry"


def format_pr_entry(target, number, auth=None):
    """Format a PR entry in the style used by our changelogs.

    Parameters
    ----------
    target : str
        The GitHub owner/repo
    number : int
        The PR number to resolve
    auth : str, optional
        The GitHub authorization token

    Returns
    -------
    str
        A formatted PR entry
    """
    owner, repo = target.split("/")
    gh = GhApi(owner=owner, repo=repo, token=auth)
    pull = gh.pulls.get(number)
    title = pull.title
    url = pull.html_url
    user_name = pull.user.login
    user_url = pull.user.html_url
    return f"- {title} [#{number}]({url}) ([@{user_name}]({user_url}))"


def get_version_entry(
    branch, repo, version, *, since=None, auth=None, resolve_backports=False
):
    """Get a changelog for the changes since the last tag on the given branch.

    Parameters
    ----------
    branch : str
        The target branch
    respo : str
        The GitHub owner/repo
    version : str
        The new version
    since: str
        Use PRs with activity since this date or git reference
    auth : str, optional
        The GitHub authorization token
    resolve_backports: bool, optional
        Whether to resolve backports to the original PR

    Returns
    -------
    str
        A formatted changelog entry with markers
    """
    since = since or util.get_latest_tag(branch)

    branch = branch.split("/")[-1]
    util.log(f"Getting changes to {repo} since {since} on branch {branch}...")

    until = util.run(f'git --no-pager log -n 1 origin/{branch} --pretty=format:"%H"')
    until = until.replace("%", "")

    md = generate_activity_md(
        repo,
        since=since,
        kind="pr",
        heading_level=2,
        auth=auth,
        branch=branch,
    )

    if not md:
        util.log("No PRs found")
        return f"## {version}\n\nNo merged PRs"

    entry = md.replace("[full changelog]", "[Full Changelog]")
    entry = entry.replace("...None", f"...{until}")

    entry = entry.splitlines()[2:]

    for (ind, line) in enumerate(entry):
        if re.search(r"\[@meeseeksmachine\]", line) is not None:
            match = re.search(r"Backport PR #(\d+)", line)
            if match:
                entry[ind] = format_pr_entry(repo, match.groups()[0])

    # Remove github actions PRs
    gh_actions = "[@github-actions](https://github.com/github-actions)"
    entry = [e for e in entry if gh_actions not in e]

    # Remove automated changelog PRs
    entry = [e for e in entry if PR_PREFIX not in e]

    entry = "\n".join(entry).strip()

    # Replace "*" unordered list marker with "-" since this is what
    # Prettier uses
    # TODO: remove after github_activity 0.1.4+ is available
    entry = re.sub(r"^\* ", "- ", entry)
    entry = re.sub(r"\n\* ", "\n- ", entry)

    output = f"""
## {version}

{entry}
""".strip()

    return output


def build_entry(branch, repo, auth, changelog_path, since, resolve_backports):
    """Build a python version entry"""
    branch = branch or util.get_branch()
    repo = repo or util.get_repo()

    # Get the new version
    version = util.get_version()

    # Get the existing changelog and run some validation
    changelog = Path(changelog_path).read_text(encoding="utf-8")

    if START_MARKER not in changelog or END_MARKER not in changelog:
        raise ValueError("Missing insert marker for changelog")

    if changelog.find(START_MARKER) != changelog.rfind(START_MARKER):
        raise ValueError("Insert marker appears more than once in changelog")

    # Get changelog entry
    entry = get_version_entry(
        f"origin/{branch}",
        repo,
        version,
        since=since,
        auth=auth,
        resolve_backports=resolve_backports,
    )

    changelog = insert_entry(changelog, entry, version=version)
    Path(changelog_path).write_text(changelog, encoding="utf-8")

    # Stage changelog
    util.run(f"git add {util.normalize_path(changelog_path)}")


def insert_entry(changelog, entry, version=None):
    """Insert the entry into the existing changelog."""
    # Test if we are augmenting an existing changelog entry (for new PRs)
    # Preserve existing PR entries since we may have formatted them
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
            for old_line in prev_entry.splitlines():
                if pr.group() in old_line:
                    lines[ind] = old_line
        changelog = changelog.replace(prev_entry, "\n".join(lines))
    else:
        changelog = changelog.replace(END_MARKER, "")
        changelog = changelog.replace(START_MARKER, new_entry)

    return format(changelog)


def format(changelog):
    """Clean up changelog formatting"""
    changelog = re.sub(r"\n\n+", r"\n\n", changelog)
    return re.sub(r"\n\n+$", r"\n", changelog)


def check_entry(branch, repo, auth, changelog_path, since, resolve_backports, output):
    """Check changelog entry"""
    branch = branch or util.get_branch()

    # Get the new version
    version = util.get_version()

    # Finalize changelog
    changelog = Path(changelog_path).read_text(encoding="utf-8")

    start = changelog.find(START_MARKER)
    end = changelog.find(END_MARKER)

    if start == -1 or end == -1:  # pragma: no cover
        raise ValueError("Missing new changelog entry delimiter(s)")

    if start != changelog.rfind(START_MARKER):  # pragma: no cover
        raise ValueError("Insert marker appears more than once in changelog")

    final_entry = changelog[start + len(START_MARKER) : end]

    repo = repo or util.get_repo()

    raw_entry = get_version_entry(
        f"origin/{branch}",
        repo,
        version,
        since=since,
        auth=auth,
        resolve_backports=resolve_backports,
    )

    if f"# {version}" not in final_entry:  # pragma: no cover
        util.log(final_entry)
        raise ValueError(f"Did not find entry for {version}")

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
        if not f"[#{pr}]" in final_entry:  # pragma: no cover
            raise ValueError(f"Missing PR #{pr} in changelog")
    for pr in final_prs:
        if not f"[#{pr}]" in raw_entry:  # pragma: no cover
            raise ValueError(f"PR #{pr} does not belong in changelog for {version}")

    if output:
        Path(output).write_text(final_entry, encoding="utf-8")


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
