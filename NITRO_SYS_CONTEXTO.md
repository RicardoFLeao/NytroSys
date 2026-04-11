


# NITRO SYS — CONTEXTO COMPLETO DO PROJETO

## VISÃO DO PROJETO
O **Nitro Sys** é um sistema comercial desktop desenvolvido em:

- Python
- PyQt6 (interface gráfica)
- MySQL + PyMySQL (banco de dados)

Objetivo:
Construir um sistema profissional, modular, escalável e com boa experiência de uso, enquanto evolui como desenvolvedor.

---

# ARQUITETURA DO SISTEMA

## Separação de responsabilidades

- Interface → telas (PyQt6)
- Lógica → métodos das telas
- Banco → `bd.py`

Regra importante:
A interface **não deve conter SQL direto**.

---

## Estrutura atual do projeto

```text
projeto/
 ├── adm_prod/        # módulo produtos
 ├── entidades/       # clientes, fornecedores, etc
 ├── estoque/         # movimentação de estoque
 │    └── tela_estoque_manual.py
 ├── util/
 │    ├── estilo.py
 │    ├── fun_telas.py
 │    ├── padrao.py
 │    └── fun_basicas.py
 ├── bd.py
 ├── telaMain.py


 MÓDULO PRODUTOS (CONCLUÍDO)
Funcionalidades

✔ Cadastro de produtos (INSERT)
✔ Edição automática (UPDATE)
✔ Exclusão com confirmação (Sim/Não)
✔ Consulta com tabela real
✔ Duplo clique para edição
✔ Separação correta entre tela e banco

Sistema de busca (AVANÇADO)
Tipos de busca
Descrição
Código
Código de barras
Referências
Busca inteligente

Entrada do usuário:

vela saveiro

Transformação:

%vela%saveiro%
Busca cruzada (IMPORTANTE)

Permite combinar descrição + aplicação:

(descricao LIKE %termo% OR aplicacao LIKE %termo%)

Exemplo real:

cabo uno
vela saveiro
freio gol
UX implementada

✔ Busca em tempo real
✔ Checkbox “Todos” inteligente
✔ Destaque de linha selecionada
✔ Interface limpa

EXCLUSÃO DE PRODUTOS

✔ Confirmação personalizada
✔ Botões em português
✔ Sem atalho (decisão de segurança)

Futuro:

implementar ativo/inativo (exclusão lógica)
ESTOQUE (EM DESENVOLVIMENTO)
Banco de dados

Campo criado:

quantidade DECIMAL(10,2) NOT NULL DEFAULT 0

✔ Tabela já mostra quantidade real
✔ Base pronta para movimentação

Decisão de arquitetura

Estoque será separado do cadastro de produtos:

estoque/tela_estoque_manual.py

Motivo:

controle de acesso futuro
organização
escalabilidade
TELA ESTOQUE MANUAL
Estrutura atual
título centralizado
quadro cinza (container principal)
área de pesquisa
tabela de produtos
campos de edição
tabela de itens alterados
botão imprimir alinhado à direita
botão sair
Padrão visual
uso de QWidget como container
layout com QVBoxLayout e QHBoxLayout
sem uso de abas (decisão correta)
CONCEITOS DOMINADOS
Layout
tamanho controlado pelo layout
uso de stretch
organização por blocos
Container
QWidget substitui abas quando necessário
Alinhamento
QHBoxLayout controla alinhamento horizontal
uso de stretch ou alignment
DECISÕES IMPORTANTES

✔ Não usar atalho para excluir
✔ Separar módulos
✔ Não misturar cadastro com estoque
✔ Construir funcional antes de sofisticar
✔ Interface limpa e objetiva

FUNCIONALIDADES FUTURAS
Produtos
campo ativo/inativo
campo validade (IMPORTANTE)
Estoque
entrada manual
saída manual
histórico de movimentações
controle por usuário
controle por lote (validade)
ONDE O PROJETO PAROU

Tela de estoque manual está pronta visualmente.

Falta implementar:

busca de produto pelo código
preencher descrição automaticamente
carregar quantidade atual
lançar entrada no banco
atualizar tabela de itens alterados
PRÓXIMOS PASSOS
Fase atual — ESTOQUE
Implementar busca de produto
Preencher campos automaticamente
Implementar entrada manual
Atualizar tabela de alterações
OBJETIVO FINAL

Criar um sistema ERP completo com:

produtos
estoque
vendas
financeiro
controle de usuários
MODO DE TRABALHO
evoluir passo a passo
validar cada etapa
evitar pular fases
priorizar entendimento
INSTRUÇÃO PARA NOVO CHAT

Continuar o desenvolvimento do Nitro Sys a partir do módulo de estoque.

Foco:

busca de produto
integração com banco
entrada de estoque manual