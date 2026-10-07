"""Ferramentas consultáveis pelo agente (function calling)."""

from emporio.tools.horario import loja_aberta_agora
from emporio.tools.pedidos import consultar_pedido
from emporio.tools.politicas import consultar_politicas
from emporio.tools.produtos import (
    buscar_produtos,
    consultar_produto,
    consultar_promocoes,
)

__all__ = [
    "buscar_produtos",
    "consultar_pedido",
    "consultar_politicas",
    "consultar_produto",
    "consultar_promocoes",
    "loja_aberta_agora",
]
