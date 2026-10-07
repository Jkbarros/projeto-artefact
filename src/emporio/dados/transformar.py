"""Transformações e limpeza dos DataFrames (Fase 3)."""

from __future__ import annotations

import json

import pandas as pd

from emporio.texto import normalizar_para_busca

MAPA_PAGAMENTO = {
    "pix": "PIX",
    "debit": "Cartão de débito",
    "boleto": "Boleto bancário",
    "credit_3x": "Cartão de crédito em 3x",
    "credit_6x": "Cartão de crédito em 6x",
    "credit_12x": "Cartão de crédito em 12x",
}


def transformar_categorias(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["nome_busca"] = saida["name"].map(normalizar_para_busca)
    return saida


def transformar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["nome_busca"] = saida["name"].map(normalizar_para_busca)
    saida["descricao_busca"] = saida["description"].fillna("").map(normalizar_para_busca)
    saida["created_at"] = pd.to_datetime(saida["created_at"], errors="coerce")
    saida["price_brl"] = pd.to_numeric(saida["price_brl"], errors="coerce")
    saida["stock_quantity"] = pd.to_numeric(saida["stock_quantity"], errors="coerce").fillna(0).astype(int)

    def _specs_validas(valor: object) -> str:
        if valor is None or (isinstance(valor, float) and pd.isna(valor)):
            return ""
        texto = str(valor).strip()
        if not texto:
            return ""
        try:
            json.loads(texto)
            return texto
        except json.JSONDecodeError:
            return texto

    saida["specs"] = saida["specs"].map(_specs_validas)
    return saida


def transformar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["nome_busca"] = saida["name"].map(normalizar_para_busca)
    saida["email_busca"] = saida["email"].fillna("").str.strip().str.lower()
    saida["telefone_busca"] = (
        saida["phone"].fillna("").astype(str).str.replace(r"\D", "", regex=True)
    )
    return saida


def transformar_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["order_date"] = pd.to_datetime(saida["order_date"], errors="coerce")
    saida["estimated_delivery"] = pd.to_datetime(saida["estimated_delivery"], errors="coerce")
    saida["total_brl"] = pd.to_numeric(saida["total_brl"], errors="coerce")
    saida["payment_method_label"] = (
        saida["payment_method"].map(MAPA_PAGAMENTO).fillna(saida["payment_method"])
    )
    return saida


def transformar_itens_pedido(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["quantity"] = pd.to_numeric(saida["quantity"], errors="coerce").fillna(1).astype(int)
    return saida


def transformar_promocoes(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    saida["vigente"] = saida["is_active"].astype(int) == 1
    saida["discount_percent"] = pd.to_numeric(saida["discount_percent"], errors="coerce").fillna(0).astype(int)
    return saida


def transformar_todos(dados: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        "categorias": transformar_categorias(dados["categorias"]),
        "produtos": transformar_produtos(dados["produtos"]),
        "clientes": transformar_clientes(dados["clientes"]),
        "pedidos": transformar_pedidos(dados["pedidos"]),
        "itens_pedido": transformar_itens_pedido(dados["itens_pedido"]),
        "promocoes": transformar_promocoes(dados["promocoes"]),
    }
