import os
from google import genai

def get_gemini_client():
    """Initializes and returns the Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    # Initialize the official Google GenAI Client
    return genai.Client(api_key=api_key)

def get_default_model():
    """Returns the default model to use (gemini-2.5-flash)."""
    return "gemini-2.5-flash"
