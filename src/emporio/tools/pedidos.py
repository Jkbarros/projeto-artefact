"""Ferramenta de consulta de pedido com validação de identidade (privacidade)."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd

from emporio.dados.repositorio import carregar_dados_processados

_MAPA_STATUS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "shipped": "Enviado",
    "delivered": "Entregue",
    "cancelled": "Cancelado",
}


def _pedidos() -> pd.DataFrame:
    return carregar_dados_processados()["pedidos"]


def _itens() -> pd.DataFrame:
    return carregar_dados_processados()["itens_pedido"]


def _clientes() -> pd.DataFrame:
    return carregar_dados_processados()["clientes"]


def _produtos() -> pd.DataFrame:
    return carregar_dados_processados()["produtos"]


def _so_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def _identidade_confere(cliente: pd.Series, identificacao: str) -> bool:
    alvo = (identificacao or "").strip().lower()
    if not alvo:
        return False
    if alvo == str(cliente["email_busca"]).strip().lower():
        return True
    digitos = _so_digitos(identificacao)
    return bool(digitos and digitos[-8:] == str(cliente["telefone_busca"])[-8:])


def consultar_pedido(id_pedido: int, identificacao: str) -> dict[str, Any]:
    """
    Consulta o status de um pedido, exigindo validação de identidade.

    Para proteger a privacidade, só retorna os dados se `identificacao`
    (e-mail OU telefone cadastrado) corresponder ao cliente do pedido.

    Args:
        id_pedido: número do pedido.
        identificacao: e-mail ou telefone do cliente dono do pedido.

    Returns:
        Dados do pedido ou mensagem de erro/validação.
    """
    pedidos = _pedidos()
    achado = pedidos[pedidos["order_id"] == int(id_pedido)]
    if achado.empty:
        return {"encontrado": False, "mensagem": f"Pedido {id_pedido} não encontrado."}

    pedido = achado.iloc[0]
    clientes = _clientes()
    cliente_rows = clientes[clientes["customer_id"] == int(pedido["customer_id"])]
    if cliente_rows.empty:
        return {"encontrado": False, "mensagem": "Cliente do pedido não localizado."}
    cliente = cliente_rows.iloc[0]

    if not _identidade_confere(cliente, identificacao):
        return {
            "encontrado": True,
            "autorizado": False,
            "mensagem": (
                "Não foi possível validar sua identidade. Para proteger seus dados, "
                "informe o e-mail ou telefone cadastrado no pedido."
            ),
        }

    itens = _itens()
    produtos = _produtos()
    itens_pedido = itens[itens["order_id"] == int(id_pedido)].merge(
        produtos[["product_id", "name", "price_brl"]], on="product_id", how="left"
    )
    lista_itens = [
        {
            "product_id": int(r["product_id"]),
            "nome": str(r["name"]) if pd.notna(r["name"]) else None,
            "quantidade": int(r["quantity"]),
        }
        for _, r in itens_pedido.iterrows()
    ]

    status = str(pedido["status"])
    data_pedido = pedido["order_date"]
    entrega = pedido["estimated_delivery"]
    rastreio = pedido["tracking_code"]

    return {
        "encontrado": True,
        "autorizado": True,
        "pedido": {
            "id_pedido": int(pedido["order_id"]),
            "status": _MAPA_STATUS.get(status, status),
            "status_codigo": status,
            "data_pedido": data_pedido.date().isoformat() if pd.notna(data_pedido) else None,
            "entrega_estimada": entrega.date().isoformat() if pd.notna(entrega) else None,
            "codigo_rastreio": str(rastreio) if pd.notna(rastreio) and str(rastreio).strip() else None,
            "forma_pagamento": str(pedido["payment_method_label"]),
            "total_brl": round(float(pedido["total_brl"]), 2) if pd.notna(pedido["total_brl"]) else None,
            "itens": lista_itens,
        },
    }
