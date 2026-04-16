from bd import conectar


class MarcaRepository:
    def salvar(self, nome):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "INSERT INTO marcas_produto (nome) VALUES (%s)"
            cursor.execute(sql, (nome,))
            conexao.commit()

            id_gerado = cursor.lastrowid
            codigo = str(id_gerado)

            sql_update = "UPDATE marcas_produto SET codigo = %s WHERE id = %s"
            cursor.execute(sql_update, (codigo, id_gerado))
            conexao.commit()

            return True

        except Exception as e:
            print(f"Erro ao salvar marca: {e}")
            return False

        finally:
            if conexao:
                conexao.close()

    def listar(self, texto="", opcao="Descrição", status="Todos"):
        conexao = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "SELECT codigo, nome, status FROM marcas_produto WHERE 1=1"
            parametros = []

            # 🔍 busca em TODA a linha (codigo + nome)
            if texto:
                sql += " AND (nome LIKE %s OR codigo LIKE %s)"
                parametros.append(f"%{texto}%")
                parametros.append(f"%{texto}%")

            # 🎯 filtro por status
            if status == "Ativo":
                sql += " AND status = 'A'"
            elif status == "Excluído":
                sql += " AND status = 'E'"

            sql += " ORDER BY nome"

            cursor.execute(sql, parametros)
            return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao listar marcas: {e}")
            return []

        finally:
            if conexao:
                conexao.close()

    def atualizar(self, codigo, nome):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
                UPDATE marcas_produto
                SET nome = %s
                WHERE codigo = %s
            """
            cursor.execute(sql, (nome, codigo))
            conexao.commit()
            return True

        except Exception as e:
            print(f"Erro ao atualizar marca: {e}")
            return False

        finally:
            if conexao:
                conexao.close()


    def alterar_status(self, codigo, status):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "UPDATE marcas_produto SET status = %s WHERE codigo = %s"
            cursor.execute(sql, (status, codigo))
            conexao.commit()
            return True

        except Exception as e:
            print(f"Erro ao alterar status da marca: {e}")
            return False

        finally:
            if conexao:
                conexao.close()

    def buscar_por_codigo(self, codigo):
        conexao = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "SELECT codigo, nome FROM marcas_produto WHERE codigo = %s"
            cursor.execute(sql, (codigo,))

            resultado = cursor.fetchone()

            if resultado:
                return {
                    "codigo": resultado[0],
                    "nome": resultado[1]
                }

            return None

        except Exception as e:
            print(f"Erro ao buscar marca: {e}")
            return None

        finally:
            if conexao:
                conexao.close()