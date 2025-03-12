import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.parser import get_file_structure
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from langchain_groq import ChatGroq

app = FastAPI()

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f".env file not found at {dotenv_path}")
load_dotenv(dotenv_path)
# Get API key with debugging
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("Warning: GROQ_API_KEY not found in environment variables")
    # You could set a default key here for testing, but not recommended for production

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 4: Initialize Groq client with explicit API key
groq_client = Groq(
    id="llama-3.3-70b-versatile",
    api_key=groq_api_key
)

# Step 5: Initialize agent with explicit API key
agent = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,)

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
        # Get file structure
        file_structure_data = get_file_structure(url)
        file_structure = file_structure_data["file_structure"]
        
        # Create prompt
        prompt = f"""
        You are an AI that generates fully formatted `README.md` files. Given the following file structure:        
        ```
        {json.dumps(file_structure, indent=2)}
        ```

        Create a README that stands out with:
        - ✨ A catchy project title with relevant emoji
        - 📝 An engaging description that communicates the project's purpose and value
        - 🚀 Clear installation instructions with code snippets
        - 💡 Creative usage examples that showcase real-world applications
        - 🔑 Key features highlighted with appropriate emojis
        - 📊 Visual elements (like badges or simple ASCII art) where appropriate
        - 📄 License information if available

        Make the README visually organized with:
        - Consistent emoji usage as section markers
        - Clean horizontal dividers between major sections
        - Proper heading hierarchy (H1, H2, H3)
        - Syntax-highlighted code blocks
        - At least one table for structured information

        The tone should be professional but friendly and enthusiastic about the project.
        Ensure the output is a valid Markdown file that can be copied and used directly.
        """

        # Use agent to generate README
        response = agent.invoke(prompt)
        
        # Important: Check the actual response structure from your Agent class
        # This assumes agent.run returns the text directly
        print(response)
        return JSONResponse(content={"success": True, "readme": response.content})
        
        # If your agent.run returns something different, you'll need to adjust accordingly
        # For example, if it returns an object with a 'text' attribute:
        # return JSONResponse(content={"success": True, "readme": response.text})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating README: {str(e)}")
