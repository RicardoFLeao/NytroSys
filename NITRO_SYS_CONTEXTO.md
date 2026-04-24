# 🚀 Nitro Sys - Contexto Atual (Tela Saída + Pagamento)

## 📌 Situação atual do sistema

O sistema já possui:

### ✅ Tela de Saída (Orçamento)
- Cadastro de produtos na tabela
- Cálculo automático:
  - Quantidade
  - Preço
  - Total
  - Desconto
- Atualização de totais:
  - Total produtos
  - Total venda
- Remoção dos CheckBox (Orçamento / CFE / NFE)
- Agora a tela é exclusivamente:
  👉 ORÇAMENTO

---

### ✅ Fluxo da Tela de Saída

- Digita produto → adiciona na tabela
- Edita quantidade e preço direto na tabela
- ENTER navega entre campos
- Quantidade = 0 → remove item
- Totais atualizam automaticamente

---

### ✅ Salvamento atual

- Orçamento é salvo no banco
- Tabela: `orcamento`
- Itens: `orcamento_itens`
- Tipo fixo:
  ```python
  tipo = "ORCAMENTO"

Número do orçamento:

SELECT MAX(id) + 1
💳 Tela de Pagamento (já construída)
✅ Funcionalidades implementadas
Fluxo inicial:
Forma → Condição → (Tabela ou OBS)
🟢 À vista
1 → Forma (à vista)
↓
Condição (dinheiro, pix, etc)
↓
OBS
↓
Finaliza

✔ Não usa tabela

🔵 A prazo
2 → Forma (a prazo)
↓
Condição
↓
Tabela parcelas
📊 Tabela de Parcelas

Colunas:

Parc | Dias | Data | % | Valor | OBS
⚙️ Inteligência implementada

✔ Digita DIAS → calcula DATA
✔ Digita DATA → calcula DIAS
✔ Digita % → calcula VALOR
✔ Digita VALOR → calcula %

✔ Formatação automática de data:

2205 → 22/05/2026
220526 → 22/05/2026
22012027 → 22/01/2027

✔ Navegação por ENTER:

Dias → Data → % → Valor → OBS → nova linha

✔ Finalização da tabela:

Linha vazia → encerra parcelas
Remove linha extra
Vai para OBS geral
🎯 Objetivo atual (PRÓXIMA ETAPA)
🔥 Integrar TelaSaida com TelaPagamento
🧠 Novo fluxo desejado
TelaSaida (F12)
↓
TelaPagamento
↓
Salvar tudo
📦 O que será feito
1. TelaSaida
F12 NÃO salva mais
F12 abre TelaPagamento
2. Enviar dados para TelaPagamento

Enviar:

Cliente
Vendedor
Totais
Desconto
Itens da tabela
3. TelaPagamento
Recebe dados da venda
Usa valor real (não mais 100.00)
Controla pagamento:
À vista
A prazo (parcelas)
4. Novo salvamento

Mover salvamento para TelaPagamento:

orcamento
orcamento_itens
novo: orcamento_pagamento
📊 Nova tabela no banco
orcamento_pagamento

Campos:

id_orcamento
forma_pagamento
condicao_pagamento
parcela
dias
data_vencimento
percentual
valor
obs
⚠️ Regras importantes
✔ À vista
1 única linha
percentual = 100%
valor = total da venda
✔ A prazo
múltiplas parcelas
cada linha da tabela é salva
🚀 Resultado esperado

Sistema com fluxo profissional:

Orçamento → Pagamento → (Futuro: Faturamento)
🧠 Visão de produto aplicada
Separação de responsabilidades:
Venda ≠ Faturamento
Interface limpa
Fluxo guiado
Uso intensivo de teclado
Automação de cálculos
🔜 Próximo passo no novo chat

Implementar:

✔ Função: abrir_tela_pagamento (TelaSaida)

Depois:

✔ Receber dados na TelaPagamento

Depois:

✔ Salvar tudo a partir da TelaPagamento
🧱 Estado do projeto

✔ Base sólida
✔ Fluxo funcional
✔ UI limpa
✔ Lógica consistente