import os

import requests
from ghapi.core import GhApi


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

    gh.repos.delete_release(release.id)

    pull = gh.pulls.create("title", "head", "base", "body", True, False, None)
    gh.issues.add_labels(pull.number, ["documentation"])
