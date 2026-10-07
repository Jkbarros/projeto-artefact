import json

import pandas as pd

from emporio.config import ARQUIVO_MANIFESTO
from emporio.dados.repositorio import (
    carregar_dados_processados,
    dados_processados_existem,
    limpar_cache,
)
from emporio.dados.transformar import transformar_produtos
from emporio.data_prep import executar_pipeline


def test_transformar_produtos_tipos():
    brutos = pd.DataFrame(
        {
            "product_id": [1],
            "price_brl": ["99.9"],
            "name": ["Teste"],
            "category_id": [5],
            "description": ["desc"],
            "stock_quantity": [3],
            "status": ["active"],
            "specs": ['{"a":1}'],
            "created_at": ["2021-01-01"],
        }
    )
    saida = transformar_produtos(brutos)
    assert saida.loc[0, "price_brl"] == 99.9
    assert saida.loc[0, "nome_busca"] == "teste"


def test_pipeline_sem_rag():
    executar_pipeline(reconstruir_rag=False)
    assert dados_processados_existem()
    assert ARQUIVO_MANIFESTO.is_file()
    manifesto = json.loads(ARQUIVO_MANIFESTO.read_text(encoding="utf-8"))
    assert manifesto["tabelas"]["produtos"] == 65
    limpar_cache()
    produtos = carregar_dados_processados()["produtos"]
    assert produtos["price_brl"].notna().all()
    assert (produtos["stock_quantity"] >= 0).all()
