from emporio.prompts import NOME_ATENDENTE, obter_system_prompt
from emporio.tools.registro import executar_ferramenta


def test_system_prompt_menciona_atendente():
    prompt = obter_system_prompt()
    assert NOME_ATENDENTE in prompt
    assert "ferramenta" in prompt.lower() or "consultar" in prompt.lower()


def test_system_prompt_ingles():
    prompt = obter_system_prompt("en")
    assert "English" in prompt


def test_system_prompt_idioma_invalido_cai_no_padrao():
    prompt = obter_system_prompt("zz")
    assert "português" in prompt.lower()


def test_despacho_buscar_produtos():
    r = executar_ferramenta(
        "buscar_produtos",
        {"categoria": "violões", "preco_max": 1000, "limite": 3},
    )
    assert "produtos" in r
    assert r["total"] >= 1


def test_despacho_ferramenta_desconhecida():
    r = executar_ferramenta("nao_existe", {})
    assert "erro" in r
