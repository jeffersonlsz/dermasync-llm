import hashlib
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("punkt")
nltk.download('punkt_tab')

# Caminho do diretório com arquivos .txt
DIRETORIO = "D:\\workspace_projects_001\\fotos_dados\\resultados\\depoimentos"  # coloque o caminho real

# Inicializa modelo
modelo = SentenceTransformer("intfloat/multilingual-e5-base")

# Inicia ChromaDB
client = chromadb.PersistentClient(path="./chroma_segmentado_txt")
collection = client.get_or_create_collection(name="dermasync_segmentos_txt")

for nome in os.listdir(DIRETORIO):
    if not nome.endswith(".txt"):
        continue

    caminho = os.path.join(DIRETORIO, nome)
    texto = ""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read().strip()

    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho}: {e}")
        continue
    if not texto:
        continue

    data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho)).strftime("%Y-%m-%d")
    relato_id = hashlib.sha1(texto.encode()).hexdigest()

    sentencas = sent_tokenize(texto, language="portuguese")
    for i, sent in enumerate(sentencas):
        if len(sent.strip()) < 15:
            continue

        segmento = sent.strip()
        id_segmento = hashlib.sha1(f"{relato_id}_{i}".encode()).hexdigest()
        embedding = modelo.encode(segmento).tolist()
        print(f"Adicionando segmento {i} do relato {relato_id} ({nome})")
        collection.add(
            ids=[id_segmento],
            documents=[segmento],
            embeddings=[embedding],
            metadatas=[{
                "relato_original_id": relato_id,
                "arquivo": nome,
                "data_coleta": data_modificacao,
                "indice_segmento": i,
                
            }]
        )
