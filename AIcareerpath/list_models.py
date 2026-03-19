import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
print("\nAvailable models:\n")
for m in genai.list_models():
    print(m.name)