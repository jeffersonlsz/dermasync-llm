import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
import onnxruntime

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Configurações da base
# Cliente com persistência local
client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="depoimentos")

# Embeddings com modelo open-source gratuito
model = SentenceTransformer("intfloat/multilingual-e5-base")

# Função para adicionar relato
def adicionar_relato(id, texto, metadados=None):
    
    try:
        embedding = model.encode(f"passage: {texto}").tolist()
        collection.delete(ids=[id])  # Remove se já existir
        collection.add(
            documents=[texto],
            embeddings=[embedding],
            ids=[id],
            metadatas=[metadados or {}]
        )
        
        print(f"✅ Adicionado: {id}")
    except Exception as e:
        print(f"❌ Erro ao adicionar {id}: {e}")



def consultar_relatos(pergunta, k=10):
    consulta_formatada = f"query: {pergunta}"
    query_embedding = model.encode(consulta_formatada).tolist()
    
    resultados = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    print("🔍 Consulta:", pergunta)
    #print("🧠 Embedding:", query_embedding[:5], "...")  # Só os primeiros valores
    #print("📦 Resultados brutos:", resultados)

    for i, doc in enumerate(resultados['documents'][0]):
        print(f"\n--- Resultado {i+1} ---")
        print("Documento:", doc)
        print("Metadados:", resultados['metadatas'][0][i])
        print("ID:", resultados['ids'][0][i])
        print("Pontuação:", resultados['distances'][0][i])

    return resultados


def new_func(adicionar_relato):
    adicionar_relato("001", "Usei pomada de calêndula e melhorei em 3 dias", {
            "id_usuario": "anon_006",
            "faixa_etaria": "30-40",
            "genero": "feminino",
            "parte_corpo": "rosto",
            "gravidade": "leve",
            "tipo_tratamento": json.dumps(["pomada", "fitoterápico"]),
            "tempo_melhora": "3 dias",
            "resposta_positiva": True
        })

    adicionar_relato("002", "Tomar banho frio ajudou a reduzir a coceira intensa", {"data": "2023-10-02"})
    adicionar_relato("003", "O uso de sabonete neutro e evitar roupas sintéticas reduziu muito as crises" , {"data": "2023-10-03"})
    adicionar_relato("004", "Pomada de corticoide foi a única que melhorou em 1 semana" , {"data": "2023-10-04"})
    adicionar_relato("005", "Chá de camomila acalmou a vermelhidão e ajudou na cicatrização" , {"data": "2023-10-05"})
    adicionar_relato("006", "o palmeiras nunca teve mundial" , {"data": "2023-10-11"})
    adicionar_relato("007", "A pomada de calêndula não fez efeito", {"data": "2023-10-12"})
    adicionar_relato("008", "Usei uma pomada chamada minâncora e deu certo", {"data": "2023-10-12"} )
    adicionar_relato("009", "Não use a pomada zudaifu", {"data": "2023-10-12"})
    adicionar_relato("010", "Eu uso muito o hidratante neutrogena, acho ele muito bom", {"data": "2023-10-12"})
    adicionar_relato("011", "Quando a crise tá feia, eu uso pomada halobex, depois fico só passando tarfic mesmo", {"data": "2023-10-12"})
    adicionar_relato("011", "Árvores de maçãs não produzem laranjas", {"data": "2023-10-12"})
                     

if __name__ == "__main__":

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base" )
    
    client1 = chromadb.PersistentClient(path="./chroma_storage")
    collection1 = client1.get_or_create_collection(name="depoimentos", embedding_function=embedding_fn)
    print(collection1.query(query_texts=["pomada"], n_results=3))
    
   
    



