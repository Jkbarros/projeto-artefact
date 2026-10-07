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

## Fase 7 (avaliação) + bilíngue

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| Seletor de idioma PT/EN (opção B) em `prompts.py`/`agent.py`/UI/CLI; `docs/Theoretical Questions.md` | Pediu lista de perguntas e suporte a inglês; commits pelo candidato |

## Fase 6 (interface e persistência)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| `memory.py` (SQLite por session_id, limite de contexto), `app_streamlit.py`, testes de memória | Aprovou implementação da Fase 6; commits pelo candidato |

## Fase 5 (agente e persona)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| `prompts.py`, `agent.py` (function calling), `tools/registro.py`, `cli.py` para testes | Persona **Lúcia**, tom acolhedor musical, emoji leve (escolha do candidato); commits pelo candidato |

## Fase 4 (ferramentas do agente)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| Tools `buscar_produtos`, `consultar_produto`, `consultar_promocoes`, `consultar_pedido` (com validação de identidade), `consultar_politicas` (RAG), `loja_aberta_agora` (fuso Campo Grande) + 21 testes | Aprovou implementação da Fase 4; commits pelo candidato |

## Fase 3 (tratamento de dados)

| O que a IA gerou | O que o usuário revisou/decidiu |
|------------------|----------------------------------|
| `data_prep.py`, módulos `dados/` e `rag/`, testes, `docs/tratamento_dados.md` | Aprovou implementação da Fase 3; commits pelo candidato |

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
