"""Ferramenta de horário de funcionamento (fuso America/Campo_Grande).

Os horários vêm do manual de políticas (seção 2):
- Segunda a Sexta: 09:00 às 18:00
- Sábado: 09:00 às 13:00
- Domingo e Feriados: Fechado

Feriados não estão listados no manual; ver suposições.
"""

from __future__ import annotations

from datetime import datetime, time
from typing import Any
from zoneinfo import ZoneInfo

FUSO_LOJA = ZoneInfo("America/Campo_Grande")

# índice: 0 = segunda ... 6 = domingo
_HORARIOS: dict[int, tuple[time, time] | None] = {
    0: (time(9, 0), time(18, 0)),
    1: (time(9, 0), time(18, 0)),
    2: (time(9, 0), time(18, 0)),
    3: (time(9, 0), time(18, 0)),
    4: (time(9, 0), time(18, 0)),
    5: (time(9, 0), time(13, 0)),
    6: None,
}

_NOME_DIA = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo",
}


def loja_aberta_agora(momento: datetime | None = None) -> dict[str, Any]:
    """
    Informa se a loja está aberta no horário de Campo Grande/MS.

    Args:
        momento: datetime opcional (para testes). Padrão: agora no fuso da loja.

    Returns:
        Status de abertura, horário do dia e observação sobre feriados.
    """
    agora = momento.astimezone(FUSO_LOJA) if momento else datetime.now(FUSO_LOJA)
    dia = agora.weekday()
    faixa = _HORARIOS[dia]

    base = {
        "dia_semana": _NOME_DIA[dia],
        "horario_consultado": agora.strftime("%Y-%m-%d %H:%M"),
        "observacao": (
            "Domingos e feriados a loja fica fechada. Feriados não constam no "
            "manual, então não são considerados automaticamente."
        ),
    }

    if faixa is None:
        return {**base, "aberta": False, "horario_hoje": "Fechado"}

    abertura, fechamento = faixa
    aberta = abertura <= agora.time() <= fechamento
    return {
        **base,
        "aberta": aberta,
        "horario_hoje": f"{abertura.strftime('%H:%M')} às {fechamento.strftime('%H:%M')}",
    }
