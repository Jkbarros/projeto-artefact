from emporio.tools.produtos import (
    buscar_produtos,
    consultar_produto,
    consultar_promocoes,
)


def test_violoes_ate_mil():
    r = buscar_produtos(categoria="violões", preco_max=1000, limite=50)
    assert r["total"] >= 1
    assert all(p["preco_brl"] <= 1000 for p in r["produtos"])


def test_busca_tolerante_a_acento():
    r = buscar_produtos(categoria="violoes", preco_max=1000)
    assert r["total"] >= 1


def test_consultar_takamine_gd20():
    r = consultar_produto(nome="Takamine GD20")
    assert r["encontrado"] is True
    assert r["product_id"] == 95
    assert r["preco_brl"] == 2199.0


def test_produto_inexistente():
    r = consultar_produto(nome="Instrumento Que Nao Existe XYZ")
    assert r["encontrado"] is False


def test_categoria_invalida():
    r = buscar_produtos(categoria="categoria inexistente")
    assert r["total"] == 0


def test_promocoes_vigentes():
    r = consultar_promocoes()
    assert r["total"] >= 1
    for p in r["promocoes"]:
        assert p["desconto_percent"] > 0
        if p["preco_brl"] is not None:
            assert p["preco_com_desconto_brl"] <= p["preco_brl"]
