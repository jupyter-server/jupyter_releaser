# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import os.path as osp
import shutil
import tarfile
from glob import glob
from pathlib import Path
from tempfile import TemporaryDirectory

from jupyter_releaser import util

PACKAGE_JSON = util.PACKAGE_JSON


def build_dist(package, dist_dir):
    """Build npm dist file(s) from a package"""
    # Clean the dist folder of existing npm tarballs
    os.makedirs(dist_dir, exist_ok=True)
    dest = Path(dist_dir)
    for pkg in glob(f"{dist_dir}/*.tgz"):
        os.remove(pkg)

    if osp.isdir(package):
        tarball = osp.join(package, util.run("npm pack", cwd=package).split("\n")[-1])
    else:
        tarball = package

    data = extract_package(tarball)

    # Move the tarball into the dist folder if public
    if not data.get("private", False):
        shutil.move(str(tarball), str(dest))
    elif osp.isdir(package):
        os.remove(tarball)

    if not osp.isdir(package):
        return

    if "workspaces" in data:
        paths = []
        for path in _get_workspace_packages(data):
            package_json = path / "package.json"
            data = json.loads(package_json.read_text(encoding="utf-8"))
            if data.get("private", False):
                continue
            paths.append(str(osp.abspath(path)).replace(os.sep, "/"))

        util.run(f"npm pack {' '.join(paths)}", cwd=dest, quiet=True)


def extract_dist(dist_dir, target):
    """Extract dist files from a dist_dir into a target dir"""
    names = []
    paths = sorted(glob(f"{dist_dir}/*.tgz"))
    util.log(f"Extracting {len(paths)} packages...")

    for package in paths:
        path = Path(package)

        data = extract_package(path)
        name = data["name"]

        # Skip if it is a private package
        if data.get("private", False):  # pragma: no cover
            util.log(f"Skipping private package {name}")
            continue

        names.append(name)

        pkg_dir = target / name
        if not pkg_dir.parent.exists():
            os.makedirs(pkg_dir.parent)

        tar = tarfile.open(path)
        tar.extractall(target)
        tar.close()

        if "main" in data:
            main = osp.join(target, "package", data["main"])
            if not osp.exists(main):
                raise ValueError(f"{name} is missing 'main' file {data['main']}")

        shutil.move(str(target / "package"), str(pkg_dir))

    return names


def check_dist(dist_dir, install_options):
    """Check npm dist file(s) in a dist dir"""
    with TemporaryDirectory() as td:

        util.run("npm init -y", cwd=td, quiet=True)
        names = []
        staging = Path(td) / "staging"

        names = extract_dist(dist_dir, staging)

        install_str = " ".join(f"./staging/{name}" for name in names)

        util.run(f"npm install {install_options} {install_str}", cwd=td, quiet=True)


def extract_package(path):
    """Get the package json info from the tarball"""
    fid = tarfile.open(path)
    fidfile = fid.extractfile("package/package.json")
    assert fidfile is not None
    data = fidfile.read()
    fidfile.close()
    data = json.loads(data.decode("utf-8"))
    fid.close()
    return data


def handle_npm_config(npm_token):
    """Handle npm_config"""
    npmrc = Path("~/.npmrc").expanduser()
    registry = os.environ.get("NPM_REGISTRY", "https://registry.npmjs.org/")
    reg_entry = text = f"registry={registry}"
    auth_entry = ""
    if npm_token:
        short_reg = registry.replace("https://", "//")
        short_reg = short_reg.replace("http://", "//")
        auth_entry = f"{short_reg}:_authToken={npm_token}"

    # Handle existing config
    if npmrc.exists():
        text = npmrc.read_text(encoding="utf-8")
        if reg_entry in text:
            reg_entry = ""
        if auth_entry in text:
            auth_entry = ""

    text += f"\n{reg_entry}\n{auth_entry}"
    text = text.strip() + "\n"
    util.log(f"writing npm config to {npmrc}")
    npmrc.write_text(text, encoding="utf-8")


def get_package_versions(version):
    """Get the formatted list of npm package names and versions"""
    message = ""
    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    npm_version = data.get("version", "")
    if npm_version != version:
        message += f"\nPython version: {version}"
        message += f'\nnpm version: {data["name"]}: {npm_version}'
    if "workspaces" in data:
        message += "\nnpm workspace versions:"
        for path in _get_workspace_packages(data):
            text = path.joinpath("package.json").read_text(encoding="utf-8")
            data = json.loads(text)
            message += f'\n{data["name"]}: {data.get("version", "")}'
    return message


def tag_workspace_packages():
    """Generate tags for npm workspace packages"""
    if not PACKAGE_JSON.exists():
        return

    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    tags = util.run("git tag", quiet=True).splitlines()
    if "workspaces" not in data:
        return

    skipped = []
    for path in _get_workspace_packages(data):
        sub_package_json = path / "package.json"
        sub_data = json.loads(sub_package_json.read_text(encoding="utf-8"))
        tag_name = f"{sub_data['name']}@{sub_data['version']}"
        if tag_name in tags:
            skipped.append(tag_name)
        else:
            util.run(f"git tag {tag_name}")
    if skipped:
        print(f"\nSkipped existing tags:\n{skipped}\n")


def _get_workspace_packages(data):
    """Get the workspace package paths for a package given package data"""
    if isinstance(data["workspaces"], dict):
        patterns = []
        for value in data["workspaces"].values():
            patterns.extend(value)
    else:
        patterns = data["workspaces"]

    paths = []
    for pattern in patterns:
        for path in glob(pattern, recursive=True):
            sub_package = Path(path)
            if not sub_package.is_dir():
                continue
            sub_package_json = sub_package / "package.json"
            if not sub_package_json.exists():
                continue
            paths.append(sub_package)

    return sorted(paths)
