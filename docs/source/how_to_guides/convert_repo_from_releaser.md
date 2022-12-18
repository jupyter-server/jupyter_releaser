# Convert a Repo to Use Releaser from Releaser

Follow the steps below to convert a repository to use Jupyter Releaser for releases, where maintainers make releases from a fork of Jupyter Releaser.

## Prerequisites

See checklist below for details:

- Markdown changelog
- Bump version configuration (if using Python), for example [tbump](https://github.com/dmerejkowsky/tbump)
- [Access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with access to target GitHub repo to run GitHub Actions.
- Access token for the [PyPI registry](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#saving-credentials-on-github)
- If needed, access token for [npm](https://docs.npmjs.com/creating-and-viewing-access-tokens).

## Checklist for Adoption

A. Prep the `jupyter_releaser` fork:

- [ ] Clone this repository onto your GitHub user account.

- [ ] Add a GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with access to target GitHub repo to run
  GitHub Actions, saved as `ADMIN_GITHUB_TOKEN` in the
  [repository secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).
  The token will need "public_repo", and "repo:status" permissions.

- [ ] Add access token for the [PyPI registry](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#saving-credentials-on-github) stored as `PYPI_TOKEN`.
  _Note_ For security reasons, it is recommended that you scope the access
  to a single repository, and use a variable called `PYPI_TOKEN_MAP` that is formatted as follows:

  ```text
  owner1/repo1,token1
  owner2/repo2,token2
  ```

  If you have multiple Python packages in the same repository, you can point to them as follows:

  ```text
  owner1/repo1/path/to/package1,token1
  owner1/repo1/path/to/package2,token2
  ```

- [ ] If needed, add access token for [npm](https://docs.npmjs.com/creating-and-viewing-access-tokens), saved as `NPM_TOKEN`.

B. Prep target repository:

- [ ] Switch to Markdown Changelog
  - We recommend [MyST](https://myst-parser.readthedocs.io/en/latest/?badge=latest), especially if some of your docs are in reStructuredText.
  - Can use `pandoc -s changelog.rst -o changelog.md` and some hand edits as needed.
  - Note that [directives](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-directives) can still be used
- [ ] Add HTML start and end comment markers to Changelog file - see example in [CHANGELOG.md](https://github.com/jupyter-server/jupyter_releaser/blob/main/CHANGELOG.md) (view in raw mode)
- [ ] We recommend using [hatch](https://hatch.pypa.io/latest/) for your
  build system and for version handling.
  - If previously providing `version_info` like `version_info = (1, 7, 0, '.dev', '0')`, use a pattern like the one below in your version file:

```toml
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

- If you need to keep node and python versions in sync, use [hatch-nodejs-version](https://github.com/agoose77/hatch-nodejs-version). See [nbformat](https://github.com/jupyter/nbformat/blob/main/pyproject.toml) for example.

- [ ] Add a GitHub Actions CI step to run the `check_release` action. For example:

```yaml
- name: Check Release
  uses: jupyter-server/jupyter_releaser/.github/actions/check-release@v2
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
```

- This should be run on `push` and `pull` request events. You can copy
  the `check-release.yml` from this repo as an example.

- [ ] If you would like the release assets to be uploaded as artifacts, add the following step after the `check_release` action:

```yaml
- name: Upload Distributions
  uses: actions/upload-artifact@v2
  with:
    name: jupyter-releaser-dist-${{ github.run_number }}
    path: .jupyter_releaser_checkout/dist
```

- [ ] Add a workflow that uses the [`enforce-label`](https://github.com/jupyterlab/maintainer-tools#enforce-labels) action from `jupyterlab/maintainer-tools` to ensure that all PRs have on of the triage labels used to
  categorize the changelog.

- [ ] Update or add `RELEASE.md` that describes the onboarding and release process, e.g. [jupyter_server](https://github.com/jupyter-server/jupyter_server/blob/main/RELEASE.md).

## Release Workflow

- [ ] Set up a fork of `jupyter-releaser` if you have not yet done so.
- [ ] Run through the release process, targeting this repo and the appropriate branch
- [ ] Optionally add configuration to the target repository if non-standard options or hooks are needed.
- [ ] If desired, add `check_release` job, changelog, and `tbump` support to other active release branches
- [ ] Try out the `Draft Changelog` and `Draft Release` process against a fork of the target repo first so you don't accidentally push tags and GitHub releases to the source repository.
- [ ] Try the `Publish Release` process using a prerelease version before publishing a final version.

## Backport Branches

- Create backport branches the usual way, e.g. `git checkout -b 3.0.x v3.0.1; git push origin 3.0.x`
- When running the `Publish Release` Workflow, an automatic PR is generated for the default branch
  in the target repo, positioned in the appropriate place in the changelog.
