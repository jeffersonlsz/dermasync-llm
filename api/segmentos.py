from fastapi import APIRouter, HTTPException
from rag.embeddings_txt import buscar_segmentos_similares
from pydantic import BaseModel
from utils.filesystem import ler_arquivo_segmento
from .schemas import ArquivoRequest
from .schemas import QueryRequest

router = APIRouter()

@router.post("/consultar-arquivo-original")
def consultar_arquivo_original(req: ArquivoRequest):
    try:
        conteudo = ler_arquivo_segmento(req.nome_arquivo)
        return {"arquivo": req.nome_arquivo, "conteudo": conteudo}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consultar-segmentos")
def consultar_segmentos(req: QueryRequest):
    resultados = buscar_segmentos_similares(req.texto, req.k)
    return {"resultados": resultados}