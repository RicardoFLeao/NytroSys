import pymysql

def verificar_login(usuario, senha):
    print(f">>> Verificando login para: {usuario} / {senha}")
    try:
        conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database="aut_com",
            port=3306
        )

        with conexao.cursor() as cursor:
            sql = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
            cursor.execute(sql, (usuario, senha))
            resultado = cursor.fetchone()
            return resultado

    except Exception as erro:
        import traceback
        traceback.print_exc()
        return None
