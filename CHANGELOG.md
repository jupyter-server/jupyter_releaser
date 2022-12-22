# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

## 1.1.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...2072877a9b442a4d3e13bcfde69f11eeee5de237))

### Enhancements made

- Add since_last_stable support in generate changelog [#482](https://github.com/jupyter-server/jupyter_releaser/pull/482) ([@blink1073](https://github.com/blink1073))
- Add more default python dist checks [#481](https://github.com/jupyter-server/jupyter_releaser/pull/481) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- ci cleanup [#478](https://github.com/jupyter-server/jupyter_releaser/pull/478) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Fix typo(?) 2 [#477](https://github.com/jupyter-server/jupyter_releaser/pull/477) ([@krassowski](https://github.com/krassowski))
- Fix typo 1 [#476](https://github.com/jupyter-server/jupyter_releaser/pull/476) ([@krassowski](https://github.com/krassowski))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-12-12&to=2022-12-22&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-12-12..2022-12-22&type=Issues) | [@codecov](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov+updated%3A2022-12-12..2022-12-22&type=Issues) | [@krassowski](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Akrassowski+updated%3A2022-12-12..2022-12-22&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 1.0.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...1638a079ee146dcae0ac2be755fa287d9cb70464))

### Bugs fixed

- Fix handling of dev mode [#473](https://github.com/jupyter-server/jupyter_releaser/pull/473) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Add log when loading configuration [#475](https://github.com/jupyter-server/jupyter_releaser/pull/475) ([@fcollonval](https://github.com/fcollonval))
- Adopt ruff and address lint [#471](https://github.com/jupyter-server/jupyter_releaser/pull/471) ([@blink1073](https://github.com/blink1073))
- Bump actions/upload-artifact from 2 to 3 [#469](https://github.com/jupyter-server/jupyter_releaser/pull/469) ([@dependabot](https://github.com/dependabot))
- Add dependabot config [#468](https://github.com/jupyter-server/jupyter_releaser/pull/468) ([@blink1073](https://github.com/blink1073))
- Update to `actions/checkout@v3` [#467](https://github.com/jupyter-server/jupyter_releaser/pull/467) ([@jtpio](https://github.com/jtpio))
- Use base setup dependency type [#465](https://github.com/jupyter-server/jupyter_releaser/pull/465) ([@blink1073](https://github.com/blink1073))
- CI Cleanup [#463](https://github.com/jupyter-server/jupyter_releaser/pull/463) ([@blink1073](https://github.com/blink1073))
- CI Cleanup [#462](https://github.com/jupyter-server/jupyter_releaser/pull/462) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-11-07&to=2022-12-12&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-11-07..2022-12-12&type=Issues) | [@codecov](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov+updated%3A2022-11-07..2022-12-12&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adependabot+updated%3A2022-11-07..2022-12-12&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2022-11-07..2022-12-12&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2022-11-07..2022-12-12&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Apre-commit-ci+updated%3A2022-11-07..2022-12-12&type=Issues)

## 1.0.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.9.8...87903196bc2951c87f59882cac32c55579ea37f1))

### Enhancements made

- Simplify security handling [#434](https://github.com/jupyter-server/jupyter_releaser/pull/434) ([@blink1073](https://github.com/blink1073))
- Handle Git Actor and Permissions [#429](https://github.com/jupyter-server/jupyter_releaser/pull/429) ([@blink1073](https://github.com/blink1073))
- Better handling of git actor [#424](https://github.com/jupyter-server/jupyter_releaser/pull/424) ([@blink1073](https://github.com/blink1073))
- Use "hatchling version" as a version command where applicable [#374](https://github.com/jupyter-server/jupyter_releaser/pull/374) ([@blink1073](https://github.com/blink1073))
- Refactor and Simplify Workflows [#363](https://github.com/jupyter-server/jupyter_releaser/pull/363) ([@blink1073](https://github.com/blink1073))
- Highlight next step using GitHub step summary [#357](https://github.com/jupyter-server/jupyter_releaser/pull/357) ([@fcollonval](https://github.com/fcollonval))
- Use bare git for dry run [#356](https://github.com/jupyter-server/jupyter_releaser/pull/356) ([@blink1073](https://github.com/blink1073))
- Use mock github when in dry run mode [#355](https://github.com/jupyter-server/jupyter_releaser/pull/355) ([@blink1073](https://github.com/blink1073))
- Add mock github api [#352](https://github.com/jupyter-server/jupyter_releaser/pull/352) ([@blink1073](https://github.com/blink1073))
- Fix pip install in git checkout [#319](https://github.com/jupyter-server/jupyter_releaser/pull/319) ([@blink1073](https://github.com/blink1073))
- Add handling of pydist resource paths [#306](https://github.com/jupyter-server/jupyter_releaser/pull/306) ([@blink1073](https://github.com/blink1073))
- Handle manual backport PRs [#303](https://github.com/jupyter-server/jupyter_releaser/pull/303) ([@blink1073](https://github.com/blink1073))
- Add a utility to get the latest draft release for a given repo [#301](https://github.com/jupyter-server/jupyter_releaser/pull/301) ([@blink1073](https://github.com/blink1073))
- Add ability to parse github release changelog [#298](https://github.com/jupyter-server/jupyter_releaser/pull/298) ([@blink1073](https://github.com/blink1073))
- Use print groups and input types [#288](https://github.com/jupyter-server/jupyter_releaser/pull/288) ([@blink1073](https://github.com/blink1073))
- Improve handling of dev versions [#287](https://github.com/jupyter-server/jupyter_releaser/pull/287) ([@blink1073](https://github.com/blink1073))
- Add support for dynamic versions [#279](https://github.com/jupyter-server/jupyter_releaser/pull/279) ([@blink1073](https://github.com/blink1073))
- Support static version in pyproject.toml [#275](https://github.com/jupyter-server/jupyter_releaser/pull/275) ([@blink1073](https://github.com/blink1073))
- Add documentation label to changelog PR [#259](https://github.com/jupyter-server/jupyter_releaser/pull/259) ([@blink1073](https://github.com/blink1073))
- Make twine check strict by default [#258](https://github.com/jupyter-server/jupyter_releaser/pull/258) ([@blink1073](https://github.com/blink1073))
- Use a more efficient fetch [#257](https://github.com/jupyter-server/jupyter_releaser/pull/257) ([@blink1073](https://github.com/blink1073))
- Add support for minor release [#256](https://github.com/jupyter-server/jupyter_releaser/pull/256) ([@blink1073](https://github.com/blink1073))
- ignore package pytest config [#246](https://github.com/jupyter-server/jupyter_releaser/pull/246) ([@minrk](https://github.com/minrk))
- Add configurable python target to check-python [#238](https://github.com/jupyter-server/jupyter_releaser/pull/238) ([@fcollonval](https://github.com/fcollonval))
- Use the last line of the `python setup.py --version` command to get the Python version [#232](https://github.com/jupyter-server/jupyter_releaser/pull/232) ([@jtpio](https://github.com/jtpio))

### Bugs fixed

- Fix handling of `GITHUB_OUTPUT` [#451](https://github.com/jupyter-server/jupyter_releaser/pull/451) ([@jtpio](https://github.com/jtpio))
- Do no install the package by default [#449](https://github.com/jupyter-server/jupyter_releaser/pull/449) ([@blink1073](https://github.com/blink1073))
- Fix variable name for GitHub output [#444](https://github.com/jupyter-server/jupyter_releaser/pull/444) ([@blink1073](https://github.com/blink1073))
- Allow dev versions [#437](https://github.com/jupyter-server/jupyter_releaser/pull/437) ([@blink1073](https://github.com/blink1073))
- Fix handling of ensure sha [#435](https://github.com/jupyter-server/jupyter_releaser/pull/435) ([@blink1073](https://github.com/blink1073))
- Use admin token [#431](https://github.com/jupyter-server/jupyter_releaser/pull/431) ([@blink1073](https://github.com/blink1073))
- Try fixing admin handling [#430](https://github.com/jupyter-server/jupyter_releaser/pull/430) ([@blink1073](https://github.com/blink1073))
- Fix ensure_sha [#427](https://github.com/jupyter-server/jupyter_releaser/pull/427) ([@blink1073](https://github.com/blink1073))
- Stop erroring on ensure_sha for now [#426](https://github.com/jupyter-server/jupyter_releaser/pull/426) ([@blink1073](https://github.com/blink1073))
- Revert "Better handling of git actor" [#425](https://github.com/jupyter-server/jupyter_releaser/pull/425) ([@blink1073](https://github.com/blink1073))
- Add more debugging to ensure_sha [#422](https://github.com/jupyter-server/jupyter_releaser/pull/422) ([@blink1073](https://github.com/blink1073))
- Another workflow fix [#418](https://github.com/jupyter-server/jupyter_releaser/pull/418) ([@blink1073](https://github.com/blink1073))
- fix default registry again [#409](https://github.com/jupyter-server/jupyter_releaser/pull/409) ([@blink1073](https://github.com/blink1073))
- Fix default twine registry [#407](https://github.com/jupyter-server/jupyter_releaser/pull/407) ([@blink1073](https://github.com/blink1073))
- Fix handling of twine repository url [#403](https://github.com/jupyter-server/jupyter_releaser/pull/403) ([@blink1073](https://github.com/blink1073))
- Fix handling of check manifest [#392](https://github.com/jupyter-server/jupyter_releaser/pull/392) ([@blink1073](https://github.com/blink1073))
- Clean up handling of draft release metadata [#387](https://github.com/jupyter-server/jupyter_releaser/pull/387) ([@blink1073](https://github.com/blink1073))
- Fix handling of fetch_draft_release param [#383](https://github.com/jupyter-server/jupyter_releaser/pull/383) ([@blink1073](https://github.com/blink1073))
- Do not fetch draft release in check_changelog [#381](https://github.com/jupyter-server/jupyter_releaser/pull/381) ([@blink1073](https://github.com/blink1073))
- Fix publish-release [#378](https://github.com/jupyter-server/jupyter_releaser/pull/378) ([@fcollonval](https://github.com/fcollonval))
- Get repository from release url if given [#377](https://github.com/jupyter-server/jupyter_releaser/pull/377) ([@blink1073](https://github.com/blink1073))
- Store ref in metadata file [#375](https://github.com/jupyter-server/jupyter_releaser/pull/375) ([@blink1073](https://github.com/blink1073))
- Fix the input parameter since_last_stable when running a full release [#366](https://github.com/jupyter-server/jupyter_releaser/pull/366) ([@brichet](https://github.com/brichet))
- Revert changes to make changelog pr [#364](https://github.com/jupyter-server/jupyter_releaser/pull/364) ([@blink1073](https://github.com/blink1073))
- Fix changelog pr for dry run [#362](https://github.com/jupyter-server/jupyter_releaser/pull/362) ([@blink1073](https://github.com/blink1073))
- Revert to using stash apply instead of merge [#360](https://github.com/jupyter-server/jupyter_releaser/pull/360) ([@fcollonval](https://github.com/fcollonval))
- Revert changes to handle dev versions [#347](https://github.com/jupyter-server/jupyter_releaser/pull/347) ([@blink1073](https://github.com/blink1073))
- Fix dev version handling in check release [#343](https://github.com/jupyter-server/jupyter_releaser/pull/343) ([@blink1073](https://github.com/blink1073))
- Fix handling of versions when dev versions are used [#341](https://github.com/jupyter-server/jupyter_releaser/pull/341) ([@blink1073](https://github.com/blink1073))
- Fix a bug when retrieving package version [#331](https://github.com/jupyter-server/jupyter_releaser/pull/331) ([@brichet](https://github.com/brichet))
- Add hatchling handling [#329](https://github.com/jupyter-server/jupyter_releaser/pull/329) ([@blink1073](https://github.com/blink1073))
- Check build-system before installing [#322](https://github.com/jupyter-server/jupyter_releaser/pull/322) ([@jtpio](https://github.com/jtpio))
- Fix handling of nested resource files [#308](https://github.com/jupyter-server/jupyter_releaser/pull/308) ([@blink1073](https://github.com/blink1073))
- Only run check-manifest if using setuptools [#302](https://github.com/jupyter-server/jupyter_releaser/pull/302) ([@blink1073](https://github.com/blink1073))
- Use setup.py --version by default [#284](https://github.com/jupyter-server/jupyter_releaser/pull/284) ([@blink1073](https://github.com/blink1073))
- Fix check_links on macOS [#282](https://github.com/jupyter-server/jupyter_releaser/pull/282) ([@blink1073](https://github.com/blink1073))
- Fix listing of tags [#281](https://github.com/jupyter-server/jupyter_releaser/pull/281) ([@jtpio](https://github.com/jtpio))
- Include explicit package data [#270](https://github.com/jupyter-server/jupyter_releaser/pull/270) ([@blink1073](https://github.com/blink1073))
- forward python imports for checking with extract_release [#268](https://github.com/jupyter-server/jupyter_releaser/pull/268) ([@wolfv](https://github.com/wolfv))
- Forwardport changelog before publishing github release [#265](https://github.com/jupyter-server/jupyter_releaser/pull/265) ([@blink1073](https://github.com/blink1073))
- Create forwardport PR after publishing [#262](https://github.com/jupyter-server/jupyter_releaser/pull/262) ([@blink1073](https://github.com/blink1073))
- Select first commit if there is no tags [#261](https://github.com/jupyter-server/jupyter_releaser/pull/261) ([@hbcarlos](https://github.com/hbcarlos))
- Test empty changelog [#243](https://github.com/jupyter-server/jupyter_releaser/pull/243) ([@hbcarlos](https://github.com/hbcarlos))
- Fix handling of doctest skip [#241](https://github.com/jupyter-server/jupyter_releaser/pull/241) ([@blink1073](https://github.com/blink1073))
- Skip doctests when checking links [#239](https://github.com/jupyter-server/jupyter_releaser/pull/239) ([@blink1073](https://github.com/blink1073))
- Add configurable python target to check-python [#238](https://github.com/jupyter-server/jupyter_releaser/pull/238) ([@fcollonval](https://github.com/fcollonval))

### Maintenance and upkeep improvements

- Maintenance cleanup [#457](https://github.com/jupyter-server/jupyter_releaser/pull/457) ([@blink1073](https://github.com/blink1073))
- Remove flake8 file [#447](https://github.com/jupyter-server/jupyter_releaser/pull/447) ([@blink1073](https://github.com/blink1073))
- Improve test speed [#445](https://github.com/jupyter-server/jupyter_releaser/pull/445) ([@blink1073](https://github.com/blink1073))
- Update handling of action outputs [#442](https://github.com/jupyter-server/jupyter_releaser/pull/442) ([@blink1073](https://github.com/blink1073))
- Use hatch envs and clean up workflows [#436](https://github.com/jupyter-server/jupyter_releaser/pull/436) ([@blink1073](https://github.com/blink1073))
- Use global hatch if available [#432](https://github.com/jupyter-server/jupyter_releaser/pull/432) ([@blink1073](https://github.com/blink1073))
- Switch to v2 tag [#419](https://github.com/jupyter-server/jupyter_releaser/pull/419) ([@blink1073](https://github.com/blink1073))
- Fix action targets [#417](https://github.com/jupyter-server/jupyter_releaser/pull/417) ([@blink1073](https://github.com/blink1073))
- Merge v2 into main [#415](https://github.com/jupyter-server/jupyter_releaser/pull/415) ([@blink1073](https://github.com/blink1073))
- Use pipx for cli scripts and hatch for hatch version [#389](https://github.com/jupyter-server/jupyter_releaser/pull/389) ([@blink1073](https://github.com/blink1073))
- More workflow cleanup [#380](https://github.com/jupyter-server/jupyter_releaser/pull/380) ([@blink1073](https://github.com/blink1073))
- Clean up workflows [#379](https://github.com/jupyter-server/jupyter_releaser/pull/379) ([@blink1073](https://github.com/blink1073))
- Fix flake8 v5 compat [#354](https://github.com/jupyter-server/jupyter_releaser/pull/354) ([@blink1073](https://github.com/blink1073))
- Use version template in pyproject [#350](https://github.com/jupyter-server/jupyter_releaser/pull/350) ([@blink1073](https://github.com/blink1073))
- Switch to hatch backend [#323](https://github.com/jupyter-server/jupyter_releaser/pull/323) ([@blink1073](https://github.com/blink1073))
- Remove dead link [#317](https://github.com/jupyter-server/jupyter_releaser/pull/317) ([@blink1073](https://github.com/blink1073))
- Handle license [#315](https://github.com/jupyter-server/jupyter_releaser/pull/315) ([@blink1073](https://github.com/blink1073))
- Allow bot PRs to be auto labeled [#314](https://github.com/jupyter-server/jupyter_releaser/pull/314) ([@blink1073](https://github.com/blink1073))
- Switch to flit [#311](https://github.com/jupyter-server/jupyter_releaser/pull/311) ([@blink1073](https://github.com/blink1073))
- Clean up pytest and add mypy handling [#300](https://github.com/jupyter-server/jupyter_releaser/pull/300) ([@blink1073](https://github.com/blink1073))
- Clean up pre-commit [#295](https://github.com/jupyter-server/jupyter_releaser/pull/295) ([@blink1073](https://github.com/blink1073))
- Update check-links and settings [#292](https://github.com/jupyter-server/jupyter_releaser/pull/292) ([@blink1073](https://github.com/blink1073))
- Clean up check links output [#289](https://github.com/jupyter-server/jupyter_releaser/pull/289) ([@blink1073](https://github.com/blink1073))
- Update to `tbump~=6.7` [#252](https://github.com/jupyter-server/jupyter_releaser/pull/252) ([@jtpio](https://github.com/jtpio))
- Update `setuptools` [#251](https://github.com/jupyter-server/jupyter_releaser/pull/251) ([@jtpio](https://github.com/jtpio))
- Update generate-changelog test [#236](https://github.com/jupyter-server/jupyter_releaser/pull/236) ([@blink1073](https://github.com/blink1073))
- Run CI on Python 3.10 [#234](https://github.com/jupyter-server/jupyter_releaser/pull/234) ([@jtpio](https://github.com/jtpio))
- Update to the new `main` default branch [#233](https://github.com/jupyter-server/jupyter_releaser/pull/233) ([@jtpio](https://github.com/jtpio))

### Documentation improvements

- Add docs for starting making prereleases [#454](https://github.com/jupyter-server/jupyter_releaser/pull/454) ([@martinRenou](https://github.com/martinRenou))
- Update conversion instructions [#450](https://github.com/jupyter-server/jupyter_releaser/pull/450) ([@blink1073](https://github.com/blink1073))
- Update screenshots for Version 2 [#446](https://github.com/jupyter-server/jupyter_releaser/pull/446) ([@blink1073](https://github.com/blink1073))
- Update how-to guides [#443](https://github.com/jupyter-server/jupyter_releaser/pull/443) ([@blink1073](https://github.com/blink1073))
- add step N to actions to make it easier [#324](https://github.com/jupyter-server/jupyter_releaser/pull/324) ([@wolfv](https://github.com/wolfv))
- Fix docs on config values [#291](https://github.com/jupyter-server/jupyter_releaser/pull/291) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-11-23&to=2022-11-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-11-23..2022-11-07&type=Issues) | [@brichet](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Abrichet+updated%3A2021-11-23..2022-11-07&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-11-23..2022-11-07&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adavidbrochart+updated%3A2021-11-23..2022-11-07&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-11-23..2022-11-07&type=Issues) | [@hbcarlos](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ahbcarlos+updated%3A2021-11-23..2022-11-07&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-11-23..2022-11-07&type=Issues) | [@martinRenou](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3AmartinRenou+updated%3A2021-11-23..2022-11-07&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aminrk+updated%3A2021-11-23..2022-11-07&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Apre-commit-ci+updated%3A2021-11-23..2022-11-07&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2021-11-23..2022-11-07&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awolfv+updated%3A2021-11-23..2022-11-07&type=Issues)

## 1.0.0a8

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...dfe1c9f37b303e740feec182df337c208997e2a8))

### Bugs fixed

- Fix handling of `GITHUB_OUTPUT` [#451](https://github.com/jupyter-server/jupyter_releaser/pull/451) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-19&to=2022-10-19&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2022-10-19..2022-10-19&type=Issues)

## 1.0.0a7

No merged PRs

## 1.0.0a6

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...75dbb5c0fe0c5182706c4c39acbaf7570aa171a3))

### Bugs fixed

- Do no install the package by default [#449](https://github.com/jupyter-server/jupyter_releaser/pull/449) ([@blink1073](https://github.com/blink1073))
- Fix variable name for GitHub output [#444](https://github.com/jupyter-server/jupyter_releaser/pull/444) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Remove flake8 file [#447](https://github.com/jupyter-server/jupyter_releaser/pull/447) ([@blink1073](https://github.com/blink1073))
- Improve test speed [#445](https://github.com/jupyter-server/jupyter_releaser/pull/445) ([@blink1073](https://github.com/blink1073))
- Update handling of action outputs [#442](https://github.com/jupyter-server/jupyter_releaser/pull/442) ([@blink1073](https://github.com/blink1073))
- Use hatch envs and clean up workflows [#436](https://github.com/jupyter-server/jupyter_releaser/pull/436) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Update conversion instructions [#450](https://github.com/jupyter-server/jupyter_releaser/pull/450) ([@blink1073](https://github.com/blink1073))
- Update screenshots for Version 2 [#446](https://github.com/jupyter-server/jupyter_releaser/pull/446) ([@blink1073](https://github.com/blink1073))
- Update how-to guides [#443](https://github.com/jupyter-server/jupyter_releaser/pull/443) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-10&to=2022-10-18&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-10-10..2022-10-18&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-10-10..2022-10-18&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Apre-commit-ci+updated%3A2022-10-10..2022-10-18&type=Issues)

## 1.0.0a4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...dac36eb6a14efaaa582fa9ce11782755b5c37c56))

### Maintenance and upkeep improvements

- Use global hatch if available [#432](https://github.com/jupyter-server/jupyter_releaser/pull/432) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-07&to=2022-10-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-10-07..2022-10-07&type=Issues)

## 1.0.0a3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...9e9e128e9beebae69cc13f096df5116a232aa1b2))

### Enhancements made

- Handle Git Actor and Permissions [#429](https://github.com/jupyter-server/jupyter_releaser/pull/429) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Use admin token [#431](https://github.com/jupyter-server/jupyter_releaser/pull/431) ([@blink1073](https://github.com/blink1073))
- Try fixing admin handling [#430](https://github.com/jupyter-server/jupyter_releaser/pull/430) ([@blink1073](https://github.com/blink1073))
- Fix ensure_sha [#427](https://github.com/jupyter-server/jupyter_releaser/pull/427) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-06&to=2022-10-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-10-06..2022-10-07&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-10-06..2022-10-07&type=Issues)

## 1.0.0a2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...e02f046e3426f3e667e03125beee6f92f0f59798))

### Enhancements made

- Better handling of git actor [#424](https://github.com/jupyter-server/jupyter_releaser/pull/424) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Stop erroring on ensure_sha for now [#426](https://github.com/jupyter-server/jupyter_releaser/pull/426) ([@blink1073](https://github.com/blink1073))
- Revert "Better handling of git actor" [#425](https://github.com/jupyter-server/jupyter_releaser/pull/425) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-05&to=2022-10-06&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-10-05..2022-10-06&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-10-05..2022-10-06&type=Issues)

## 1.0.0a1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v2...2d957e05d510f5a707760141a9b18d63464f80cd))

### Bugs fixed

- Add more debugging to ensure_sha [#422](https://github.com/jupyter-server/jupyter_releaser/pull/422) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Switch to v2 tag [#419](https://github.com/jupyter-server/jupyter_releaser/pull/419) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-10-03&to=2022-10-05&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-10-03..2022-10-05&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Apre-commit-ci+updated%3A2022-10-03..2022-10-05&type=Issues)

## 1.0.0a0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...aa1abbf0f1126aab3130fb0d9427425c85ecd468))

### Bugs fixed

- Another workflow fix [#418](https://github.com/jupyter-server/jupyter_releaser/pull/418) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Fix action targets [#417](https://github.com/jupyter-server/jupyter_releaser/pull/417) ([@blink1073](https://github.com/blink1073))
- Merge v2 into main [#415](https://github.com/jupyter-server/jupyter_releaser/pull/415) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-09-26&to=2022-10-03&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-09-26..2022-10-03&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-09-26..2022-10-03&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Apre-commit-ci+updated%3A2022-09-26..2022-10-03&type=Issues)

## 0.25.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...33996f2b913c752a7c57f8a840ee72a77c4395f9))

### Bugs fixed

- fix default registry again [#409](https://github.com/jupyter-server/jupyter_releaser/pull/409) ([@blink1073](https://github.com/blink1073))
- Fix default twine registry [#407](https://github.com/jupyter-server/jupyter_releaser/pull/407) ([@blink1073](https://github.com/blink1073))
- Fix handling of twine repository url [#403](https://github.com/jupyter-server/jupyter_releaser/pull/403) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-09-20&to=2022-09-26&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-09-20..2022-09-26&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-09-20..2022-09-26&type=Issues)

## 0.24.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0146419f57e6194a6433e76ff1160adfa50105be))

### Bugs fixed

- Fix handling of check manifest [#392](https://github.com/jupyter-server/jupyter_releaser/pull/392) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-09-19&to=2022-09-20&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-09-19..2022-09-20&type=Issues)

## 0.24.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...691989055256400c36ed736433d92c75975f6c14))

### Bugs fixed

- Clean up handling of draft release metadata [#387](https://github.com/jupyter-server/jupyter_releaser/pull/387) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Use pipx for cli scripts and hatch for hatch version [#389](https://github.com/jupyter-server/jupyter_releaser/pull/389) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-09-15&to=2022-09-19&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-09-15..2022-09-19&type=Issues)

## 0.24.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...24b290556edbd5bbae9ea05a7e6149b8da290fd7))

### Bugs fixed

- Fix handling of fetch_draft_release param [#383](https://github.com/jupyter-server/jupyter_releaser/pull/383) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-09-15&to=2022-09-15&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-09-15..2022-09-15&type=Issues)

## 0.24.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...e602314062f8e04ca5f94f375e34c3025effcb98))

### Enhancements made

- Use "hatchling version" as a version command where applicable [#374](https://github.com/jupyter-server/jupyter_releaser/pull/374) ([@blink1073](https://github.com/blink1073))
- Refactor and Simplify Workflows [#363](https://github.com/jupyter-server/jupyter_releaser/pull/363) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Do not fetch draft release in check_changelog [#381](https://github.com/jupyter-server/jupyter_releaser/pull/381) ([@blink1073](https://github.com/blink1073))
- Fix publish-release [#378](https://github.com/jupyter-server/jupyter_releaser/pull/378) ([@fcollonval](https://github.com/fcollonval))
- Get repository from release url if given [#377](https://github.com/jupyter-server/jupyter_releaser/pull/377) ([@blink1073](https://github.com/blink1073))
- Store ref in metadata file [#375](https://github.com/jupyter-server/jupyter_releaser/pull/375) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- More workflow cleanup [#380](https://github.com/jupyter-server/jupyter_releaser/pull/380) ([@blink1073](https://github.com/blink1073))
- Clean up workflows [#379](https://github.com/jupyter-server/jupyter_releaser/pull/379) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-08-22&to=2022-09-15&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-08-22..2022-09-15&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-08-22..2022-09-15&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adavidbrochart+updated%3A2022-08-22..2022-09-15&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2022-08-22..2022-09-15&type=Issues)

## 0.23.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6c449c7e998c61789915ffbdf11990109c1d6f4b))

### Bugs fixed

- Fix the input parameter since_last_stable when running a full release [#366](https://github.com/jupyter-server/jupyter_releaser/pull/366) ([@brichet](https://github.com/brichet))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-08-11&to=2022-08-22&type=c))

[@brichet](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Abrichet+updated%3A2022-08-11..2022-08-22&type=Issues)

## 0.23.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...b193f224481f680bb0e9347ff0e5a3c0ca64f57d))

### Bugs fixed

- Revert changes to make changelog pr [#364](https://github.com/jupyter-server/jupyter_releaser/pull/364) ([@blink1073](https://github.com/blink1073))
- Fix changelog pr for dry run [#362](https://github.com/jupyter-server/jupyter_releaser/pull/362) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-08-10&to=2022-08-11&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-08-10..2022-08-11&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-08-10..2022-08-11&type=Issues)

## 0.23.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...87b32ed3dd7448bd2dd915a8babd65eb2749f017))

### Bugs fixed

- Revert to using stash apply instead of merge [#360](https://github.com/jupyter-server/jupyter_releaser/pull/360) ([@fcollonval](https://github.com/fcollonval))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-08-09&to=2022-08-10&type=c))

[@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2022-08-09..2022-08-10&type=Issues)

## 0.23.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1c4a1e67902b050d3af47510bfb53d697d78d3da))

### Enhancements made

- Highlight next step using GitHub step summary [#357](https://github.com/jupyter-server/jupyter_releaser/pull/357) ([@fcollonval](https://github.com/fcollonval))
- Use bare git for dry run [#356](https://github.com/jupyter-server/jupyter_releaser/pull/356) ([@blink1073](https://github.com/blink1073))
- Use mock github when in dry run mode [#355](https://github.com/jupyter-server/jupyter_releaser/pull/355) ([@blink1073](https://github.com/blink1073))
- Add mock github api [#352](https://github.com/jupyter-server/jupyter_releaser/pull/352) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Fix flake8 v5 compat [#354](https://github.com/jupyter-server/jupyter_releaser/pull/354) ([@blink1073](https://github.com/blink1073))
- Use version template in pyproject [#350](https://github.com/jupyter-server/jupyter_releaser/pull/350) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-07-11&to=2022-08-08&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-07-11..2022-08-08&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-07-11..2022-08-08&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2022-07-11..2022-08-08&type=Issues)

## 0.22.5

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...915239416cf90ef93e136553bc87aa38e5f31a96))

### Bugs fixed

- Revert changes to handle dev versions [#347](https://github.com/jupyter-server/jupyter_releaser/pull/347) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-07-08&to=2022-07-11&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-07-08..2022-07-11&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-07-08..2022-07-11&type=Issues)

## 0.22.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...a441599cef4e832cfc841d5d75b50a25263a2fec))

### Bugs fixed

- Fix dev version handling in check release [#343](https://github.com/jupyter-server/jupyter_releaser/pull/343) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-07-07&to=2022-07-08&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-07-07..2022-07-08&type=Issues)

## 0.22.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...face9d62bd6dbab7599b7b2463f198afcbe4b9ac))

### Bugs fixed

- Fix handling of versions when dev versions are used [#341](https://github.com/jupyter-server/jupyter_releaser/pull/341) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-06-14&to=2022-07-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-06-14..2022-07-07&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-06-14..2022-07-07&type=Issues)

## 0.22.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0f61e78511ea099b4b00d271807a021cbec05162))

### Bugs fixed

- Fix a bug when retrieving package version [#331](https://github.com/jupyter-server/jupyter_releaser/pull/331) ([@brichet](https://github.com/brichet))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-06-14&to=2022-06-14&type=c))

[@brichet](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Abrichet+updated%3A2022-06-14..2022-06-14&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2022-06-14..2022-06-14&type=Issues)

## 0.22.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...ecb30ecadc10241b74b87eea5448d8773019fa4a))

### Bugs fixed

- Add hatchling handling [#329](https://github.com/jupyter-server/jupyter_releaser/pull/329) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-05-19&to=2022-06-14&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-05-19..2022-06-14&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-05-19..2022-06-14&type=Issues)

## 0.22.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...21a39f512d8f8333d637532ab6d4fec5dff47e22))

### Bugs fixed

- Check build-system before installing [#322](https://github.com/jupyter-server/jupyter_releaser/pull/322) ([@jtpio](https://github.com/jtpio))

### Maintenance and upkeep improvements

- Switch to hatch backend [#323](https://github.com/jupyter-server/jupyter_releaser/pull/323) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- add step N to actions to make it easier [#324](https://github.com/jupyter-server/jupyter_releaser/pull/324) ([@wolfv](https://github.com/wolfv))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-05-18&to=2022-05-19&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-05-18..2022-05-19&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2022-05-18..2022-05-19&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awolfv+updated%3A2022-05-18..2022-05-19&type=Issues)

## 0.21.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...ede808f57e73bfec22a796ee2bb86c7f25e5e709))

### Enhancements made

- Fix pip install in git checkout [#319](https://github.com/jupyter-server/jupyter_releaser/pull/319) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Remove dead link [#317](https://github.com/jupyter-server/jupyter_releaser/pull/317) ([@blink1073](https://github.com/blink1073))
- Handle license [#315](https://github.com/jupyter-server/jupyter_releaser/pull/315) ([@blink1073](https://github.com/blink1073))
- Allow bot PRs to be auto labeled [#314](https://github.com/jupyter-server/jupyter_releaser/pull/314) ([@blink1073](https://github.com/blink1073))
- Switch to flit [#311](https://github.com/jupyter-server/jupyter_releaser/pull/311) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-05-02&to=2022-05-18&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-05-02..2022-05-18&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-05-02..2022-05-18&type=Issues)

## 0.20.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...d847dd94a7e1bb70f036ac46fa6145197ee0b0cb))

### Bugs fixed

- Fix handling of nested resource files [#308](https://github.com/jupyter-server/jupyter_releaser/pull/308) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-25&to=2022-05-02&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-25..2022-05-02&type=Issues)

## 0.19.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...bb94f113285986ed4a97150dd0507f7a2e38e897))

### Enhancements made

- Add handling of pydist resource paths [#306](https://github.com/jupyter-server/jupyter_releaser/pull/306) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-18&to=2022-04-25&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-18..2022-04-25&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-04-18..2022-04-25&type=Issues)

## 0.18.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1b5a66584078f85fa0e72c6c111563bd5cde7b0b))

### Enhancements made

- Handle manual backport PRs [#303](https://github.com/jupyter-server/jupyter_releaser/pull/303) ([@blink1073](https://github.com/blink1073))
- Add a utility to get the latest draft release for a given repo [#301](https://github.com/jupyter-server/jupyter_releaser/pull/301) ([@blink1073](https://github.com/blink1073))
- Add ability to parse github release changelog [#298](https://github.com/jupyter-server/jupyter_releaser/pull/298) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Only run check-manifest if using setuptools [#302](https://github.com/jupyter-server/jupyter_releaser/pull/302) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Clean up pytest and add mypy handling [#300](https://github.com/jupyter-server/jupyter_releaser/pull/300) ([@blink1073](https://github.com/blink1073))
- Clean up pre-commit [#295](https://github.com/jupyter-server/jupyter_releaser/pull/295) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-07&to=2022-04-18&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-07..2022-04-18&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-04-07..2022-04-18&type=Issues)

## 0.17.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...749241d219b73e22eea1702dfb7e615b897abc3e))

### Maintenance and upkeep improvements

- Update check-links and settings [#292](https://github.com/jupyter-server/jupyter_releaser/pull/292) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Fix docs on config values [#291](https://github.com/jupyter-server/jupyter_releaser/pull/291) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-06&to=2022-04-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-06..2022-04-07&type=Issues)

## 0.16.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...db5ba0757cf504c6258ca71e02fe5e6e026084c0))

### Enhancements made

- Use print groups and input types [#288](https://github.com/jupyter-server/jupyter_releaser/pull/288) ([@blink1073](https://github.com/blink1073))
- Improve handling of dev versions [#287](https://github.com/jupyter-server/jupyter_releaser/pull/287) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Clean up check links output [#289](https://github.com/jupyter-server/jupyter_releaser/pull/289) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-04&to=2022-04-06&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-04..2022-04-06&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-04-04..2022-04-06&type=Issues)

## 0.15.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...e60175aa7ca19838cf3326703ab72589890d1e79))

### Bugs fixed

- Use setup.py --version by default [#284](https://github.com/jupyter-server/jupyter_releaser/pull/284) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-04-01&to=2022-04-04&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-04-01..2022-04-04&type=Issues)

## 0.15.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...b5c58b89dbc3e981ffbc1dab88f6bfb128c492a4))

### Enhancements made

- Add support for dynamic versions [#279](https://github.com/jupyter-server/jupyter_releaser/pull/279) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Fix check_links on macOS [#282](https://github.com/jupyter-server/jupyter_releaser/pull/282) ([@blink1073](https://github.com/blink1073))
- Fix listing of tags [#281](https://github.com/jupyter-server/jupyter_releaser/pull/281) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-03-31&to=2022-04-01&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-03-31..2022-04-01&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2022-03-31..2022-04-01&type=Issues)

## 0.14.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...7d4dc94377caada8a71ae08b147228677df42316))

### Enhancements made

- Support static version in pyproject.toml [#275](https://github.com/jupyter-server/jupyter_releaser/pull/275) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-03-25&to=2022-03-31&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-03-25..2022-03-31&type=Issues)

## 0.13.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...2a10db69739f622eb605068d5771e86027318657))

### Bugs fixed

- Include explicit package data [#270](https://github.com/jupyter-server/jupyter_releaser/pull/270) ([@blink1073](https://github.com/blink1073))
- forward python imports for checking with extract_release [#268](https://github.com/jupyter-server/jupyter_releaser/pull/268) ([@wolfv](https://github.com/wolfv))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-03-11&to=2022-03-25&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-03-11..2022-03-25&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-03-11..2022-03-25&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2022-03-11..2022-03-25&type=Issues) | [@wolfv](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awolfv+updated%3A2022-03-11..2022-03-25&type=Issues)

## 0.13.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...9aaad0bd2bb91dfd3f8085bae7fcd4fa5d17f832))

### Bugs fixed

- Forwardport changelog before publishing github release [#265](https://github.com/jupyter-server/jupyter_releaser/pull/265) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-03-10&to=2022-03-11&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-03-10..2022-03-11&type=Issues)

## 0.13.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...7daf1cebb31c640c6ccf03dd43bdcbd251fc61d0))

### Bugs fixed

- Create forwardport PR after publishing [#262](https://github.com/jupyter-server/jupyter_releaser/pull/262) ([@blink1073](https://github.com/blink1073))
- Select first commit if there is no tags [#261](https://github.com/jupyter-server/jupyter_releaser/pull/261) ([@hbcarlos](https://github.com/hbcarlos))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-02-14&to=2022-03-10&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-02-14..2022-03-10&type=Issues) | [@hbcarlos](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ahbcarlos+updated%3A2022-02-14..2022-03-10&type=Issues)

## 0.13.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...3fbe0cfe40667da0cdeafab2bee7d3597fd2a436))

### Enhancements made

- Add documentation label to changelog PR [#259](https://github.com/jupyter-server/jupyter_releaser/pull/259) ([@blink1073](https://github.com/blink1073))
- Make twine check strict by default [#258](https://github.com/jupyter-server/jupyter_releaser/pull/258) ([@blink1073](https://github.com/blink1073))
- Use a more efficient fetch [#257](https://github.com/jupyter-server/jupyter_releaser/pull/257) ([@blink1073](https://github.com/blink1073))
- Add support for minor release [#256](https://github.com/jupyter-server/jupyter_releaser/pull/256) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-27&to=2022-02-14&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-01-27..2022-02-14&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-01-27..2022-02-14&type=Issues)

## 0.12.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...8c97f42f9857fbfbe63ced2f37bc1a6776f82dcb))

### Maintenance and upkeep improvements

- Update to `tbump~=6.7` [#252](https://github.com/jupyter-server/jupyter_releaser/pull/252) ([@jtpio](https://github.com/jtpio))
- Update `setuptools` [#251](https://github.com/jupyter-server/jupyter_releaser/pull/251) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-21&to=2022-01-27&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-01-21..2022-01-27&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-01-21..2022-01-27&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2022-01-21..2022-01-27&type=Issues)

## 0.11.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...d84497abaab91bcfa8810c295fdba89881bc1e1e))

### Enhancements made

- ignore package pytest config [#246](https://github.com/jupyter-server/jupyter_releaser/pull/246) ([@minrk](https://github.com/minrk))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-19&to=2022-01-21&type=c))

[@minrk](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aminrk+updated%3A2022-01-19..2022-01-21&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2022-01-19..2022-01-21&type=Issues)

## 0.11.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...455050d2193cd026136f034b9220c788e94b725d))

### Bugs fixed

- Test empty changelog [#243](https://github.com/jupyter-server/jupyter_releaser/pull/243) ([@hbcarlos](https://github.com/hbcarlos))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-17&to=2022-01-19&type=c))

[@hbcarlos](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ahbcarlos+updated%3A2022-01-17..2022-01-19&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2022-01-17..2022-01-19&type=Issues)

## 0.11.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...fe2a3ab5ede03d3aac6d894807c82efb07171369))

### Bugs fixed

- Fix handling of doctest skip [#241](https://github.com/jupyter-server/jupyter_releaser/pull/241) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-13&to=2022-01-17&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-01-13..2022-01-17&type=Issues)

## 0.11.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...318577cc3d4a7d97717b87c35141e26140ddf236))

### Enhancements made

- Add configurable python target to check-python [#238](https://github.com/jupyter-server/jupyter_releaser/pull/238) ([@fcollonval](https://github.com/fcollonval))

### Bugs fixed

- Skip doctests when checking links [#239](https://github.com/jupyter-server/jupyter_releaser/pull/239) ([@blink1073](https://github.com/blink1073))
- Add configurable python target to check-python [#238](https://github.com/jupyter-server/jupyter_releaser/pull/238) ([@fcollonval](https://github.com/fcollonval))

### Maintenance and upkeep improvements

- Update generate-changelog test [#236](https://github.com/jupyter-server/jupyter_releaser/pull/236) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2022-01-02&to=2022-01-13&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2022-01-02..2022-01-13&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2022-01-02..2022-01-13&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2022-01-02..2022-01-13&type=Issues)

## 0.10.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...233f676c93ffddcbef3f651cb9e8a49f4254c25d))

### Bugs fixed

- Fix handling of empty documentation header [#230](https://github.com/jupyter-server/jupyter_releaser/pull/230) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-12-14&to=2021-12-15&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-12-14..2021-12-15&type=Issues)

## 0.10.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...ed027eafed881cfb013aade9e4dc4b296ca837ba))

### Bugs fixed

- Fix handling of dev version in version bump [#228](https://github.com/jupyter-server/jupyter_releaser/pull/228) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-12-13&to=2021-12-14&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-12-13..2021-12-14&type=Issues)

## 0.10.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1c4b528e27af0b594807f6ee0b27e190d25a4936))

### Enhancements made

- Make branch and version spec optional [#223](https://github.com/jupyter-server/jupyter_releaser/pull/223) ([@blink1073](https://github.com/blink1073))
- Add 'next' convenience for tbump [#221](https://github.com/jupyter-server/jupyter_releaser/pull/221) ([@blink1073](https://github.com/blink1073))
- Sort the list of workspace package versions [#218](https://github.com/jupyter-server/jupyter_releaser/pull/218) ([@jtpio](https://github.com/jtpio))
- Improve Python multi-package handling [#216](https://github.com/jupyter-server/jupyter_releaser/pull/216) ([@davidbrochart](https://github.com/davidbrochart))
- Remove empty documentation entry [#211](https://github.com/jupyter-server/jupyter_releaser/pull/211) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Fix default branch handling and update UX [#224](https://github.com/jupyter-server/jupyter_releaser/pull/224) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Fix missing quote in Draft Changelog [#217](https://github.com/jupyter-server/jupyter_releaser/pull/217) ([@jtpio](https://github.com/jtpio))

- Cleanup Docs and Base Setup Action [#214](https://github.com/jupyter-server/jupyter_releaser/pull/214) ([@blink1073](https://github.com/blink1073))

- Beautify rendering of the configuration file list [#220](https://github.com/jupyter-server/jupyter_releaser/pull/220) ([@krassowski](https://github.com/krassowski))

- Fix a typo (missing `=`) [#219](https://github.com/jupyter-server/jupyter_releaser/pull/219) ([@krassowski](https://github.com/krassowski))

- Cleanup Docs and Base Setup Action [#214](https://github.com/jupyter-server/jupyter_releaser/pull/214) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-11-23&to=2021-12-13&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-11-23..2021-12-13&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-11-23..2021-12-13&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adavidbrochart+updated%3A2021-11-23..2021-12-13&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-11-23..2021-12-13&type=Issues) | [@krassowski](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Akrassowski+updated%3A2021-11-23..2021-12-13&type=Issues)

## 0.9.8

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1bc9790061ba61de52ee3dba5c55a5bffc34a682))

### Bugs fixed

- Fix multi python package publishing [#201](https://github.com/jupyter-server/jupyter_releaser/pull/201) ([@davidbrochart](https://github.com/davidbrochart))

### Maintenance and upkeep improvements

- Enforce labels on PRs [#209](https://github.com/jupyter-server/jupyter_releaser/pull/209) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-11-17&to=2021-11-23&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-11-17..2021-11-23&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adavidbrochart+updated%3A2021-11-17..2021-11-23&type=Issues)

## 0.9.7

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6f2947e69a2532979b1834276a9da1e7ebda6afc))

### Enhancements made

- Allow publish with no assets [#207](https://github.com/jupyter-server/jupyter_releaser/pull/207) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-11-17&to=2021-11-17&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-11-17..2021-11-17&type=Issues)

## 0.9.6

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0fbfbdf2bd2c52763d82b45c5cf863b78ee6093d))

### Enhancements made

- Allow for a single private package [#205](https://github.com/jupyter-server/jupyter_releaser/pull/205) ([@blink1073](https://github.com/blink1073))

### Maintenance

- Fix PR formatting [#198](https://github.com/jupyter-server/jupyter_releaser/pull/198) ([@krassowski](https://github.com/krassowski))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-22&to=2021-11-17&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-22..2021-11-17&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-10-22..2021-11-17&type=Issues) | [@krassowski](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Akrassowski+updated%3A2021-10-22..2021-11-17&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2021-10-22..2021-11-17&type=Issues)

## 0.9.5

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...95b14a79f2f59b0c31e2230a3b407c674007cacb))

### Bugs fixed

- Remove default branch logic [#195](https://github.com/jupyter-server/jupyter_releaser/pull/195) ([@jtpio](https://github.com/jtpio))

### Maintenance and upkeep improvements

- Clean up actions and workflows [#194](https://github.com/jupyter-server/jupyter_releaser/pull/194) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-21&to=2021-10-22&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-21..2021-10-22&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-10-21..2021-10-22&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-10-21..2021-10-22&type=Issues)

## 0.9.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6daa3cc0f156ac390e17fe9a5b03395226022149))

### Bugs fixed

- Skip branch setup on publish [#192](https://github.com/jupyter-server/jupyter_releaser/pull/192) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-20&to=2021-10-21&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-10-20..2021-10-21&type=Issues)

## 0.9.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...25c6e9b61ea383e086e6ff25f4d73b8cbeb26d0d))

### Bugs fixed

- Pass `version_spec` in check-release [#190](https://github.com/jupyter-server/jupyter_releaser/pull/190) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-20&to=2021-10-20&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-10-20..2021-10-20&type=Issues)

## 0.9.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...dd219deac5b308dc68e36e1661921771237b03c1))

### Bugs fixed

- Make all of the actions use v1 tag internally [#187](https://github.com/jupyter-server/jupyter_releaser/pull/187) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Clarify scopes needed for admin token [#186](https://github.com/jupyter-server/jupyter_releaser/pull/186) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-19&to=2021-10-20&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-19..2021-10-20&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-10-19..2021-10-20&type=Issues)

## 0.9.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6a7cb67964d7ae5f881389081fbddca98cc2bdca))

### Bugs fixed

- Fix Check Release and Check Links Actions [#184](https://github.com/jupyter-server/jupyter_releaser/pull/184) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-19&to=2021-10-19&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-19..2021-10-19&type=Issues)

## 0.9.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6cd54f1097a01ac69d9c0212a1a37828950c8895))

### Maintenance and upkeep improvements

- Refactor CI [#182](https://github.com/jupyter-server/jupyter_releaser/pull/182) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-14&to=2021-10-19&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-14..2021-10-19&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-10-14..2021-10-19&type=Issues)

## 0.8.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...391fbc44a68747280ab323958f2fd57ba76cc37c))

### Enhancements made

- Add ability to skip steps [#180](https://github.com/jupyter-server/jupyter_releaser/pull/180) ([@blink1073](https://github.com/blink1073))
- Handle multiple Python packages [#176](https://github.com/jupyter-server/jupyter_releaser/pull/176) ([@davidbrochart](https://github.com/davidbrochart))

### Bugs fixed

- Fix escaping of the changelog comment [#179](https://github.com/jupyter-server/jupyter_releaser/pull/179) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-10-07&to=2021-10-14&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-10-07..2021-10-14&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-10-07..2021-10-14&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Adavidbrochart+updated%3A2021-10-07..2021-10-14&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-10-07..2021-10-14&type=Issues)

## 0.7.6

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0c3494dde2690badcf44a437e93ed2da45f4dfb3))

### Bugs fixed

- Escape the npm version string in PR text [#177](https://github.com/jupyter-server/jupyter_releaser/pull/177) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-30&to=2021-10-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-09-30..2021-10-07&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-09-30..2021-10-07&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-30..2021-10-07&type=Issues)

## 0.7.5

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...7edf4b97fb2ca2105192a599cbf7155f9c6fa58c))

### Bugs fixed

- Debug token map handling [#173](https://github.com/jupyter-server/jupyter_releaser/pull/173) ([@blink1073](https://github.com/blink1073))

### Documentation improvements

- Add generated docs and logos [#172](https://github.com/jupyter-server/jupyter_releaser/pull/172) ([@blink1073](https://github.com/blink1073))
- Reorganize docs [#171](https://github.com/jupyter-server/jupyter_releaser/pull/171) ([@blink1073](https://github.com/blink1073))
- Add Sphinx Docs [#166](https://github.com/jupyter-server/jupyter_releaser/pull/166) ([@jtpio](https://github.com/jtpio))
- Document uploading release assets as artifacts [#165](https://github.com/jupyter-server/jupyter_releaser/pull/165) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-15&to=2021-09-30&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-09-15..2021-09-30&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-09-15..2021-09-30&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-15..2021-09-30&type=Issues)

## 0.7.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...ccd4eb7cfa280079745730af7c5d7b297f243801))

### Bugs fixed

- Fix Handling of Since Last Stable [#163](https://github.com/jupyter-server/jupyter_releaser/pull/163) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-15&to=2021-09-15&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-15..2021-09-15&type=Issues)

## 0.7.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...98d6e21224c6a39e2e1467e1b4a2bd9d95448cb4))

### Merged PRs

- Cleanup [#161](https://github.com/jupyter-server/jupyter_releaser/pull/161) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-13&to=2021-09-15&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-13..2021-09-15&type=Issues)

## 0.7.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6e91f54d41029666078bdfad0b7e1957d092ca1d))

### Bugs fixed

- Publish Fixes [#159](https://github.com/jupyter-server/jupyter_releaser/pull/159) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-13&to=2021-09-13&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-13..2021-09-13&type=Issues)

## 0.7.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...00b07713e91443b84f5efbf554449b0c6b08e5a6))

### Bugs fixed

- Fix typo in the draft release action [#157](https://github.com/jupyter-server/jupyter_releaser/pull/157) ([@jtpio](https://github.com/jtpio))
- Fix handling of PYPI token map [#155](https://github.com/jupyter-server/jupyter_releaser/pull/155) ([@jtpio](https://github.com/jtpio))

### Documentation improvements

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-13&to=2021-09-13&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-09-13..2021-09-13&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-13..2021-09-13&type=Issues)

## 0.7.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...b8d9eec5e08b99e3ed6afc57366d7a6d9b3bda47))

### Enhancements made

- Move registry options to settings [#152](https://github.com/jupyter-server/jupyter_releaser/pull/152) ([@jtpio](https://github.com/jtpio))
- Enable Auto Publish [#149](https://github.com/jupyter-server/jupyter_releaser/pull/149) ([@jtpio](https://github.com/jtpio))
- Add Since Last Stable Option for Changelog [#147](https://github.com/jupyter-server/jupyter_releaser/pull/147) ([@jtpio](https://github.com/jtpio))
- Add support for PYPI token map [#146](https://github.com/jupyter-server/jupyter_releaser/pull/146) ([@jtpio](https://github.com/jtpio))
- Make tag name configurable [#145](https://github.com/jupyter-server/jupyter_releaser/pull/145) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Simpler Solution for Full Publish [#153](https://github.com/jupyter-server/jupyter_releaser/pull/153) ([@jtpio](https://github.com/jtpio))
- Fix auto publish workflow indent [#151](https://github.com/jupyter-server/jupyter_releaser/pull/151) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-09&to=2021-09-13&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-09-09..2021-09-13&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-09-09..2021-09-13&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-09..2021-09-13&type=Issues)

## 0.6.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0272fbfdf1027fe5519565084167bc07757211a7))

### Bugs fixed

- Read npm versions before `git checkout -- .` [#143](https://github.com/jupyter-server/jupyter_releaser/pull/143) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-08&to=2021-09-09&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-08..2021-09-09&type=Issues)

## 0.6.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...42212a21001fe7ce6fadeb267aeb7b675fd09db0))

### Bugs fixed

- Read the schema on import [#140](https://github.com/jupyter-server/jupyter_releaser/pull/140) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-08&to=2021-09-08&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-08..2021-09-08&type=Issues)

## 0.6.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...26b2c42cf5fc1ec46a9e76a2228cdac2d442b22a))

### Maintenance and upkeep improvements

- Add JSON Schema for Config [#134](https://github.com/jupyter-server/jupyter_releaser/pull/134) ([@fcollonval](https://github.com/fcollonval))
- Quieter Output Again [#132](https://github.com/jupyter-server/jupyter_releaser/pull/132) ([@blink1073](https://github.com/blink1073))
- Remove "Release" from the GitHub Release title [#130](https://github.com/jupyter-server/jupyter_releaser/pull/130) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-09-01&to=2021-09-07&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-09-01..2021-09-07&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-09-01..2021-09-07&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-09-01..2021-09-07&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-09-01..2021-09-07&type=Issues)

## 0.5.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...083fff21bb78ebe8e39d649e54f838557a447ed8))

### Bugs fixed

- Fix Generate Changelog Action [#126](https://github.com/jupyter-server/jupyter_releaser/pull/126) ([@afshin](https://github.com/afshin))

### Maintenance and upkeep improvements

- Clean up NPM Package Handling [#128](https://github.com/jupyter-server/jupyter_releaser/pull/128) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-25&to=2021-09-01&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-25..2021-09-01&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-08-25..2021-09-01&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-08-25..2021-09-01&type=Issues)

## 0.5.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...8d11e4a8b89a9717d88b960768ba3562fdffe133))

### Maintenance and upkeep improvements

- Skip second check changelog during check release action [#124](https://github.com/jupyter-server/jupyter_releaser/pull/124) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-25&to=2021-08-25&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-08-25..2021-08-25&type=Issues)

## 0.5.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...a554583cff280384b701379772770907d08cd8f4))

### Bugs fixed

- Fix Extract Release Config and Npm Config Handling [#122](https://github.com/jupyter-server/jupyter_releaser/pull/122) ([@fcollonval](https://github.com/fcollonval))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-24&to=2021-08-25&type=c))

[@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-08-24..2021-08-25&type=Issues)

## 0.4.7

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...91e63d950ec8accad6066adece1fabb8741d6749))

### Bugs fixed

- Fix usage of since parameter [#120](https://github.com/jupyter-server/jupyter_releaser/pull/120) ([@fcollonval](https://github.com/fcollonval))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-23&to=2021-08-24&type=c))

[@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-08-23..2021-08-24&type=Issues)

## 0.4.6

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...6758413e8cc4c5dc4d68b0c3c758b412735cd753))

### Enhancements made

- Allow to set commit message [#115](https://github.com/jupyter-server/jupyter_releaser/pull/115) ([@fcollonval](https://github.com/fcollonval))

### Bugs fixed

- Restore capture of since parameter [#118](https://github.com/jupyter-server/jupyter_releaser/pull/118) ([@fcollonval](https://github.com/fcollonval))
- Cleanup [#116](https://github.com/jupyter-server/jupyter_releaser/pull/116) ([@fcollonval](https://github.com/fcollonval))

### Maintenance and upkeep improvements

- Fix branch name used in CI [#114](https://github.com/jupyter-server/jupyter_releaser/pull/114) ([@afshin](https://github.com/afshin))

### Documentation improvements

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-18&to=2021-08-23&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-18..2021-08-23&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-08-18..2021-08-23&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-08-18..2021-08-23&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-08-18..2021-08-23&type=Issues)

## 0.4.5

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...cb86e29f8b042bf0d16a6c7dcfdd4c6fc267937c))

### Bugs fixed

- Fix Create Changelog Action [#112](https://github.com/jupyter-server/jupyter_releaser/pull/112) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-18&to=2021-08-18&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-18..2021-08-18&type=Issues)

## 0.4.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1d37638e62a2300bab78d39bf33897dfc5af7c81))

### Enhancements made

- Add Generate Changelog Workflow [#106](https://github.com/jupyter-server/jupyter_releaser/pull/106) ([@fcollonval](https://github.com/fcollonval))

### Bugs fixed

- Fix handling of "since" parameter [#110](https://github.com/jupyter-server/jupyter_releaser/pull/110) ([@fcollonval](https://github.com/fcollonval))
- More Cleanup [#107](https://github.com/jupyter-server/jupyter_releaser/pull/107) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- More Cleanup [#108](https://github.com/jupyter-server/jupyter_releaser/pull/108) ([@fcollonval](https://github.com/fcollonval))

### Documentation improvements

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-11&to=2021-08-18&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-08-11..2021-08-18&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-08-11..2021-08-18&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-08-11..2021-08-18&type=Issues)

## 0.4.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...80cf2677aa447988605d3bb84999856ba5ed685d))

### Merged PRs

- Fix Changelog Build [#104](https://github.com/jupyter-server/jupyter_releaser/pull/104) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-11&to=2021-08-11&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-11..2021-08-11&type=Issues)

## 0.4.2

No merged PRs

## 0.4.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...7f94b3cdd8e916d84c7fe8ff1be39b7672dd2334))

### Bugs fixed

- Fix up hook handling [#100](https://github.com/jupyter-server/jupyter_releaser/pull/100) ([@afshin](https://github.com/afshin))

### Maintenance and upkeep improvements

- Clean up build output [#99](https://github.com/jupyter-server/jupyter_releaser/pull/99) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-07&to=2021-08-10&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-07..2021-08-10&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-08-07..2021-08-10&type=Issues)

## 0.4.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...a485f446f1214419f414bede35a24a2bc3e29a5f))

### Enhancements made

- Add an action for check-links [#97](https://github.com/jupyter-server/jupyter_releaser/pull/97) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-08-03&to=2021-08-07&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-08-03..2021-08-07&type=Issues)

## 0.3.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...561823dd8ca448d8eae0e7b7c5b8f8cd784a1908))

### Merged PRs

- More cleanup of tag lock [#95](https://github.com/jupyter-server/jupyter_releaser/pull/95) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-30&to=2021-08-03&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-30..2021-08-03&type=Issues)

## 0.3.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...671445e0f441005b8b4134c80976d3f20ebade31))

### Bugs fixed

- Fix Handling of Tag Lock [#93](https://github.com/jupyter-server/jupyter_releaser/pull/93) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-30&to=2021-07-30&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-30..2021-07-30&type=Issues)

## 0.3.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...ffe52ea6acd21f0e7fac0c1da5a9880c81989c75))

### Maintenance and upkeep improvements

- More Cleanup [#91](https://github.com/jupyter-server/jupyter_releaser/pull/91) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-27&to=2021-07-30&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-07-27..2021-07-30&type=Issues)

## 0.3.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...675950d7756e678961ed63e9ee3194af5bab5d57))

### Bugs fixed

- support structured branch name [#89](https://github.com/jupyter-server/jupyter_releaser/pull/89) ([@fcollonval](https://github.com/fcollonval))

### Maintenance and upkeep improvements

- Update check-release.yml [#88](https://github.com/jupyter-server/jupyter_releaser/pull/88) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-21&to=2021-07-27&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-21..2021-07-27&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-21..2021-07-27&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Afcollonval+updated%3A2021-07-21..2021-07-27&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Awelcome+updated%3A2021-07-21..2021-07-27&type=Issues)

## 0.3.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...3ce39f01e9171098afe19b98b9838f1cc71a64fa))

### Enhancements made

- Add ability to skip steps [#84](https://github.com/jupyter-server/jupyter_releaser/pull/84) ([@blink1073](https://github.com/blink1073))

### Bugs fixed

- Allow after-prep-git to work [#85](https://github.com/jupyter-server/jupyter_releaser/pull/85) ([@blink1073](https://github.com/blink1073))

### Maintenance and upkeep improvements

- Add extra changelog check before push [#86](https://github.com/jupyter-server/jupyter_releaser/pull/86) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-20&to=2021-07-21&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-07-20..2021-07-21&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-20..2021-07-21&type=Issues)

## 0.2.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...bea9fc265b8616eb10ea1b330388507b43ef155c))

### Bugs fixed

- Fix installing the releaser in the check release workflow [#82](https://github.com/jupyter-server/jupyter_releaser/pull/82) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-19&to=2021-07-20&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-19..2021-07-20&type=Issues)

## 0.2.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...02cd1089a0181e783f8e640f5138d34ce8de3d5f))

### Bugs fixed

- Fix handling of error output [#79](https://github.com/jupyter-server/jupyter_releaser/pull/79) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-19&to=2021-07-19&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-19..2021-07-19&type=Issues)

## 0.2.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...5d92c21f03bd5300e11cd89ce1dd044c4bcda12b))

### Enhancements made

- Use Async Output Where Possible [#76](https://github.com/jupyter-server/jupyter_releaser/pull/76) ([@jtpio](https://github.com/jtpio))

### Bugs fixed

- Better Handling of Already Existing Packages [#77](https://github.com/jupyter-server/jupyter_releaser/pull/77) ([@jtpio](https://github.com/jtpio))
- Handle commit message failure [#75](https://github.com/jupyter-server/jupyter_releaser/pull/75) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-16&to=2021-07-19&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-16..2021-07-19&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-16..2021-07-19&type=Issues)

## 0.2.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...b543ce51f0260babc1aa942e0ad643991d413d86))

### Bugs fixed

- Restore guard to pip install if releaser [#73](https://github.com/jupyter-server/jupyter_releaser/pull/73) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-16&to=2021-07-16&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-16..2021-07-16&type=Issues)

## 0.2.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...1d9d22c10864a4ec22465207e46e844a24cc6a7a))

### Bugs fixed

- Add default for `RH_IS_CHECK_RELEASE` [#70](https://github.com/jupyter-server/jupyter_releaser/pull/70) ([@jtpio](https://github.com/jtpio))

### Maintenance and upkeep improvements

- Even more cleanup [#71](https://github.com/jupyter-server/jupyter_releaser/pull/71) ([@blink1073](https://github.com/blink1073))
- Improve Check Release Isolation [#68](https://github.com/jupyter-server/jupyter_releaser/pull/68) ([@jtpio](https://github.com/jtpio))

### Documentation improvements

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-08&to=2021-07-16&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-07-08..2021-07-16&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-08..2021-07-16&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-08..2021-07-16&type=Issues)

## 0.1.17

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...16bd7ca4af02310eeb3929d66d950ba44d9b765d))

### Maintenance and upkeep improvements

- Improve Check Release Isolation [#68](https://github.com/jupyter-server/jupyter_releaser/pull/68) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-08&to=2021-07-16&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-08..2021-07-16&type=Issues)

## 0.1.16

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...e168f06434523529be27b5d95cfead16f9c69577))

### Bugs fixed

- Pin versions [#65](https://github.com/jupyter-server/jupyter_releaser/pull/65) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-08&to=2021-07-08&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-08..2021-07-08&type=Issues)

## 0.1.15

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...a8b6700aa6b6a2e642894e9fbe0f486ff1b14ca5))

### Bugs fixed

- Add missing `return` to `draft_changelog` [#63](https://github.com/jupyter-server/jupyter_releaser/pull/63) ([@jtpio](https://github.com/jtpio))
- Handle the case where there are no changes in changelog [#61](https://github.com/jupyter-server/jupyter_releaser/pull/61) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-06&to=2021-07-08&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-07-06..2021-07-08&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-06..2021-07-08&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-06..2021-07-08&type=Issues)

## 0.1.14

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0c977a12197f0947c1dbdbf983beda1b97535b58))

### Bugs fixed

- Fix typo [#59](https://github.com/jupyter-server/jupyter_releaser/pull/59) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-06&to=2021-07-06&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-07-06..2021-07-06&type=Issues)

## 0.1.13

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...7bdc7f8698fab65bc7ac6247ac2f8d867feaeace))

### Bugs fixed

- Fix handling of default version bump [#57](https://github.com/jupyter-server/jupyter_releaser/pull/57) ([@blink1073](https://github.com/blink1073))
- Fix handling of workspace paths [#56](https://github.com/jupyter-server/jupyter_releaser/pull/56) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-02&to=2021-07-06&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-07-02..2021-07-06&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-02..2021-07-06&type=Issues)

## 0.1.12

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...38f772bac2e0e5321b8c56b4461b232a5d19f42e))

### Bugs fixed

- More fixups [#54](https://github.com/jupyter-server/jupyter_releaser/pull/54) ([@jtpio](https://github.com/jtpio))
- Fix Handling of Workspace Packages [#53](https://github.com/jupyter-server/jupyter_releaser/pull/53) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-07-02&to=2021-07-02&type=c))

[@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-07-02..2021-07-02&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-07-02..2021-07-02&type=Issues)

## 0.1.11

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...39b8e3b62242a6371caae3470bbca2a31b960640))

### Enhancements made

- Handle missing version from package.json in `get_version` [#51](https://github.com/jupyter-server/jupyter_releaser/pull/51) ([@jtpio](https://github.com/jtpio))

### Bugs fixed

- Handle missing `version` from `package.json` [#46](https://github.com/jupyter-server/jupyter_releaser/pull/46) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-06-29&to=2021-07-02&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-06-29..2021-07-02&type=Issues)

## 0.1.10

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...f15fa653aee8112842e564870a35a123bb3a5c7c))

### Bugs fixed

- Handle already published workspace packages [#49](https://github.com/jupyter-server/jupyter_releaser/pull/49) ([@blink1073](https://github.com/blink1073))
- Install yarn if it is not already installed [#47](https://github.com/jupyter-server/jupyter_releaser/pull/47) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-06-23&to=2021-06-29&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-06-23..2021-06-29&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-06-23..2021-06-29&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-06-23..2021-06-29&type=Issues)

## 0.1.9

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...15c962b0750ff879276ccfeb0b2ab660eff6315b))

### Bugs fixed

- Write .npmrc to dist_dir [#43](https://github.com/jupyter-server/jupyter_releaser/pull/43) ([@jtpio](https://github.com/jtpio))
- Remove extra dollar sign for registry inputs [#41](https://github.com/jupyter-server/jupyter_releaser/pull/41) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-06-23&to=2021-06-23&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-06-23..2021-06-23&type=Issues)

## 0.1.8

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...0e521a279197eddae5a1a0373849c389e0324cdb))

### Bugs fixed

- Fix usage of registry value [#39](https://github.com/jupyter-server/jupyter_releaser/pull/39) ([@blink1073](https://github.com/blink1073))
- Use the last line of the `npm pack` command [#37](https://github.com/jupyter-server/jupyter_releaser/pull/37) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-06-16&to=2021-06-23&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-06-16..2021-06-23&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-06-16..2021-06-23&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-06-16..2021-06-23&type=Issues)

## 0.1.7

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...43ec6119006214ff88120497735291d7a681c24d))

### Bugs fixed

- Fix handling of npm token [#34](https://github.com/jupyter-server/jupyter_releaser/pull/34) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-24&to=2021-06-16&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-05-24..2021-06-16&type=Issues)

## 0.1.6

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.1.5...1466f348fdaccd6f079f8278f213ca7611011f54))

### Maintenance and upkeep improvements

- Properly install NPM Packages [#31](https://github.com/jupyter-server/jupyter_releaser/pull/31) ([@jtpio](https://github.com/jtpio))
- Use Releaser to Tag Itself [#32](https://github.com/jupyter-server/jupyter_releaser/pull/32) ([@afshin](https://github.com/afshin))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-21&to=2021-05-24&type=c))

[@afshin](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Aafshin+updated%3A2021-05-21..2021-05-24&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-21..2021-05-24&type=Issues)

## 0.1.5

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.1.4...6499aa163689c110b50ed9e8345969581908d4d9))

### Maintenance and upkeep improvements

- More Changes Needed to Support Lumino [#29](https://github.com/jupyter-server/jupyter_releaser/pull/29) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-20&to=2021-05-21&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-20..2021-05-21&type=Issues)

## 0.1.4

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.1.3...73cacdd8fc99c7d1a197b245a702ddd1605329f7))

### Maintenance and upkeep improvements

- More Cleanup in Preparation for Usage with Lumino [#27](https://github.com/jupyter-server/jupyter_releaser/pull/27) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-19&to=2021-05-20&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-19..2021-05-20&type=Issues)

## 0.1.3

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.1.2...666df24d9e3885d468072c5f8b0dca93df1ef777))

### Bugs fixed

- Fix Check Release for NPM-Only Packages [#25](https://github.com/jupyter-server/jupyter_releaser/pull/25) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-13&to=2021-05-19&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-13..2021-05-19&type=Issues)

## 0.1.2

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v0.1.1...4272ada592ee6efeda656a775ae88e9f906bb82f))

### Bugs fixed

- More Cleanup [#23](https://github.com/jupyter-server/jupyter_releaser/pull/23) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-12&to=2021-05-13&type=c))

[@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-12..2021-05-13&type=Issues)

## 0.1.1

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...844d9e66bb8376f65c23188fa2868b655d2756a7))

### Enhancements made

- Add Support for Since Parameter [#20](https://github.com/jupyter-server/jupyter_releaser/pull/20) ([@jtpio](https://github.com/jtpio))
- Prep for PyPI Release [#16](https://github.com/jupyter-server/jupyter_releaser/pull/16) ([@jtpio](https://github.com/jtpio))

### Documentation improvements

- Restore 0.1.0 Changelog entry [#21](https://github.com/jupyter-server/jupyter_releaser/pull/21) ([@blink1073](https://github.com/blink1073))
- Use raw GitHub Links [#18](https://github.com/jupyter-server/jupyter_releaser/pull/18) ([@blink1073](https://github.com/blink1073))
- Add forwardport pr screenshot and update publish release screenshot [#17](https://github.com/jupyter-server/jupyter_releaser/pull/17) ([@blink1073](https://github.com/blink1073))
- Prep for PyPI Release [#16](https://github.com/jupyter-server/jupyter_releaser/pull/16) ([@jtpio](https://github.com/jtpio))

### Other merged PRs

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-04&to=2021-05-12&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-05-04..2021-05-12&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-05-04..2021-05-12&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-04..2021-05-12&type=Issues)

## 0.1.0

([Full Changelog](https://github.com/jupyter-server/jupyter_releaser/compare/v1...a637305d93becb9f42eed3628b41055d0d44ea18))

### Enhancements made

- Prep for PyPI Release [#16](https://github.com/jupyter-server/jupyter_releaser/pull/16) ([@jtpio](https://github.com/jtpio))

### Documentation improvements

- Use raw GitHub Links [#18](https://github.com/jupyter-server/jupyter_releaser/pull/18) ([@blink1073](https://github.com/blink1073))
- Add forwardport pr screenshot and update publish release screenshot [#17](https://github.com/jupyter-server/jupyter_releaser/pull/17) ([@blink1073](https://github.com/blink1073))
- Prep for PyPI Release [#16](https://github.com/jupyter-server/jupyter_releaser/pull/16) ([@jtpio](https://github.com/jtpio))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter-server/jupyter_releaser/graphs/contributors?from=2021-05-04&to=2021-05-05&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ablink1073+updated%3A2021-05-04..2021-05-05&type=Issues) | [@codecov-commenter](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Acodecov-commenter+updated%3A2021-05-04..2021-05-05&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyter-server%2Fjupyter_releaser+involves%3Ajtpio+updated%3A2021-05-04..2021-05-05&type=Issues)

## 0.0.1

Initial Version
