from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import re

def parse_owner_repo(url: str):
    pattern = r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
    match = re.match(pattern, url)
    if match:
        owner = match.group("owner")
        repo = match.group("repo")
        return owner, repo
    return None, None

app = FastAPI()

@app.get("/file_struct")
def get_file_structure(url: str):
    #first is to get owner then repo name then sha then repo json.
    #then get the tree sha from the repo json
    owner, repo = parse_owner_repo(url)

    return {"owner": owner, "repo": repo}
