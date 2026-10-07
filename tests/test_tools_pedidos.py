from emporio.tools.pedidos import consultar_pedido


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
