import sqlite3

try:
    con = sqlite3.connect("dados.db", timeout=10)
    con.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("Conexão com o banco realizada com sucesso.")
except sqlite3.Error as erro:
    print("Erro ao conectar:", erro)
finally:
    con.close()
