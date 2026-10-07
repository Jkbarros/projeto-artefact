"""Schemas OpenAI e despacho das ferramentas Python."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from emporio.tools.horario import loja_aberta_agora
from emporio.tools.pedidos import consultar_pedido, listar_pedidos_do_cliente
from emporio.tools.politicas import consultar_politicas
from emporio.tools.produtos import (
    buscar_produtos,
    consultar_produto,
    consultar_promocoes,
)

FERRAMENTAS_OPENAI: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "buscar_produtos",
            "description": (
                "Busca produtos no catálogo com filtros opcionais (nome, categoria, preço). "
                "Use para listagens como violões até um valor ou busca por termo."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termo": {"type": "string", "description": "Texto para buscar no nome/descrição."},
                    "categoria": {
                        "type": "string",
                        "description": "Ex.: violões, guitarras, ukuleles.",
                    },
                    "preco_max": {"type": "number", "description": "Preço máximo em reais."},
                    "preco_min": {"type": "number", "description": "Preço mínimo em reais."},
                    "apenas_disponiveis": {
                        "type": "boolean",
                        "description": "Se true, só produtos ativos com estoque.",
                    },
                    "limite": {"type": "integer", "description": "Máximo de itens (padrão 10)."},
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_produto",
            "description": "Detalhes, preço e estoque de um produto por ID ou nome.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "ID do produto."},
                    "nome": {"type": "string", "description": "Nome ou parte do nome."},
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_promocoes",
            "description": "Lista promoções vigentes com desconto e preço calculado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limite": {"type": "integer", "description": "Máximo de promoções."},
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_pedidos_do_cliente",
            "description": (
                "Lista os números de pedido (id_pedido) do cliente quando ele não sabe "
                "o número, mas informa e-mail ou telefone cadastrado. Não mostra pedidos de terceiros."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "identificacao": {
                        "type": "string",
                        "description": "E-mail ou telefone cadastrado na loja.",
                    },
                    "limite": {"type": "integer", "description": "Máximo de pedidos listados."},
                },
                "required": ["identificacao"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_pedido",
            "description": (
                "Detalhes de um pedido (status, itens, rastreio). Obrigatório id_pedido e "
                "identificacao (e-mail ou telefone). Se o cliente não tiver o número, use "
                "listar_pedidos_do_cliente antes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "id_pedido": {"type": "integer", "description": "Número do pedido."},
                    "identificacao": {
                        "type": "string",
                        "description": "E-mail ou telefone do cliente dono do pedido.",
                    },
                },
                "required": ["id_pedido", "identificacao"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_politicas",
            "description": (
                "Busca trechos do manual: endereço, horários, pagamento, troca, devolução, "
                "frete, garantia, atendimento humano."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pergunta": {"type": "string", "description": "Dúvida do cliente."},
                    "quantidade": {
                        "type": "integer",
                        "description": "Quantos trechos recuperar (padrão 3).",
                    },
                },
                "required": ["pergunta"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "loja_aberta_agora",
            "description": "Verifica se a loja física está aberta no horário de Campo Grande/MS.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
]

_IMPLEMENTACOES: dict[str, Callable[..., dict[str, Any]]] = {
    "buscar_produtos": buscar_produtos,
    "consultar_produto": consultar_produto,
    "consultar_promocoes": consultar_promocoes,
    "listar_pedidos_do_cliente": listar_pedidos_do_cliente,
    "consultar_pedido": consultar_pedido,
    "consultar_politicas": consultar_politicas,
    "loja_aberta_agora": lambda **_: loja_aberta_agora(),
}


def executar_ferramenta(nome: str, argumentos: dict[str, Any] | None) -> dict[str, Any]:
    """Executa uma tool pelo nome (usado pelo agente e pelos testes)."""
    if nome not in _IMPLEMENTACOES:
        return {"erro": f"Ferramenta desconhecida: {nome}"}
    args = argumentos or {}
    try:
        return _IMPLEMENTACOES[nome](**args)
    except TypeError as erro:
        return {"erro": f"Argumentos inválidos para {nome}: {erro}"}
    except Exception as erro:  # noqa: BLE001 — não derrubar o agente por falha de tool
        return {"erro": f"Falha ao executar {nome}: {erro}"}


def argumentos_de_json(texto: str | None) -> dict[str, Any]:
    if not texto or not texto.strip():
        return {}
    try:
        valor = json.loads(texto)
    except json.JSONDecodeError:
        return {}
    return valor if isinstance(valor, dict) else {}
