import psycopg2
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TelaEditar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Campo de busca
        self.input_busca = TextInput(hint_text='Digite o título ou ID do livro')
        btn_buscar = Button(text='Buscar Livro', on_press=self.buscar_livro)

        # Campos editáveis
        self.input_titulo = TextInput(hint_text='Título do Livro')
        self.input_autor = TextInput(hint_text='Autor')
        self.input_status = TextInput(hint_text='Status (Disponível/Emprestado)')
        
        # Botões
        btn_salvar = Button(text='Salvar Alterações', on_press=self.salvar_alteracoes)
        btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20, on_press=self.voltar_tela)
        
        # Adicionando widgets ao layout
        self.layout.add_widget(Label(text="Editar Livro", font_size=20))
        self.layout.add_widget(self.input_id)
        self.layout.add_widget(btn_buscar)
        self.layout.add_widget(self.input_titulo)
        self.layout.add_widget(self.input_autor)
        self.layout.add_widget(self.input_ano)
        self.layout.add_widget(btn_salvar)
        self.layout.add_widget(btn_voltar)


        self.add_widget(self.layout)

    def buscar_livro(self, instance):
        livro_id = self.input_id.text

        if livro_id:
            try:
                conn = psycopg2.connect(
                    dbname = "biblioteca",
                    user = "postgres",
                    password = "123",
                    host = "localhost",
                    port = "5432"
                )
                cursor = conn.cursor()

                cursor.execute("SELECT titulo, autor, ano, FROM livros WHERE id = %s", (livro_id,))
                livro = cursor.fetchone()

                cursor.close()
                conn.close()

                if livro:
                    self.input_titulo.text = livro[0]
                    self.input_autor.text = livro[1]
                    self.input_ano.text = str(livro[2])
                else:
                    print("Livro não encontrado")
            except Exception as e:
                print("Erro ao buscar livro:", e)


    def salvar_alteracoes(self, instance):
        livro_id = self.input_id.text
        titulo = self.input_titulo.text
        autor = self.input_autor.text
        ano = self.input_ano.text

        if livro_id and titulo and autor and ano:
            try:
                conn = psycopg2.connect(
                    dbname = "biblioteca",
                    user = "postgres",
                    password = "123",
                    host = "localhost",
                    port = "5432"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE livros SET titulo = %s, ano = %s, WHERE id = %s",
                    (titulo, autor, ano, livro_id)
                )
                conn.commit()
                
                cursor.close
                conn.close()

                print("Livro Autualizado com sucesso!!!")
                self.input_id.text = ""
                self.input_titulo.text = ""
                self.input_autor.text = ""
                self.input_ano.text = ""
            except Exception as e:
                print("Erro ao atualizar o livro: ", e)
        else:
            print("Preencha todos os campos!!!")

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"