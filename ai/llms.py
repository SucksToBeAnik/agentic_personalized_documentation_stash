from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()


def get_groq_model():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    
    secret_api_key = SecretStr(groq_api_key)
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=secret_api_key)
