"""Testes de configuração (sem chamar a API)."""

from emporio.config import PASTA_DADOS_BRUTOS, RAIZ_PROJETO


def test_pastas_do_projeto_existem():
    assert RAIZ_PROJETO.is_dir()
    assert PASTA_DADOS_BRUTOS.is_dir()
