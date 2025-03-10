import json
import requests
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.parser import parse_owner_repo , fetch_repo_sha , fetch_repo_tree , parse_github_tree
from typing import Dict, Any, Union

app = FastAPI()


@app.get("/file_struct/{url:path}", response_class=JSONResponse)
def get_file_structure(url: str):
    #first is to get owner then repo name then sha then repo json.
    #then get the tree sha from the repo json
    owner, repo, last_string = parse_owner_repo(url)
    sha = fetch_repo_sha(owner, repo)
    tree = fetch_repo_tree(owner, repo, sha)
    file_structure = parse_github_tree({"owner": owner, "repo": repo, "tree": tree})
    return {"owner": owner, "repo": repo, "last_string": last_string, "sha": sha, "tree": tree, "file_structure": file_structure}

class FileStructureRequest(BaseModel):
    file_structure: Dict[str, Any]

@app.post("/generate_readme", response_class=JSONResponse)
async def generate_readme(request: FileStructureRequest):
    """
    Sends a request to Ollama API to generate a README.md based on the file structure.
    
    Args:
        request: A request object containing the file structure
        
    Returns:
        JSONResponse: The generated README content or error message
    """
    try:

        prompt = f"""
        Generate a well-structured `README.md` file for the following project based on its file structure:

        {json.dumps(request.file_structure, indent=2)}

        Ensure the `README.md` contains:
        - A **clear project title** at the top.
        - A **concise description** explaining what the project does.
        - **Installation instructions** (if applicable).
        - **Usage instructions** with relevant examples.
        - A **folder structure section** explaining key directories and files.
        - **Contribution guidelines** (if relevant).

        Format the output as a valid Markdown file so that it can be copied and used directly.
        """

        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post("http://127.0.0.1:11434/api/generate", json=payload)
        
        if response.status_code == 200:
            return {"readme": response.json()["response"]}
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Ollama API error: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating README: {str(e)}")

#covert that to a way where we can send it to ai model