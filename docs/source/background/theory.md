# Theory

## Motivation

This project should help maintainers reduce toil and save time in the release process by enforcing best practices to:

- Automate a changelog for every release
- Verify the install and import of dist asset(s)
- Commit a message with hashes of dist file(s)
- Annotate the git tag in standard format
- Create a GitHub release with changelog entry
- Forward port changelog entries into default branch
- Dry run publish on CI
- Revert to Dev version after release (optional)

## Action Details

Detailed workflows are available to draft a changelog, draft a release, publish a release, and check a release.

### Prep Release Action

- Inputs are the target repo, branch, and the version spec
- Bumps the version
  - By default, uses [hatch](https://hatch.pypa.io/latest/), [tbump](https://github.com/tankerhq/tbump) or [bump2version](https://github.com/c4urself/bump2version) to bump the version based on presence of config files
    - We recommend `hatch` for most cases because it is very easy to set up.
- Prepares the environment
  - Sets up git config and branch
- Generates a changelog (using [github-activity](https://github.com/executablebooks/github-activity)) using the PRs since the last tag on this branch.
  - Gets the current version and then does a git checkout to clear state
  - Adds a new version entry using a HTML comment markers in the changelog file
  - Optionally resolves [meeseeks](https://github.com/MeeseeksBox/MeeseeksDev) backport PRs to their original PR
- Creates a Draft GitHub release with the changelog changes and an attached
  metadata.json file capturing the inputs to the workflow.

### Populate Release Action

- Input is typically the URL of the draft GitHub Release created in the Prep Release workflow, or no input to use the most recent draft release.
- Fetches the `metadata.json` file and the changelog entry from the draft
  release.
- Prepares the environment using the same method as the changelog action
- Bumps the version
- For Python packages:
  - Builds the wheel and source distributions if applicable
  - Makes sure Python dists can be installed and imported in a virtual environment
- For npm package(s) (including workspace support):
  - Builds tarball(s) using `npm pack`
  - Make sure tarball(s) can be installed and imported in a new npm package
- Adds a commit that includes the hashes of the dist files
- Creates an annotated version tag in standard format
- If given, bumps the version using the post version spec. he post version
  spec can also be given as a setting, [Write Releaser Config Guide](../how_to_guides/write_config.md).
- Verifies that the SHA of the most recent commit has not changed on the target
  branch, preventing a mismatch of release commit.
- Pushes the commits and tag to the target `branch`
- Pusehes the created assets to the draft release, along with an `asset_shas.json` file capturing the checksums of the files.

### Finalize Release Action

- Input is the url of the draft GitHub release from the Populate Release
  action.
- Downloads the dist assets from the release
- Verifies shas of release assets against the `asset_shas.json` file.
- Publishes assets to appropriate registries.
- Publishes the final GitHub release
- If the tag is on a backport branch, makes a forwardport PR for the changelog entry

Typically the Populate Release action and Finalize release action are
run as part of the same workflow.

### Check Release Action

- Runs on CI in the target repository to verify compatibility and release-ability.
- Runs the `Draft Changelog` and `Draft Release` actions in dry run mode
- Publishes to the local PyPI server and/or dry-run `npm publish`.
- Does not make PRs or push git changes
