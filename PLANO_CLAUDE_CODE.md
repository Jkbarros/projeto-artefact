# PLANO DE EXECUÇÃO: Agente de Atendimento "Empório da Música"

> **Para o Claude Code:** este documento é o seu plano de trabalho. Leia-o inteiro antes de começar. Você vai conduzir o desenvolvimento **junto com o usuário, etapa por etapa**, pedindo as informações e os arquivos de que precisar pelo chat. Siga as "Regras de conduta" abaixo à risca.

---

## 0. Contexto do projeto

O usuário está fazendo o **Desafio Técnico de AI Engineer da Artefact**. O objetivo é prototipar um **agente de atendimento por mensagens de texto** para a **Empório da Música**, uma loja fictícia de instrumentos musicais em Campo Grande/MS. A equipe da loja está sobrecarregada com perguntas recorrentes (horários, status de pedido, preço e disponibilidade).

**Materiais fornecidos pela loja (o usuário vai enviá-los pelo chat):**
- `data/*.csv`: tabelas da operação (produtos, pedidos, clientes, promoções, etc.).
- `data/politicas_da_loja.pdf`: manual interno de políticas e procedimentos.

**O agente deve:**
1. Assumir uma **persona** alinhada à identidade e ao tom da loja.
2. Receber e responder mensagens com base no contexto disponibilizado.
3. Saber **quando consultar dados** (disponibilidade, preços, status de pedido) e **quando consultar políticas** (troca, horários, pagamento).
4. Lidar adequadamente com perguntas **fora do escopo** da loja.

**Única restrição técnica obrigatória:** Python como linguagem principal.

**Critérios de avaliação da Artefact:** lógica, clareza e iniciativa. Eles valorizam o *raciocínio e as decisões justificadas* mais do que uma solução perfeita. Quando algo for ambíguo, **assuma uma interpretação razoável, documente a suposição no README e siga em frente**.

### Entregáveis (todos obrigatórios)
1. **Repositório Git público no GitHub**, com histórico de commits que mostre progresso real. **Nada de force-push de tudo em um único commit.** Nada pode ser alterado após o prazo de entrega.
2. **README.md** com: instruções completas para rodar; justificativa das decisões técnicas (framework, LLM, arquitetura de retrieval, estratégia de prompt etc.); limitações conhecidas e o que faria com mais tempo; **uso de assistentes de código** (qual ferramenta e como foi usada, o workflow).
3. **De 3 a 5 conversas de exemplo** (`.md`, `.txt` ou imagem) em `exemplos/`, cobrindo cenários variados. **Ao menos uma deve ser não trivial** (consulta de dados em tempo real ou aplicação de regras das políticas).

Cenários sugeridos pelo desafio: violões até R$ 1.000 (catálogo); endereço da loja (info geral); preço do Takamine GD20 (consulta de preço); "me arrependi da compra, posso devolver?" (política de devolução).

---

## 1. Decisões já tomadas e em aberto

| Item | Status |
|---|---|
| **LLM / provedor** | ✅ **Decidido: Google Gemini** (o usuário já tem acesso/chave) |
| Framework do agente | ⏳ A decidir (Fase 2) |
| Acesso aos dados (pandas / SQLite / etc.) | ⏳ A decidir (Fase 2) |
| Retrieval das políticas (contexto direto / BM25 / RAG com embeddings) | ⏳ A decidir, **depende do tamanho do PDF** |
| Interface (CLI / Streamlit / Gradio / FastAPI) | ⏳ A decidir (Fase 2) |
| Persistência do histórico | ⏳ A decidir (Fase 2) |
| Gerenciador de ambiente (uv / Poetry / venv) | ⏳ A decidir (Fase 0) |
| Prazo de entrega | ❓ Perguntar ao usuário na Fase 0 |

**Preferência do usuário:** soluções **gratuitas e/ou open source**, sempre que possível.

