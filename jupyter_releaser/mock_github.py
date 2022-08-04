import atexit
import datetime
import os
import pickle
import tempfile
import uuid
from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from jupyter_releaser.util import MOCK_GITHUB_URL

app = FastAPI()

if "RH_GITHUB_STATIC_DIR" in os.environ:
    static_dir = os.environ["RH_GITHUB_STATIC_DIR"]
else:
    static_dir_obj = tempfile.TemporaryDirectory()
    atexit.register(static_dir_obj.cleanup)
    static_dir = static_dir_obj.name

app.mount("/static", StaticFiles(directory=static_dir), name="static")


def load_from_pickle(name):
    source_file = os.path.join(static_dir, name + ".pkl")
    if not os.path.exists(source_file):
        return {}
    with open(source_file, "rb") as fid:
        return pickle.load(fid)


def write_to_pickle(name, data):
    source_file = os.path.join(static_dir, name + ".pkl")
    with open(source_file, "wb") as fid:
        pickle.dump(data, fid)


releases: Dict[int, "Release"] = load_from_pickle("releases")
pulls: Dict[int, "PullRequest"] = load_from_pickle("pulls")
release_ids_for_asset: Dict[int, int] = load_from_pickle("release_ids_for_asset")
tag_refs: Dict[str, "Tag"] = load_from_pickle("tag_refs")


class Asset(BaseModel):
    id: int
    name: str
    content_type: str
    size: int
    state: str = "uploaded"
    url: str
    node_id: str = ""
    download_count: int = 0
    label: str = ""
    uploader: None = None
    browser_download_url: str = ""
    created_at: str = ""
    updated_at: str = ""


class Release(BaseModel):
    assets_url: str = ""
    upload_url: str
    tarball_url: str = ""
    zipball_url: str = ""
    created_at: str
    published_at: str = ""
    draft: bool
    body: str = ""
    id: int
    node_id: str = ""
    author: str = ""
    html_url: str
    name: str = ""
    prerelease: bool
    tag_name: str
    target_commitish: str
    assets: List[Asset]
    url: str


class User(BaseModel):
    login: str = "bar"
    html_url: str = "http://bar.com"


class PullRequest(BaseModel):
    number: int = 0
    html_url: str = "http://foo.com"
    title: str = "foo"
    user: User = User()


class TagObject(BaseModel):
    sha: str


class Tag(BaseModel):
    ref: str
    object: TagObject


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/repos/{owner}/{repo}/releases")
def list_releases(owner: str, repo: str) -> List[Release]:
    """https://docs.github.com/en/rest/releases/releases#list-releases"""
    return list(releases.values())


@app.post("/repos/{owner}/{repo}/releases")
async def create_a_release(owner: str, repo: str, request: Request) -> Release:
    """https://docs.github.com/en/rest/releases/releases#create-a-release"""
    release_id = uuid.uuid4().int
    data = await request.json()
    url = f"https://github.com/repos/{owner}/{repo}/releases/{release_id}"
    html_url = f"https://github.com/{owner}/{repo}/releases/tag/{data['tag_name']}"
    upload_url = f"{MOCK_GITHUB_URL}/repos/{owner}/{repo}/releases/{release_id}/assets"
    fmt_str = r"%Y-%m-%dT%H:%M:%SZ"
    created_at = datetime.datetime.utcnow().strftime(fmt_str)
    model = Release(
        id=release_id,
        url=url,
        html_url=html_url,
        assets=[],
        upload_url=upload_url,
        created_at=created_at,
        **data,
    )
    releases[model.id] = model
    write_to_pickle("releases", releases)
    return model


@app.patch("/repos/{owner}/{repo}/releases/{release_id}")
async def update_a_release(owner: str, repo: str, release_id: int, request: Request) -> Release:
    """https://docs.github.com/en/rest/releases/releases#update-a-release"""
    data = await request.json()
    model = releases[release_id]
    for name, value in data.items():
        setattr(model, name, value)
    write_to_pickle("releases", releases)
    return model


@app.post("/repos/{owner}/{repo}/releases/{release_id}/assets")
async def upload_a_release_asset(owner: str, repo: str, release_id: int, request: Request) -> None:
    """https://docs.github.com/en/rest/releases/assets#upload-a-release-asset"""
    model = releases[release_id]
    asset_id = uuid.uuid4().int
    name = request.query_params["name"]
    with open(f"{static_dir}/{asset_id}", "wb") as fid:
        async for chunk in request.stream():
            fid.write(chunk)
    headers = request.headers
    url = f"{MOCK_GITHUB_URL}/static/{asset_id}"
    asset = Asset(
        id=asset_id,
        name=name,
        size=headers["content-length"],
        url=url,
        content_type=headers["content-type"],
    )
    release_ids_for_asset[asset_id] = release_id
    model.assets.append(asset)
    write_to_pickle("releases", releases)
    write_to_pickle("release_ids_for_asset", release_ids_for_asset)


@app.delete("/repos/{owner}/{repo}/releases/assets/{asset_id}")
async def delete_a_release_asset(owner: str, repo: str, asset_id: int) -> None:
    """https://docs.github.com/en/rest/releases/assets#delete-a-release-asset"""
    release = releases[release_ids_for_asset[asset_id]]
    os.remove(f"{static_dir}/{asset_id}")
    release.assets = [a for a in release.assets if a.id != asset_id]
    del release_ids_for_asset[asset_id]
    write_to_pickle("releases", releases)
    write_to_pickle("release_ids_for_asset", release_ids_for_asset)


@app.delete("/repos/{owner}/{repo}/releases/{release_id}")
def delete_a_release(owner: str, repo: str, release_id: int) -> None:
    """https://docs.github.com/en/rest/releases/releases#delete-a-release"""
    del releases[release_id]
    write_to_pickle("releases", releases)


@app.get("/repos/{owner}/{repo}/pulls/{pull_number}")
def get_a_pull_request(owner: str, repo: str, pull_number: int) -> PullRequest:
    """https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request"""
    if pull_number not in pulls:
        pulls[pull_number] = PullRequest()
    write_to_pickle("pulls", pulls)
    return pulls[pull_number]


@app.post("/repos/{owner}/{repo}/pulls")
def create_a_pull_request(owner: str, repo: str) -> PullRequest:
    """https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request"""
    pull = PullRequest()
    pulls[pull.number] = pull
    write_to_pickle("releases", releases)
    return pull


@app.post("/repos/{owner}/{repo}/issues/{issue_number}/labels")
def add_labels_to_an_issue(owner: str, repo: str, issue_number: int) -> BaseModel:
    """https://docs.github.com/en/rest/issues/labels#add-labels-to-an-issue"""
    return BaseModel()


@app.post("/create_tag_ref/{tag_ref}/{sha}")
def create_tag_ref(tag_ref: str, sha: str) -> None:
    """Create a remote tag ref object for testing"""
    tag = Tag(ref=f"refs/tags/{tag_ref}", object=TagObject(sha=sha))
    tag_refs[tag_ref] = tag
    write_to_pickle("tag_refs", tag_refs)


@app.get("/repos/{owner}/{repo}/git/matching-refs/tags/{tag_ref}")
def list_matching_references(owner: str, repo: str, tag_ref: str) -> List[Tag]:
    """https://docs.github.com/en/rest/git/refs#list-matching-references"""
    # raise ValueError("we should have an api to set a sha for a tag ref for tests")
    return [tag_refs[tag_ref]]
