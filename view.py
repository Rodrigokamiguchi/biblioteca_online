import sqlite3

# Conectar ao banco de dados
def connect():
    con = sqlite3.connect("dados.db", timeout=10)
    return con

# Função para inserir um novo livro
def insert_book(title, autor, editora, ano_publicado, isbn):
    try:
        con = connect()
        con.execute("""
            INSERT INTO livros(title, autor, editora, ano_publicado, isbn)
            VALUES(?, ?, ?, ?, ?)
        """, (title, autor, editora, ano_publicado, isbn))
        con.commit()
        print("Livro inserido com sucesso!")
    except sqlite3.Error as erro:
        print("Erro ao inserir livro:", erro)
    finally:
        con.close()

# Função para inserir usuários
def insert_users(nome, sobrenome, endereco, email, telefone):
    try:
        con = connect()
        con.execute("""
            INSERT INTO usuarios(nome, sobrenome, endereco, email, telefone)
            VALUES(?, ?, ?, ?, ?)
        """, (nome, sobrenome, endereco, email, telefone))
        con.commit()
        print("Usuário inserido com sucesso!")
    except sqlite3.Error as erro:
        print("Erro ao inserir usuário:", erro)
    finally:
        con.close()


# Função para exibir os livros
def exibir_livros():
    con = connect()
    livros = con.execute("SELECT * FROM livros").fetchall()
    con.close()
    
    if not livros:
        print("Nenhum livro encontrado na biblioteca.")
        return
    
    print("livros na biblioteca: ")
    for livro in livros:
        print(f"ID: {livro[0]}")
        print(f"TITLE: {livro[1]}")
        print(f"AUTOR: {livro[2]}")
        print(f"EDITORA: {livro[3]}")
        print(f"ANO_PUBLICADO: {livro[4]}")
        print(f"ISBN: {livro[5]}")
        print("\n")

# Função para realizar emprestiimos
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao):
    try:
        con = connect()
        con.execute("INSERT INTO emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao)\
                    VALUES(?, ?, ?, ?)",(id_livro, id_usuario, data_emprestimo, data_devolucao))
        
        con.commit()
        print("status do livro atualizado")
    except sqlite3.Error as erro:
        print("não foi possivel atualizar o status do livro", erro)
    finally:
        con.close()

# Função para exibir todos os livros emprestado no momento
def get_books_on_load():
    con = connect()
    result = con.execute("""
        SELECT livros.title, usuarios.nome, usuarios.sobrenome, emprestimos.id, emprestimos.data_emprestimo, emprestimos.data_devolucao
        FROM emprestimos
        INNER JOIN livros ON livros.id = emprestimos.id_livro
        INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario
        WHERE emprestimos.data_devolucao IS NULL
    """).fetchall()
    
    con.close()
    return result

# Função para a atualizar a data de devolução de emprestimo
def update_loan_return_date(id_emprestimo, data_devolucao):
    con = connect()
    con.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?",(id_emprestimo, data_devolucao))
    con.commit()
    con.close()





# Exemplo de uso das funções
#insert_book("Rei leao", "Wlaty Disney", "Editora 1", 2005, "123457")
#insert_users("Guilherme", "Kamiguchi", "Aguas claras", "rodrigo@gmail.com", "61996945622")
#insert_loan(1, 1, "12/05/2025", None)
#exibir_livros()
livros_emprestado = get_books_on_load()
print(livros_emprestado)
update_loan_return_date(1, "23/05/2025")