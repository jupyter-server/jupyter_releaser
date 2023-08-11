set -eux

# Update the stable tag for GitHub Actions consumers
if [[ ${RH_DRY_RUN:=true} != 'true' ]]; then
    git tag -f -a v3 -m "Github Action release"
    git push origin -f --tags
fi
