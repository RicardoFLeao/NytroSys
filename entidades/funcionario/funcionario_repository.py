import pymysql

from bd import conectar


class FuncionarioRepository:
    def garantir_tabela(self):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS funcionarios (
                        id INT NOT NULL AUTO_INCREMENT,
                        codigo VARCHAR(20) DEFAULT NULL,
                        nome VARCHAR(100) DEFAULT NULL,
                        usuario VARCHAR(50) DEFAULT NULL,
                        senha VARCHAR(50) DEFAULT NULL,
                        apelido VARCHAR(50) DEFAULT NULL,
                        endereco TEXT,
                        numero VARCHAR(10) DEFAULT NULL,
                        bairro VARCHAR(100) DEFAULT NULL,
                        cep VARCHAR(10) DEFAULT NULL,
                        telefone1 VARCHAR(20) DEFAULT NULL,
                        telefone2 VARCHAR(20) DEFAULT NULL,
                        rg VARCHAR(20) DEFAULT NULL,
                        cpf VARCHAR(11) DEFAULT NULL,
                        data_nascimento DATE DEFAULT NULL,
                        sexo VARCHAR(10) DEFAULT NULL,
                        nome_mae VARCHAR(150) DEFAULT NULL,
                        nome_pai VARCHAR(150) DEFAULT NULL,
                        cidade_nascimento VARCHAR(100) DEFAULT NULL,
                        pais_nascimento VARCHAR(100) DEFAULT NULL,
                        carteira_trabalho VARCHAR(30) DEFAULT NULL,
                        email VARCHAR(100) DEFAULT NULL,
                        cargo VARCHAR(50) DEFAULT NULL,
                        salario DECIMAL(10,2) DEFAULT NULL,
                        estado CHAR(2) DEFAULT NULL,
                        cidade VARCHAR(150) DEFAULT NULL,
                        data_admissao DATE DEFAULT NULL,
                        pis_pasep VARCHAR(30) DEFAULT NULL,
                        data_demissao DATE DEFAULT NULL,
                        motivo_demissao VARCHAR(255) DEFAULT NULL,
                        info_adicional TEXT,
                        status CHAR(1) DEFAULT 'A',
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                    """
                )

                cursor.execute("SHOW COLUMNS FROM funcionarios")
                existentes = {coluna[0] for coluna in cursor.fetchall()}

                colunas_necessarias = {
                    "codigo": "VARCHAR(20) DEFAULT NULL",
                    "numero": "VARCHAR(10) DEFAULT NULL",
                    "bairro": "VARCHAR(100) DEFAULT NULL",
                    "cep": "VARCHAR(10) DEFAULT NULL",
                    "data_nascimento": "DATE DEFAULT NULL",
                    "sexo": "VARCHAR(10) DEFAULT NULL",
                    "nome_mae": "VARCHAR(150) DEFAULT NULL",
                    "nome_pai": "VARCHAR(150) DEFAULT NULL",
                    "cidade_nascimento": "VARCHAR(100) DEFAULT NULL",
                    "pais_nascimento": "VARCHAR(100) DEFAULT NULL",
                    "data_admissao": "DATE DEFAULT NULL",
                    "pis_pasep": "VARCHAR(30) DEFAULT NULL",
                    "data_demissao": "DATE DEFAULT NULL",
                    "motivo_demissao": "VARCHAR(255) DEFAULT NULL",
                    "info_adicional": "TEXT",
                    "status": "CHAR(1) DEFAULT 'A'",
                }

                for nome, definicao in colunas_necessarias.items():
                    if nome not in existentes:
                        cursor.execute(f"ALTER TABLE funcionarios ADD COLUMN {nome} {definicao}")

                cursor.execute("UPDATE funcionarios SET codigo = CAST(id AS CHAR) WHERE codigo IS NULL OR codigo = ''")
                cursor.execute("UPDATE funcionarios SET status = 'A' WHERE status IS NULL OR status = ''")

            conexao.commit()

        except Exception as erro:
            print("ERRO AO GARANTIR TABELA FUNCIONARIOS:", erro)

        finally:
            if conexao is not None:
                conexao.close()

    def salvar(self, dados):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO funcionarios (
                        codigo,
                        nome,
                        apelido,
                        cpf,
                        rg,
                        data_nascimento,
                        sexo,
                        cep,
                        endereco,
                        numero,
                        bairro,
                        cidade,
                        estado,
                        telefone1,
                        telefone2,
                        nome_mae,
                        nome_pai,
                        cidade_nascimento,
                        pais_nascimento,
                        email,
                        data_admissao,
                        salario,
                        cargo,
                        carteira_trabalho,
                        pis_pasep,
                        data_demissao,
                        motivo_demissao,
                        info_adicional,
                        status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    dados["codigo"] or None,
                    dados["nome"],
                    dados["apelido"],
                    dados["cpf"],
                    dados["rg"],
                    dados["data_nascimento"],
                    dados["sexo"],
                    dados["cep"],
                    dados["endereco"],
                    dados["numero"],
                    dados["bairro"],
                    dados["cidade"],
                    dados["estado"],
                    dados["whatsapp"],
                    dados["telefone"],
                    dados["nome_mae"],
                    dados["nome_pai"],
                    dados["cidade_nascimento"],
                    dados["pais_nascimento"],
                    dados["email"],
                    dados["data_admissao"],
                    dados["salario"],
                    dados["cargo"],
                    dados["carteira_trabalho"],
                    dados["pis_pasep"],
                    dados["data_demissao"],
                    dados["motivo_demissao"],
                    dados["info_adicional"],
                    dados["status"],
                ))

                id_gerado = cursor.lastrowid
                cursor.execute(
                    """
                    UPDATE funcionarios
                    SET codigo = %s
                    WHERE id = %s
                    """,
                    (str(id_gerado), id_gerado),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Funcionario salvo com sucesso!"}

        except Exception as erro:
            print("ERRO AO SALVAR FUNCIONARIO:", erro)
            return {"sucesso": False, "mensagem": "Erro ao salvar funcionario."}

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_funcionario(self, opcao, texto, status, buscar_todos):
        conexao = None

        try:
            conexao = conectar()
            mapa_campos = {
                "Codigo": "codigo",
                "Nome": "nome",
                "CPF": "cpf",
                "Cargo": "cargo",
            }
            campo = mapa_campos.get(opcao)

            sql = """
                SELECT codigo, nome, apelido, cargo, telefone1, email, status
                FROM funcionarios
                WHERE 1=1
            """
            parametros = []

            if status == "Ativos":
                sql += " AND status = %s"
                parametros.append("A")
            elif status == "Excluidos":
                sql += " AND status = %s"
                parametros.append("E")

            if not buscar_todos and campo and texto:
                if opcao == "CPF":
                    sql += " AND cpf LIKE %s"
                    parametros.append(f"%{texto}%")
                else:
                    sql += f" AND {campo} LIKE %s"
                    parametros.append(f"%{texto}%")

            sql += " ORDER BY nome"

            with conexao.cursor() as cursor:
                cursor.execute(sql, tuple(parametros))
                return cursor.fetchall()

        except Exception as erro:
            print("ERRO NA BUSCA DE FUNCIONARIO:", erro)
            return []

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_codigo(self, codigo):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                    SELECT
                        codigo,
                        nome,
                        apelido,
                        cpf,
                        rg,
                        data_nascimento,
                        sexo,
                        cep,
                        endereco,
                        numero,
                        bairro,
                        cidade,
                        estado,
                        telefone1 AS whatsapp,
                        telefone2 AS telefone,
                        nome_mae,
                        nome_pai,
                        cidade_nascimento,
                        pais_nascimento,
                        email,
                        data_admissao,
                        salario,
                        cargo,
                        carteira_trabalho,
                        pis_pasep,
                        data_demissao,
                        motivo_demissao,
                        info_adicional,
                        status
                    FROM funcionarios
                    WHERE codigo = %s
                """
                cursor.execute(sql, (codigo,))
                return cursor.fetchone()

        except Exception as erro:
            print("ERRO AO BUSCAR FUNCIONARIO POR CODIGO:", erro)
            return None

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_documento(self, cpf):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT codigo, status
                    FROM funcionarios
                    WHERE cpf = %s
                    LIMIT 1
                    """,
                    (cpf,),
                )
                return cursor.fetchone()

        except Exception as erro:
            print("ERRO AO BUSCAR FUNCIONARIO POR DOCUMENTO:", erro)
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
                    UPDATE funcionarios SET
                        nome = %s,
                        apelido = %s,
                        cpf = %s,
                        rg = %s,
                        data_nascimento = %s,
                        sexo = %s,
                        cep = %s,
                        endereco = %s,
                        numero = %s,
                        bairro = %s,
                        cidade = %s,
                        estado = %s,
                        telefone1 = %s,
                        telefone2 = %s,
                        nome_mae = %s,
                        nome_pai = %s,
                        cidade_nascimento = %s,
                        pais_nascimento = %s,
                        email = %s,
                        data_admissao = %s,
                        salario = %s,
                        cargo = %s,
                        carteira_trabalho = %s,
                        pis_pasep = %s,
                        data_demissao = %s,
                        motivo_demissao = %s,
                        info_adicional = %s,
                        status = %s
                    WHERE codigo = %s
                """
                cursor.execute(sql, (
                    dados["nome"],
                    dados["apelido"],
                    dados["cpf"],
                    dados["rg"],
                    dados["data_nascimento"],
                    dados["sexo"],
                    dados["cep"],
                    dados["endereco"],
                    dados["numero"],
                    dados["bairro"],
                    dados["cidade"],
                    dados["estado"],
                    dados["whatsapp"],
                    dados["telefone"],
                    dados["nome_mae"],
                    dados["nome_pai"],
                    dados["cidade_nascimento"],
                    dados["pais_nascimento"],
                    dados["email"],
                    dados["data_admissao"],
                    dados["salario"],
                    dados["cargo"],
                    dados["carteira_trabalho"],
                    dados["pis_pasep"],
                    dados["data_demissao"],
                    dados["motivo_demissao"],
                    dados["info_adicional"],
                    dados["status"],
                    dados["codigo"],
                ))

            conexao.commit()
            return {"sucesso": True, "mensagem": "Funcionario atualizado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ATUALIZAR FUNCIONARIO:", erro)
            return {"sucesso": False, "mensagem": "Erro ao atualizar funcionario."}

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
                    UPDATE funcionarios
                    SET status = %s
                    WHERE codigo = %s
                    """,
                    (status, codigo),
                )

            conexao.commit()
            return {"sucesso": True, "mensagem": "Status atualizado com sucesso!"}

        except Exception as erro:
            print("ERRO AO ALTERAR STATUS DE FUNCIONARIO:", erro)
            return {"sucesso": False, "mensagem": "Erro ao alterar status."}

        finally:
            if conexao is not None:
                conexao.close()

    def buscar_login(self, usuario, senha):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT codigo, nome, usuario, status
                    FROM funcionarios
                    WHERE usuario = %s
                    AND senha = %s
                    AND status = %s
                    LIMIT 1
                    """,
                    (usuario, senha, "A"),
                )
                return cursor.fetchone()

        except Exception as erro:
            print("ERRO AO VALIDAR LOGIN DE FUNCIONARIO:", erro)
            return None

        finally:
            if conexao is not None:
                conexao.close()


    def salvar_usuario_senha(self, codigo, usuario, senha):
        conexao = None

        try:
            conexao = conectar()
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE funcionarios
                    SET usuario = %s, senha = %s
                    WHERE codigo = %s
                    """,
                    (usuario, senha, codigo),
                )
            conexao.commit()
            return True

        except Exception as erro:
            print("ERRO AO SALVAR USUARIO E SENHA:", erro)
            return False

        finally:
            if conexao is not None:
                conexao.close()
