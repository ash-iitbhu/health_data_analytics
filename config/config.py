import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PRIMARY_MODEL_NAME = "openai/gpt-oss-20b"
    #JUDGE_MODEL_NAME = "llama-3.3-70b-versatile"
    JUDGE_MODEL_NAME = "openai/gpt-oss-120b"
    disclaimer_phrase = "❗️ **Disclaimer:** The following analysis is based on a hypothetical dataset and does not constitute medical advice. Consult a qualified healthcare professional for any health concerns."
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
