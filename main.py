from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.parser import parse_owner_repo

app = FastAPI()


@app.get("/file_struct/{url:path}", response_class=JSONResponse)
def get_file_structure(url: str):
    #first is to get owner then repo name then sha then repo json.
    #then get the tree sha from the repo json
    owner, repo = parse_owner_repo(url)

    return {"owner": owner, "repo": repo}
