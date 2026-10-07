# Instruções para avaliar o agente em localhost

Guia para clonar o repositório, configurar o ambiente e abrir a **interface web (Streamlit)** no navegador. A atendente virtual se chama **Lúcia** (Empório da Música).

**Repositório:** https://github.com/Jkbarros/projeto-artefact

---

## O que você vai precisar

| Item | Detalhe |
|------|---------|
| **Python** | 3.12 ou superior ([python.org](https://www.python.org/downloads/)) |
| **Chave OpenAI** | Conta em [platform.openai.com](https://platform.openai.com/) com crédito/saldo para API |
| **Internet** | Chamadas à API OpenAI (chat + embeddings do RAG de políticas) |
| **Navegador** | Chrome, Edge, Firefox, etc. |

Os dados da loja (CSVs + PDF de políticas) já vêm em `data/raw/`. Os arquivos processados **não** estão no Git — é necessário rodar o preparo de dados uma vez após o clone.

---

## Passo a passo (Windows — PowerShell)

Abra o PowerShell na pasta onde deseja clonar o projeto.

### 1. Clonar e entrar na pasta

```powershell
git clone https://github.com/Jkbarros/projeto-artefact.git
cd projeto-artefact
```

### 2. Ambiente virtual e dependências

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Importante (Windows):** depois do passo 2, o prompt deve mostrar `(.venv)` no início da linha.
Só então o comando `python` aponta para o ambiente virtual. Se **não** ativou o venv e aparece
*“Python was not found”*, use o caminho completo:

```powershell
.\.venv\Scripts\python.exe -m emporio.data_prep
```

(ou ative o venv com `.\.venv\Scripts\Activate.ps1`).

**Se aparecer *“running scripts is disabled on this system”* ao ativar o venv:**

Opção A — só nesta janela do PowerShell (recomendado, não altera o PC de forma permanente):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Opção B — permitir scripts para seu usuário (permanente, se a empresa/Windows não bloquear por política de grupo):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Opção C — **sem** `Activate.ps1`: use sempre o Python do venv pelo caminho completo:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m emporio.data_prep
.\.venv\Scripts\python.exe -m streamlit run src/emporio/app_streamlit.py
```

Opção D — **Prompt de Comando (cmd)**, que não usa `ExecutionPolicy`:

```cmd
cd C:\Users\user\Desktop\Projeto Artefact
.\.venv\Scripts\activate.bat
set PYTHONPATH=src
python -m emporio.data_prep
```

### 3. Configurar a chave da API

```powershell
copy .env.example .env
```

Edite o arquivo `.env` e preencha:

```env
OPENAI_API_KEY=sua_chave_aqui
```

Os outros campos (`OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`) podem permanecer como no exemplo.

**Teste rápido da chave:**

```powershell
$env:PYTHONPATH = "src"
python -m emporio.testar_conexao
```

Deve imprimir algo como `OpenAI respondeu: ok`.

### 4. Preparar dados (obrigatório na primeira vez)

```powershell
$env:PYTHONPATH = "src"
python -m emporio.data_prep
```

Isso gera Parquets, índice de políticas (Chroma) e banco de conversas em `data/processed/`.

### 5. Subir a plataforma no localhost

Na **mesma** sessão do PowerShell (com o venv ativo):

```powershell
$env:PYTHONPATH = "src"
python -m streamlit run src/emporio/app_streamlit.py
```

O terminal mostrará URLs semelhantes a:

```text
Local URL: http://localhost:8501
```

Abra **http://localhost:8501** no navegador (se a porta 8501 estiver ocupada, o Streamlit pode usar **8502** — use a URL que aparecer no terminal).

Para encerrar o servidor: `Ctrl+C` no terminal.

---

## Passo a passo (macOS / Linux)

```bash
git clone https://github.com/Jkbarros/projeto-artefact.git
cd projeto-artefact
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env e defina OPENAI_API_KEY
export PYTHONPATH=src
python -m emporio.testar_conexao
python -m emporio.data_prep
python -m streamlit run src/emporio/app_streamlit.py
```

Acesse a **Local URL** exibida no terminal (em geral `http://localhost:8501`).

---

## Como usar a interface (Streamlit)

- **Chat:** digite perguntas sobre produtos, pedidos (com e-mail ou telefone cadastrado), políticas da loja e horário de funcionamento.
- **Sidebar — Idioma:** Português ou English (respostas da Lúcia no idioma escolhido).
- **Sidebar — Mostrar ferramentas usadas:** exibe quais funções o agente chamou (útil para avaliar consultas reais aos dados e ao PDF).
- **Nova conversa / sessões:** histórico salvo localmente em `data/processed/conversas.db`.

### Exemplos rápidos para testar

| Pergunta | O que esperar |
|----------|----------------|
| Quais violões vocês têm até R$ 1.000? | Lista de produtos da base |
| Qual o endereço da loja? | Informação do manual (RAG) |
| Meus pedidos: pedro.oliveira@jmail.com | Números de pedido do cliente de teste |
| Vocês estão abertos agora? | Aberta/fechada conforme horário de Campo Grande |

Mais roteiros de teste podem estar em `docs/` (se incluídos no repositório na versão avaliada).

---

## Alternativa: terminal (CLI, sem navegador)

```powershell
$env:PYTHONPATH = "src"
python -m emporio.cli --verbose --idioma pt
```

Digite `sair` para encerrar. `--verbose` mostra as ferramentas chamadas, como na sidebar do Streamlit.

---

## Testes automatizados (opcional)

```powershell
$env:PYTHONPATH = "src"
pytest
```

Não exige chave OpenAI para a maior parte dos testes de ferramentas/dados.

---

## Problemas comuns

| Sintoma | Solução |
|---------|---------|
| `Python was not found` (Windows) | Ative o venv (`.\.venv\Scripts\Activate.ps1`) ou use `.\.venv\Scripts\python.exe` em vez de `python` |
| `running scripts is disabled` (PowerShell) | `Set-ExecutionPolicy -Scope Process Bypass` e ative de novo; ou use `activate.bat` no cmd; ou `.\.venv\Scripts\python.exe` |
| `ModuleNotFoundError: emporio` | Defina `PYTHONPATH=src` (ou `export PYTHONPATH=src`) antes de rodar |
| Erro de saldo / billing na OpenAI | Verifique créditos em platform.openai.com |
| Agente sem dados / erro ao buscar produtos | Rode `python -m emporio.data_prep` |
| Streamlit pede e-mail no primeiro uso | Pressione Enter em branco ou use: `$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS="false"` antes do comando `streamlit run` |
| Porta diferente de 8501 | Use sempre a **Local URL** que o terminal imprimir |
| Políticas genéricas ou vazias | Confirme que `data_prep` terminou sem erro e que existe pasta `data/processed/chroma/` |

---

## Resumo em uma linha (após clone e `.env`)

Com venv ativo e `PYTHONPATH=src`:

```text
python -m emporio.data_prep
python -m streamlit run src/emporio/app_streamlit.py
```

Depois abra **http://localhost:8501** (ou a porta indicada).
