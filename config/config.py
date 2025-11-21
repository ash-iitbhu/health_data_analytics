import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    #PRIMARY_MODEL_NAME = "llama-3.3-70b-versatile" 
    PRIMARY_MODEL_NAME = "openai/gpt-oss-20b"
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    

    dataset_path1 = "/app/data/health_dataset1.csv"
    dataset_path2 = "/app/data/health_dataset2.csv"
