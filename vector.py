import pandas as pd
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os
from langchain_core.documents import Document

model = OllamaEmbeddings(model="mxbai-embed-large")


df = pd.read_csv("hotelreview.csv")

file_location = "./chomedb_langchain"
add__documents = not os.path.exists(file_location)

if add__documents:
    documents = []
    ids = []
    for i , row in df.iterrows():
        document = Document(page_content=row['Review']+" "+row['Title'],
                        metadata={"rating": row["Rating"], "date": row["Date"]},
                        id=str(i)
                        ) 
        documents.append(document)
        ids.append(str(i))

vector_store = Chroma(
    persist_directory=file_location,
    embedding_function=model,
    collection_name="hotelreviews"
)

if add__documents:
    vector_store.add_documents(documents, ids=ids)

retriever = vector_store.as_retriever(
 
    search_kwargs={"k":5}
)

