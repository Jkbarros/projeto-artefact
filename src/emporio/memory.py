"""Persistência do histórico de conversas em SQLite (por session_id)."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from emporio.config import ARQUIVO_HISTORICO, MAX_MENSAGENS_CONTEXTO

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    papel TEXT NOT NULL CHECK (papel IN ('user', 'assistant')),
    conteudo TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sessao ON mensagens(session_id, id);
"""


def _caminho_banco(caminho: Path | None = None) -> Path:
    destino = caminho or ARQUIVO_HISTORICO
    destino.parent.mkdir(parents=True, exist_ok=True)
    return destino


@contextmanager
def _conexao(caminho: Path | None = None):
    conn = sqlite3.connect(_caminho_banco(caminho))
    try:
        conn.executescript(_ESQUEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def salvar_mensagem(session_id: str, papel: str, conteudo: str, caminho: Path | None = None) -> None:
    with _conexao(caminho) as conn:
        conn.execute(
            "INSERT INTO mensagens (session_id, papel, conteudo) VALUES (?, ?, ?)",
            (session_id, papel, conteudo),
        )


def carregar_historico(session_id: str, caminho: Path | None = None) -> list[dict[str, str]]:
    """Todas as mensagens da sessão (ordem cronológica), estilo OpenAI."""
    with _conexao(caminho) as conn:
        linhas = conn.execute(
            "SELECT papel, conteudo FROM mensagens WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
    return [{"role": papel, "content": conteudo} for papel, conteudo in linhas]


def historico_para_contexto(
    session_id: str,
    limite: int = MAX_MENSAGENS_CONTEXTO,
    caminho: Path | None = None,
) -> list[dict[str, str]]:
    """Últimas N mensagens, para limitar custo/contexto enviado ao modelo."""
    completo = carregar_historico(session_id, caminho)
    return completo[-limite:] if limite > 0 else completo


def listar_sessoes(caminho: Path | None = None) -> list[dict[str, str]]:
    """Sessões existentes com a 1ª mensagem como resumo e data."""
    with _conexao(caminho) as conn:
        linhas = conn.execute(
            """
            SELECT session_id,
                   MIN(criado_em) AS inicio,
                   COUNT(*) AS total
            FROM mensagens
            GROUP BY session_id
            ORDER BY inicio DESC
            """
        ).fetchall()
    return [
        {"session_id": s, "inicio": inicio, "total": total}
        for s, inicio, total in linhas
    ]


def apagar_sessao(session_id: str, caminho: Path | None = None) -> None:
    with _conexao(caminho) as conn:
        conn.execute("DELETE FROM mensagens WHERE session_id = ?", (session_id,))
