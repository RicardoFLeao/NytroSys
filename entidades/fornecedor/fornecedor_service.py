from util.fun_basicas import validar_cnpj, validar_cpf
from entidades.fornecedor.fornecedor_repository import FornecedorRepository


class FornecedorService:
    def __init__(self, repository=None):
        self.repository = repository or FornecedorRepository()

    def salvar_fornecedor(self, dados_formulario):
        razao_social = dados_formulario.get("razao_social", "").strip().upper()
        if not razao_social:
            return {"sucesso": False, "mensagem": "Razão social / nome é obrigatório."}

        tipo_pessoa = dados_formulario.get("tipo_pessoa", "").strip()
        if tipo_pessoa not in {"J", "F"}:
            return {"sucesso": False, "mensagem": "Selecione Jurídica ou Física."}

        cpf_cnpj = dados_formulario.get("cpf_cnpj", "").strip()

        # 🔥 VALIDAÇÃO CPF/CNPJ
        validacao_documento = self.validar_documento(tipo_pessoa, cpf_cnpj)
        if not validacao_documento["sucesso"]:
            return validacao_documento

        # 🔥 NOVO: VERIFICAR SE JÁ EXISTE
        existente = self.repository.buscar_por_documento(cpf_cnpj)

        if existente:
            status = existente.get("status")

            if status == "A":
                return {"sucesso": False, "mensagem": "Fornecedor já cadastrado."}

            elif status == "E":
                return {"sucesso": False, "mensagem": "Fornecedor já cadastrado (excluído)."}

        dados_tratados = self._tratar_dados(dados_formulario)
        return self.repository.salvar(dados_tratados)


    def buscar_fornecedor(self, opcao, texto, ativo, buscar_todos):
        texto = (texto or "").strip()
        opcao = (opcao or "").strip()
        ativo = (ativo or "").strip()

        # 🔥 remover máscara para CPF/CNPJ e telefone
        if opcao in ("CPF / CNPJ", "Telefone"):
            texto = "".join(filter(str.isdigit, texto))

        if not texto and not buscar_todos:
            return []

        return self.repository.buscar_fornecedor(opcao, texto, ativo, buscar_todos)

    def validar_documento(self, tipo_pessoa, documento):
        numeros_doc = "".join(filter(str.isdigit, documento or ""))

        if not numeros_doc:
            return {"sucesso": True, "mensagem": ""}

        if tipo_pessoa == "J":
            if len(numeros_doc) != 14 or not validar_cnpj(numeros_doc):
                return {"sucesso": False, "mensagem": "CNPJ inválido."}

        elif tipo_pessoa == "F":
            if len(numeros_doc) != 11 or not validar_cpf(numeros_doc):
                return {"sucesso": False, "mensagem": "CPF inválido."}

        else:
            return {"sucesso": False, "mensagem": "Selecione Jurídica ou Física."}

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
            "info_adicional": dados.get("info_adicional", "").strip().upper(),
            "status": dados.get("status", "A").strip(),
        }

    def _normalizar_data(self, data_referencia):
        data_referencia = (data_referencia or "").strip()
        if not data_referencia:
            return None

        partes = data_referencia.split("/")
        if len(partes) == 3:
            return f"{partes[2]}-{partes[1]}-{partes[0]}"

        return None
    

    def buscar_por_codigo(self, codigo):
        return self.repository.buscar_por_codigo(codigo)
    
    def atualizar_fornecedor(self, dados_formulario):
        razao_social = dados_formulario.get("razao_social", "").strip().upper()
        if not razao_social:
            return {"sucesso": False, "mensagem": "Razão social / nome é obrigatório."}

        tipo_pessoa = dados_formulario.get("tipo_pessoa", "").strip()
        if tipo_pessoa not in {"J", "F"}:
            return {"sucesso": False, "mensagem": "Selecione Jurídica ou Física."}

        cpf_cnpj = dados_formulario.get("cpf_cnpj", "").strip()
        validacao_documento = self.validar_documento(tipo_pessoa, cpf_cnpj)
        if not validacao_documento["sucesso"]:
            return validacao_documento

        dados_tratados = self._tratar_dados(dados_formulario)
        return self.repository.atualizar(dados_tratados)
    
    def excluir_fornecedor(self, codigo):
        if not codigo:
            return {"sucesso": False, "mensagem": "Código inválido."}

        return self.repository.excluir(codigo)

    def alterar_status(self, codigo, status):
        return self.repository.alterar_status(codigo, status)
