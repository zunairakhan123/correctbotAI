import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-8b-8192" # or try "llama3-70b-8192", "gemma-7b-it", etc.
SAFE_PROMPT_PREFIX = "You are a friendly and safe AI mentor for kids and teens. Respond positively and constructively."