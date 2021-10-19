import os


def setup():
    # Set up env variables
    os.environ.setdefault("RH_REPOSITORY", os.environ["GITHUB_REPOSITORY"])
    os.environ.setdefault("RH_REF", os.environ["GITHUB_REF"])

    if not os.environ.get("RH_BRANCH"):
        if os.environ.get("GITHUB_BASE_REF"):
            base_ref = os.environ.get("GITHUB_BASE_REF")
            print(f"Using GITHUB_BASE_REF: ${base_ref}")
            os.environ["RH_BRANCH"] = base_ref

        else:
            # e.g refs/head/foo or refs/tag/bar
            ref = os.environ["GITHUB_REF"]
            print(f"Using GITHUB_REF: {ref}")
            os.environ["RH_BRANCH"] = "/".join(ref.split("/")[2:])
