import sqlite3

# Conectar ao banco de dados ou criar um novo banco de dados 
con = sqlite3.connect("dados.db")

# Tabela de Livros
con.execute("CREATE TABLE livros(\
                id INTEGER PRIMARY KEY,\
                title TEXT,\
                autor TEXT,\
                editora TEXT,\
                ano_publicado INTEGER,\
                isbn TEXT)")

# Tabela de Usuarios
con.execute("CREATE TABLE usuarios(\
                id INTEGER PRIMARY KEY,\
                nome TEXT,\
                sobrenome TEXT,\
                endereco TEXT,\
                email TEXT,\
                telefone TEXT)")

# Tabela de Emprestimos
con.execute("CREATE TABLE emprestimos(\
                id INTEGER PRIMARY KEY,\
                id_livro INTEGER,\
                id_usuario INTEGER,\
                data_emprestimo TEXT,\
                data_devolucao TEXT,\
                FOREIGN KEY(id_livro) REFERENCES livros(id),\
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id))")

con.commit()
con.close()
