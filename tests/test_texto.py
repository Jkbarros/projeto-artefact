from emporio.texto import normalizar_para_busca


def test_normalizar_para_busca_remove_acento():
    assert normalizar_para_busca("Violão Takamine") == "violao takamine"
