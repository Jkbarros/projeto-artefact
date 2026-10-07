"""Pipeline reproduzível: CSVs tratados + índice RAG do manual."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import pandas as pd

from emporio.config import ARQUIVO_MANIFESTO, PASTA_DADOS_PROCESSADOS
from emporio.dados.brutos import carregar_todos_brutos
from emporio.dados.repositorio import limpar_cache
from emporio.dados.transformar import transformar_todos
from emporio.rag.indice_politicas import construir_indice
from emporio.rag.pdf_politicas import carregar_chunks_politicas


def _validar_produtos(df: pd.DataFrame) -> None:
    if df["price_brl"].isna().any():
        raise ValueError("Existem produtos com preço nulo após o tratamento.")
    if (df["stock_quantity"] < 0).any():
        raise ValueError("Estoque negativo encontrado após o tratamento.")


def salvar_parquets(dados: dict[str, pd.DataFrame]) -> None:
    PASTA_DADOS_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    for nome, frame in dados.items():
        caminho = PASTA_DADOS_PROCESSADOS / f"{nome}.parquet"
        frame.to_parquet(caminho, index=False)


def executar_pipeline(reconstruir_rag: bool = True) -> dict:
    brutos = carregar_todos_brutos()
    tratados = transformar_todos(brutos)
    _validar_produtos(tratados["produtos"])
    salvar_parquets(tratados)

    chunks = carregar_chunks_politicas()
    total_chunks = len(chunks)
    total_indexado = 0
    if reconstruir_rag:
        total_indexado = construir_indice(chunks, recriar=True)

    limpar_cache()

    manifesto = {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "tabelas": {nome: len(df) for nome, df in tratados.items()},
        "chunks_politicas": total_chunks,
        "documentos_rag_indexados": total_indexado,
    }
    ARQUIVO_MANIFESTO.write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifesto


def main() -> None:
    parser = argparse.ArgumentParser(description="Trata CSVs e constrói índice RAG.")
    parser.add_argument(
        "--sem-rag",
        action="store_true",
        help="Só gera Parquets, sem chamar API de embeddings.",
    )
    args = parser.parse_args()
    manifesto = executar_pipeline(reconstruir_rag=not args.sem_rag)
    print("Pipeline concluído:")
    print(json.dumps(manifesto, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
