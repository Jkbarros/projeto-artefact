from emporio.rag.pdf_politicas import carregar_chunks_politicas, extrair_texto_pdf


def test_pdf_tem_texto_suficiente():
    texto = extrair_texto_pdf()
    assert len(texto) > 5_000
    assert "Emp" in texto or "Música" in texto or "Musica" in texto


def test_chunks_por_secao():
    chunks = carregar_chunks_politicas()
    assert len(chunks) >= 8
    ids = {c.secao_id for c in chunks}
    assert "4_trocas_devolucoes" in ids
    assert all(c.texto.strip() for c in chunks)
