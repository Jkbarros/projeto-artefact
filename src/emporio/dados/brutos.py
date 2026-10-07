"""Leitura dos CSVs em data/raw/ (nomes com prefixo do desafio)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from emporio.config import PASTA_DADOS_BRUTOS

SUFIXOS = {
    "categorias": "categories.csv",
    "produtos": "products.csv",
    "clientes": "customers.csv",
    "pedidos": "orders.csv",
    "itens_pedido": "order_items.csv",
    "promocoes": "promotions.csv",
}


def _resolver_arquivo(sufixo: str) -> Path:
    candidatos = list(PASTA_DADOS_BRUTOS.glob(f"*{sufixo}"))
    if not candidatos:
        raise FileNotFoundError(
            f"CSV não encontrado em {PASTA_DADOS_BRUTOS} (sufixo esperado: {sufixo})"
        )
    if len(candidatos) > 1:
        candidatos.sort(key=lambda p: p.name)
    return candidatos[0]


def carregar_csv_bruto(nome_logico: str) -> pd.DataFrame:
    sufixo = SUFIXOS[nome_logico]
    caminho = _resolver_arquivo(sufixo)
    return pd.read_csv(caminho, encoding="utf-8")


def carregar_todos_brutos() -> dict[str, pd.DataFrame]:
    return {nome: carregar_csv_bruto(nome) for nome in SUFIXOS}
