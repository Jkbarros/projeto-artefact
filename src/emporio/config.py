"""Configuração do projeto (variáveis de ambiente e caminhos)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_DADOS_BRUTOS = RAIZ_PROJETO / "data" / "raw"
PASTA_DADOS_PROCESSADOS = RAIZ_PROJETO / "data" / "processed"

MODELO_OPENAI_PADRAO = "gpt-4o-mini"
MODELO_EMBEDDING_PADRAO = "text-embedding-3-small"
PASTA_CHROMA = PASTA_DADOS_PROCESSADOS / "chroma"
NOME_COLECAO_POLITICAS = "politicas_loja"
ARQUIVO_MANIFESTO = PASTA_DADOS_PROCESSADOS / "manifesto.json"


def carregar_configuracao() -> None:
    """Carrega o arquivo `.env` na raiz do projeto, se existir."""
    load_dotenv(RAIZ_PROJETO / ".env", override=False)


def obter_chave_openai() -> str:
    carregar_configuracao()
    chave = os.getenv("OPENAI_API_KEY")
    if not chave or not chave.strip():
        raise ValueError(
            "Chave da API não encontrada. Defina OPENAI_API_KEY no arquivo .env "
            "(veja .env.example). Nunca commite a chave."
        )
    return chave.strip()


def obter_modelo_openai() -> str:
    carregar_configuracao()
    return os.getenv("OPENAI_MODEL", MODELO_OPENAI_PADRAO).strip()
