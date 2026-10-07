# Suposições

Toda ambiguidade ou lacuna nos dados da loja será registrada aqui (nunca inventar fatos da Empório da Música).

| Data | Suposição | Motivo |
|------|-----------|--------|
| 2026-10-06 | Promoção “vigente” = registro em `promotions` com `is_active = 1` | CSV não traz `start_date` / `end_date` |
| 2026-10-06 | Preço final com desconto = `price_brl * (1 - discount_percent/100)` quando houver promoção ativa para o `product_id` | Não há coluna de preço promocional no CSV |
| 2026-10-06 | Consulta de pedido exigirá **número do pedido + segundo identificador** (ex.: e-mail ou telefone cadastrado) | Privacidade; CSV tem `customer_id` ligado a contato |
| 2026-10-06 | Regra de “arrependimento online (7 dias)” aplica-se quando o pedido existir em `orders` com status compatível com entrega (`delivered` + `order_date` / `estimated_delivery`); canal “online” não está em coluna dedicada | Lacuna no schema de `orders` |
| 2026-10-06 | Produtos `status != active` não entram em busca de catálogo padrão, salvo o cliente pedir explicitamente | `discontinued` e `coming_soon` no dataset |
| 2026-10-06 | Fuso horário “loja aberta agora” = `America/Campo_Grande` | Campo Grande/MS (manual e clientes) |
| 2026-10-06 | Validação de identidade no pedido aceita **e-mail completo** OU os **8 últimos dígitos do telefone** cadastrado | Equilíbrio entre segurança e usabilidade; dados disponíveis em `customers` |
| 2026-10-06 | `loja_aberta_agora` **não** considera feriados (só domingo como dia fechado fixo) | Manual não lista feriados; evita inventar datas |
| 2026-10-06 | Persona: **Lúcia**, assistente virtual; tom **acolhedor musical**; até **1 emoji leve** por mensagem | Escolha do candidato; alinhada ao manual (saudação, consulta ao sistema, resposta clara) |
