from entidades.cliente.cliente_repository import ClienteRepository
from util.fun_basicas import validar_cnpj, validar_cpf


class ClienteService:
    def __init__(self, repository=None):
        self.repository = repository or ClienteRepository()
        self.repository.garantir_tabela()

    def salvar_cliente(self, dados_formulario):
        validacao = self._validar_dados_principais(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        cpf_cnpj = dados_formulario.get("cpf_cnpj", "").strip()
        existente = self.repository.buscar_por_documento(cpf_cnpj)
        if existente:
            if existente.get("status") == "A":
                return {"sucesso": False, "mensagem": "Cliente ja cadastrado."}
            return {"sucesso": False, "mensagem": "Cliente ja cadastrado (excluido)."}

        dados_tratados = self._tratar_dados(dados_formulario)
        return self.repository.salvar(dados_tratados)

    def atualizar_cliente(self, dados_formulario):
        validacao = self._validar_dados_principais(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        cpf_cnpj = dados_formulario.get("cpf_cnpj", "").strip()
        codigo = dados_formulario.get("codigo", "").strip()
        existente = self.repository.buscar_por_documento(cpf_cnpj)
        if existente and existente.get("codigo") != codigo:
            return {"sucesso": False, "mensagem": "Ja existe outro cliente com este documento."}

        dados_tratados = self._tratar_dados(dados_formulario)
        return self.repository.atualizar(dados_tratados)

    def buscar_cliente(self, opcao, texto, status, buscar_todos):
        texto = (texto or "").strip()
        opcao = (opcao or "").strip()
        status = (status or "").strip()

        if opcao in ("CPF / CNPJ", "WhatsApp", "Codigo"):
            texto = "".join(filter(str.isdigit, texto)) if opcao != "Codigo" else texto

        if not texto and not buscar_todos:
            return []

        return self.repository.buscar_cliente(opcao, texto, status, buscar_todos)

    def buscar_por_codigo(self, codigo):
        return self.repository.buscar_por_codigo(codigo)

    def alterar_status(self, codigo, status):
        return self.repository.alterar_status(codigo, status)

    def validar_documento(self, tipo_pessoa, documento):
        numeros_doc = "".join(filter(str.isdigit, documento or ""))
        if not numeros_doc:
            return {"sucesso": True, "mensagem": ""}

        if tipo_pessoa == "J":
            if len(numeros_doc) != 14 or not validar_cnpj(numeros_doc):
                return {"sucesso": False, "mensagem": "CNPJ invalido."}
        elif tipo_pessoa == "F":
            if len(numeros_doc) != 11 or not validar_cpf(numeros_doc):
                return {"sucesso": False, "mensagem": "CPF invalido."}
        else:
            return {"sucesso": False, "mensagem": "Selecione Juridica ou Fisica."}

        return {"sucesso": True, "mensagem": ""}

    def _validar_dados_principais(self, dados_formulario):
        razao_social = dados_formulario.get("razao_social", "").strip().upper()
        if not razao_social:
            return {"sucesso": False, "mensagem": "Razao social / nome e obrigatorio."}

        tipo_pessoa = dados_formulario.get("tipo_pessoa", "").strip()
        if tipo_pessoa not in {"J", "F"}:
            return {"sucesso": False, "mensagem": "Selecione Juridica ou Fisica."}

        validacao_documento = self.validar_documento(
            tipo_pessoa, dados_formulario.get("cpf_cnpj", "")
        )
        if not validacao_documento["sucesso"]:
            return validacao_documento

        return {"sucesso": True, "mensagem": ""}

    def _tratar_dados(self, dados):
        return {
            "codigo": dados.get("codigo", "").strip(),
            "tipo_pessoa": dados.get("tipo_pessoa", "").strip(),
            "razao_social": dados.get("razao_social", "").strip().upper(),
            "nome_fantasia": dados.get("nome_fantasia", "").strip().upper(),
            "contato": dados.get("contato", "").strip().upper(),
            "whatsapp": dados.get("whatsapp", "").strip(),
            "telefone": dados.get("telefone", "").strip(),
            "email": dados.get("email", "").strip().lower(),
            "cep": dados.get("cep", "").strip(),
            "endereco": dados.get("endereco", "").strip().upper(),
            "numero": dados.get("numero", "").strip(),
            "bairro": dados.get("bairro", "").strip().upper(),
            "cidade": dados.get("cidade", "").strip().upper(),
            "uf": dados.get("uf", "").strip().upper(),
            "cpf_cnpj": dados.get("cpf_cnpj", "").strip(),
            "inscricao_estadual": dados.get("inscricao_estadual", "").strip().upper(),
            "inscricao_municipal": dados.get("inscricao_municipal", "").strip().upper(),
            "data_referencia": self._normalizar_data(dados.get("data_referencia", "")),
            "sexo": dados.get("sexo", "").strip(),

            "nome_mae": dados.get("nome_mae", "").strip().upper(),
            "nome_pai": dados.get("nome_pai", "").strip().upper(),
            "cidade_nascimento": dados.get("cidade_nascimento", "").strip().upper(),
            "pais_nascimento": dados.get("pais_nascimento", "").strip().upper(),

            "local_trabalho": dados.get("local_trabalho", "").strip().upper(),
            "cargo": dados.get("cargo", "").strip().upper(),
            "tempo_servico": dados.get("tempo_servico", "").strip().upper(),
            "salario": dados.get("salario", "").strip(),
            "telefone_trabalho": dados.get("telefone_trabalho", "").strip(),

            "cep_trabalho": dados.get("cep_trabalho", "").strip(),
            "endereco_trabalho": dados.get("endereco_trabalho", "").strip().upper(),
            "numero_trabalho": dados.get("numero_trabalho", "").strip(),
            "bairro_trabalho": dados.get("bairro_trabalho", "").strip().upper(),
            "cidade_trabalho": dados.get("cidade_trabalho", "").strip().upper(),
            "uf_trabalho": dados.get("uf_trabalho", "").strip().upper(),

            "info_adicional": dados.get("info_adicional", "").strip().upper(),
            "status": dados.get("status", "A").strip() or "A",
        }

    def _normalizar_data(self, data_referencia):
        data_referencia = (data_referencia or "").strip()
        if not data_referencia:
            return None

        partes = data_referencia.split("/")
        if len(partes) == 3:
            return f"{partes[2]}-{partes[1]}-{partes[0]}"

        return None
