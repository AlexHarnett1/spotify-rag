import os
import openai
import json
from dotenv import load_dotenv
from db_search import get_top_artists

load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function registry (map of function names to callables)
function_registry = {
    "get_top_artists": get_top_artists
}

tools = [{
    "type": "function",
    "name": "get_top_artists",
    "description": "Get my top listened to artists.",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of artists e.g. 25, 40"
            }
        },
        "additionalProperties": False
    }
}]
