# Theory

## Motivation

This project should help maintainers reduce toil and save time in the release process by enforcing best practices to:

- Automate a changelog for every release
- Pre-publish to test server and verify the install and import of dist asset(s)
- Commit a message with hashes of dist file(s)
- Annotate the git tag in standard format
- Create a GitHub release with changelog entry
- Verify url links in markdown and reStructuredText files
- Verify integrity of Python manifest
- Forward port changelog entries into default branch
- Dry run publish on CI
- Revert to Dev version after release (optional)

## Workflow Details

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
  - Input is the URL of the draft GitHub Release created in the Draft Changelog
    workflow.
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
- If given, bumps the version using the post version spec. he post version
  spec can also be given as a setting, [Write Releaser Config Guide](../how_to_guides/write_config.html#automatic-dev-versions).
- Pushes the commits and tag to the target `branch`
- Updates the draft GitHub release for the tag with the changelog entry as the text

### Publish Release Workflow

- Manual Github workflow
  - Input is the url of the draft GitHub release
- Downloads the dist assets from the release
- Verifies shas and integrity of release assets
- Publishes assets to appropriate registries
- If the tag is on a backport branch, makes a forwardport PR for the changelog entry

### Full Release Workflow

- Combines the Draft and Publish workflows into a single workflow.
- If this workflow fails during the publish step, you can address any
  credential errors and run the Publish Release Workflow to publish assets.

### Check Release Workflow

- Runs on CI in the target repository to verify compatibility and release-ability.
- Runs the `Draft Changelog` and `Draft Release` actions in dry run mode
- Publishes to the local PyPI server and/or dry-run `npm publish`.
- Does not make PRs or push git changes
