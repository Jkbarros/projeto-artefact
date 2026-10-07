"""Extração e divisão do manual de políticas (PDF)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from emporio.config import PASTA_DADOS_BRUTOS
from emporio.texto import limpar_texto_pdf

# Seções principais do manual (títulos aproximados após limpeza do PDF)
_MARCADORES_SECAO: list[tuple[str, str]] = [
    (r"1\.\s+Sobre", "1_sobre_loja"),
    (r"2\.\s+Hor", "2_horario"),
    (r"3\.\s+Formas", "3_pagamento"),
    (r"4\.\s+Pol.tica de Trocas", "4_trocas_devolucoes"),
    (r"5\.\s+Pol.tica de Frete", "5_frete"),
    (r"6\.\s+Promo", "6_promocoes_manual"),
    (r"7\.\s+Atendimento", "7_atendimento_whatsapp"),
    (r"8\.\s+Garantia", "8_garantia"),
    (r"9\.\s+Privacidade", "9_privacidade"),
    (r"10\.\s+Dispos", "10_disposicoes_finais"),
]

_TAMANHO_MAX_CHUNK = 2_500


@dataclass(frozen=True)
class ChunkPolitica:
    chunk_id: str
    secao_id: str
    titulo: str
    texto: str


def resolver_pdf_politicas() -> Path:
    candidatos = list(PASTA_DADOS_BRUTOS.glob("*.pdf"))
    if not candidatos:
        raise FileNotFoundError(f"PDF de políticas não encontrado em {PASTA_DADOS_BRUTOS}")
    return candidatos[0]


def extrair_texto_pdf(caminho: Path | None = None) -> str:
    arquivo = caminho or resolver_pdf_politicas()
    leitor = PdfReader(str(arquivo))
    bruto = "\n".join((pagina.extract_text() or "") for pagina in leitor.pages)
    return limpar_texto_pdf(bruto)


def _encontrar_inicios(texto: str) -> list[tuple[int, str, str]]:
    posicoes: list[tuple[int, str, str]] = []
    for padrao, secao_id in _MARCADORES_SECAO:
        match = re.search(padrao, texto, flags=re.IGNORECASE)
        if match:
            posicoes.append((match.start(), secao_id, padrao))
    posicoes.sort(key=lambda item: item[0])
    return posicoes


def _subdividir_secao(secao_id: str, titulo: str, corpo: str) -> list[ChunkPolitica]:
    if len(corpo) <= _TAMANHO_MAX_CHUNK:
        return [
            ChunkPolitica(
                chunk_id=f"{secao_id}_0",
                secao_id=secao_id,
                titulo=titulo,
                texto=corpo.strip(),
            )
        ]

    partes = re.split(r"(?<=\.)\s+(?=\d+\.\d+\s+)", corpo)
    chunks: list[ChunkPolitica] = []
    buffer = ""
    indice = 0
    for parte in partes:
        candidato = f"{buffer} {parte}".strip() if buffer else parte.strip()
        if len(candidato) > _TAMANHO_MAX_CHUNK and buffer:
            chunks.append(
                ChunkPolitica(
                    chunk_id=f"{secao_id}_{indice}",
                    secao_id=secao_id,
                    titulo=titulo,
                    texto=buffer.strip(),
                )
            )
            indice += 1
            buffer = parte.strip()
        else:
            buffer = candidato
    if buffer.strip():
        chunks.append(
            ChunkPolitica(
                chunk_id=f"{secao_id}_{indice}",
                secao_id=secao_id,
                titulo=titulo,
                texto=buffer.strip(),
            )
        )
    return chunks


def dividir_em_chunks(texto: str) -> list[ChunkPolitica]:
    inicios = _encontrar_inicios(texto)
    if not inicios:
        return [
            ChunkPolitica(
                chunk_id="manual_completo_0",
                secao_id="manual_completo",
                titulo="Manual completo",
                texto=texto,
            )
        ]

    chunks: list[ChunkPolitica] = []
    for indice, (posicao, secao_id, _) in enumerate(inicios):
        fim = inicios[indice + 1][0] if indice + 1 < len(inicios) else len(texto)
        bloco = texto[posicao:fim].strip()
        titulo_match = re.match(r"\d{1,2}\.\s+[^.]+\.?", bloco)
        titulo = titulo_match.group(0) if titulo_match else secao_id
        chunks.extend(_subdividir_secao(secao_id, titulo, bloco))
    return chunks


def carregar_chunks_politicas() -> list[ChunkPolitica]:
    texto = extrair_texto_pdf()
    return dividir_em_chunks(texto)
