import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    BASE_URL_EXTRACTION = os.getenv("BASE_URL", "")

    VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector-store")
    VECTOR_STORE_PERSIST_DIR = os.getenv("VECTOR_STORE_PERSIST_DIR", "./chroma_langchain_db")
    
    WEIGHT_KEYWORD_RETRIVER = os.getenv("WEIGHT_KEYWORD_RETRIVER",0)
    WEIGHT_SEMANTIC_RETRIVER = os.getenv("WEIGHT_SEMANTIC_RETRIVER", 1)
    
    OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL","http://localhost:11434")

    SECRET_KEY= os.getenv("SECRET_KEY","09d25e094faa6ca2556c818166b7a9563b93f7099usf6f0f4caa6cf63b88e8d3e7")
    ALGORITHM= os.getenv("ALGORITHM","HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",240))