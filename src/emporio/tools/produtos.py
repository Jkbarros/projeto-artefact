"""Ferramentas de catálogo: busca, detalhe e promoção de produtos (Pandas)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from emporio.dados.repositorio import carregar_dados_processados
from emporio.texto import normalizar_para_busca

# Mapa auxiliar de sinônimos comuns para nomes de categoria.
_SINONIMOS_CATEGORIA = {
    "violao": "violoes",
    "violoes": "violoes",
    "guitarra": "guitarras",
    "guitarras": "guitarras",
    "baixo": "baixos",
    "baixos": "baixos",
    "bateria": "baterias e percussao",
    "teclado": "teclados e pianos",
    "piano": "teclados e pianos",
    "ukulele": "ukuleles",
}


def _produtos() -> pd.DataFrame:
    return carregar_dados_processados()["produtos"]


def _categorias() -> pd.DataFrame:
    return carregar_dados_processados()["categorias"]


def _promocoes() -> pd.DataFrame:
    return carregar_dados_processados()["promocoes"]


def _promocao_vigente_do_produto(product_id: int) -> dict[str, Any] | None:
    promo = _promocoes()
    ativas = promo[(promo["product_id"] == product_id) & (promo["vigente"])]
    if ativas.empty:
        return None
    linha = ativas.sort_values("discount_percent", ascending=False).iloc[0]
    return {
        "promotion_id": int(linha["promotion_id"]),
        "discount_percent": int(linha["discount_percent"]),
        "description": str(linha["description"]),
    }


def _resolver_categoria_id(categoria: str | None) -> int | None:
    if not categoria or not categoria.strip():
        return None
    chave = normalizar_para_busca(categoria)
    chave = _SINONIMOS_CATEGORIA.get(chave, chave)
    cats = _categorias()
    correspondencia = cats[cats["nome_busca"] == chave]
    if correspondencia.empty:
        correspondencia = cats[cats["nome_busca"].str.contains(chave, na=False)]
    if correspondencia.empty:
        return None
    return int(correspondencia.iloc[0]["category_id"])


def _formatar_produto(linha: pd.Series, incluir_promocao: bool = True) -> dict[str, Any]:
    product_id = int(linha["product_id"])
    preco = float(linha["price_brl"])
    item: dict[str, Any] = {
        "product_id": product_id,
        "nome": str(linha["name"]),
        "preco_brl": round(preco, 2),
        "estoque": int(linha["stock_quantity"]),
        "disponivel": int(linha["stock_quantity"]) > 0 and str(linha["status"]) == "active",
        "status": str(linha["status"]),
    }
    if incluir_promocao:
        promo = _promocao_vigente_do_produto(product_id)
        if promo:
            preco_final = round(preco * (1 - promo["discount_percent"] / 100), 2)
            item["promocao"] = {
                "desconto_percent": promo["discount_percent"],
                "descricao": promo["description"],
                "preco_com_desconto_brl": preco_final,
            }
    return item


def buscar_produtos(
    termo: str | None = None,
    categoria: str | None = None,
    preco_max: float | None = None,
    preco_min: float | None = None,
    apenas_disponiveis: bool = False,
    limite: int = 10,
) -> dict[str, Any]:
    """
    Busca produtos no catálogo com filtros opcionais.

    Args:
        termo: texto livre para casar com nome/descrição (tolerante a acentos).
        categoria: nome da categoria (ex.: "violões", "guitarras").
        preco_max: preço máximo em reais.
        preco_min: preço mínimo em reais.
        apenas_disponiveis: se True, retorna só itens ativos com estoque > 0.
        limite: número máximo de produtos retornados.

    Returns:
        Dicionário com a lista de produtos encontrados e a contagem total.
    """
    df = _produtos().copy()

    categoria_id = _resolver_categoria_id(categoria)
    if categoria and categoria_id is None:
        return {
            "produtos": [],
            "total": 0,
            "mensagem": f"Categoria '{categoria}' não encontrada no catálogo.",
        }
    if categoria_id is not None:
        df = df[df["category_id"] == categoria_id]

    if termo and termo.strip():
        alvo = normalizar_para_busca(termo)
        mascara = df["nome_busca"].str.contains(alvo, na=False) | df[
            "descricao_busca"
        ].str.contains(alvo, na=False)
        df = df[mascara]

    if preco_max is not None:
        df = df[df["price_brl"] <= float(preco_max)]
    if preco_min is not None:
        df = df[df["price_brl"] >= float(preco_min)]
    if apenas_disponiveis:
        df = df[(df["stock_quantity"] > 0) & (df["status"] == "active")]

    total = len(df)
    df = df.sort_values("price_brl").head(max(1, int(limite)))
    produtos = [_formatar_produto(linha) for _, linha in df.iterrows()]

    resultado: dict[str, Any] = {"produtos": produtos, "total": total}
    if total == 0:
        resultado["mensagem"] = "Nenhum produto encontrado com esses critérios."
    return resultado


def consultar_produto(
    product_id: int | None = None, nome: str | None = None
) -> dict[str, Any]:
    """
    Retorna detalhes de um produto por ID ou nome (preço, estoque e promoção).

    Args:
        product_id: identificador do produto.
        nome: nome (ou parte do nome) do produto.

    Returns:
        Detalhes do produto ou mensagem de não encontrado.
    """
    df = _produtos()

    if product_id is not None:
        achado = df[df["product_id"] == int(product_id)]
    elif nome and nome.strip():
        alvo = normalizar_para_busca(nome)
        achado = df[df["nome_busca"].str.contains(alvo, na=False)]
    else:
        return {"encontrado": False, "mensagem": "Informe product_id ou nome."}

    if achado.empty:
        return {"encontrado": False, "mensagem": "Produto não encontrado."}

    if len(achado) > 1 and product_id is None:
        opcoes = [
            {"product_id": int(r["product_id"]), "nome": str(r["name"]),
             "preco_brl": round(float(r["price_brl"]), 2)}
            for _, r in achado.sort_values("price_brl").head(5).iterrows()
        ]
        return {
            "encontrado": False,
            "ambiguo": True,
            "mensagem": "Vários produtos correspondem ao nome. Especifique melhor.",
            "opcoes": opcoes,
        }

    item = _formatar_produto(achado.iloc[0])
    item["encontrado"] = True
    descricao = achado.iloc[0].get("description")
    if isinstance(descricao, str) and descricao.strip():
        item["descricao"] = descricao
    return item


def consultar_promocoes(limite: int = 20) -> dict[str, Any]:
    """
    Lista as promoções vigentes (is_active) com o preço já calculado.

    Returns:
        Lista de promoções vigentes e contagem.
    """
    promo = _promocoes()
    produtos = _produtos()
    vigentes = promo[promo["vigente"]]
    if vigentes.empty:
        return {"promocoes": [], "total": 0, "mensagem": "Não há promoções vigentes."}

    juntos = vigentes.merge(
        produtos[["product_id", "name", "price_brl", "stock_quantity", "status"]],
        on="product_id",
        how="left",
    )
    lista: list[dict[str, Any]] = []
    for _, r in juntos.sort_values("discount_percent", ascending=False).head(limite).iterrows():
        preco = float(r["price_brl"]) if pd.notna(r["price_brl"]) else None
        desconto = int(r["discount_percent"])
        item = {
            "product_id": int(r["product_id"]),
            "nome": str(r["name"]) if pd.notna(r["name"]) else None,
            "desconto_percent": desconto,
            "descricao": str(r["description"]),
            "preco_brl": round(preco, 2) if preco is not None else None,
            "preco_com_desconto_brl": round(preco * (1 - desconto / 100), 2)
            if preco is not None
            else None,
        }
        lista.append(item)
    return {"promocoes": lista, "total": len(vigentes)}
