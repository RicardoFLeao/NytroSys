from adm_prod.marca_repository import MarcaRepository


class MarcaService:
    def __init__(self):
        self.repository = MarcaRepository()


    def salvar_marca(self, nome):
        nome = nome.strip().upper()

        if not nome:
            return {
                "sucesso": False,
                "mensagem": "Informe a descrição da marca."
            }

        sucesso = self.repository.salvar(nome)

        return {
            "sucesso": sucesso,
            "mensagem": "Marca salva com sucesso." if sucesso else "Erro ao salvar marca."
        }


    def atualizar_marca(self, codigo, nome):
        codigo = codigo.strip()
        nome = nome.strip().upper()

        if not codigo:
            return {
                "sucesso": False,
                "mensagem": "Código da marca não informado."
            }

        if not nome:
            return {
                "sucesso": False,
                "mensagem": "Informe a descrição da marca."
            }

        sucesso = self.repository.atualizar(codigo, nome)

        return {
            "sucesso": sucesso,
            "mensagem": "Marca alterada com sucesso." if sucesso else "Erro ao alterar marca."
        }


    def listar_marcas(self, texto="", opcao="Descrição", status="Todos"):
        texto = texto.strip().upper()
        return self.repository.listar(texto, opcao, status)


    def alterar_status_marca(self, codigo, status_atual):
        if not codigo:
            return {
                "sucesso": False,
                "mensagem": "Código da marca não informado."
            }

        if status_atual == "A":
            novo_status = "E"
            mensagem = "Marca excluída com sucesso."
        else:
            novo_status = "A"
            mensagem = "Marca ativada com sucesso."

        sucesso = self.repository.alterar_status(codigo, novo_status)

        return {
            "sucesso": sucesso,
            "mensagem": mensagem if sucesso else "Erro ao alterar status da marca."
        }