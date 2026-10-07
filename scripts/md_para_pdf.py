"""Converte Markdown simples (docs de perguntas) em PDF com fonte do sistema."""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

LARGURA_UTIL = A4[0] - 30 * mm
FONT_REGULAR = "ArialUnicode"
FONT_BOLD = "ArialUnicode-Bold"


def _registrar_fontes() -> None:
    pasta = Path(r"C:\Windows\Fonts")
    regular = pasta / "arial.ttf"
    bold = pasta / "arialbd.ttf"
    if not regular.is_file():
        raise FileNotFoundError("Fonte Arial não encontrada em C:\\Windows\\Fonts")
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(regular)))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold)))


def _limpar_inline(texto: str) -> str:
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    texto = texto.replace("`", "")
    return texto.strip()


def _quebrar_linhas(canvas_obj: canvas.Canvas, texto: str, fonte: str, tamanho: float) -> list[str]:
    canvas_obj.setFont(fonte, tamanho)
    palavras = texto.split()
    if not palavras:
        return [""]
    linhas: list[str] = []
    atual = ""
    for palavra in palavras:
        candidato = f"{atual} {palavra}".strip()
        if canvas_obj.stringWidth(candidato, fonte, tamanho) <= LARGURA_UTIL:
            atual = candidato
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas or [""]


def md_para_pdf(caminho_md: Path, caminho_pdf: Path) -> None:
    _registrar_fontes()
    linhas_md = caminho_md.read_text(encoding="utf-8").splitlines()

    c = canvas.Canvas(str(caminho_pdf), pagesize=A4)
    y = A4[1] - 20 * mm
    margem_inferior = 15 * mm

    def nova_pagina() -> None:
        nonlocal y
        c.showPage()
        y = A4[1] - 20 * mm

    def avancar(altura: float) -> None:
        nonlocal y
        y -= altura
        if y < margem_inferior:
            nova_pagina()

    def escrever(texto: str, tamanho: float, negrito: bool = False) -> None:
        fonte = FONT_BOLD if negrito else FONT_REGULAR
        for linha in _quebrar_linhas(c, _limpar_inline(texto), fonte, tamanho):
            avancar(tamanho * 0.45)
            c.setFont(fonte, tamanho)
            c.drawString(15 * mm, y, linha)

    for raw in linhas_md:
        linha = raw.rstrip()
        if not linha:
            avancar(4)
            continue
        if linha.strip() == "---":
            avancar(6)
            continue
        if linha.startswith("# "):
            escrever(linha[2:], 16, negrito=True)
            avancar(4)
            continue
        if linha.startswith("## "):
            escrever(linha[3:], 13, negrito=True)
            avancar(2)
            continue
        if linha.startswith("### "):
            escrever(linha[4:], 11, negrito=True)
            avancar(2)
            continue
        if re.match(r"^\|.+\|$", linha) and not re.match(r"^\|[-:\s|]+\|$", linha):
            escrever(linha.replace("|", "  |  "), 8)
            continue
        if re.match(r"^\|[-:\s|]+\|$", linha):
            continue
        if linha.startswith("- "):
            escrever("• " + linha[2:], 10)
            continue
        if linha.startswith("| "):
            escrever(linha, 8)
            continue
        escrever(linha, 10)

    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Markdown → PDF (tabelas em texto)")
    parser.add_argument("entrada", type=Path, nargs="+", help="Arquivo(s) .md")
    parser.add_argument(
        "-o",
        "--saida",
        type=Path,
        help="PDF de saída (só com um arquivo); padrão: mesmo nome .pdf",
    )
    args = parser.parse_args()

    if len(args.entrada) > 1 and args.saida:
        parser.error("Use --saida apenas com um arquivo de entrada.")

    for md in args.entrada:
        pdf = args.saida if args.saida and len(args.entrada) == 1 else md.with_suffix(".pdf")
        md_para_pdf(md, pdf)
        print(f"Gerado: {pdf}")


if __name__ == "__main__":
    main()
