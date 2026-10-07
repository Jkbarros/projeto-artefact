"""Acesso aos Parquets gerados pelo pipeline (uso nas tools, Fase 4+)."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from emporio.config import PASTA_DADOS_PROCESSADOS

TABELAS = (
    "categorias",
    "produtos",
    "clientes",
    "pedidos",
    "itens_pedido",
    "promocoes",
)


def caminho_parquet(nome: str) -> str:
    return str(PASTA_DADOS_PROCESSADOS / f"{nome}.parquet")


def dados_processados_existem() -> bool:
    return all((PASTA_DADOS_PROCESSADOS / f"{nome}.parquet").is_file() for nome in TABELAS)


@lru_cache(maxsize=1)
def carregar_dados_processados() -> dict[str, pd.DataFrame]:
    if not dados_processados_existem():
        raise FileNotFoundError(
            "Dados processados não encontrados. Execute: python -m emporio.data_prep"
        )
    return {nome: pd.read_parquet(caminho_parquet(nome)) for nome in TABELAS}


def limpar_cache() -> None:
    carregar_dados_processados.cache_clear()
