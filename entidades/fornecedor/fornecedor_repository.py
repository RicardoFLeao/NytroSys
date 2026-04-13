from bd import conectar


class FornecedorRepository:
    def salvar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
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
                        status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql, (
                    dados["codigo"],
                    dados["tipo_pessoa"],
                    dados["razao_social"],
                    dados["nome_fantasia"],
                    dados["contato"],
                    dados["whatsapp"],
                    dados["telefone"],
                    dados["email"],
                    dados["cep"],
                    dados["endereco"],
                    dados["numero"],
                    dados["bairro"],
                    dados["cidade"],
                    dados["uf"],
                    dados["cpf_cnpj"],
                    dados["inscricao_estadual"],
                    dados["inscricao_municipal"],
                    dados["data_referencia"],
                    dados["sexo"],
                    dados["info_adicional"],
                    dados["status"],
                ))

                id_gerado = cursor.lastrowid

                sql_update = """
                    UPDATE fornecedores
                    SET codigo = %s
                    WHERE id = %s
                """
                cursor.execute(sql_update, (str(id_gerado), id_gerado))

            conexao.commit()
            return {"sucesso": True, "mensagem": "Fornecedor salvo com sucesso!"}

        except Exception as e:
            print("ERRO AO SALVAR FORNECEDOR:", e)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao salvar fornecedor."}

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_fornecedor(self, opcao, texto, status, buscar_todos):
        conexao = None

        try:
            conexao = conectar()

            mapa_campos = {
                "Código": "codigo",
                "Nome / Razão Social": "razao_social",
                "CPF / CNPJ": "cpf_cnpj",
                "WhatsApp": "whatsapp",
                "Email": "email",
                "E-mail": "email",
            }

            campo = mapa_campos.get(opcao)

            sql = """
                SELECT codigo, razao_social, cpf_cnpj, whatsapp, email, status
                FROM fornecedores
                WHERE 1=1
            """
            parametros = []

            if status == "Ativos":
                sql += " AND status = %s"
                parametros.append("A")
            elif status == "Exclúidos" or status == "Excluídos":
                sql += " AND status = %s"
                parametros.append("E")
            elif status == "Todos":
                pass

            if not buscar_todos and campo and texto:
                if opcao in ("CPF / CNPJ", "WhatsApp"):
                    sql += f"""
                        AND REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        REPLACE({campo}, '.', ''),
                                    '-', ''),
                                '/', ''),
                            '(', ''),
                        ')', '') LIKE %s
                    """
                    parametros.append(f"%{texto}%")
                else:
                    sql += f" AND {campo} LIKE %s"
                    parametros.append(f"%{texto}%")

            sql += " ORDER BY razao_social"

            with conexao.cursor() as cursor:
                cursor.execute(sql, tuple(parametros))
                resultados = cursor.fetchall()

            return resultados

        except Exception as e:
            print("ERRO NA BUSCA DE FORNECEDOR:", e)
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

            sql = """
                SELECT *
                FROM fornecedores
                WHERE codigo = %s
            """

            with conexao.cursor() as cursor:
                cursor.execute(sql, (codigo,))
                resultado = cursor.fetchone()

            return resultado

        except Exception as e:
            print("ERRO AO BUSCAR FORNECEDOR POR CÓDIGO:", e)
            import traceback
            traceback.print_exc()
            return None

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_documento(self, cpf_cnpj):
        conexao = None

        try:
            conexao = conectar()

            sql = """
                SELECT codigo, status
                FROM fornecedores
                WHERE cpf_cnpj = %s
                LIMIT 1
            """

            with conexao.cursor() as cursor:
                cursor.execute(sql, (cpf_cnpj,))
                resultado = cursor.fetchone()

            if resultado:
                return {
                    "codigo": resultado[0],
                    "status": resultado[1]
                }

            return None

        except Exception as e:
            print("ERRO AO BUSCAR FORNECEDOR POR DOCUMENTO:", e)
            import traceback
            traceback.print_exc()
            return None

        finally:
            if conexao is not None:
                conexao.close()

    def atualizar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                sql = """
                    UPDATE fornecedores SET
                        tipo_pessoa = %s,
                        razao_social = %s,
                        nome_fantasia = %s,
                        contato = %s,
                        whatsapp = %s,
                        telefone = %s,
                        email = %s,
                        cep = %s,
                        endereco = %s,
                        numero = %s,
                        bairro = %s,
                        cidade = %s,
                        uf = %s,
                        cpf_cnpj = %s,
                        inscricao_estadual = %s,
                        inscricao_municipal = %s,
                        data_referencia = %s,
                        sexo = %s,
                        info_adicional = %s,
                        status = %s
                    WHERE codigo = %s
                """

                cursor.execute(sql, (
                    dados["tipo_pessoa"],
                    dados["razao_social"],
                    dados["nome_fantasia"],
                    dados["contato"],
                    dados["whatsapp"],
                    dados["telefone"],
                    dados["email"],
                    dados["cep"],
                    dados["endereco"],
                    dados["numero"],
                    dados["bairro"],
                    dados["cidade"],
                    dados["uf"],
                    dados["cpf_cnpj"],
                    dados["inscricao_estadual"],
                    dados["inscricao_municipal"],
                    dados["data_referencia"],
                    dados["sexo"],
                    dados["info_adicional"],
                    dados["status"],
                    dados["codigo"],
                ))

            conexao.commit()
            return {"sucesso": True, "mensagem": "Fornecedor atualizado com sucesso!"}

        except Exception as e:
            print("ERRO AO ATUALIZAR FORNECEDOR:", e)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao atualizar fornecedor."}

        finally:
            if conexao is not None:
                conexao.close()

    def excluir(self, codigo):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                sql = """
                    UPDATE fornecedores
                    SET status = %s
                    WHERE codigo = %s
                """
                cursor.execute(sql, ("E", codigo))

            conexao.commit()
            return {"sucesso": True, "mensagem": "Fornecedor excluído com sucesso!"}

        except Exception as e:
            print("ERRO AO EXCLUIR FORNECEDOR:", e)
            import traceback
            traceback.print_exc()
            return {"sucesso": False, "mensagem": "Erro ao excluir fornecedor."}

        finally:
            if conexao is not None:
                conexao.close()

    def alterar_status(self, codigo, status):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                sql = """
                    UPDATE fornecedores
                    SET status = %s
                    WHERE codigo = %s
                """
                cursor.execute(sql, (status, codigo))

            conexao.commit()
            return {"sucesso": True, "mensagem": "Status atualizado com sucesso!"}

        except Exception as e:
            print("ERRO AO ALTERAR STATUS:", e)
            return {"sucesso": False, "mensagem": "Erro ao alterar status."}

        finally:
            if conexao:
                conexao.close()
