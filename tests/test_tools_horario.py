from datetime import datetime
from zoneinfo import ZoneInfo

from emporio.tools.horario import FUSO_LOJA, loja_aberta_agora


def test_segunda_de_manha_aberta():
    momento = datetime(2026, 10, 5, 10, 0, tzinfo=FUSO_LOJA)  # segunda
    r = loja_aberta_agora(momento)
    assert r["aberta"] is True
    assert r["horario_hoje"] == "09:00 às 18:00"


def test_domingo_fechada():
    momento = datetime(2026, 10, 4, 10, 0, tzinfo=FUSO_LOJA)  # domingo
    r = loja_aberta_agora(momento)
    assert r["aberta"] is False
    assert r["horario_hoje"] == "Fechado"


def test_sabado_a_tarde_fechada():
    momento = datetime(2026, 10, 3, 15, 0, tzinfo=FUSO_LOJA)  # sábado 15h
    r = loja_aberta_agora(momento)
    assert r["aberta"] is False


def test_fora_do_horario_noite():
    momento = datetime(2026, 10, 5, 20, 0, tzinfo=ZoneInfo("America/Campo_Grande"))
    r = loja_aberta_agora(momento)
    assert r["aberta"] is False
