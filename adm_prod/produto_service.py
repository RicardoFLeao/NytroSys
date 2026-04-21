from adm_prod.produto_repository import ProdutoRepository
from entidades.fornecedor.fornecedor_repository import FornecedorRepository
from adm_prod.marca_repository import MarcaRepository


class ProdutoService:
    def __init__(self, repository=None, fornecedor_repository=None):
        self.repository = repository or ProdutoRepository()
        self.fornecedor_repository = fornecedor_repository or FornecedorRepository()
        self.repository_marca = MarcaRepository()

    def listar_produtos_para_consulta(self):
        return self.repository.listar_para_consulta()

    def pesquisar_produtos_para_consulta(self, opcao, texto, buscar_todos=False, status=None):
        texto = (texto or "").strip().upper()
        status = (status or "").strip()

        if buscar_todos:
            return self.repository.listar_para_consulta(status=status)

        if not texto:
            return self.repository.listar_para_consulta(status=status)

        return self.repository.pesquisar_para_consulta(opcao, texto, status=status)

    def buscar_produto_por_codigo(self, codigo):
        codigo = (codigo or "").strip()
        if not codigo:
            return None
        return self.repository.buscar_por_codigo(codigo)

    def salvar_produto(self, dados_formulario):
        validacao = self._validar_dados(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        dados_tratados = self._tratar_dados(dados_formulario)

        dados_tratados["cod_marca"] = dados_formulario.get("cod_marca")
        return self.repository.salvar(dados_tratados)

    def atualizar_produto(self, dados_formulario):
        codigo = (dados_formulario.get("codigo") or "").strip()
        if not codigo:
            return {"sucesso": False, "mensagem": "Código do produto é obrigatório para atualização."}

        validacao = self._validar_dados(dados_formulario)
        if not validacao["sucesso"]:
            return validacao

        dados_tratados = self._tratar_dados(dados_formulario)
        return self.repository.atualizar(dados_tratados)

    def calcular_preco_venda(self, preco_custo_texto, margem_texto):
        preco_custo = self._to_float(preco_custo_texto)
        margem = self._to_float(margem_texto)

        if preco_custo <= 0:
            raise ValueError("Preço de custo deve ser maior que zero.")

        return preco_custo + (preco_custo * margem / 100)

    def calcular_margem_lucro(self, preco_custo_texto, preco_venda_texto):
        preco_custo = self._to_float(preco_custo_texto)
        preco_venda = self._to_float(preco_venda_texto)

        if preco_custo <= 0:
            raise ValueError("Preço de custo deve ser maior que zero.")

        return ((preco_venda - preco_custo) / preco_custo) * 100

    def _validar_dados(self, dados):
        descricao = (dados.get("descricao") or "").strip()
        if not descricao:
            return {"sucesso": False, "mensagem": "Descrição é obrigatória."}

        tipo_quantidade = (dados.get("tipo_quantidade") or "").strip()
        if tipo_quantidade not in {"Inteiro", "Decimal"}:
            return {"sucesso": False, "mensagem": "Tipo de quantidade inválido."}

        for campo in ("estoque_minimo", "preco_custo", "preco_venda", "preco_promocao", "margem_lucro", "desconto"):
            try:
                self._to_float(dados.get(campo))
            except ValueError:
                return {"sucesso": False, "mensagem": f"Valor inválido para {campo.replace('_', ' ')}."}

        cod_fornecedor = (dados.get("cod_fornecedor") or "").strip()
        if cod_fornecedor:
            fornecedor = self.fornecedor_repository.buscar_por_codigo(
                cod_fornecedor)
            if not fornecedor:
                return {"sucesso": False, "mensagem": "Fornecedor não foi encontrado."}

            status = fornecedor.get("status", "")
            if status == "E":
                return {"sucesso": False, "mensagem": "Fornecedor informado está excluído."}

        return {"sucesso": True, "mensagem": ""}

    def _tratar_dados(self, dados):
        cod_fornecedor = (dados.get("cod_fornecedor") or "").strip()
        nome_fornecedor = (dados.get("nome_fornecedor") or "").strip().upper()

        if cod_fornecedor:
            fornecedor = self.fornecedor_repository.buscar_por_codigo(
                cod_fornecedor)
            if fornecedor:
                nome_fornecedor = (
                    fornecedor.get("nome_fantasia")
                    or fornecedor.get("razao_social")
                    or ""
                ).strip().upper()

        return {
            "codigo": (dados.get("codigo") or "").strip(),
            "cod_barras": (dados.get("cod_barras") or "").strip(),
            "cod_barras2": (dados.get("cod_barras2") or "").strip(),
            "descricao": (dados.get("descricao") or "").strip().upper(),
            "ref_forn": (dados.get("ref_forn") or "").strip().upper(),
            "ref_orig": (dados.get("ref_orig") or "").strip().upper(),
            "ref_similar": (dados.get("ref_similar") or "").strip().upper(),
            "aplicacao": (dados.get("aplicacao") or "").strip().upper(),
            "estoque_minimo": self._to_float(dados.get("estoque_minimo")),
            "cod_fornecedor": cod_fornecedor,
            "nome_fornecedor": nome_fornecedor,
            "repositor": (dados.get("repositor") or "").strip().upper(),
            "un_compra": (dados.get("un_compra") or "").strip().upper(),
            "quant_compra": self._to_float(dados.get("quant_compra")),
            "un_venda": (dados.get("un_venda") or "").strip().upper(),
            "quant_venda": self._to_float(dados.get("quant_venda")),
            "preco_custo": self._to_float(dados.get("preco_custo")),
            "preco_venda": self._to_float(dados.get("preco_venda")),
            "preco_promocao": self._to_float(dados.get("preco_promocao")),
            "margem_lucro": self._to_float(dados.get("margem_lucro")),
            "desconto": self._to_float(dados.get("desconto")),
            "tipo_quantidade": (dados.get("tipo_quantidade") or "").strip(),
            "cod_marca": dados.get("cod_marca"),
            "rua": (dados.get("rua") or "").strip().upper(),
            "bloco": (dados.get("bloco") or "").strip().upper(),
            "prateleira": (dados.get("prateleira") or "").strip().upper(),
            "gaveta": (dados.get("gaveta") or "").strip().upper(),
            "foto_1": (dados.get("foto_1") or "").strip(),
            "foto_2": (dados.get("foto_2") or "").strip(),
            "foto_3": (dados.get("foto_3") or "").strip(),
        }

    def _to_float(self, valor):
        texto = str(valor or "").strip()
        if not texto or texto == "None":
            return 0.0

        texto = texto.replace(" ", "")
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")

        return float(texto)

    def alterar_status_produto(self, codigo, status_atual):
        codigo = (codigo or "").strip()

        if not codigo:
            return {
                "sucesso": False,
                "mensagem": "Código do produto inválido."
            }

        if status_atual == "A":
            novo_status = "E"
            mensagem = "Produto excluído com sucesso."
        else:
            novo_status = "A"
            mensagem = "Produto ativado com sucesso."

        return self.repository.alterar_status(codigo, novo_status)

    def buscar_marca_por_codigo(self, codigo):
        return self.repository_marca.buscar_por_codigo(codigo)
