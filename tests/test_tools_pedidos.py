from emporio.tools.pedidos import consultar_pedido, listar_pedidos_do_cliente


def test_listar_pedidos_retorna_numeros():
    r = listar_pedidos_do_cliente("pedro.oliveira@jmail.com")
    assert r["encontrado"] is True
    assert r["total"] >= 1
    assert any(p["id_pedido"] == 1 for p in r["pedidos"])


def test_listar_pedidos_identidade_invalida():
    r = listar_pedidos_do_cliente("naoexiste@email.com")
    assert r["encontrado"] is False


def test_pedido_com_email_correto():
    r = consultar_pedido(id_pedido=1, identificacao="pedro.oliveira@jmail.com")
    assert r["autorizado"] is True
    assert r["pedido"]["id_pedido"] == 1
    assert r["pedido"]["status_codigo"] in {
        "pending", "confirmed", "shipped", "delivered", "cancelled"
    }


def test_pedido_com_telefone_correto():
    r = consultar_pedido(id_pedido=1, identificacao="(67) 98432-1098")
    assert r["autorizado"] is True


def test_pedido_identidade_invalida():
    r = consultar_pedido(id_pedido=1, identificacao="errado@email.com")
    assert r["autorizado"] is False
    assert "pedido" not in r


def test_pedido_inexistente():
    r = consultar_pedido(id_pedido=99999, identificacao="qualquer@email.com")
    assert r["encontrado"] is False
