import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Inicializa ChromaDB e modelo
client = chromadb.PersistentClient(path="./chroma_segmentado_txt")
collection = client.get_collection(name="dermasync_segmentos_txt")

model = SentenceTransformer("intfloat/multilingual-e5-base")

# Query do usuário (exemplo)
query = "Quais hábitos devo mudar?"

# Embedding da query
embedding = model.encode(query).tolist()

# Consulta no banco
resultado = collection.query(
    query_embeddings=[embedding],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)
#import pdb
#pdb.set_trace()

for key, value in resultado.items():
    print(f"{key}: {value}")

# Exibe resultados
"""for i in range(len(resultado["documents"][0])):
    print(f"Documento {i+1}:")
    print(f"Raw: {resultado['documents'][0]}")
     print(f"Documento {i+1}:")
    print(f"Texto: {resultado['documents'][0][i]}")
    print(f"Distância (quanto menor, melhor): {resultado['distances'][0][i]:.3f}")
    print(f"Metadados: {resultado['metadatas'][0][i]}")
    print("-" * 50) """
