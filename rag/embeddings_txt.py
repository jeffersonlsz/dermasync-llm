# rag/embeddings_txt.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Inicializa ChromaDB persistente
client = chromadb.PersistentClient(path="./chroma_segmentado_txt")
collection = client.get_collection(name="dermasync_segmentos_txt")

# Modelo de embedding
model = SentenceTransformer("intfloat/multilingual-e5-base")

def buscar_segmentos_similares(query: str, k: int = 5):
    embedding = model.encode(query).tolist()
    resultado = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    # Empacota os resultados em lista de dicts
    resultados_formatados = []
    for i in range(len(resultado["documents"][0])):
        resultados_formatados.append({
            "texto": resultado["documents"][0][i],
            "metadados": resultado["metadatas"][0][i],
            "distancia": resultado["distances"][0][i]
        })
    return resultados_formatados
