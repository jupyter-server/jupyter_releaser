# FAQ

## How to resume a failed release?

If the workflow failed to publish the release, for example because PyPI or npm was down during the release process, we can try to re-run the failed "Publish Release" workflow.

If the draft GitHub release was correctly created, re-run the workflow this time specifying `populate-release` as a step to skip. That way the assets already attached to the draft GitHub Release and the associated release commit will not be recreated, and the workflow will skip to the "Finalize Release" step directly.

## Failed to publish a package to `npm`

The releaser may fail to publish a package to the `npm` in the following cases:

- `npmjs.com` is down, or `npm` is encountering issues publishing new packages
- the account publishing the package to npm is not part of the list of collaborators
- the package you are trying to publish does not contain the correct publish config. If the package is meant to be public, add the following to `package.json`:

```json
"publishConfig": {
  "access": "public"
},
```

## `check-python` step fails with Python monorepos

If you develop multiple Python packages within the same repository (as a monorepo), and the Python packages depend on each other, for example:

```
packages
├── bar
└── foo
```

And `bar` depends on `foo`, for example with `foo>=1.0.0`. You may see the following error during the `check-python` step:

```
ERROR: Could not find a version that satisfies the requirement foo>=1.0.0 (from bar) (from versions: 1.0.0b4, 1.0.0b5, 1.0.0b6, 1.0.0b8)
ERROR: No matching distribution found for foo>=1.0.0
```

This issue is not fixed yet and is being tracked in [this issue](https://github.com/jupyter-server/jupyter_releaser/issues/499).

As a workaround, you can skip the `check-python` step with the following releaser config:

```toml
[tool.jupyter-releaser]
skip = ["check-python"]
```

## How to only publish to `npm`?

If you would like to use the Jupyter Releaser to publish to `npm` only, you can configure the releaser to skip the `build-python` step:

```toml
[tool.jupyter-releaser]
skip = ["build-python"]
```

## My changelog is out of sync

Create a new manual PR to fix the PR and re-orient the changelog entry markers.

## PR is merged to the target branch in the middle of a "Draft Release"

The release will fail to push commits because it will not be up to date. Delete the pushed tags and re-start with "Draft Changelog" to
pick up the new PR.

## What happens if one of my steps is failing but I want to force a release?

This could happen for example if you need to override PRs to include in the changelog. In that case you would pass "check-changelog" to the
workflow's "steps_to_skip" input option.
