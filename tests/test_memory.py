from emporio.memory import (
    apagar_sessao,
    carregar_historico,
    historico_para_contexto,
    listar_sessoes,
    salvar_mensagem,
)


def test_salvar_e_carregar(tmp_path):
    banco = tmp_path / "conversas.db"
    salvar_mensagem("s1", "user", "oi", caminho=banco)
    salvar_mensagem("s1", "assistant", "olá!", caminho=banco)

    hist = carregar_historico("s1", caminho=banco)
    assert hist == [
        {"role": "user", "content": "oi"},
        {"role": "assistant", "content": "olá!"},
    ]


def test_limite_de_contexto(tmp_path):
    banco = tmp_path / "conversas.db"
    for i in range(20):
        salvar_mensagem("s1", "user", f"m{i}", caminho=banco)
    ctx = historico_para_contexto("s1", limite=5, caminho=banco)
    assert len(ctx) == 5
    assert ctx[-1]["content"] == "m19"


def test_listar_e_apagar(tmp_path):
    banco = tmp_path / "conversas.db"
    salvar_mensagem("s1", "user", "a", caminho=banco)
    salvar_mensagem("s2", "user", "b", caminho=banco)
    assert len(listar_sessoes(caminho=banco)) == 2

    apagar_sessao("s1", caminho=banco)
    restantes = {s["session_id"] for s in listar_sessoes(caminho=banco)}
    assert restantes == {"s2"}
