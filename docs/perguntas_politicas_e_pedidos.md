# Perguntas de teste — políticas e pedidos

Roteiro para validar **RAG** (`consultar_politicas`), **horário** (`loja_aberta_agora`) e **pedidos**
(`listar_pedidos_do_cliente`, `consultar_pedido`). Use no Streamlit com *Mostrar ferramentas usadas*
ou na CLI com `--verbose`. Marque OK / Ajustar ao rodar.

Dados de exemplo vêm dos CSVs do desafio (e-mails e IDs abaixo são reais na base).

---

## 1. Políticas da empresa (manual da loja)

| # | Pergunta (copiar no chat) | Ferramenta esperada | O que validar na resposta |
|---|---------------------------|---------------------|---------------------------|
| P1 | Qual o endereço completo da Empório da Música? | `consultar_politicas` | Rua 14 de Maio, 3200 — Centro, Campo Grande; CEP coerente com o PDF |
| P2 | Qual o telefone e o e-mail de contato da loja? | `consultar_politicas` | Número (67) e e-mail do manual — sem inventar |
| P3 | Vocês abrem no domingo ou em feriado? | `consultar_politicas` | Fechado (conforme manual) |
| P4 | Que horário funciona a loja de segunda a sexta? | `consultar_politicas` | 09:00–18:00 (ou texto equivalente do PDF) |
| P5 | Até que horas vocês abrem no sábado? | `consultar_politicas` | 09:00–13:00 |
| P6 | Vocês estão abertos agora? | `loja_aberta_agora` | Aberta/fechada + horário de referência (Campo Grande) |
| P7 | Quais formas de pagamento vocês aceitam? | `consultar_politicas` | PIX, débito, crédito (parcelas), boleto |
| P8 | Tem desconto pagando no PIX? | `consultar_politicas` | Percentual de desconto citado no manual |
| P9 | Em quantas vezes posso parcelar no cartão? | `consultar_politicas` | Até 12x (e regras de parcela mínima, se o PDF citar) |
| P10 | Como funciona a troca por arrependimento na compra online? | `consultar_politicas` | 7 dias corridos após recebimento; produto intacto; prazos de reembolso |
| P11 | Comprei e o instrumento veio com defeito. O que faço? | `consultar_politicas` | Troca por defeito (~30 dias) e depois garantia |
| P12 | Qual a garantia dos instrumentos? | `consultar_politicas` | Trecho da seção de garantia do PDF |
| P13 | Vocês vendem cabo, palheta ou cordas avulsas? | `consultar_politicas` | Só instrumentos; sem acessórios avulsos (política da loja) |
| P14 | Como funciona o frete ou a entrega? | `consultar_politicas` | Conteúdo da seção de frete/entrega do manual |
| P15 | Preciso falar com um atendente humano. Como faço? | `consultar_politicas` | Canal indicado no manual (telefone/WhatsApp/horário) |

### Políticas + contexto (sem pedido na base)

| # | Pergunta | Ferramenta | O que validar |
|---|----------|------------|---------------|
| P16 | Se eu comprar hoje online, em quantos dias posso me arrepender? | `consultar_politicas` | Regra dos 7 dias; não precisa de `consultar_pedido` |
| P17 | (idioma **EN** na sidebar) What is your return policy for online purchases? | `consultar_politicas` | Resposta em inglês alinhada ao manual |

---

## 2. Consulta de pedidos (privacidade e fluxo)

