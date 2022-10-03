set -eux

# Update the v1 tag for GitHub Actions consumers
if [[ ${RH_DRY_RUN:=true} != 'true' ]]; then
    git tag -f -a v2 -m "Github Action release"
    git push origin -f --tags
fi
