import pymysql


def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="aut_com",
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )