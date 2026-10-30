import os
import numpy
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() #by deafult looks for all .env file in the current directory 
clint= OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL= os.getenv("EMBED_MODEL")
KB_FOLDER= os.getenv("KB_FOLDER")

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

#Load the documents
def load_documents(folder=KB_FOLDER):
    documents=[]

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path= os.path.join(folder, filename)

        #Using "with", so that the opened file should get closed by itself
        with open(path, "r", encoding="utf-8") as f:
            documents.append({
                "source":filename,
                "text":f.read()
            })

    return documents


#Add embadding to the documents
def add_embadding(documents):
    for document in documents:
        vector= get_embedding(document["text"])
        document["vector"]= vector

    return documents

#Search method: to search the top_k documents to the user query
def search(query, documents, top_k=3):
    query_vector= get_embedding(query)

    results=[]
    for document in documents:
        score= cosine_similarity(query_vector, document["vector"])
        results.append({
            "score":float(score),
            "source":document["source"],
            "text":document["text"],
            "size":len(document["text"])
        })

    results.sort(key= lambda rec: rec["score"], reverse=True)

    return results[:top_k]


#testing method
def test(user_query, documents, top_k=3):
    print(f"\nUser Query: {user_query}\n")

    results=search(user_query, documents, top_k)

    for r in results:
        print(f" {r["score"]:.2f} - {r["source"]} - {r["size"]} charcaters")


#Starting testing

documents= load_documents()
documents= add_embadding(documents)

print(f"We have {len(documents)} embedded documents")

user_query= " How many days will I get for Maternity Leave"

test(user_query, documents, 3)