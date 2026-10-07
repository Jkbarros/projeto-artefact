"""Ferramenta de consulta ao manual de políticas (RAG sobre o PDF)."""

from __future__ import annotations

from typing import Any

from emporio.rag.indice_politicas import consultar_politicas_indice


def consultar_politicas(pergunta: str, quantidade: int = 3) -> dict[str, Any]:
    """
    Busca no manual de políticas da loja os trechos mais relevantes à pergunta.

    Use para dúvidas sobre horário, endereço, formas de pagamento, trocas,
    devoluções, garantia, frete, privacidade e atendimento.

    Args:
        pergunta: dúvida do cliente em linguagem natural.
        quantidade: número de trechos a recuperar (padrão 3).

    Returns:
        Trechos do manual com seção e título, para o agente fundamentar a resposta.
    """
    if not pergunta or not pergunta.strip():
        return {"trechos": [], "mensagem": "Pergunta vazia."}

    try:
        resultados = consultar_politicas_indice(pergunta, quantidade=max(1, int(quantidade)))
    except FileNotFoundError as erro:
        return {"trechos": [], "erro": str(erro)}

    if not resultados:
        return {
            "trechos": [],
            "mensagem": "Não encontrei esse assunto no manual de políticas.",
        }

    trechos = [
        {
            "titulo": r.get("titulo"),
            "secao_id": r.get("secao_id"),
            "texto": r.get("texto"),
        }
        for r in resultados
    ]
    return {"trechos": trechos, "total": len(trechos)}
