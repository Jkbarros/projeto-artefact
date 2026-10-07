"""Fixtures compartilhadas: garante dados processados (sem RAG) para as tools."""

import pytest

from emporio.dados.repositorio import dados_processados_existem, limpar_cache
from emporio.data_prep import executar_pipeline


@pytest.fixture(scope="session", autouse=True)
def _garantir_dados_processados():
    if not dados_processados_existem():
        executar_pipeline(reconstruir_rag=False)
    limpar_cache()
    yield
