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

def criar_tabela():
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

# Chama a função para criar a tabela
criar_tabela()
