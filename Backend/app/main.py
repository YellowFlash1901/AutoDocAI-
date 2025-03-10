import json
import requests
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from utils.parser import get_file_structure
from typing import Dict, Any, Union
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.post("/generate_readme/{url:path}", response_class=JSONResponse)
async def generate_readme(url: str):
    """
    Generates a README.md based on the file structure using an AI model.
    
    Args:
        url (str): GitHub repository URL
    
    Returns:
        JSONResponse: The generated README content or error message
    """
    try:
        file_structure_data = get_file_structure(url)
        file_structure = file_structure_data["file_structure"]  # Access dictionary correctly

        
        prompt = f"""
        You are an AI that generates fully formatted `README.md` files.

        Generate a well-structured **Markdown (`README.md`)** file based on the following project file structure:
        
        ```
        {json.dumps(file_structure, indent=2)}
        ```

        Ensure the output is a valid Markdown file that can be copied and used directly.
        """

        payload = {
            "model": "llama3.2",  # Ensure this is the correct model
            "prompt": prompt,
            "stream": False
        }

        response = requests.post("http://127.0.0.1:11434/api/generate", json=payload)

        if response.status_code == 200:
            response_data = response.json()
            readme = response_data.get("response", "").strip()
            return JSONResponse(content={"success": True, "code": response.status_code, "readme": readme})
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Ollama API error: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating README: {str(e)}")