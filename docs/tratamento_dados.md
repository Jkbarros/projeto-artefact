# Tratamento de dados (Fase 3)

## Comando

```powershell
$env:PYTHONPATH = "src"
python -m emporio.data_prep
```

Somente Parquets (sem embeddings / sem custo de API):

```powershell
python -m emporio.data_prep --sem-rag
```

## Saídas em `data/processed/`

| Artefato | Descrição |
|----------|-----------|
| `*.parquet` | Tabelas tratadas (`categorias`, `produtos`, `clientes`, `pedidos`, `itens_pedido`, `promocoes`) |
| `chroma/` | Índice vetorial do manual (RAG) |
| `manifesto.json` | Metadados da última execução (contagens, data UTC) |

## Transformações aplicadas

- **Produtos:** `nome_busca`, `descricao_busca`, `price_brl` numérico, `created_at` datetime, `stock_quantity` int ≥ 0.
- **Clientes:** `nome_busca`, `email_busca`, `telefone_busca` (só dígitos).
- **Pedidos:** datas ISO, `payment_method_label` legível em português.
- **Promoções:** coluna `vigente` (de `is_active`).
- **PDF:** texto limpo, chunks por **seção principal** do manual; subseções grandes são subdivididas.

Arquivos em `data/raw/` **não são modificados**.
