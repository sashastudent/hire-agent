from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()  # Load variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)