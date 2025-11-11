import os
from dotenv import load_dotenv

load_dotenv() 

QDRANT_HOST = os.getenv("QDRANT_HOST")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")
