"""Índice vetorial (ChromaDB) do manual de políticas."""

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from emporio.config import (
    NOME_COLECAO_POLITICAS,
    PASTA_CHROMA,
    obter_chave_openai,
)
from emporio.rag.pdf_politicas import ChunkPolitica, carregar_chunks_politicas

if TYPE_CHECKING:
    from chromadb.api.models.Collection import Collection


def obter_modelo_embedding() -> str:
    from emporio.config import MODELO_EMBEDDING_PADRAO, carregar_configuracao

    carregar_configuracao()
    return os.getenv("OPENAI_EMBEDDING_MODEL", MODELO_EMBEDDING_PADRAO).strip()


def _funcao_embedding() -> OpenAIEmbeddingFunction:
    return OpenAIEmbeddingFunction(
        api_key=obter_chave_openai(),
        model_name=obter_modelo_embedding(),
    )


def _cliente_chroma() -> chromadb.PersistentClient:
    PASTA_CHROMA.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(PASTA_CHROMA))


def indice_politicas_existe() -> bool:
    if not PASTA_CHROMA.is_dir():
        return False
    cliente = _cliente_chroma()
    try:
        colecao = cliente.get_collection(
            name=NOME_COLECAO_POLITICAS,
            embedding_function=_funcao_embedding(),
        )
        return colecao.count() > 0
    except Exception:  # noqa: BLE001 - coleção ausente/corrompida = índice inexistente
        return False


def obter_colecao(recriar: bool = False) -> Collection:
    cliente = _cliente_chroma()
    if recriar and PASTA_CHROMA.is_dir():
        try:
            cliente.delete_collection(NOME_COLECAO_POLITICAS)
        except Exception:  # noqa: BLE001,S110 - coleção pode não existir ainda
            pass

    return cliente.get_or_create_collection(
        name=NOME_COLECAO_POLITICAS,
        embedding_function=_funcao_embedding(),
        metadata={"hnsw:space": "cosine"},
    )


def construir_indice(chunks: list[ChunkPolitica] | None = None, recriar: bool = True) -> int:
    """
    Indexa os chunks no Chroma. Retorna quantidade de documentos indexados.

    `recriar=True` apaga a coleção anterior para resultado reproduzível.
    """
    if recriar and PASTA_CHROMA.exists():
        shutil.rmtree(PASTA_CHROMA, ignore_errors=True)

    lista = chunks or carregar_chunks_politicas()
    if not lista:
        raise ValueError("Nenhum chunk de políticas para indexar.")

    colecao = obter_colecao(recriar=True)
    colecao.add(
        ids=[c.chunk_id for c in lista],
        documents=[c.texto for c in lista],
        metadatas=[
            {"secao_id": c.secao_id, "titulo": c.titulo[:200]} for c in lista
        ],
    )
    return colecao.count()


def consultar_politicas_indice(pergunta: str, quantidade: int = 3) -> list[dict]:
    """Busca semântica no manual (usada pela tool na Fase 4)."""
    colecao = obter_colecao(recriar=False)
    if colecao.count() == 0:
        raise FileNotFoundError(
            "Índice RAG vazio. Execute python -m emporio.data_prep"
        )
    resultado = colecao.query(query_texts=[pergunta], n_results=quantidade)
    documentos = resultado.get("documents", [[]])[0]
    metadados = resultado.get("metadatas", [[]])[0]
    distancias = resultado.get("distances", [[]])[0]
    saida: list[dict] = []
    for doc, meta, dist in zip(documentos, metadados, distancias, strict=True):
        saida.append(
            {
                "texto": doc,
                "secao_id": meta.get("secao_id"),
                "titulo": meta.get("titulo"),
                "distancia": dist,
            }
        )
    return saida
