# rag/chroma.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

import os

# Caminho onde está seu ChromaDB persistido
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_storage")
COLLECTION_NAME = "relatos"

# Inicializa o modelo de embedding
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

# Conecta ao banco vetorial persistido
vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_model
)

# Cria um retriever com top 3 resultados
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
