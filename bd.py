import pymysql


def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="aut_com",
        port=3306
    )


def verificar_login(usuario, senha):
    conexao = None

    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = """
                SELECT id
                FROM funcionarios
                WHERE usuario = %s
                  AND senha = %s
                  AND status = %s
                LIMIT 1
            """
            cursor.execute(sql, (usuario, senha, "A"))
            resultado = cursor.fetchone()
            return resultado is not None

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()


def salvar_produto(dados):
    conexao = None
    try:
        conexao = conectar()

        cod_barras = dados["cod_barras"].strip()
        cod_barras_2 = dados["cod_barras2"].strip()
        descricao = dados["descricao"].strip()
        ref_fornecedor = dados["ref_forn"].strip()
        ref_original = dados["ref_orig"].strip()
        ref_similar = dados["ref_similar"].strip()
        aplicacao = dados["aplicacao"].strip()

        estoque_minimo = float(dados["estoque_minimo"].replace(",", ".")) if dados["estoque_minimo"] else 0
        cod_fornecedor = dados["cod_fornecedor"].strip()
        nome_fornecedor = dados["nome_fornecedor"].strip()
        repositor = dados["repositor"].strip()

        preco_custo = float(dados["preco_custo"].replace(",", ".")) if dados["preco_custo"] else 0
        preco_venda = float(dados["preco_venda"].replace(",", ".")) if dados["preco_venda"] else 0
        preco_promocao = float(dados["preco_promocao"].replace(",", ".")) if dados["preco_promocao"] else 0
        margem_lucro = float(dados["margem_lucro"].replace(",", ".")) if dados["margem_lucro"] else 0
        desconto = float(dados["desconto"].replace(",", ".")) if dados["desconto"] else 0

        with conexao.cursor() as cursor:
            sql = """
                INSERT INTO produtos (
                    cod_barras,
                    cod_barras_2,
                    ref_fornecedor,
                    ref_original,
                    ref_similar,
                    descricao,
                    aplicacao,
                    estoque_minimo,
                    cod_fornecedor,
                    nome_fornecedor,
                    repositor,
                    preco_custo,
                    preco_venda,
                    margem_lucro,
                    preco_promocao,
                    desconto,
                    tipo_quantidade
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                cod_barras,
                cod_barras_2,
                ref_fornecedor,
                ref_original,
                ref_similar,
                descricao,
                aplicacao,
                estoque_minimo,
                cod_fornecedor,
                nome_fornecedor,
                repositor,
                preco_custo,
                preco_venda,
                margem_lucro,
                preco_promocao,
                desconto,
                dados["tipo_quantidade"]
            ))

            id_gerado = cursor.lastrowid

            sql_update = """
                UPDATE produtos
                SET codigo = %s
                WHERE id = %s
            """
            cursor.execute(sql_update, (str(id_gerado), id_gerado))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()

def listar_produtos():
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = """
                SELECT 
                    codigo,
                    descricao,
                    quantidade,
                    preco_venda
                FROM produtos
                ORDER BY descricao
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return []

    finally:
        if conexao is not None:
            conexao.close()


def buscar_produto_por_codigo(codigo):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM produtos WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            return cursor.fetchone()

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return None

    finally:
        if conexao:
            conexao.close()

