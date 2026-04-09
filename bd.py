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
    print(f">>> Verificando login para: {usuario} / {senha}")
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
            cursor.execute(sql, (usuario, senha))
            resultado = cursor.fetchone()
            return resultado

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return None


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
                    preco_custo,
                    preco_venda,
                    margem_lucro,
                    preco_promocao,
                    desconto
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                cod_barras,
                cod_barras_2,
                ref_fornecedor,
                ref_original,
                ref_similar,
                descricao,
                aplicacao,
                preco_custo,
                preco_venda,
                margem_lucro,
                preco_promocao,
                desconto
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
                    0 AS quantidade,
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

        preco_custo = float(dados["preco_custo"].replace(",", ".")) if dados["preco_custo"] else 0
        preco_venda = float(dados["preco_venda"].replace(",", ".")) if dados["preco_venda"] else 0
        preco_promocao = float(dados["preco_promocao"].replace(",", ".")) if dados["preco_promocao"] else 0
        margem_lucro = float(dados["margem_lucro"].replace(",", ".")) if dados["margem_lucro"] else 0
        desconto = float(dados["desconto"].replace(",", ".")) if dados["desconto"] else 0

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
                    preco_custo = %s,
                    preco_venda = %s,
                    margem_lucro = %s,
                    preco_promocao = %s,
                    desconto = %s
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
                preco_custo,
                preco_venda,
                margem_lucro,
                preco_promocao,
                desconto,
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


def pesquisar_produtos(nome_pesquisa=""):
    conexao = None
    try:
        conexao = conectar()

        with conexao.cursor() as cursor:
            sql = """
                SELECT 
                    codigo,
                    descricao,
                    0 AS quantidade,
                    preco_venda
                FROM produtos
                WHERE descricao LIKE %s
                ORDER BY descricao
            """
            termos = nome_pesquisa.split()
            filtro = "%" + "%".join(termos) + "%"

            cursor.execute(sql, (filtro,))
            resultados = cursor.fetchall()
            return resultados

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return []

    finally:
        if conexao is not None:
            conexao.close()