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
        basedir = package
        tarball = osp.join(package, util.run("npm pack", cwd=package).split("\n")[-1])
    else:
        basedir = osp.dirname(package)
        tarball = package

    data = extract_package(tarball)

    # Move the tarball into the dist folder if public
    if not data.get("private", False) == True:
        shutil.move(str(tarball), str(dest))
    elif osp.isdir(package):
        os.remove(tarball)

    if not osp.isdir(package):
        return

    if "workspaces" in data:
        all_data = dict()
        for pattern in _get_workspace_packages(data):
            for path in glob(osp.join(basedir, pattern), recursive=True):
                path = Path(path)
                package_json = path / "package.json"
                if not osp.exists(package_json):
                    continue
                data = json.loads(package_json.read_text(encoding="utf-8"))
                if data.get("private", False) == True:
                    continue
                data["__path__"] = path
                all_data[data["name"]] = data

        i = 0
        for (name, data) in sorted(all_data.items()):
            i += 1
            path = data["__path__"]
            util.log(f'({i}/{len(all_data)}) Packing {data["name"]}...')
            tarball = path / util.run("npm pack", cwd=path, quiet=True)
            shutil.move(str(tarball), str(dest))


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


def check_dist(dist_dir):
    """Check npm dist file(s) in a dist dir"""
    tmp_dir = Path(TemporaryDirectory().name)
    os.makedirs(tmp_dir)

    util.run("npm init -y", cwd=tmp_dir)
    names = []
    staging = tmp_dir / "staging"

    names = extract_dist(dist_dir, staging)

    install_str = " ".join(f"./staging/{name}" for name in names)

    util.run(f"npm install {install_str}", cwd=tmp_dir)

    shutil.rmtree(str(tmp_dir), ignore_errors=True)


def extract_package(path):
    """Get the package json info from the tarball"""
    fid = tarfile.open(path)
    data = fid.extractfile("package/package.json").read()
    data = json.loads(data.decode("utf-8"))
    fid.close()
    return data


def handle_npm_config(npm_token):
    """Handle npm_config"""
    npmrc = Path(".npmrc")
    registry = os.environ.get("NPM_REGISTRY", "https://registry.npmjs.org/")
    text = f"registry={registry}"
    if npm_token:
        registry = registry.replace("https:", "")
        registry = registry.replace("http:", "")
        text += f"\n{registry}:_authToken={npm_token}"
    if npmrc.exists():
        text = npmrc.read_text(encoding="utf-8") + text
    npmrc.write_text(text, encoding="utf-8")


def get_package_versions(version):
    """Get the formatted list of npm package names and versions"""
    message = ""
    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    if data["version"] != version:
        message += f"\nPython version: {version}"
        message += f'\nnpm version: {data["name"]}: {data["version"]}'
    if "workspaces" in data:
        message += "\nnpm workspace versions:"
        for pattern in _get_workspace_packages(data):
            for path in glob(pattern, recursive=True):
                text = Path(path).joinpath("package.json").read_text()
                data = json.loads(text)
                message += f'\n{data["name"]}: {data["version"]}'
    return message


def tag_workspace_packages():
    """Generate tags for npm workspace packages"""
    if not PACKAGE_JSON.exists():
        return

    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    tags = util.run("git tag").splitlines()
    if not "workspaces" in data:
        return

    for pattern in _get_workspace_packages(data):
        for path in glob(pattern, recursive=True):
            sub_package_json = Path(path) / "package.json"
            sub_data = json.loads(sub_package_json.read_text(encoding="utf-8"))
            tag_name = f"{sub_data['name']}@{sub_data['version']}"
            if tag_name in tags:
                util.log(f"Skipping existing tag {tag_name}")
            else:
                util.run(f"git tag {tag_name}")


def _get_workspace_packages(data):
    """Get the workspace packages for a package given package data"""
    if isinstance(data["workspaces"], dict):
        packages = []
        for value in data["workspaces"].values():
            packages.extend(value)
    else:
        packages = data["workspaces"]
    return packages
