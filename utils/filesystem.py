import os

# Diretórios onde os arquivos .txt estão armazenados
DIRETORIOS_BUSCA = [
    r"D:\workspace_projects_001\fotos_dados\resultados\coleta",
    r"D:\workspace_projects_001\fotos_dados\resultados\depoimentos"
]

def ler_arquivo_segmento(nome_arquivo: str) -> str:
    if not nome_arquivo.endswith(".txt"):
        raise ValueError("Apenas arquivos .txt são permitidos.")
    
    if ".." in nome_arquivo or "/" in nome_arquivo or "\\" in nome_arquivo:
        raise ValueError("Nome de arquivo inválido.")

    for diretorio in DIRETORIOS_BUSCA:
        caminho = os.path.join(diretorio, nome_arquivo)
        if os.path.exists(caminho) and caminho.endswith(".txt"):
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
    
    raise FileNotFoundError(f"Arquivo .txt '{nome_arquivo}' não encontrado nos diretórios esperados.")
