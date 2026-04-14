from entidades.funcionario.funcionario_repository import FuncionarioRepository
from util.fun_basicas import texto_para_float, validar_cpf


class FuncionarioService:
    def __init__(self, repository=None):
        self.repository = repository or FuncionarioRepository()
        self.repository.garantir_tabela()

    def salvar_funcionario(self, dados_formulario):
        validacao = self._validar_dados(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        cpf = dados_formulario.get("cpf", "").strip()
        if cpf:
            existente = self.repository.buscar_por_documento(cpf)
            if existente:
                if existente.get("status") == "A":
                    return {"sucesso": False, "mensagem": "Funcionario ja cadastrado."}
                return {"sucesso": False, "mensagem": "Funcionario ja cadastrado (excluido)."}

        return self.repository.salvar(self._tratar_dados(dados_formulario))

    def atualizar_funcionario(self, dados_formulario):
        validacao = self._validar_dados(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        cpf = dados_formulario.get("cpf", "").strip()
        codigo = dados_formulario.get("codigo", "").strip()
        if cpf:
            existente = self.repository.buscar_por_documento(cpf)
            if existente and existente.get("codigo") != codigo:
                return {"sucesso": False, "mensagem": "Ja existe outro funcionario com este CPF."}

        return self.repository.atualizar(self._tratar_dados(dados_formulario))

    def buscar_funcionario(self, opcao, texto, status, buscar_todos):
        texto = (texto or "").strip()
        opcao = (opcao or "").strip()
        status = (status or "").strip()

        if opcao == "CPF":
            texto = "".join(filter(str.isdigit, texto))

        if not texto and not buscar_todos:
            return []

        return self.repository.buscar_funcionario(opcao, texto, status, buscar_todos)

    def buscar_por_codigo(self, codigo):
        return self.repository.buscar_por_codigo(codigo)

    def alterar_status(self, codigo, status):
        return self.repository.alterar_status(codigo, status)

    def validar_documento(self, cpf):
        numeros = "".join(filter(str.isdigit, cpf or ""))
        if not numeros:
            return {"sucesso": True, "mensagem": ""}
        if len(numeros) != 11 or not validar_cpf(numeros):
            return {"sucesso": False, "mensagem": "CPF invalido."}
        return {"sucesso": True, "mensagem": ""}

    def _validar_dados(self, dados):
        nome = dados.get("nome", "").strip().upper()
        if not nome:
            return {"sucesso": False, "mensagem": "Nome do funcionario e obrigatorio."}

        validacao_documento = self.validar_documento(dados.get("cpf", ""))
        if not validacao_documento["sucesso"]:
            return validacao_documento

        return {"sucesso": True, "mensagem": ""}

    def _tratar_dados(self, dados):
        return {
            "codigo": dados.get("codigo", "").strip(),
            "nome": dados.get("nome", "").strip().upper(),
            "apelido": dados.get("apelido", "").strip().upper(),
            "cpf": "".join(filter(str.isdigit, dados.get("cpf", ""))),
            "rg": dados.get("rg", "").strip().upper(),
            "data_nascimento": self._normalizar_data(dados.get("data_nascimento", "")),
            "sexo": dados.get("sexo", "").strip(),
            "cep": dados.get("cep", "").strip(),
            "endereco": dados.get("endereco", "").strip().upper(),
            "numero": dados.get("numero", "").strip(),
            "bairro": dados.get("bairro", "").strip().upper(),
            "cidade": dados.get("cidade", "").strip().upper(),
            "estado": dados.get("estado", "").strip().upper(),
            "whatsapp": dados.get("whatsapp", "").strip(),
            "telefone": dados.get("telefone", "").strip(),
            "nome_mae": dados.get("nome_mae", "").strip().upper(),
            "nome_pai": dados.get("nome_pai", "").strip().upper(),
            "cidade_nascimento": dados.get("cidade_nascimento", "").strip().upper(),
            "pais_nascimento": dados.get("pais_nascimento", "").strip().upper(),
            "email": dados.get("email", "").strip().lower(),
            "data_admissao": self._normalizar_data(dados.get("data_admissao", "")),
            "salario": self._normalizar_salario(dados.get("salario", "")),
            "cargo": dados.get("cargo", "").strip().upper(),
            "carteira_trabalho": dados.get("carteira_trabalho", "").strip().upper(),
            "pis_pasep": dados.get("pis_pasep", "").strip().upper(),
            "data_demissao": self._normalizar_data(dados.get("data_demissao", "")),
            "motivo_demissao": dados.get("motivo_demissao", "").strip().upper(),
            "info_adicional": dados.get("info_adicional", "").strip().upper(),
            "status": dados.get("status", "A").strip() or "A",
        }

    def _normalizar_data(self, data_texto):
        data_texto = (data_texto or "").strip()

        numeros = "".join(filter(str.isdigit, data_texto))
        if len(numeros) != 8:
            return None

        partes = data_texto.split("/")
        if len(partes) == 3:
            dia, mes, ano = partes
            if len(dia) == 2 and len(mes) == 2 and len(ano) == 4:
                return f"{ano}-{mes}-{dia}"

        return None

    def _normalizar_salario(self, salario):
        if salario is None:
            return None
        texto = str(salario).strip()
        if not texto:
            return None
        return texto_para_float(texto)
