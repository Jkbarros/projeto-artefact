"""Camada fina de acesso à OpenAI (SDK oficial `openai`)."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from openai import APIError, OpenAI, RateLimitError

from emporio.config import obter_chave_openai, obter_modelo_openai

if TYPE_CHECKING:
    pass


class ErroLimiteTaxa(Exception):
    """API retornou limite de taxa após tentativas de retry."""


class ErroLLM(Exception):
    """Falha ao chamar o provedor de LLM."""


class ErroSaldoInsuficiente(ErroLLM):
    """Conta OpenAI sem crédito ou cota esgotada (não adianta tentar de novo)."""


def _sem_credito_openai(erro: BaseException) -> bool:
    """Distingue 429 por quota zerada de 429 por rate limit temporário."""
    texto = str(erro).lower()
    if "insufficient_quota" in texto or "credit_balance_exhausted" in texto:
        return True
    if "no credits remaining" in texto:
        return True
    corpo = getattr(erro, "body", None)
    if isinstance(corpo, dict):
        detalhe = corpo.get("error") or {}
        if detalhe.get("code") == "credit_balance_exhausted":
            return True
        if detalhe.get("type") == "insufficient_quota":
            return True
    return False


def criar_cliente() -> OpenAI:
    return OpenAI(api_key=obter_chave_openai())


def gerar_texto(
    mensagem: str,
    *,
    modelo: str | None = None,
    tentativas_maximas: int = 4,
    atraso_inicial_segundos: float = 1.0,
) -> str:
    """
    Envia um prompt simples à OpenAI e devolve o texto da resposta.

    Faz retry com backoff exponencial em erros de rate limit.
    """
    cliente = criar_cliente()
    nome_modelo = modelo or obter_modelo_openai()
    atraso = atraso_inicial_segundos
    ultimo_erro: Exception | None = None

    for tentativa in range(1, tentativas_maximas + 1):
        try:
            resposta = cliente.chat.completions.create(
                model=nome_modelo,
                messages=[{"role": "user", "content": mensagem}],
            )
            texto = resposta.choices[0].message.content
            if texto is None or not str(texto).strip():
                raise ErroLLM("O modelo não retornou texto na resposta.")
            return str(texto).strip()
        except RateLimitError as erro:
            ultimo_erro = erro
            if _sem_credito_openai(erro):
                raise ErroSaldoInsuficiente(
                    "Sua conta OpenAI está sem créditos (credit_balance_exhausted). "
                    "Adicione saldo em https://platform.openai.com/settings/organization/billing "
                    "ou use outro provedor de LLM no .env."
                ) from erro
            if tentativa < tentativas_maximas:
                time.sleep(atraso)
                atraso *= 2
                continue
            raise ErroLimiteTaxa(
                "Limite de requisições atingido. Tente novamente em alguns instantes."
            ) from erro
        except APIError as erro:
            ultimo_erro = erro
            if _sem_credito_openai(erro):
                raise ErroSaldoInsuficiente(
                    "Sua conta OpenAI está sem créditos. "
                    "Veja https://platform.openai.com/settings/organization/billing"
                ) from erro
            codigo = getattr(erro, "status_code", None)
            if codigo in (429, 503) and tentativa < tentativas_maximas:
                time.sleep(atraso)
                atraso *= 2
                continue
            raise ErroLLM(f"Erro na API OpenAI: {erro}") from erro
        except Exception as erro:
            ultimo_erro = erro
            mensagem_erro = str(erro).lower()
            if "rate" in mensagem_erro or "429" in mensagem_erro:
                if tentativa < tentativas_maximas:
                    time.sleep(atraso)
                    atraso *= 2
                    continue
                raise ErroLimiteTaxa(
                    "Limite de requisições atingido. Tente novamente em alguns instantes."
                ) from erro
            raise ErroLLM(f"Falha ao chamar a OpenAI: {erro}") from erro

    raise ErroLimiteTaxa(
        f"Limite de requisições após {tentativas_maximas} tentativas."
    ) from ultimo_erro
