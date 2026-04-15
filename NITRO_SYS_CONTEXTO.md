


PROMPT PADRÃO - NITRO SYS

Você é um desenvolvedor sênior especialista em Python, PyQt6 e MySQL.

Sua função é me ajudar a desenvolver o sistema comercial desktop chamado
Nitro Sys, seguindo boas práticas de programação, organização e clareza.

COMO RESPONDER: - use respostas o mais simples possivel, em etapas sem encher a tela, ex. de respostas: o arquivo ... vamos mudar a função ..., ou está parte da função ... por está parte ...

PADRÃO DE CÓDIGO: - Código limpo e organizado - Funções com nomes
simples (ex: menu(), salvar()) - Separar interface, lógica e banco -
Usar try/except no banco - Fechar conexões corretamente - Evitar
complexidade desnecessária

REGRAS DO PROJETO: (Cole aqui o conteúdo do seu NITRO_SYS_CONTEXTO.md)

COMO AJUDAR: - Sugerir melhorias - Corrigir erros - Explicar passo a
passo - Guiar no desenvolvimento

IMPORTANTE: - Não complicar soluções simples - Priorizar clareza -
Pensar como sistema real

OBJETIVO: Ajudar a construir um sistema comercial completo e evoluir
como desenvolvedor.

# 🚀 NITRO SYS — CONTEXTO GERAL (15/04/2026)

---

# 🧠 VISÃO DO PROJETO

Sistema comercial desktop desenvolvido com:

- Python
- PyQt6
- MySQL (PyMySQL)

Objetivo:
Construir um sistema **profissional, modular, organizado e escalável**, seguindo boas práticas.

---

# 🏗️ ARQUITETURA PADRÃO

Separação clara:

- Interface → telas (PyQt)
- Service → regras de negócio
- Repository → acesso ao banco
- bd.py → apenas conexão

✔ Tela NÃO faz SQL direto  
✔ Repository NÃO tem regra de negócio  
✔ Service controla fluxo  

---

# 📦 PADRÃO DE STATUS (IMPORTANTE)

Padronizado em todo o sistema:

| Valor | Significado |
|------|-----------|
| A    | Ativo     |
| E    | Excluído  |

✔ Já aplicado em:
- Marcas
- Produtos
- Fornecedores

---

# 📦 MÓDULOS

---

## 🟢 MÓDULO MARCAS

### ✔ Implementado

- Tela completa (Consulta + Cadastro)
- Repository:
  - salvar()
  - atualizar()
  - listar()
  - alterar_status()
- Service:
  - salvar_marca()
  - atualizar_marca()
  - listar_marcas()
  - alterar_status_marca()

### ✔ Funcionalidades

- Cadastro
- Alteração
- Exclusão lógica (A ↔ E)
- Filtro por:
  - Ativo
  - Excluído
  - Todos
- Pesquisa dinâmica (digitando)
- F8 → busca geral
- Status exibido como:
  - Ativo
  - Excluído (vermelho)

### ✔ UX

- Botão dinâmico:
  - Excluir ↔ Ativar
- Tabela limpa ao iniciar

---

## 🟢 MÓDULO PRODUTOS

### ✔ Banco ajustado

- Coluna:
  - ativo → status
- Valores:
  - S → A

---

### ✔ Repository

- salvar()
- atualizar()
- listar_para_consulta()
- pesquisar_para_consulta()
- buscar_por_codigo()
- alterar_status()

🚫 Removido:
- delete físico

---

### ✔ Service

- salvar_produto()
- atualizar_produto()
- pesquisar_produtos_para_consulta()
- buscar_produto_por_codigo()
- alterar_status_produto()

---

### ✔ Tela (`cad_prod`)

#### Consulta
- Pesquisa por:
  - descrição
  - código
  - código de barras
  - referências
- F8 → busca
- Combo status:
  - Ativo
  - Excluído
  - Todos
- Checkbox "Todos" (redundante, manter por enquanto)

#### Tabela
- Código
- Descrição
- Quantidade
- Preço
- Status

✔ Status:
- Ativo normal
- Excluído vermelho

---

### ✔ Cadastro

- Todos os campos principais funcionando
- Cálculo automático:
  - preço venda
  - margem
- Validações básicas
- Integração com fornecedor

---

### ✔ Exclusão lógica

- Botão dinâmico:
  - Excluir ↔ Ativar
- Funciona direto pela tabela
- Não depende do cadastro carregado

---

# 🟡 NOVO: INTEGRAÇÃO COM MARCA

## ✔ UI criada

Na aba **Abastecimento**:

- edit_nome_marca
- edit_cod_marca (não usado manualmente por enquanto)

---

## ✔ F8 no campo marca

Funcionando:

- foco no campo marca
- F8 abre TelaMarcaProd

---

# 🔥 ONDE PARAMOS

## 🎯 PONTO ATUAL

Precisamos implementar:

### 👉 seleção de marca na TelaMarcaProd

Regra:

- Se abrir normal → NÃO faz nada
- Se abrir pelo cad_prod → seleciona marca

---

# 🚀 PRÓXIMO PASSO

## 1. TelaMarcaProd precisa:

### ✔ receber tela origem
```python
def __init__(self, tela_origem=None):
✔ detectar duplo clique
self.tabela_resultado.cellDoubleClicked.connect(self.selecionar_marca)
✔ criar função:
def selecionar_marca(self):
    if self.tela_origem is None:
        return
✔ comportamento:
pega linha selecionada
valida status (não permitir excluído)
devolve:
código
nome
fecha tela
2. cad_prod

Na abertura:

TelaMarcaProd(self)
🔮 PRÓXIMOS PASSOS FUTUROS
🔹 Marca
carregar marca no produto
salvar corretamente no banco
mostrar na consulta (opcional)
🔹 Produto
filtro mais avançado
integração com estoque
melhorar UX
🔹 Sistema geral
padronizar todos módulos
criar tela padrão de pesquisa (genérica)
criar relatórios
🧠 APRENDIZADO IMPORTANTE

✔ sistema deixou de ser "tela"
✔ agora existe padrão de arquitetura
✔ fluxo consistente entre módulos
✔ reutilização de lógica

🧠 FRASE DO MOMENTO

"Agora não estamos mais fazendo telas… estamos construindo um sistema."

🔚 OBS FINAL

Projeto está em excelente evolução:

✔ estrutura profissional
✔ padrões definidos
✔ código cada vez mais limpo

👉 próximo passo (marca ↔ produto) é um dos mais importantes do sistema.



