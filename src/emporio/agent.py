"""Loop do agente com function calling da OpenAI."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from openai import APIError, OpenAI, RateLimitError

from emporio.config import obter_chave_openai, obter_modelo_openai
from emporio.llm import (
    ErroLimiteTaxa,
    ErroLLM,
    _sem_credito_openai,
)
from emporio.prompts import obter_system_prompt
from emporio.tools.registro import (
    FERRAMENTAS_OPENAI,
    argumentos_de_json,
    executar_ferramenta,
)

MAX_ITERACOES_FERRAMENTAS = 8


@dataclass
class RegistroFerramenta:
    nome: str
    argumentos: dict[str, Any]
    resultado: dict[str, Any]


@dataclass
class RespostaAgente:
    texto: str
    ferramentas: list[RegistroFerramenta] = field(default_factory=list)
    erro: bool = False


def _mensagem_assistente_para_dict(mensagem: Any) -> dict[str, Any]:
    dados: dict[str, Any] = {"role": "assistant", "content": mensagem.content}
    if mensagem.tool_calls:
        dados["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in mensagem.tool_calls
        ]
    return dados


def responder(
    mensagem_usuario: str,
    historico: list[dict[str, str]] | None = None,
    *,
    modelo: str | None = None,
) -> RespostaAgente:
    """
    Processa uma mensagem do cliente e devolve a resposta final do agente.

    `historico` deve ser lista OpenAI-style (user/assistant), sem system.
    """
    cliente = OpenAI(api_key=obter_chave_openai())
    nome_modelo = modelo or obter_modelo_openai()
    mensagens: list[dict[str, Any]] = [
        {"role": "system", "content": obter_system_prompt()},
        *(historico or []),
        {"role": "user", "content": mensagem_usuario},
    ]
    log: list[RegistroFerramenta] = []

    for _ in range(MAX_ITERACOES_FERRAMENTAS):
        try:
            resposta = cliente.chat.completions.create(
                model=nome_modelo,
                messages=mensagens,
                tools=FERRAMENTAS_OPENAI,
                tool_choice="auto",
            )
        except RateLimitError as erro:
            if _sem_credito_openai(erro):
                return RespostaAgente(
                    texto=(
                        "No momento não consigo acessar o serviço de IA (sem créditos na API). "
                        "Tente mais tarde ou contate a loja pelo (67) 3341-4444."
                    ),
                    ferramentas=log,
                    erro=True,
                )
            raise ErroLimiteTaxa(
                "Limite de requisições atingido. Tente novamente em instantes."
            ) from erro
        except APIError as erro:
            if _sem_credito_openai(erro):
                return RespostaAgente(
                    texto="Serviço de IA indisponível. Por favor, tente mais tarde.",
                    ferramentas=log,
                    erro=True,
                )
            raise ErroLLM(f"Erro na API OpenAI: {erro}") from erro

        escolha = resposta.choices[0].message

        if escolha.tool_calls:
            mensagens.append(_mensagem_assistente_para_dict(escolha))
            for chamada in escolha.tool_calls:
                nome = chamada.function.name
                args = argumentos_de_json(chamada.function.arguments)
                resultado = executar_ferramenta(nome, args)
                log.append(
                    RegistroFerramenta(nome=nome, argumentos=args, resultado=resultado)
                )
                mensagens.append(
                    {
                        "role": "tool",
                        "tool_call_id": chamada.id,
                        "content": json.dumps(resultado, ensure_ascii=False),
                    }
                )
            continue

        texto = escolha.content
        if texto is None or not str(texto).strip():
            return RespostaAgente(
                texto="Desculpe, não consegui formular uma resposta. Pode reformular?",
                ferramentas=log,
                erro=True,
            )
        return RespostaAgente(texto=str(texto).strip(), ferramentas=log)

    return RespostaAgente(
        texto=(
            "Precisei de muitas consultas e não consegui fechar sua resposta. "
            "Pode simplificar a pergunta ou ligar para (67) 3341-4444?"
        ),
        ferramentas=log,
        erro=True,
    )
