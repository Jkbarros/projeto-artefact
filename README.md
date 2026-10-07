# projeto-artefact — Agente Empório da Música

Protótipo de agente de atendimento por texto para o desafio técnico de **AI Engineer (Artefact)**. Loja fictícia **Empório da Música** (Campo Grande/MS).

> README completo (como rodar, decisões e limitações) será finalizado na **Fase 8**. Este arquivo será expandido ao longo do desenvolvimento.

## Decisões iniciais

- **LLM:** OpenAI ([documentação](https://platform.openai.com/docs/quickstart))
- **Ambiente:** Python 3.12+ com `venv` e `requirements.txt`
- **Código:** identificadores em português

## Estrutura (em construção)

```
data/raw/          # CSVs e PDF originais
data/processed/    # dados tratados (fases posteriores)
src/emporio/       # código do agente
docs/              # prazo, decisões, suposições, uso de IA
tests/
exemplos/          # conversas de exemplo (entregável)
```

## Configuração rápida (Fase 0)

```powershell
cd "c:\Users\user\Desktop\Projeto Artefact"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edite .env e coloque sua OPENAI_API_KEY (não commite)
$env:PYTHONPATH = "src"
python -m emporio.testar_conexao
python -m emporio.data_prep
python -m emporio.cli --verbose
streamlit run src/emporio/app_streamlit.py
pytest
```

Detalhes do pipeline: [docs/tratamento_dados.md](docs/tratamento_dados.md).

## Repositório

https://github.com/Jkbarros/projeto-artefact
