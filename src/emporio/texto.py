"""Utilitários de normalização de texto para busca e RAG."""

from __future__ import annotations

import re
import unicodedata


def remover_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def normalizar_para_busca(texto: str) -> str:
    """Minúsculas, sem acento e espaços extras — uso em busca de produtos."""
    if not texto or not str(texto).strip():
        return ""
    limpo = remover_acentos(str(texto).strip().lower())
    return re.sub(r"\s+", " ", limpo)


def limpar_texto_pdf(texto_bruto: str) -> str:
    """Junta quebras artificiais do pypdf em texto contínuo legível."""
    texto = re.sub(r"\s+", " ", texto_bruto)
    return texto.strip()
