import os
import json
from datetime import datetime

DIRETORIOS_BUSCA = [
    r"D:\workspace_projects_001\fotos_dados\resultados\coleta",
    r"D:\workspace_projects_001\fotos_dados\resultados\depoimentos"
]

dados = []

for diretorio in DIRETORIOS_BUSCA:
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.endswith(".txt"):
            caminho = os.path.join(diretorio, nome_arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                modificado = os.path.getmtime(caminho)
                data_modificacao = datetime.fromtimestamp(modificado).isoformat()
                dados.append({
                    "arquivo": nome_arquivo,
                    "data_modificacao": data_modificacao,
                    "conteudo": conteudo.strip()
                })
            except Exception as e:
                print(f"Erro ao processar {caminho}: {e}")

# Salva como JSONL
with open("depoimentos_extraidos.jsonl", "w", encoding="utf-8") as saida:
    for item in dados:
        json.dump(item, saida, ensure_ascii=False)
        saida.write("\n")

print(f"✅ {len(dados)} arquivos exportados para depoimentos_extraidos.jsonl")
