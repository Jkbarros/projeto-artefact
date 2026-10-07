# Decisões técnicas

Registro das escolhas do projeto (base para o README final).

## Já definidas

| Decisão | Escolha | Motivo (resumo) |
|---------|---------|-----------------|
| LLM | OpenAI | Escolha do candidato (alterado de Gemini); chave via platform.openai.com |
| Gerenciador de ambiente | `venv` + `requirements.txt` | Simples, universal, fácil de reproduzir na avaliação |
| Idioma do código | Português (identificadores) | Preferência do candidato; domínio da loja em PT-BR |
| Abordagem do agente (2.1) | **Function calling nativo da OpenAI, sem framework** | Poucas dependências, controle total do loop, fácil de depurar e defender em entrevista |
| Acesso aos dados (2.2) | **Pandas + funções parametrizadas** | Rápido para o prazo; ferramentas explícitas evitam text-to-SQL e vazamento entre clientes |
| Políticas / PDF (2.3) | **RAG com embeddings** | Escala com novos documentos de política; chunks por **seção** do manual |
| Detalhe 2.3 | `pypdf` → texto limpo → **ChromaDB** em `data/processed/` → embeddings **OpenAI** (`text-embedding-3-small`) | Índice reproduzível via `data_prep` (Fase 3) |
| Interface (2.4) | **Streamlit** | Demo visual; chat no navegador; `agent.py` permanece o núcleo |
| Persistência (2.5) | **SQLite por `session_id`** | Retomar conversas entre execuções; histórico fora do `session_state` do Streamlit |
| Qualidade (2.6) | **pytest** + **ruff** + **python-dotenv** | Já no `requirements.txt`; testes nas tools e no pipeline de dados |

**Nota:** catálogo, pedidos e promoções continuam em **Pandas**. RAG cobre **texto de políticas** (PDF e futuros documentos).

**Persona (Fase 5):** atendente **Lúcia** — tom acolhedor musical, no máximo 1 emoji por mensagem (`prompts.py`).

**Fase 2:** arquitetura fechada — próximo passo é **Fase 3** (tratamento de dados + build do índice RAG).
