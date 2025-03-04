from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.parser import parse_owner_repo , fetch_repo_sha , fetch_repo_tree

app = FastAPI()


@app.get("/file_struct/{url:path}", response_class=JSONResponse)
def get_file_structure(url: str):
    #first is to get owner then repo name then sha then repo json.
    #then get the tree sha from the repo json
    owner, repo, last_string = parse_owner_repo(url)
    sha = fetch_repo_sha(owner, repo)
    tree = fetch_repo_tree(owner, repo, sha)
    return {"owner": owner, "repo": repo, "last_string": last_string, "sha": sha, "tree": tree}
     
