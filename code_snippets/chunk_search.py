import os
import numpy
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() #by deafult looks for all .env file in the current directory 
clint= OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL= os.getenv("EMBED_MODEL")
KB_FOLDER= os.getenv("KB_FOLDER")
VECTOR_STORE_FILE= os.getenv("VECTOR_STORE_FILE")

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


#Add embadding to the chunks
def add_embadding(chunks):
    for chunk in chunks:
        vector= get_embedding(chunk["text"])
        chunk["vector"]= vector

    return chunks

#Search method: to search the top_k chunks to the user query
def search(query, chunks, top_k=3):
    query_vector= get_embedding(query)

    results=[]
    for chunk in chunks:
        score= cosine_similarity(query_vector, chunk["vector"])
        results.append({
            "score":float(score),
            "source":chunk["source"],
            "chunk_id":chunk["chunk_id"],
            "text":chunk["text"],
            "size":len(chunk["text"])
        })

    results.sort(key= lambda rec: rec["score"], reverse=True)

    return results[:top_k]

#Takes one file and create multiple chunks from it
def chunk_document(document):
    chunks_in_doc=[]
    chunk_id=0
    for part in document["text"].split("\n\n"):
        part= part.strip()
        if part:
            chunks_in_doc.append({
                "source": document["source"],
                "chunk_id": chunk_id,
                "text": part
            })
            chunk_id+=1

    return chunks_in_doc

def create_chunks():
    documents= load_documents()
    chunks=[]

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks


#testing method
def test(user_query, chunks, top_k=3):
    print(f"\nUser Query: {user_query}\n")

    results=search(user_query, chunks, top_k)

    for r in results:
        print(f" {r["score"]:.2f} - {r["source"]} - {r["size"]} charcaters")

def save_vector_store(chunks):
    with open(VECTOR_STORE_FILE,"w", encoding="utf-8") as f:
        json.dump(chunks, f , indent=4)

def load_vector_store():
    with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
#Starting testing

chunks=[]
if(os.path.exists(VECTOR_STORE_FILE)):
    chunks= load_vector_store()
    print(f"Chunks are loaded {len(chunks)} chunks from vector store")
else: 
    chunks= create_chunks()
    chunks= add_embadding(chunks)
    save_vector_store(chunks)
    print(f"Create and embedded {len(chunks)} and saved to the vector store file.")



print(f"We have {len(chunks)} embedded chunks.")

user_query= " What are the benifits of Maternity Leave?"

test(user_query, chunks, 3)