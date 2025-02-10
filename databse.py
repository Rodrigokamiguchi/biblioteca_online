import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="biblioteca",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        print("Conexão bem-sucedida!!!")
        return conexao
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def criar_tabela_livros():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    autor VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Disponivel'
                );
            """)
            conexao.commit()
            print("Tabela criada com sucesso!")
            cursor.close()
        except Exception as e:
            print(f"Erro ao criar a tabela: {e}")
        finally:
            conexao.close()

def criar_tabela_usuarios():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    cpf VARCHAR(11) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    telefone VARCHAR(20)
                );
            """)
            conexao.commit()
            print("Tabela de usuários criada com sucesso!")
            cursor.close()
        except Exception as e:
            print(f"Erro ao criar a tabela de usuários: {e}")
        finally:
            conexao.close()

def criar_tabela_funcionarios():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    cpf VARCHAR(11) UNIQUE NOT NULL,
                    cargo VARCHAR(100) NOT NULL,
                    salario DECIMAL(10, 2) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    telefone VARCHAR(20),
                    data_admissao DATE NOT NULL
                );
            """)
            conexao.commit()
            print("Tabela de funcionários criada com sucesso!")
            cursor.close()
        except Exception as e:
            print(f"Erro ao criar a tabela de funcionários: {e}")
        finally:
            conexao.close()
    
# Chama a função para criar a tabela
criar_tabela_livros()
criar_tabela_usuarios()
criar_tabela_funcionarios()