def atualizar_produto(dados):
    conexao = None
    try:
        conexao = conectar()

        codigo = dados["codigo"].strip()
        cod_barras = dados["cod_barras"].strip()
        cod_barras_2 = dados["cod_barras2"].strip()
        descricao = dados["descricao"].strip()
        ref_fornecedor = dados["ref_forn"].strip()
        ref_original = dados["ref_orig"].strip()
        ref_similar = dados["ref_similar"].strip()
        aplicacao = dados["aplicacao"].strip()

        estoque_minimo = float(dados["estoque_minimo"].replace(",", ".")) if dados["estoque_minimo"] else 0
        cod_fornecedor = dados["cod_fornecedor"].strip()
        nome_fornecedor = dados["nome_fornecedor"].strip()
        repositor = dados["repositor"].strip()

        preco_custo = float(dados["preco_custo"].replace(",", ".")) if dados["preco_custo"] else 0
        preco_venda = float(dados["preco_venda"].replace(",", ".")) if dados["preco_venda"] else 0
        margem_lucro = float(dados["margem_lucro"].replace(",", ".")) if dados["margem_lucro"] else 0
        desconto = float(dados["desconto"].replace(",", ".")) if dados["desconto"] else 0
       
        valor = dados["preco_promocao"]

        if valor and valor != "None":
            preco_promocao = float(valor.replace(",", "."))
        else:
            preco_promocao = 0

        with conexao.cursor() as cursor:
            sql = """
                UPDATE produtos
                SET
                    cod_barras = %s,
                    cod_barras_2 = %s,
                    ref_fornecedor = %s,
                    ref_original = %s,
                    ref_similar = %s,
                    descricao = %s,
                    aplicacao = %s,
                    estoque_minimo = %s,
                    cod_fornecedor = %s,
                    nome_fornecedor = %s,
                    repositor = %s,
                    preco_custo = %s,
                    preco_venda = %s,
                    margem_lucro = %s,
                    preco_promocao = %s,
                    desconto = %s,
                    tipo_quantidade = %s
                WHERE codigo = %s
            """

            cursor.execute(sql, (
                cod_barras,
                cod_barras_2,
                ref_fornecedor,
                ref_original,
                ref_similar,
                descricao,
                aplicacao,
                estoque_minimo,
                cod_fornecedor,
                nome_fornecedor,
                repositor,
                preco_custo,
                preco_venda,
                margem_lucro,
                preco_promocao,
                desconto,
                dados["tipo_quantidade"],
                codigo
            ))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()
            
def pesquisar_produtos_avancado(opcao, valor):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            if opcao == "Descrição":
                termos = valor.split()

                condicoes = []
                parametros = []

                for termo in termos:
                    condicoes.append("(descricao LIKE %s OR aplicacao LIKE %s)")
                    filtro = f"%{termo}%"
                    parametros.extend([filtro, filtro])

                where = " AND ".join(condicoes)

                sql = f"""
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        preco_venda,
                        tipo_quantidade
                    FROM produtos
                    WHERE {where}
                    ORDER BY descricao
                """

                cursor.execute(sql, parametros)

            elif opcao == "Código":
                sql = """
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        preco_venda,
                        tipo_quantidade
                    FROM produtos
                    WHERE codigo = %s
                    ORDER BY descricao
                """
                cursor.execute(sql, (valor,))

            elif opcao == "Cód. Barras":
                sql = """
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        preco_venda,
                        tipo_quantidade
                    FROM produtos
                    WHERE cod_barras LIKE %s
                       OR cod_barras_2 LIKE %s
                    ORDER BY descricao
                """
                filtro = f"%{valor}%"
                cursor.execute(sql, (filtro, filtro))

            elif opcao == "Referências":
                termos = valor.split()
                filtro = "%" + "%".join(termos) + "%"

                sql = """
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        preco_venda,
                        tipo_quantidade
                    FROM produtos
                    WHERE ref_fornecedor LIKE %s
                       OR ref_original LIKE %s
                       OR ref_similar LIKE %s
                    ORDER BY descricao
                """
                cursor.execute(sql, (filtro, filtro, filtro))

            else:
                return []

            return cursor.fetchall()

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return []

    finally:
        if conexao is not None:
            conexao.close()


def excluir_produto(codigo):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = "DELETE FROM produtos WHERE codigo = %s"
            cursor.execute(sql, (codigo,))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()

def atualizar_quantidade_produto(codigo, nova_quantidade):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = """
                UPDATE produtos
                SET quantidade = %s
                WHERE codigo = %s
            """
            cursor.execute(sql, (nova_quantidade, codigo))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()



