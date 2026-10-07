# Uso de assistentes de código (IA)

Registro para a seção obrigatória do README.

## Ferramentas

- **Cursor** (assistente de código no IDE), incluindo chat e agente.

## Fase 0 (preparação)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| Estrutura de pastas, `requirements.txt`, módulos `config`/`llm`, docs iniciais | Escolha de **venv** e **identificadores em português**; prazo e URL do GitHub informados pelo usuário |
| Instalação de Python 3.12 via winget no ambiente local | — |

## Fase 1 (exploração dos dados)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| Análise dos CSVs/PDF, `docs/exploracao_dados.md`, atualização de `docs/suposicoes.md` | **Aprovou** o resumo da Fase 1; **commits ficam a cargo do candidato** |

## Fase 2 (arquitetura)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| Opções 2.1 (framework do agente) | Escolha **A**: function calling OpenAI sem framework |
| Opções 2.2 (acesso aos dados) | Escolha **A**: Pandas + funções parametrizadas |
| Opções 2.3 (políticas/PDF) | Escolha **D**: RAG com embeddings (Chroma + seções do manual); motivação: preparar crescimento de documentos/políticas |
| Opções 2.4 (interface) | Escolha **B**: Streamlit |
| Opções 2.5 (histórico) | Escolha **B**: SQLite por `session_id` (retomar conversas) |

## Decisões sempre do usuário

- LLM: OpenAI (alterado pelo candidato em relação ao plano inicial com Gemini)
- Gerenciador: venv
- Idioma do código: português
- Agente: function calling nativo OpenAI (opção A)
- Dados: Pandas + funções parametrizadas (opção A)
- Políticas: RAG com embeddings (opção D)
- Interface: Streamlit (opção B)
- Histórico: SQLite por `session_id` (opção B)
