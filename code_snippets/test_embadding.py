
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() #by deafult looks for all .env file in the current directory 
clint= OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

response= clint.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    input=["I am a good boy", "I need a job"]
)

print(len(response.data[0].embedding));