📄 NITRO_SYS_CONTEXTO_ATUAL.md
📍 Situação Atual do Projeto (Nitro Sys)
✅ Estrutura
Projeto restaurado com sucesso via backup
Refatoração aplicada novamente:
tela_saida.py
funcao_venda.py
Organização separando:
Interface → tela_saida
Lógica → funcao_venda
🧩 Módulo de Venda (Saída)
✔️ Funcionalidades OK
Busca de produto (F8)
Adição de produto na tabela
Edição de:
Quantidade
Preço unitário
Remoção automática (quantidade = 0)
Cálculo:
Total produtos
Total venda
Destaque de linha
Exibição:
Localização
Aplicação
Foto
👤 Cliente
✔️ Cliente cadastrado
F6 → foco no código
F8 → pesquisa cliente
Enter → busca por código
Código = 0 → limpa cliente
✔️ Comportamento correto
Nome travado após seleção ✔️
CPF travado após seleção ✔️
Campos liberados após limpar ✔️
⚡ Cliente Rápido
✔️ Funcionando
Abre ao digitar no campo nome
Não abre quando cliente já está selecionado
Cursor corrigido (sem seleção bugada)
Layout completo:
Nome
CPF
Telefone
CEP (com consulta automática)
Endereço
Número
Bairro
Cidade
UF
✔️ CEP
Consulta via API (ViaCEP)
Preenche automaticamente:
Endereço
Bairro
Cidade
UF
🔄 Fluxo Atual (Cliente → Venda)
F6 → código cliente
Enter → vai para nome
Se cliente cadastrado:
trava nome e CPF
Se digitar no nome:
abre cliente rápido
Após cliente:
segue fluxo → vendedor → desconto → produto
⚠️ Pendência Principal
🔴 Cliente Rápido - CONFIRMAR

Ainda falta:

Ao clicar em Confirmar:

retornar dados para tela_saida
preencher:
nome
cpf
salvar em memória:
self.cliente_rapido = {
    "nome": ...,
    "cpf": ...,
    "telefone": ...,
    "cep": ...,
    "endereco": ...,
    "numero": ...,
    "bairro": ...,
    "cidade": ...,
    "uf": ...
}
🚀 Próximos Passos
1. Cliente Rápido
 Implementar botão Confirmar
 Retornar dados para tela_saida
 Preencher campos na tela
 Guardar em self.cliente_rapido
2. Venda / Orçamento
 Preparar estrutura para salvar venda
 Diferenciar:
cliente cadastrado (cod_cliente)
cliente rápido (dados avulsos)
3. Salvamento
 Criar fluxo de salvar orçamento
 Incluir dados do cliente rápido
 Persistir itens da tabela
4. Finalização
 Implementar botão "Finalizar"
 Preparar para:
impressão
integração futura
🧠 Observações Importantes
Sempre fazer backup antes de refatorar
Preferir mudanças pequenas e seguras
Separação de responsabilidades está correta:
tela → interface
função → lógica