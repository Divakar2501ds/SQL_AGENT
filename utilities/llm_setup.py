from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
novita_client = OpenAI(
    api_key=NOVITA_API_KEY,
   base_url="https://api.novita.ai/openai"
)