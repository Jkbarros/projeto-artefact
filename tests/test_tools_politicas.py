from emporio.tools.politicas import consultar_politicas


def test_pergunta_vazia_nao_consulta_indice():
    r = consultar_politicas("")
    assert r["trechos"] == []
