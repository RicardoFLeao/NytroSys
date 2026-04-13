from estoque.estoque_repository import EstoqueRepository


class EstoqueService:
    def __init__(self, repository=None):
        self.repository = repository or EstoqueRepository()

    def buscar_produtos(self, opcao, texto):
        texto = (texto or "").strip().upper()

        if not texto:
            return []

        return self.repository.pesquisar_produtos(opcao, texto)

    def registrar_acerto(
        self,
        codigo,
        descricao,
        quant_antiga,
        quant_nova_texto,
        tipo_quantidade,
        usuario="admin",
    ):
        codigo = (codigo or "").strip()
        descricao = (descricao or "").strip()
        quant_antiga = str(quant_antiga or "").strip()
        quant_nova_texto = (quant_nova_texto or "").strip()
        tipo_quantidade = (tipo_quantidade or "").strip().lower()

        if not codigo:
            return {"sucesso": False, "mensagem": "Selecione um produto para ajustar."}

        if not quant_nova_texto:
            return {"sucesso": False, "mensagem": "Informe a nova quantidade."}

        try:
            quant_nova = float(quant_nova_texto.replace(",", "."))
        except ValueError:
            return {"sucesso": False, "mensagem": "Digite uma quantidade válida."}

        if quant_nova < 0:
            return {"sucesso": False, "mensagem": "Quantidade não pode ser negativa."}

        if tipo_quantidade == "inteiro":
            if not quant_nova.is_integer():
                return {"sucesso": False, "mensagem": "Apenas quantidade inteira."}
            quant_nova = int(quant_nova)

        resultado = self.repository.registrar_acerto_estoque(
            codigo,
            descricao,
            quant_antiga,
            quant_nova,
            usuario,
        )

        if not resultado["sucesso"]:
            return resultado

        return {
            "sucesso": True,
            "mensagem": resultado["mensagem"],
            "quantidade_nova": quant_nova,
        }