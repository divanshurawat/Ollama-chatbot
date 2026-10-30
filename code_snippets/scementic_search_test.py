import os

from dotenv import load_dotenv
from openai import OpenAI
import numpy


load_dotenv() #by deafult looks for all .env file in the current directory 
clint= OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    response= clint.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    dotProduct= numpy.dot(a, b)
    lenA= numpy.linalg.norm(a)
    lenB= numpy.linalg.norm(b)
    ans= dotProduct/(lenA*lenB)
    return ans

text1="Python is a programming language"
text2= "We mainly use python for AI development"
text3= "I am a good boy"

emb_1= get_embedding(text1)
emb_2= get_embedding(text2)
emb_3= get_embedding(text3)

print(cosine_similarity(emb_1, emb_2))
print(cosine_similarity(emb_1, emb_3))
print(cosine_similarity(emb_2, emb_3))