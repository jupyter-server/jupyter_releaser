import os

import requests
from ghapi.core import GhApi

from jupyter_releaser.mock_github import Asset, Release, load_from_file, write_to_file


def test_mock_github(mock_github):
    owner = "foo"
    repo_name = "bar"
    auth = "hi"

    gh = GhApi(owner=owner, repo=repo_name, token=auth)
    print(list(gh.repos.list_releases()))

    here = os.path.dirname(os.path.abspath(__file__))
    files = [os.path.join(here, f) for f in os.listdir(here)]
    files = [f for f in files if not os.path.isdir(f)]

    release = gh.create_release(
        "v1.0.0",
        "main",
        "v1.0.0",
        "body",
        True,
        True,
        files=files,
    )

    print(release.html_url)

    release = gh.repos.update_release(
        release["id"],
        release["tag_name"],
        release["target_commitish"],
        release["name"],
        "body",
        False,
        release["prerelease"],
    )
    assert release.draft is False

    for asset in release.assets:
        headers = dict(Authorization=f"token {auth}", Accept="application/octet-stream")
        print(asset.name)
        with requests.get(asset.url, headers=headers, stream=True) as r:
            r.raise_for_status()
            for _ in r.iter_content(chunk_size=8192):
                pass

    gh.git.create_ref("v1.1.0", "aaaa")
    tags = gh.list_tags("v1.1.0")
    assert tags[0]["object"]["sha"] == "aaaa"

    gh.repos.delete_release(release.id)

    pull = gh.pulls.create("title", "head", "base", "body", True, False, None)
    gh.issues.add_labels(pull.number, ["documentation"])


def test_cache_storage():
    asset = Asset(
        id=1,
        name="hi",
        size=122,
        url="hi",
        content_type="hi",
    )
    model = Release(
        id=1,
        url="hi",
        html_url="ho",
        assets=[asset],
        upload_url="hi",
        created_at="1",
        draft=False,
        prerelease=False,
        target_commitish="1",
        tag_name="1",
    )
    write_to_file("releases", dict(test=model))
    data = load_from_file("releases", Release)
    assert isinstance(data["test"], Release)
    assert isinstance(data["test"].assets[0], Asset)
    assert data["test"].assets[0].url == asset.url
