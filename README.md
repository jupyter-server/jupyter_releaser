# Jupyter Releaser

**Jupyter Releaser** contains a set of helper scripts and GitHub Actions to aid in automated releases of Python and npm packages.

## Installation

To install the latest release locally, make sure you have
[pip installed](https://pip.readthedocs.io/en/stable/installing/) and run:

```bash
    pip install git+https://github.com/jupyter-server/jupyter-releaser
```

## Library Usage

```bash
    jupyter-releaser --help
    jupyter-releaser build-python --help
    jupyter-releaser check-links --help
```

## Checklist for Adoption

See the [adoption docs](https://jupyter-releaser.readthedocs.io/en/latest/how_to_guides/convert_repo.html).

## Workflows

Detailed workflows are available to draft a changelog, draft a release, publish a release, and check a release.

### Draft ChangeLog Workflow

- Manual Github workflow
  - Inputs are the target repo, branch, and the version spec
- Bumps the version
  - By default, uses [tbump](https://github.com/tankerhq/tbump) or [bump2version](https://github.com/c4urself/bump2version) to bump the version based on presence of config files
    - We recommend `tbump` instead of `bump2version` for most cases because it does not handle patch releases well when using [prereleases](https://github.com/c4urself/bump2version/issues/190).
- Prepares the environment
  - Sets up git config and branch
- Generates a changelog (using [github-activity](https://github.com/executablebooks/github-activity)) using the PRs since the last tag on this branch.
  - Gets the current version and then does a git checkout to clear state
  - Adds a new version entry using a HTML comment markers in the changelog file
  - Optionally resolves [meeseeks](https://github.com/MeeseeksBox/MeeseeksDev) backport PRs to their original PR
- Creates a PR with the changelog changes
- Can be re-run using the same version spec. It will add new entries but preserve existing ones (in case they have been hand modified).
- Note: Pre-release changelog sections are not automatically combined,
  but you may wish to do so manually.

### Draft Release Workflow

- Manual Github workflow
  - Inputs are target repository, branch, version spec and optional post version spec
- Bumps version using the same method as the changelog action
- Prepares the environment using the same method as the changelog action
- Checks the changelog entry
  - Looks for the current entry using the HTML comment markers
  - Gets the expected changelog values using `github-activity`
  - Ensures that all PRs are the same between the two
- For Python packages:
  - Builds the wheel and source distributions if applicable
  - Makes sure Python dists can be installed and imported in a virtual environment
- For npm package(s) (including workspace support):
  - Builds tarball(s) using `npm pack`
  - Make sure tarball(s) can be installed and imported in a new npm package
- Checks the package manifest using [`check-manifest`](https://github.com/mgedmin/check-manifest)
- Checks the links in Markdown and reStructuredText files
- Adds a commit that includes the hashes of the dist files
- Creates an annotated version tag in standard format
- If given, bumps the version using the post version spec
- Pushes the commits and tag to the target `branch`
- Publishes a draft GitHub release for the tag with the changelog entry as the text

### Publish Release Workflow

- Manual Github workflow
  - Input is the url of the draft release
- Downloads the dist assets from the release
- Verifies shas and integrity of release assets
- Publishes assets to appropriate registries
- If the tag is on a backport branch, makes a forwardport PR for the changelog entry

### Check Release Workflow

- Runs on CI in the target repository to verify compatibility and release-ability.
- Runs the `Draft Changelog` and `Draft Release` actions in dry run mode
- Publishes to the local PyPI server and/or dry-run `npm publish`.
- Does not make PRs or push git changes

## FAQs

### My changelog is out of sync

Create a new manual PR to fix the PR and re-orient the changelog entry markers.

### PR is merged to the target branch in the middle of a "Draft Release"

The release will fail to push commits because it will not be up to date. Delete the pushed tags and re-start with "Draft Changelog" to
pick up the new PR.

## How to keep fork of Jupyter Releaser up to date

The manual workflow files target the `@v1` actions in the source repository, which means that as long as
the workflow files themselves are up to date, you will always be running the most up to date actions.