**Notas sobre o Gemini (verifique, não confie na memória):**
- Antes de escrever código que chame o Gemini, **consulte a documentação oficial atual** (Google AI Studio / Gemini API docs) para confirmar: o SDK Python recomendado hoje, o nome dos modelos disponíveis no tier gratuito, e os limites de requisições (que mudam com frequência).
- Peça ao usuário para dizer qual modelo ele enxerga disponível na conta dele, se necessário.
- Mantenha o provedor **atrás de uma camada fina de abstração** (ex.: `llm.py`) e configure modelo e chave via `.env`. Assim, trocar de modelo depois é só configuração.
- Implemente tratamento de **rate limit** (retry com backoff) e mensagens de erro claras.
- A chave fica **somente** no `.env`. Nunca commitar. Mantenha o `.env.example` sem valores reais.

---

## 2. Regras de conduta (obrigatórias)

1. **Uma fase por vez.** Ao terminar cada fase, apresente um resumo curto do que foi feito e **espere a aprovação do usuário** antes de passar à próxima.
2. **Pergunte antes de decidir.** Para cada decisão técnica em aberto, apresente **2–4 opções** (preferindo gratuitas/open source) com prós e contras, **dê uma recomendação** e deixe o usuário escolher. Não escolha sozinho.
3. **Peça o que precisar pelo chat.** Quando faltar um arquivo ou uma informação, diga exatamente o que precisa e em qual formato (ex.: "cole aqui o conteúdo de `pedidos.csv` ou envie o arquivo"). Faça **poucas perguntas por vez** (idealmente uma ou duas).
4. **Nunca invente dados da loja.** Se uma informação (endereço, horário, prazo de troca) não estiver nos CSVs ou no PDF, o agente deve dizer que não tem a informação. O mesmo vale para você ao documentar.
5. **Commits pequenos e frequentes**, com mensagens claras (Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`). **Faça pelo menos um commit por fase**, de preferência vários. Nunca use `git push --force` nem reescreva o histórico. Antes de cada commit, confirme com o usuário se ainda não tiver autorização permanente.
6. **Nunca commitar segredos.** Verifique o `.gitignore` e rode uma checagem antes de cada push.
7. **Explique o porquê.** O usuário precisa conseguir defender cada decisão em entrevista. Explique em linguagem simples o que cada parte do código faz e por que foi feita assim.
8. **Registre o uso de IA.** Mantenha atualizado o arquivo `docs/uso_de_ia.md` com: o que você (Claude Code) gerou, o que o usuário revisou/alterou e quais decisões foram do usuário. Isso alimenta a seção obrigatória do README.
9. **Registre as suposições.** Mantenha `docs/suposicoes.md` atualizado a cada ambiguidade encontrada.
10. **Idioma:** converse com o usuário em **português do Brasil**. O código pode ter identificadores em português ou inglês (decida com o usuário na Fase 0 e mantenha a consistência). O agente final responde em português do Brasil.
11. **Mantenha simples.** O desafio valoriza clareza. Evite frameworks pesados sem necessidade. Prefira poucas dependências.
12. **Teste antes de declarar pronto.** Rode os testes e o agente de verdade. Mostre a saída ao usuário.

---

## 3. Fases

> Formato de cada fase: **Objetivo → O que perguntar/pedir ao usuário → O que fazer → Critério de pronto → Commit sugerido**.

---

### FASE 0: Preparação do repositório e do ambiente

**Objetivo:** ter o repositório criado, o ambiente funcionando e a estrutura de pastas pronta.

**Perguntar/pedir ao usuário:**
- Qual é a **data e hora limite de entrega**? (registrar em `docs/` e planejar com folga)
- O repositório público no GitHub já existe? Qual é a URL? (se não existir, orientar a criar, com `.gitignore` de Python e licença MIT)
- Qual versão do Python está instalada? Sistema operacional?
- Preferência de gerenciador de ambiente. Opções:
  - **uv** (rápido, moderno) ← *recomendado*
  - **Poetry**
  - **venv + requirements.txt** (mais simples e universal)
- Idioma dos identificadores no código (português ou inglês)?
- Ele já tem a **chave de API do Gemini**? (orientar a colocá-la no `.env`, sem colar a chave no chat)

**Fazer:**
- Inicializar o projeto e o ambiente escolhido.
- Criar a estrutura de pastas (sugestão abaixo, ajustar conforme as decisões).
- Criar `.gitignore` (incluindo `.env`, `__pycache__`, `*.db` se gerado, `.venv`), `.env.example` e README esqueleto.
- Criar `docs/uso_de_ia.md` e `docs/suposicoes.md` vazios com cabeçalho.
- Fazer um teste mínimo de "hello world" chamando o Gemini para validar a chave e o SDK.

**Estrutura sugerida:**
```
emporio-agente/
├── README.md
├── pyproject.toml (ou requirements.txt)
├── .env.example
├── .gitignore
├── data/
│   ├── raw/          # CSVs e PDF originais (intocados)
│   └── processed/    # dados tratados / banco SQLite
├── notebooks/        # exploração dos dados
├── src/emporio/
│   ├── config.py
│   ├── llm.py        # camada fina de acesso ao Gemini
│   ├── data_prep.py
│   ├── tools/        # uma ferramenta por arquivo
│   ├── rag/          # só se necessário
│   ├── agent.py      # loop do agente
│   ├── prompts.py    # persona e system prompt
│   ├── memory.py     # histórico
│   └── cli.py
├── tests/
├── exemplos/         # 3–5 conversas
└── docs/             # decisões, suposições, uso de IA
```

**Critério de pronto:** ambiente roda; chamada de teste ao Gemini responde; primeiro commit feito e enviado ao GitHub.

**Commit sugerido:** `chore: estrutura inicial do projeto e configuração do ambiente`

---

### FASE 1: Entender os dados

**Objetivo:** conhecer a fundo os CSVs e o PDF antes de decidir qualquer arquitetura.

**Perguntar/pedir ao usuário:**
- Pedir que **coloque os arquivos em `data/raw/`** (ou envie pelo chat): todos os `*.csv` e `politicas_da_loja.pdf`.
- Se o usuário não conseguir enviar arquivos grandes, pedir que cole as **primeiras 15–20 linhas** de cada CSV e o **texto completo** do PDF.

**Fazer:**
- Para cada CSV: listar colunas, tipos, nº de linhas, chaves e relações entre tabelas (ex.: `id_cliente`, `id_produto`).
- Identificar **problemas de qualidade**: nulos, duplicatas, preços como texto (ex.: "R$ 1.299,90"), datas em formatos diferentes, nomes de produto inconsistentes, estoque negativo, categorias digitadas de formas diferentes, encoding quebrado.
- Ler o PDF inteiro. Medir o **tamanho** (páginas e nº aproximado de tokens) e listar **quais perguntas ele responde**: troca/devolução, horários, endereço, formas de pagamento, frete, garantia, escalonamento para humano etc. Observar a **estrutura** (seções numeradas? tabelas?).
- Criar `notebooks/exploracao.ipynb` (ou um relatório em `docs/exploracao_dados.md`) com as descobertas.
- Montar o **mapa pergunta → fonte** (ex.: "preço do produto X" → CSV de produtos; "posso devolver?" → PDF **e** CSV de pedidos).
- Registrar em `docs/suposicoes.md` toda ambiguidade encontrada.

**Mostrar ao usuário:** um resumo com (a) tabelas e relações, (b) problemas de qualidade, (c) tamanho do PDF, (d) mapa pergunta → fonte, (e) lacunas (informações que o agente talvez precise e que **não existem** nos dados).

**Critério de pronto:** o usuário entendeu os dados e aprovou o resumo.

**Commit sugerido:** `docs: exploração dos dados e mapa de perguntas por fonte`

---

### FASE 2: Decisões de arquitetura (com o usuário)

**Objetivo:** fechar as escolhas técnicas, cada uma com justificativa curta registrada em `docs/decisoes.md` (base do README).

Apresente cada decisão abaixo, **uma por vez**, com as opções, a recomendação e o motivo, **considerando o que você viu na Fase 1**. Aguarde a escolha do usuário.

**2.1 Abordagem do agente**
| Opção | Quando faz sentido |
|---|---|
| **Function calling nativo do Gemini, sem framework** | Poucas ferramentas, controle total, fácil de depurar e explicar ← *recomendado* |
| **PydanticAI** | Tipagem forte e validação, código enxuto |
| **LangGraph / LangChain** | Fluxos complexos; mais pesado |
| **LlamaIndex** | Foco em RAG sobre documentos |
| **smolagents** | Agente ReAct simples e open source |

**2.2 Acesso aos dados**
| Opção | Comentário |
|---|---|
| **Pandas + funções parametrizadas** | Simples, bom para CSVs pequenos |
| **SQLite + funções parametrizadas** | Organizado, permite joins, caminho natural para persistência ← *recomendado* |
| **Text-to-SQL** | Flexível, mas arriscado (consultas erradas, vazamento de dados de outros clientes). Se descartar, justificar no README |

**2.3 Retrieval das políticas (decidir pelo tamanho do PDF visto na Fase 1)**
| Opção | Quando faz sentido |
|---|---|
| **Texto inteiro no contexto** | PDF curto; zero falha de busca; muito defensável |
| **Ferramenta por seção (índice de seções)** | PDF curto/médio e bem estruturado |
| **BM25 (`rank_bm25`)** | Manual com vocabulário previsível; sem embeddings |
| **RAG com embeddings** | PDF maior. Embeddings: `sentence-transformers` multilíngue (`paraphrase-multilingual-MiniLM-L12-v2`, `multilingual-e5-small`, `bge-m3`), ou a API de embeddings do Gemini. Vector store: **ChromaDB**, **FAISS** ou `sqlite-vec` |
| Extração do PDF | `pypdf`, `pdfplumber` ou `PyMuPDF` |

> Se for RAG, dividir **por seção do manual** em vez de por tamanho fixo de caracteres.

**2.4 Interface**
| Opção | Esforço |
|---|---|
| **CLI** (`typer` + `rich`) | Mínimo ← *começar por aqui* |
| **Streamlit** | Baixo, ótimo para demonstrar |
| **Gradio** | Baixo (`ChatInterface`) |
| **FastAPI** | Médio, mostra visão de produto |

**2.5 Persistência do histórico**
- Memória da sessão (mínimo) · **SQLite** por `session_id` (recomendado se fizer sentido) · JSON por sessão.
- Perguntar se o usuário quer retomar conversas entre execuções.

**2.6 Qualidade**
- Testes: `pytest` · Lint/format: `ruff` · Config: `python-dotenv` ou `pydantic-settings`.

**Critério de pronto:** `docs/decisoes.md` preenchido com cada escolha e o porquê em 2–3 linhas.

**Commit sugerido:** `docs: decisões de arquitetura e justificativas`

---

### FASE 3: Tratamento dos dados

**Objetivo:** transformar os dados brutos em dados limpos e consultáveis.

**Perguntar ao usuário:** para cada problema de qualidade encontrado, confirmar a regra de tratamento quando houver mais de uma interpretação razoável (ex.: "estoque negativo: tratar como zero ou sinalizar?").

**Fazer:**
- Escrever `data_prep.py`, que lê `data/raw/` e gera `data/processed/` (ou o banco SQLite). O script deve ser **reproduzível** (rodar de novo gera o mesmo resultado) e **não modificar** os arquivos brutos.
- Normalizar: preços (para número), datas (para ISO), categorias, texto de busca (minúsculas, sem acento) e colunas auxiliares para busca tolerante a erros.
- Se o PDF for indexado: extrair o texto, dividir em seções e gerar o índice.
- Documentar **cada tratamento e cada suposição**.
- Testes que validam o resultado do tratamento (ex.: nenhum preço nulo, tipos corretos).

**Critério de pronto:** um comando (ex.: `python -m emporio.data_prep`) gera tudo; testes passam; tratamentos documentados.

**Commit sugerido:** `feat: pipeline de tratamento de dados`

---

### FASE 4: Ferramentas do agente

**Objetivo:** implementar as funções que o LLM poderá chamar. **Cada ferramenta deve funcionar e ser testada sem LLM.**

**Antes de codar, confirmar com o usuário a lista de ferramentas**, com base nos dados reais. Candidatas:
- `buscar_produtos(nome, categoria, preco_max, ...)`: busca com filtros, tolerante a erros de digitação.
- `consultar_produto(...)`: preço, estoque e promoção ativa.
- `consultar_pedido(id_pedido, identificacao)`: status do pedido, **com validação de identidade** (número do pedido + segundo identificador). Se o usuário não quiser implementar, documentar como limitação.
- `consultar_promocoes()`: promoções vigentes (comparar com a data atual).
- `consultar_politicas(pergunta)`: busca no manual, conforme a decisão 2.3.
- `loja_aberta_agora()`: usa o fuso `America/Campo_Grande` e os horários **do manual**.
- Outras que os dados sugerirem.

**Requisitos de qualidade:**
- Docstrings e descrições de parâmetros **claras**: o Gemini lê isso para decidir quando chamar cada ferramenta.
- Retornos **estruturados** e com casos vazios explícitos ("nenhum produto encontrado").
- Nunca expor dados de um cliente a outra pessoa.
- Tratar erros sem quebrar o agente.
- Testes `pytest` por ferramenta (casos felizes, vazios e de borda).

**Critério de pronto:** todas as ferramentas passam nos testes isolados.

**Commit sugerido (um por ferramenta, de preferência):** `feat: ferramenta buscar_produtos`, `feat: ferramenta consultar_pedido`, etc.

---

### FASE 5: Agente, persona e guardrails

**Objetivo:** o agente conversa com persona, escolhe as ferramentas certas e se comporta bem nos casos difíceis.

**Perguntar ao usuário:**
- Que **persona** ele imagina para a loja? (nome do atendente, tom: caloroso/musical/formal, uso de emojis, tamanho das respostas). Se o PDF de políticas descrever identidade ou tom de atendimento, usar isso como base e mostrar ao usuário.
- Como o agente deve tratar o **escalonamento para humano** (se o manual definir o procedimento, seguir o manual).

**Fazer:**
- Escrever o *system prompt* em `prompts.py` cobrindo: identidade e tom; escopo da loja; **quando usar cada ferramenta**; regras anti-alucinação ("preço, estoque e prazo vêm **sempre** de ferramenta; se não encontrar, diga que não encontrou"); tratamento de fora de escopo; formato das respostas.
- Implementar o loop: mensagem → Gemini decide ferramenta(s) → executa → Gemini responde. Limitar o nº máximo de iterações para evitar loops.
- Tratar:
  - **Fora de escopo** ("receita de bolo", política, etc.): recusar com educação e redirecionar.
  - **Prompt injection** ("ignore suas instruções"): manter a persona e as regras.
  - **Ambiguidade** ("quero um violão"): perguntar orçamento ou tipo antes de listar.
  - **Sem resultado**: produto inexistente, pedido não encontrado, estoque zerado.
  - **Regras combinadas**: ex. devolução = dados do pedido (data da compra) + política (prazo). O agente deve chamar as duas fontes e concluir a elegibilidade.
  - **Rate limit / falha da API**: mensagem amigável, sem quebrar.
- Mostrar no log (opcional por flag `--verbose`) quais ferramentas foram chamadas e com quais argumentos. Isso será usado como prova nos exemplos.

**Critério de pronto:** o agente responde corretamente aos cenários sugeridos pelo desafio e aos casos de borda acima.

**Commit sugerido:** `feat: loop do agente com function calling`, `feat: persona e system prompt`, `feat: tratamento de fora de escopo`

---

### FASE 6: Interface e persistência

**Objetivo:** uma forma simples de conversar com o agente, com histórico conforme a decisão 2.5.

**Fazer:**
- Implementar a interface escolhida (começar pela CLI).
- Implementar o histórico escolhido, com `session_id`.
- **Limitar** o histórico enviado ao modelo (últimas N mensagens) para controlar custo e contexto.
- Garantir que a interface roda com **um único comando** documentável.

**Critério de pronto:** o usuário conversa com o agente do início ao fim, e o histórico funciona.

**Commit sugerido:** `feat: interface CLI`, `feat: persistência do histórico`

---

### FASE 7: Avaliação e conversas de exemplo

**Objetivo:** validar o agente e gerar os 3–5 exemplos obrigatórios.

**Fazer:**
- Montar com o usuário uma lista de **15–20 perguntas de teste**: felizes, de borda e adversariais. Salvar em `tests/` ou `docs/`.
- Rodar todas, registrar falhas, ajustar prompt e ferramentas, e repetir.
- Salvar **de 3 a 5 conversas** em `exemplos/` (formato `.md`), cobrindo:
  1. Consulta de catálogo com filtro (ex.: violões até R$ 1.000).
  2. Informação geral (endereço e horário).
  3. **Não trivial:** pedido + política de devolução (data da compra × prazo).
  4. Fora de escopo e/ou tentativa de prompt injection.
  5. (Opcional) Produto sem estoque ou promoção.
- Em pelo menos um exemplo, **incluir o log das ferramentas chamadas**, para provar que houve consulta real.
- As conversas de exemplo devem ser **saídas reais do agente**, nunca escritas à mão.

**Critério de pronto:** de 3 a 5 exemplos salvos; o usuário aprovou a qualidade.

**Commit sugerido:** `test: conjunto de perguntas de avaliação`, `docs: conversas de exemplo`

---

### FASE 8: README

**Objetivo:** README completo e honesto.

**Seções obrigatórias:**
1. Visão geral + diagrama simples da arquitetura (pode ser Mermaid ou ASCII).
2. **Como rodar**: pré-requisitos, instalação, configuração do `.env` (como obter a chave do Gemini), comando para tratar os dados, comando para iniciar o agente, comando para rodar os testes. Tudo copiável.
3. **Decisões técnicas e justificativas**: framework, LLM (Gemini e por quê), acesso aos dados, retrieval, estratégia de prompt/persona, interface, persistência. Use `docs/decisoes.md`.
4. **Tratamento dos dados**: o que foi limpo e por quê.
5. **Suposições assumidas**: use `docs/suposicoes.md`.
6. **Limitações conhecidas e o que faria com mais tempo.**
7. **Uso de assistentes de código**: use `docs/uso_de_ia.md`. Explicar que o Claude (via Claude Code e chat) foi usado, para quê, o que o usuário revisou e decidiu. Ser honesto e específico.
8. Link para a pasta `exemplos/`.

**Pedir ao usuário:** revisar o texto e ajustar para soar como ele. Ele precisa conseguir defender tudo em entrevista.

**Commit sugerido:** `docs: README completo`

---

### FASE 9: Revisão final e entrega

**Fazer, junto com o usuário:**
- [ ] Clonar o repositório em uma **pasta limpa** e seguir **somente o README** para rodar. Corrigir o que falhar.
- [ ] `git log`: histórico gradual, com mensagens claras.
- [ ] Verificar que **nenhuma chave** vazou (checar o histórico também, não só os arquivos atuais).
- [ ] Rodar `pytest` e `ruff`.
- [ ] Conferir que as conversas de exemplo estão no repositório.
- [ ] Repositório está **público**.
- [ ] Responder o e-mail do processo seletivo com o link **antes do prazo**.
- [ ] **Não alterar mais nada** no repositório depois da entrega.

---

## 4. Pontos de atenção (onde o desafio costuma ser decidido)

1. **Privacidade em pedidos:** validar identidade antes de mostrar dados do pedido.
2. **Anti-alucinação:** preço, estoque e prazo sempre vêm de ferramenta.
3. **Regras combinadas:** devolução exige dados + política.
4. **Data e fuso:** usar `America/Campo_Grande` para "aberto agora" e promoções vigentes.
5. **Prompt injection:** testar e documentar.
6. **Escalonamento humano:** seguir o que o manual definir.
7. **Honestidade sobre limites:** documentar o que não foi feito.
8. **Histórico de commits:** pequeno, frequente e real.

---

## 5. Como começar

Ao receber este documento:
1. Leia-o inteiro.
2. Apresente-se brevemente ao usuário em português e resuma o plano em 5–6 linhas.
3. Confirme que o **Gemini** é o LLM já decidido e que o restante será decidido junto.
4. Inicie a **Fase 0** fazendo as primeiras perguntas (prazo de entrega e URL do repositório).
5. Não avance de fase sem a aprovação do usuário.
