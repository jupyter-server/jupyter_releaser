# Jupyter Releaser

**Jupyter Releaser** contains a set of helper scripts and GitHub Actions to aid in automated releases of Python and npm packages.

## Installation

To install the latest release locally, make sure you have
[pip installed](https://pip.readthedocs.io/en/stable/installing/) and run:

```bash
    pip install git+https://github.com/jupyter-server/jupyter-releaser
```

## Library Usage

```bash
    jupyter-releaser --help
    jupyter-releaser build-python --help
    jupyter-releaser check-npm --help
```

## Checklist for Adoption

See the [adoption guides](https://jupyter-releaser.readthedocs.io/en/latest/how_to_guides/index.html).

## Actions

GitHub actions scripts are available to draft a changelog, draft a release, publish a release, and check a release.

See the [action details documentation](https://jupyter-releaser.readthedocs.io/en/latest/background/theory.html#action-details) for more information.

The actions can be run on a [fork](https://jupyter-releaser.readthedocs.io/en/latest/how_to_guides/convert_repo_from_releaser.html) of `jupyter_releaser` and target multiple
repositories, or run as workflows on the [source repositories](https://jupyter-releaser.readthedocs.io/en/latest/how_to_guides/convert_repo_from_repo.html), using
shared credentials.
