# 🚀 NITRO SYS - CONTEXTO ATUAL (MOVIMENTAÇÃO / VENDA)

## ✅ SITUAÇÃO ATUAL

### 🔷 ESTRUTURA DO MÓDULO MOVIMENTAÇÃO


movimentacao/
tela_movimentacao.py
saida/
tela_saida.py


✔ Tela intermediária criada (`tela_movimentacao.py`)  
✔ Fluxo definido com subpastas (organização correta)  
✔ Tela de saída (`tela_saida.py`) iniciada  

---

## 🎨 UI - TELA DE SAÍDA (VENDA)

### ✔ O QUE JÁ ESTÁ PRONTO

- Tela base criada
- Layout geral funcionando
- Botões laterais:
  - Vendas
  - Consultas
  - Relatórios
- Quadro cinza principal criado (área de trabalho)
- Layout alinhado corretamente (topo ajustado)
- Visual já no padrão Nitro Sys

👉 Resultado: Base sólida e profissional

---

## 🎯 OBJETIVO DA TELA

Criar uma **tela única de venda (tipo PDV leve)** onde:

- O usuário faz tudo sem trocar de tela
- Alta velocidade de operação
- UX simples e eficiente

---

## 🧠 ESTRUTURA DEFINIDA DA TELA (DENTRO DO QUADRO CINZA)

### 🔷 TOPO DA VENDA
- Nº Venda
- Data/Hora automática
- Checkboxes:
  - Orçamento
  - CFE
  - NFE

---

### 🔷 DADOS PRINCIPAIS
- Cliente
- Vendedor
- Desconto

---

### 🔷 RESUMO (lado direito)
- Total Produtos
- Total Venda

---

### 🔷 DIVISÃO VISUAL
Label:

PRODUTOS


---

### 🔷 TABELA DE PRODUTOS
Colunas:
- Código
- Descrição
- Quantidade
- Preço
- Subtotal

---

### 🔷 AÇÕES (rodapé)
- Adicionar Produto
- Remover Produto
- Finalizar Venda
- Cancelar

---

## 🧱 ARQUITETURA (MANTER PADRÃO)

- UI → `tela_saida.py`
- Regras → `saida_service.py`
- Banco → `saida_repository.py`

❗ Regra importante:
- NÃO colocar lógica de negócio na UI

---

## 🚀 PRÓXIMOS PASSOS

1. Montar topo da venda (nº + data + checkboxes)
2. Criar campos cliente / vendedor / desconto
3. Criar área de totais (lado direito)
4. Criar label "PRODUTOS"
5. Criar tabela
6. Criar botões de ação
7. Depois integrar com:
   - pesquisa de produtos
   - movimentação de estoque
   - banco de dados

---

## 💬 OBSERVAÇÃO

A base atual está muito boa.

👉 Esse módulo de venda é o coração do sistema  
👉 O foco deve ser velocidade e simplicidade  

---

## 🔥 STATUS

✔ Estrutura pronta  
✔ UI base pronta  
🚧 Iniciando construção da tela de venda  