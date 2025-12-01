# Convert a Repo to Use Releaser from Repo

Follow the steps below to convert a repository to use Jupyter Releaser for releases, where maintainers make releases from the repository itself.

## Prerequisites

See checklist below for details:

- Markdown changelog
- Bump version configuration (if using Python), for example [hatch](https://hatch.pypa.io/latest/)
- [Add a trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) to your PyPI project
- If publishing to npm, we recommend using [npm Trusted Publishers](https://docs.npmjs.com/trusted-publishers) (requires npm >= 11.5.1, available via Node.js >= 24). Otherwise, create an access token for [npm](https://docs.npmjs.com/creating-and-viewing-access-tokens).

## Checklist for Adoption

- [ ] Set up a [GitHub App](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps#github-apps-that-act-on-their-own-behalf) on your organization (or personal account for a personal project).

  - Disable the web hook
  - Enable Repository permissions > Contents > Read and write
  - Select "Only on this account"
  - Click "Create GitHub App"
  - Browse to the App Settings
  - Select "Install App" and install on all repositories
  - Under "General" click "Generate a private key"
  - Store the `APP_ID` and the private key in a secure location (Jupyter Vault if using a Jupyter Org)

- [ ] Create a "release" [environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) on your repository and add an `APP_ID` Environment Variable and `APP_PRIVATE_KEY` secret.
  The environment should be enabled for ["Protected branches only"](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-branches-and-tags).

- [ ] Configure [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) for the repository

  - Set up branch protection (with default rules) on publication branches
  - Remove global tag protection.
  - Add a branch Ruleset for all branches
    - Allow the GitHub App to bypass protections
    - Set up Pull Request and Required Checks
  - Add a tags Ruleset for all tags
    - Allow the GitHub App to bypass protections

- [ ] Copy `prep-release.yml` and `publish-release.yml` (or only `full-release.yml`) from the
  [example-workflows](https://github.com/jupyter-server/jupyter_releaser/tree/main/example-workflows) folder in this repository.

- [ ] Set up PyPI:

  - Set up your PyPI project by [adding a trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
    - if you use the example workflows, the _workflow name_ is `publish-release.yml` (or `full-release.yml`) and the
      _environment_ should be `release` (the name of the GitHub environment).
  - Ensure the publish release job as `permissions`: `id-token : write` (see the [documentation](https://docs.pypi.org/trusted-publishers/using-a-publisher/))

- [ ] Set up npm (if publishing to npm):

<details><summary>Using npm Trusted Publishers (recommended)</summary>

- npm Trusted Publishers is supported with npm >= 11.5.1

- Ensure the publish release job has `permissions`: `id-token: write` (see the [documentation](https://docs.npmjs.com/generating-provenance-statements))

- Set up the Node.js version in your workflow using one of these approaches:

  Using the `base-setup` action from `jupyterlab/maintainer-tools`:

  ```yaml
  - uses: jupyterlab/maintainer-tools/.github/actions/base-setup@v1
  ```

  Or using the standard `setup-node` action:

  ```yaml
  - uses: actions/setup-node@v6
    with:
      node-version: "24.x"
  ```

- With Trusted Publishers enabled, npm packages will be published with provenance automatically, without needing to store an `NPM_TOKEN` secret

</details>

<details><summary>Using NPM_TOKEN (legacy way)</summary>

- Create an access token for [npm](https://docs.npmjs.com/creating-and-viewing-access-tokens), saved as `NPM_TOKEN`
- This should be created using a machine account that only has publish access
- If you want to set _provenance_ on your package, you need to ensure the publish release job has `permissions`: `id-token: write` (see the [documentation](https://docs.npmjs.com/generating-provenance-statements#publishing-packages-with-provenance-via-github-actions))

</details>

- [ ] Ensure that only trusted users with 2FA have admin access to the repository, since they will be able to trigger releases.

- [ ] Switch to Markdown Changelog

  - We recommend [MyST](https://myst-parser.readthedocs.io/en/latest/?badge=latest), especially if some of your docs are in reStructuredText.
  - Can use `pandoc -s changelog.rst -o changelog.md` and some hand edits as needed.
  - Note that [directives](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-directives) can still be used

- [ ] Add HTML start and end comment markers to Changelog file

  - see example in [CHANGELOG.md](https://github.com/jupyter-server/jupyter_releaser/blob/main/CHANGELOG.md) (view in raw mode)

```md
# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

<!-- <END NEW CHANGELOG ENTRY> -->
```

- [ ] We recommend using [hatch](https://hatch.pypa.io/latest/) for your
  build system and for version handling.
  - If previously providing `version_info` like `version_info = (1, 7, 0, '.dev', '0')`,
    use a pattern like the one below in your version file:

```python
import re
from typing import List

# Version string must appear intact for hatch versioning
__version__ = "6.16.0"

# Build up version_info tuple for backwards compatibility
pattern = r"(?P<major>\d+).(?P<minor>\d+).(?P<patch>\d+)(?P<rest>.*)"
match = re.match(pattern, __version__)
assert match is not None
parts: List[object] = [int(match[part]) for part in ["major", "minor", "patch"]]
if match["rest"]:
    parts.append(match["rest"])
version_info = tuple(parts)
```

- If you need to keep node and python versions in sync, use [hatch-nodejs-version](https://github.com/agoose77/hatch-nodejs-version).

  - See [nbformat](https://github.com/jupyter/nbformat/blob/main/pyproject.toml) for example.

- [ ] Add a GitHub Actions CI step to run the `check_release` action. For example:

  - This should be run on `push` and `pull` request events. You can copy
    the `check-release.yml` from this repo as an example.

```yaml
- name: Check Release
  uses: jupyter-server/jupyter_releaser/.github/actions/check-release@v2
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] If you would like the release assets to be uploaded as artifacts, add the following step after the `check_release` action:

```yaml
- name: Upload Distributions
  uses: actions/upload-artifact@v4
  with:
    name: dist-${{ github.run_number }}
    path: .jupyter_releaser_checkout/dist
```

- [ ] Add a workflow that uses the [`enforce-label`](https://github.com/jupyterlab/maintainer-tools#enforce-labels) action
  from `jupyterlab/maintainer-tools` to ensure that all PRs have on of the triage labels used to categorize the changelog.

```yaml
name: Enforce PR label

on:
  pull_request:
    types: [labeled, unlabeled, opened, edited, synchronize]

jobs:
  enforce-label:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - name: enforce-triage-label
        uses: jupyterlab/maintainer-tools/.github/actions/enforce-label@v1
```

- [ ] Update or add `RELEASE.md` that describes the onboarding and release process, e.g. [jupyter_server](https://github.com/jupyter-server/jupyter_server/blob/main/RELEASE.md).

- [ ] Optionally add configuration to the repository if non-standard options or hooks are needed.

- [ ] If desired, add `check_release` job, changelog, and `hatch` support to other active release branches

## Initial Release Workflow

- [ ] Try out the `Prep Release` and `Publish Release` process against a fork of the target repo first so you don't accidentally push tags and GitHub releases to the source repository. Set the `TWINE_REPOSITORY_URL` environment variable to `https://test.pypi.org/legacy/` in the "Finalize Release" action part of the workflow

- [ ] Try the `Publish Release` process using a prerelease version on the main
  repository before publishing a final version.

## Backport Branches

- Create backport branches the usual way, e.g. `git checkout -b 3.0.x v3.0.1; git push origin 3.0.x`
- When running the `Publish Release` Workflow, an automatic PR is generated for the default branch
  in the target repo, positioned in the appropriate place in the changelog.