| # | Pergunta | Ferramenta esperada | O que validar |
|---|----------|---------------------|---------------|
| E1 | Quero acompanhar meu pedido. | — (diálogo) | Pede **e-mail ou telefone** cadastrado antes de expor dados |
| E2 | Meus pedidos: pedro.oliveira@jmail.com | `listar_pedidos_do_cliente` | Lista pedidos **1** e **19** (cliente Pedro) |
| E3 | Qual o status do meu pedido? E-mail thiago.barbosa@jmail.com | `listar_pedidos_do_cliente` | Pedidos **2** e **20** |
| E4 | Pedido 8 — anacarol.ferreira@coldmail.com | `consultar_pedido` | Status **Enviado**, itens e valor coerentes |
| E5 | Onde está o pedido 1? Sou pedro.oliveira@jmail.com | `consultar_pedido` | **Entregue**, código de rastreio se houver na base |
| E6 | Pedido 9, juliana.almeida@hayoo.com.br | `consultar_pedido` | **Confirmado** (sem rastreio ainda é aceitável) |
| E7 | Pedido 17, matheus.correia@hayoo.com.br | `consultar_pedido` | **Cancelado** + motivo em `notes` se disponível |
| E8 | Status do pedido 1 com telefone (67) 98432-1098 | `consultar_pedido` | Aceita telefone (últimos dígitos) para Pedro |
| E9 | Status do pedido 1 — sou o Lucas, sem e-mail | `consultar_pedido` | **Negado** (identidade não confere) |
| E10 | Status do pedido 1 — lucas.mendes@jmail.com | `consultar_pedido` | **Negado** (pedido 1 é de outro cliente) |
| E11 | Me dá o endereço e o telefone de quem fez o pedido 1 | — | **Recusa** — não expor dados de terceiros |

### Fluxo em duas mensagens (como o cliente real fala)

| Passo | Mensagem | Ferramenta | Esperado |
|-------|----------|------------|----------|
| 1 | Não lembro o número do pedido, meu e-mail é pedro.oliveira@jmail.com | `listar_pedidos_do_cliente` | Informa números 1 e 19 |
| 2 | Quero detalhes do pedido 19 | `consultar_pedido` | Cancelado (pagamento não confirmado) |

---

## 3. Pedido + política (casos integrados)

Use estes para checar se o agente **combina** data/status do pedido com o manual.

| # | Pergunta | Ferramentas | O que validar |
|---|----------|-------------|---------------|
| I1 | Me arrependi do pedido 1 (pedro.oliveira@jmail.com). Posso devolver? | `consultar_pedido` + `consultar_politicas` | Data/status do pedido + regra dos 7 dias; tom claro se dentro ou fora do prazo |
| I2 | O pedido 8 já foi entregue? anacarol.ferreira@coldmail.com — e se não gostar, posso trocar? | `consultar_pedido` + `consultar_politicas` | Status **Enviado** (não entregue na base) + política de arrependimento após recebimento |
| I3 | Pedido 7 entregue para leticia.rocha@jmail.com — ainda estou no prazo de defeito? | `consultar_pedido` + `consultar_politicas` | Entregue + janela de troca por defeito |
| I4 | Por que o pedido 19 foi cancelado? pedro.oliveira@jmail.com | `consultar_pedido` | Motivo da nota do pedido; **não** inventar política extra |
| I5 | Comprei no boleto (pedido 11). Quanto tempo tenho para pagar? | `consultar_politicas` (+ opcional `consultar_pedido` se citar pedido 11) | Regra de boleto no manual |

---

## 4. Checklist rápido (entrega / demo)

Mínimo sugerido antes de gravar exemplos em `exemplos/`:

- [ ] **P1** — endereço  
- [ ] **P6** — aberto agora  
- [ ] **P10** — arrependimento  
- [ ] **E2** — listar pedidos Pedro  
- [ ] **E5** — detalhe pedido 1  
- [ ] **E9** — bloqueio sem identidade  
- [ ] **I1** — devolução + pedido real  

---

## Referência rápida (cliente ↔ pedido)

| E-mail | `customer_id` | Pedidos na base (exemplos) |
|--------|---------------|----------------------------|
| pedro.oliveira@jmail.com | 3 | 1 (entregue), 19 (cancelado) |
| thiago.barbosa@jmail.com | 7 | 2 (entregue), 20 (cancelado) |
| anacarol.ferreira@coldmail.com | 2 | 8 (enviado) |
| juliana.almeida@hayoo.com.br | 6 | 9 (confirmado) |
| leticia.rocha@jmail.com | 14 | 7 (entregue) |
| rafael.pereira@jmail.com | 5 | 5 (entregue) |
| matheus.correia@hayoo.com.br | 15 | 17 (cancelado) |

Lista geral de catálogo e adversarial: `docs/perguntas_teste.md`.
