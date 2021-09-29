# Write Releaser Config

## Command Options and Environment Variables

All of the commands support CLI and Environment Variable Overrides.
The environment variables are defined by the `envvar` parameters in the
command options in `cli.py`. The environment variables unique to
`jupyter-releaser` are prefixed with `RH_`. A list of all env variables can be seen
by running `jupyter-releaser list-envvars`.

## Default Values, Options, Skip, and Hooks

The default values can also be overriden using a config file.

Options can be overridden using the `options` section.

You can skip one or more commands using a `skip` section, which is a list of
commands to skip.

You can also define hooks to run before and after
commands in a `hooks` section. Hooks can be a shell command to run or
a list of shell commands, and are specified to run `before-` or `after-`
a command.
Note: the only unusable hook names are `before-prep-git` and `before-extract-release`, since a checkout of the target repository is not yet available at that point.

## Configuration File Priority

This is where `jupyter-releaser` looks for configuration (first one found is used):

```code
    .jupyter-releaser.toml
    pyproject.toml (in the tools.jupyter-releaser section )
    package.json (in the jupyter-releaser property)
```

Example `.jupyter-releaser.toml`:

```toml
[options]
dist_dir = "mydist"

skip = ["check-links"]

[hooks]
before-tag-version = "npm run pre:tag:script"
```

Example `pyproject.toml` section:

```toml
[tools.jupyter-releaser.options]
dist_dir = "mydist"

[tools.jupyter-releaser]
skip = ["check-links"]

[tools.jupyter-releaser.hooks]
after-build-python = ["python scripts/cleanup.py", "python scripts/send_email.py"]
```

Example `package.json`:

```json
{
  "name": "my-package",
  "jupyter-releaser": {
    "options": {
      "dist_dir": "mydist"
    },
    "skip": ["check-manifest"],
    "hooks": {
      "before-publish-dist": "npm run pre:publish:dist"
    }
  }
}
```