def salvar_historico_estoque(codigo, descricao, quant_antiga, quant_nova, usuario):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = """
                INSERT INTO historico_estoque (
                    codigo_produto,
                    descricao,
                    quantidade_anterior,
                    quantidade_nova,
                    usuario
                ) VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                codigo,
                descricao,
                quant_antiga,
                quant_nova,
                usuario
            ))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()


def pesquisar_produtos_estoque(opcao, valor):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            if opcao == "Descrição":
                termos = valor.split()

                condicoes = []
                parametros = []

                for termo in termos:
                    condicoes.append("(descricao LIKE %s OR aplicacao LIKE %s)")
                    filtro = f"%{termo}%"
                    parametros.extend([filtro, filtro])

                where = " AND ".join(condicoes)

                sql = f"""
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        tipo_quantidade
                    FROM produtos
                    WHERE {where}
                    ORDER BY descricao
                """

                cursor.execute(sql, parametros)

            elif opcao == "Código":
                sql = """
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        tipo_quantidade
                    FROM produtos
                    WHERE codigo = %s
                """
                cursor.execute(sql, (valor,))

            elif opcao == "Referências":
                termos = valor.split()
                filtro = "%" + "%".join(termos) + "%"

                sql = """
                    SELECT 
                        codigo,
                        descricao,
                        quantidade,
                        tipo_quantidade
                    FROM produtos
                    WHERE ref_fornecedor LIKE %s
                       OR ref_original LIKE %s
                       OR ref_similar LIKE %s
                """
                cursor.execute(sql, (filtro, filtro, filtro))

            else:
                return []

            return cursor.fetchall()

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return []

    finally:
        if conexao is not None:
            conexao.close()

def salvar_fornecedor(dados):
    conexao = None
    try:
        conexao = conectar()

        codigo = dados["codigo"].strip()
        tipo_pessoa = dados["tipo_pessoa"].strip()
        razao_social = dados["razao_social"].strip()
        nome_fantasia = dados["nome_fantasia"].strip()
        contato = dados["contato"].strip()
        whatsapp = dados["whatsapp"].strip()
        telefone = dados["telefone"].strip()
        email = dados["email"].strip()
        cep = dados["cep"].strip()
        endereco = dados["endereco"].strip()
        numero = dados["numero"].strip()
        bairro = dados["bairro"].strip()
        cidade = dados["cidade"].strip()
        uf = dados["uf"].strip()
        cpf_cnpj = dados["cpf_cnpj"].strip()
        inscricao_estadual = dados["inscricao_estadual"].strip()
        inscricao_municipal = dados["inscricao_municipal"].strip()
        
        data_referencia = dados["data_referencia"].strip()
        if data_referencia:
            partes = data_referencia.split("/")
            if len(partes) == 3:
                data_referencia = f"{partes[2]}-{partes[1]}-{partes[0]}"
            else:
                data_referencia = None
        else:
            data_referencia = None

        sexo = dados["sexo"].strip()
        info_adicional = dados["info_adicional"].strip()
        ativo = dados["ativo"].strip()

        with conexao.cursor() as cursor:
            sql_verifica = """
                SELECT id FROM fornecedores
                WHERE cpf_cnpj = %s
            """
            cursor.execute(sql_verifica, (cpf_cnpj,))

            if cursor.fetchone():
                return "existe"

            sql = """
                INSERT INTO fornecedores (
                    codigo,
                    tipo_pessoa,
                    razao_social,
                    nome_fantasia,
                    contato,
                    whatsapp,
                    telefone,
                    email,
                    cep,
                    endereco,
                    numero,
                    bairro,
                    cidade,
                    uf,
                    cpf_cnpj,
                    inscricao_estadual,
                    inscricao_municipal,
                    data_referencia,
                    sexo,
                    info_adicional,
                    ativo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                codigo,
                tipo_pessoa,
                razao_social,
                nome_fantasia,
                contato,
                whatsapp,
                telefone,
                email,
                cep,
                endereco,
                numero,
                bairro,
                cidade,
                uf,
                cpf_cnpj,
                inscricao_estadual,
                inscricao_municipal,
                data_referencia,
                sexo,
                info_adicional,
                ativo
            ))

            id_gerado = cursor.lastrowid

            sql_update = """
                UPDATE fornecedores
                SET codigo = %s
                WHERE id = %s
            """
            cursor.execute(sql_update, (str(id_gerado), id_gerado))

        conexao.commit()
        return True

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return False

    finally:
        if conexao is not None:
            conexao.close()