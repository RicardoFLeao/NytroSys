import pymysql

from bd import conectar


class EstoqueRepository:
    def pesquisar_produtos(self, opcao, valor):
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
                    sql = f"""
                        SELECT codigo, descricao, quantidade, tipo_quantidade
                        FROM produtos
                        WHERE {where}
                        ORDER BY descricao
                    """
                    cursor.execute(sql, parametros)

                elif opcao == "Código":
                    cursor.execute(
                        """
                            SELECT codigo, descricao, quantidade, tipo_quantidade
                            FROM produtos
                            WHERE codigo = %s
                        """,
                        (valor,),
                    )

                elif opcao == "Referências":
                    filtro = "%" + "%".join(valor.split()) + "%"
                    cursor.execute(
                        """
                            SELECT codigo, descricao, quantidade, tipo_quantidade
                            FROM produtos
                            WHERE ref_fornecedor LIKE %s
                               OR ref_original LIKE %s
                               OR ref_similar LIKE %s
                            ORDER BY descricao
                        """,
                        (filtro, filtro, filtro),
                    )

                else:
                    return []

                return cursor.fetchall()

        except Exception as erro:
            print("ERRO AO PESQUISAR PRODUTOS NO ESTOQUE:", erro)
            import traceback
            traceback.print_exc()
            return []

        finally:
            if conexao is not None:
                conexao.close()

    def registrar_acerto_estoque(self, codigo, descricao, quant_antiga, quant_nova, usuario):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE produtos
                        SET quantidade = %s
                        WHERE codigo = %s
                    """,
                    (quant_nova, codigo),
                )

                cursor.execute(
                    """
                        INSERT INTO historico_estoque (
                            codigo_produto,
                            descricao,
                            quantidade_anterior,
                            quantidade_nova,
                            usuario
                        ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (codigo, descricao, quant_antiga, quant_nova, usuario),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Acerto de estoque registrado com sucesso!"}

        except Exception as erro:
            print("ERRO AO REGISTRAR ACERTO DE ESTOQUE:", erro)
            import traceback
            traceback.print_exc()

            if conexao is not None:
                conexao.rollback()

            return {"sucesso": False, "mensagem": "Não foi possível registrar o acerto de estoque."}

        finally:
            if conexao is not None:
                conexao.close()