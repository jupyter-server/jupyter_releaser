# FAQ

## My changelog is out of sync

Create a new manual PR to fix the PR and re-orient the changelog entry markers.

## PR is merged to the target branch in the middle of a "Draft Release"

The release will fail to push commits because it will not be up to date. Delete the pushed tags and re-start with "Draft Changelog" to
pick up the new PR.

## What happens if one of my steps is failing but I want to force a release?

This could happen for example if you need to override PRs to include in the changelog. In that case you would pass "check-changlog" to the
workflow's "steps_to_skip" input option.
