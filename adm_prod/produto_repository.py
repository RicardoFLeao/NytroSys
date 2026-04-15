import pymysql

from bd import conectar


class ProdutoRepository:
    def salvar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
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
                cursor.execute(
                    sql,
                    (
                        dados["cod_barras"],
                        dados["cod_barras2"],
                        dados["ref_forn"],
                        dados["ref_orig"],
                        dados["ref_similar"],
                        dados["descricao"],
                        dados["aplicacao"],
                        dados["estoque_minimo"],
                        dados["cod_fornecedor"],
                        dados["nome_fornecedor"],
                        dados["repositor"],
                        dados["preco_custo"],
                        dados["preco_venda"],
                        dados["margem_lucro"],
                        dados["preco_promocao"],
                        dados["desconto"],
                        dados["tipo_quantidade"],
                    ),
                )

                id_gerado = cursor.lastrowid

                cursor.execute(
                    """
                    UPDATE produtos
                    SET codigo = %s
                    WHERE id = %s
                    """,
                    (str(id_gerado), id_gerado),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Produto salvo com sucesso!"}

        except Exception as erro:
            print("ERRO AO SALVAR PRODUTO:", erro)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao salvar produto."}

        finally:
            if conexao is not None:
                conexao.close()


    def atualizar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
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
                cursor.execute(
                    sql,
                    (
                        dados["cod_barras"],
                        dados["cod_barras2"],
                        dados["ref_forn"],
                        dados["ref_orig"],
                        dados["ref_similar"],
                        dados["descricao"],
                        dados["aplicacao"],
                        dados["estoque_minimo"],
                        dados["cod_fornecedor"],
                        dados["nome_fornecedor"],
                        dados["repositor"],
                        dados["preco_custo"],
                        dados["preco_venda"],
                        dados["margem_lucro"],
                        dados["preco_promocao"],
                        dados["desconto"],
                        dados["tipo_quantidade"],
                        dados["codigo"],
                    ),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Produto atualizado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ATUALIZAR PRODUTO:", erro)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao atualizar produto."}

        finally:
            if conexao is not None:
                conexao.close()


    def listar_para_consulta(self, status="Ativo"):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                    SELECT codigo, descricao, quantidade, preco_venda, status
                    FROM produtos
                """

                if status == "Ativo":
                    sql += " WHERE status = 'A'"
                elif status == "Excluído":
                    sql += " WHERE status = 'E'"

                sql += " ORDER BY descricao"

                cursor.execute(sql)
                return cursor.fetchall()

        except Exception as erro:
            print("ERRO AO LISTAR PRODUTOS:", erro)
            import traceback
            traceback.print_exc()
            return []

        finally:
            if conexao is not None:
                conexao.close()


    def pesquisar_para_consulta(self, opcao, valor, status="Ativo"):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                if opcao == "Descrição":
                    termos = valor.split()
                    condicoes = []
                    parametros = []

                    for termo in termos:
                        condicoes.append("(descricao LIKE %s OR aplicacao LIKE %s)")
                        filtro = f"%{termo}%"
                        parametros.extend([filtro, filtro])

                    where = " AND ".join(condicoes)

                    if status == "Ativo":
                        where += " AND status = 'A'"
                    elif status == "Excluído":
                        where += " AND status = 'E'"

                    sql = f"""
                        SELECT codigo, descricao, quantidade, preco_venda, status
                        FROM produtos
                        WHERE {where}
                        ORDER BY descricao
                    """
                    cursor.execute(sql, parametros)

                elif opcao == "Código":
                    sql = """
                        SELECT codigo, descricao, quantidade, preco_venda, status
                        FROM produtos
                        WHERE codigo = %s
                    """
                    parametros = [valor]

                    if status == "Ativo":
                        sql += " AND status = 'A'"
                    elif status == "Excluído":
                        sql += " AND status = 'E'"

                    sql += " ORDER BY descricao"

                    cursor.execute(sql, parametros)

                elif opcao == "Cód. Barras":
                    filtro = f"%{valor}%"
                    sql = """
                        SELECT codigo, descricao, quantidade, preco_venda, status
                        FROM produtos
                        WHERE (cod_barras LIKE %s OR cod_barras_2 LIKE %s)
                    """
                    parametros = [filtro, filtro]

                    if status == "Ativo":
                        sql += " AND status = 'A'"
                    elif status == "Excluído":
                        sql += " AND status = 'E'"

                    sql += " ORDER BY descricao"

                    cursor.execute(sql, parametros)

                elif opcao == "Referências":
                    filtro = "%" + "%".join(valor.split()) + "%"
                    sql = """
                        SELECT codigo, descricao, quantidade, preco_venda, status
                        FROM produtos
                        WHERE (ref_fornecedor LIKE %s
                        OR ref_original LIKE %s
                        OR ref_similar LIKE %s)
                    """
                    parametros = [filtro, filtro, filtro]

                    if status == "Ativo":
                        sql += " AND status = 'A'"
                    elif status == "Excluído":
                        sql += " AND status = 'E'"

                    sql += " ORDER BY descricao"

                    cursor.execute(sql, parametros)

                else:
                    return []

                return cursor.fetchall()

        except Exception as erro:
            print("ERRO AO PESQUISAR PRODUTOS:", erro)
            import traceback
            traceback.print_exc()
            return []

        finally:
            if conexao is not None:
                conexao.close()


    def buscar_por_codigo(self, codigo):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM produtos WHERE codigo = %s",
                    (codigo,),
                )
                return cursor.fetchone()

        except Exception as erro:
            print("ERRO AO BUSCAR PRODUTO:", erro)
            import traceback
            traceback.print_exc()
            return None

        finally:
            if conexao is not None:
                conexao.close()


    def alterar_status(self, codigo, status):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    "UPDATE produtos SET status = %s WHERE codigo = %s",
                    (status, codigo),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Status do produto alterado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ALTERAR STATUS DO PRODUTO:", erro)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao alterar status do produto."}

        finally:
            if conexao is not None:
                conexao.close()