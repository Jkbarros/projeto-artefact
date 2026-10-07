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


def _cliente_por_identificacao(identificacao: str) -> pd.Series | None:
    """Localiza o cliente pelo e-mail ou telefone (sem expor outros cadastros)."""
    if not identificacao or not identificacao.strip():
        return None
    clientes = _clientes()
    alvo = identificacao.strip().lower()
    por_email = clientes[clientes["email_busca"] == alvo]
    if not por_email.empty:
        return por_email.iloc[0]
    digitos = _so_digitos(identificacao)
    if len(digitos) >= 8:
        sufixo = digitos[-8:]
        for _, linha in clientes.iterrows():
            if str(linha["telefone_busca"]).endswith(sufixo):
                return linha
    return None


def listar_pedidos_do_cliente(identificacao: str, limite: int = 10) -> dict[str, Any]:
    """
    Lista os números de pedido do cliente após validar e-mail ou telefone.

    Use quando o cliente não souber o número do pedido, mas tiver e-mail/telefone
    cadastrado. Não expõe pedidos de outras pessoas.

    Args:
        identificacao: e-mail ou telefone cadastrado na loja.
        limite: quantidade máxima de pedidos retornados (mais recentes primeiro).

    Returns:
        Lista com id_pedido, data, status e total; ou mensagem se não autorizado.
    """
    cliente = _cliente_por_identificacao(identificacao)
    if cliente is None:
        return {
            "encontrado": False,
            "mensagem": (
                "Não localizamos cadastro com esse e-mail ou telefone. "
                "Confira os dados ou entre em contato com a loja."
            ),
        }

    pedidos = _pedidos()
    do_cliente = pedidos[pedidos["customer_id"] == int(cliente["customer_id"])].copy()
    if do_cliente.empty:
        return {
            "encontrado": True,
            "pedidos": [],
            "total": 0,
            "mensagem": "Não há pedidos vinculados a este cadastro.",
        }

    do_cliente = do_cliente.sort_values("order_date", ascending=False).head(max(1, int(limite)))
    lista = []
    for _, linha in do_cliente.iterrows():
        status = str(linha["status"])
        data = linha["order_date"]
        lista.append(
            {
                "id_pedido": int(linha["order_id"]),
                "data_pedido": data.date().isoformat() if pd.notna(data) else None,
                "status": _MAPA_STATUS.get(status, status),
                "total_brl": round(float(linha["total_brl"]), 2)
                if pd.notna(linha["total_brl"])
                else None,
            }
        )
    return {
        "encontrado": True,
        "pedidos": lista,
        "total": int(len(lista)),
        "mensagem": (
            "Use o número id_pedido com consultar_pedido e a mesma identificação "
            "para ver detalhes, itens e rastreio."
        ),
    }


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
