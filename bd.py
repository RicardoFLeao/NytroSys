import pymysql

def verificar_login(usuario, senha):
    print(f">>> Verificando login para: {usuario} / {senha}")
    try:
        print(">>> Tentando conectar ao banco (pymysql)...")
        conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database="aut_com",
            port=3306
        )
        print(">>> Conectado com sucesso (pymysql).")

        with conexao.cursor() as cursor:
            sql = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
            cursor.execute(sql, (usuario, senha))
            resultado = cursor.fetchone()
            print(">>> Resultado da consulta:", resultado)
            return resultado

    except Exception as erro:
        import traceback
        print(">>> ERRO DETALHADO:")
        traceback.print_exc()
        return None
