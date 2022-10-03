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

- `.jupyter-releaser.toml`
- `pyproject.toml` (in the tool.jupyter-releaser section)
- `package.json` (in the jupyter-releaser property)

Example `.jupyter-releaser.toml`:

```toml
[options]
dist_dir = "mydist"

[hooks]
before-tag-version = "npm run pre:tag:script"
```

Example `pyproject.toml` section:

```toml
[tool.jupyter-releaser.options]
dist_dir = "mydist"

[tool.jupyter-releaser]

[tool.jupyter-releaser.hooks]
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
    "skip": ["check-npm"],
    "hooks": {
      "before-publish-dist": "npm run pre:publish:dist"
    }
  }
}
```

## Automatic Dev Versions

If you'd like to use dev versions for your repository between builds,
use `dev` as the `post-version-spec` setting, e.g.

```toml
[tool.jupyter-releaser.options]
post-version-spec = "dev"
```

This will bump it to the next minor release with a `.dev0` suffix.

## Ensuring Python Resource Files

If you want to ensure that resource files are included in your installed Python
package
(from an sdist or a wheel), include configuration like the following:

```toml
[tool.jupyter-releaser.options]
pydist_resource_paths = ["my-package/img1.png", "my-package/foo/bar.json"]
```
