# Release Process

- Run through the "Draft Changelog", "Draft Release", and "Publish Release" workflows
- Update the tag for GitHub Actions consumers, e.g.

```bash
git fetch origin main
git checkout main
git tag -f v1
git push -f origin --tags
```
