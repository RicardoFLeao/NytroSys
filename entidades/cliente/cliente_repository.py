from bd import conectar


class ClienteRepository:
    def garantir_tabela(self):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INT NOT NULL AUTO_INCREMENT,
                        codigo VARCHAR(20) DEFAULT NULL,
                        tipo_pessoa CHAR(1) DEFAULT NULL,
                        razao_social VARCHAR(150) DEFAULT NULL,
                        nome_fantasia VARCHAR(150) DEFAULT NULL,
                        contato VARCHAR(100) DEFAULT NULL,
                        whatsapp VARCHAR(20) DEFAULT NULL,
                        telefone VARCHAR(20) DEFAULT NULL,
                        email VARCHAR(100) DEFAULT NULL,
                        cep VARCHAR(10) DEFAULT NULL,
                        endereco VARCHAR(150) DEFAULT NULL,
                        numero VARCHAR(10) DEFAULT NULL,
                        bairro VARCHAR(100) DEFAULT NULL,
                        cidade VARCHAR(100) DEFAULT NULL,
                        uf VARCHAR(2) DEFAULT NULL,
                        cpf_cnpj VARCHAR(20) DEFAULT NULL,
                        inscricao_estadual VARCHAR(20) DEFAULT NULL,
                        inscricao_municipal VARCHAR(20) DEFAULT NULL,
                        data_referencia DATE DEFAULT NULL,
                        sexo VARCHAR(10) DEFAULT NULL,
                        info_adicional TEXT,
                        status CHAR(1) DEFAULT 'A',
                        PRIMARY KEY (id),
                        UNIQUE KEY uk_clientes_codigo (codigo),
                        UNIQUE KEY uk_clientes_cpf_cnpj (cpf_cnpj)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                    """
                )
            conexao.commit()
        except Exception as erro:
            print("ERRO AO GARANTIR TABELA CLIENTES:", erro)
        finally:
            if conexao is not None:
                conexao.close()

    def salvar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO clientes (
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
                        status,
                        nome_mae,
                        local_trabalho,
                        cargo,
                        salario,
                        telefone_trabalho,
                        nome_pai,
                        cidade_nascimento,
                        pais_nascimento,
                        tempo_servico,
                        cep_trabalho,
                        endereco_trabalho,
                        numero_trabalho,
                        bairro_trabalho,
                        cidade_trabalho,
                        uf_trabalho
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql,
                    (
                        dados["codigo"] or None,
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
                        dados["nome_mae"],
                        dados["local_trabalho"],
                        dados["cargo"],
                        dados["salario"],
                        dados["telefone_trabalho"],
                        dados["nome_pai"],
                        dados["cidade_nascimento"],
                        dados["pais_nascimento"],
                        dados["tempo_servico"],
                        dados["cep_trabalho"],
                        dados["endereco_trabalho"],
                        dados["numero_trabalho"],
                        dados["bairro_trabalho"],
                        dados["cidade_trabalho"],
                        dados["uf_trabalho"],
                    ),
                )

                id_gerado = cursor.lastrowid
                codigo = str(id_gerado)
                cursor.execute(
                    """
                    UPDATE clientes
                    SET codigo = %s
                    WHERE id = %s
                    """,
                    (codigo, id_gerado),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Cliente salvo com sucesso!"}

        except Exception as erro:
            print("ERRO AO SALVAR CLIENTE:", erro)
            return {"sucesso": False, "mensagem": "Erro ao salvar cliente."}

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_cliente(self, opcao, texto, status, buscar_todos):
        conexao = None

        try:
            conexao = conectar()

            mapa_campos = {
                "Codigo": "codigo",
                "Nome / Razão Social": "razao_social",
                "CPF / CNPJ": "cpf_cnpj",
                "WhatsApp": "whatsapp",
                "Email": "email",
                "E-mail": "email",
            }
            campo = mapa_campos.get(opcao)

            sql = """
                SELECT codigo, razao_social, cpf_cnpj, whatsapp, email, status
                FROM clientes
                WHERE 1=1
            """
            parametros = []

            status = status.strip().lower()

            if status == "ativos":
                sql += " AND status = %s"
                parametros.append("A")
            elif status in ("excluídos", "excluidos"):
                sql += " AND status = %s"
                parametros.append("E")

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
                return cursor.fetchall()

        except Exception as erro:
            print("ERRO NA BUSCA DE CLIENTE:", erro)
            return []

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_codigo(self, codigo):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
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
                        status,
                        nome_mae,
                        local_trabalho,
                        cargo,
                        salario,
                        telefone_trabalho,
                        nome_pai,
                        cidade_nascimento,
                        pais_nascimento,
                        tempo_servico,
                        cep_trabalho,
                        endereco_trabalho,
                        numero_trabalho,
                        bairro_trabalho,
                        cidade_trabalho,
                        uf_trabalho
                    FROM clientes
                    WHERE codigo = %s
                    """,
                    (codigo,),
                )
                return cursor.fetchone()

        except Exception as erro:
            print("ERRO AO BUSCAR CLIENTE POR CODIGO:", erro)
            return None

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_documento(self, cpf_cnpj):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT codigo, status
                    FROM clientes
                    WHERE cpf_cnpj = %s
                    LIMIT 1
                    """,
                    (cpf_cnpj,),
                )
                resultado = cursor.fetchone()

            if resultado:
                return {"codigo": resultado[0], "status": resultado[1]}

            return None

        except Exception as erro:
            print("ERRO AO BUSCAR CLIENTE POR DOCUMENTO:", erro)
            return None

        finally:
            if conexao is not None:
                conexao.close()

    def atualizar(self, dados):
        conexao = None

        try:
            conexao = conectar()

            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE clientes SET
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
                        status = %s,
                        nome_mae = %s,
                        local_trabalho = %s,
                        cargo = %s,
                        salario = %s,
                        telefone_trabalho = %s,
                        nome_pai = %s,
                        cidade_nascimento = %s,
                        pais_nascimento = %s,
                        tempo_servico = %s,
                        cep_trabalho = %s,
                        endereco_trabalho = %s,
                        numero_trabalho = %s,
                        bairro_trabalho = %s,
                        cidade_trabalho = %s,
                        uf_trabalho = %s
                    WHERE codigo = %s
                    """,
                    (
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
                        dados["nome_mae"],
                        dados["local_trabalho"],
                        dados["cargo"],
                        dados["salario"],
                        dados["telefone_trabalho"],
                        dados["nome_pai"],
                        dados["cidade_nascimento"],
                        dados["pais_nascimento"],
                        dados["tempo_servico"],
                        dados["cep_trabalho"],
                        dados["endereco_trabalho"],
                        dados["numero_trabalho"],
                        dados["bairro_trabalho"],
                        dados["cidade_trabalho"],
                        dados["uf_trabalho"],
                        dados["codigo"],
                    ),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Cliente atualizado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ATUALIZAR CLIENTE:", erro)
            return {"sucesso": False, "mensagem": "Erro ao atualizar cliente."}

        finally:
            if conexao is not None:
                conexao.close()

    def alterar_status(self, codigo, status):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE clientes
                    SET status = %s
                    WHERE codigo = %s
                    """,
                    (status, codigo),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Status atualizado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ALTERAR STATUS DE CLIENTE:", erro)
            return {"sucesso": False, "mensagem": "Erro ao alterar status."}

        finally:
            if conexao is not None:
                conexao.close()