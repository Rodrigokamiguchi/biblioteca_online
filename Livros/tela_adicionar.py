from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import psycopg2


class TelaAdicionar(Screen):
    """Tela para adicionar um livro"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        #Campo de entrada

        self.input_titulo = TextInput(jint_text="Titulo do Livro")
        self.input_autor = TextInput(jint_text="Autor")
        self.input_ano = TextInput(jint_text="Ano de Publicação", input_filter="int")

        #Botão para adicionar livro
        btn_adicionar    = Button(text="Adicionar Livro", on_press=self.adicionar_livro)
        btn_voltar = Button(text="Tela Principal", on_press=self.tela_principal)

        # Adicionar widgets do Layout
        self.layout.add_widget(Label(text="Adicionar Novo Livro", font_size=20))
        self.layout.add_widget(Label(self.input_titulo))
        self.layout.add_widget(Label(self.input_ano))
        self.layout.add_widget(Label(self.input_autor))
        self.layout.add_widget(Label(btn_adicionar))
        self.layout.add_widget(Label(btn_voltar))


        self.add_widget(self.layout)

    def salvar_livro(self, instance):

        titulo = self.input_titulo.text
        autor = self.input_autor.text
        ano = self.input_ano.text

        if titulo and autor and ano:
            try:
                conn = psycopg2.connect(
                    dbname = "biblioteca",
                    user = "postgres",
                    password = "123",
                    host = "localhost",
                    port = "5432"
                )
                cursor = conn.cursor()

                #Inserir no banco de daods
                cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUE (%s, %s, %s)", (titulo, autor, ano))
                conn.commit()

                cursor.close()
                conn.close()

                print("Livro adicionado com sucesso!")
                self.input_titulo.text = ""
                self.input_autor.text = ""
                self.input_ano.text =""

            except Exception as e:
                print("Adicionado com sucesso !", e)
        else:
            print("Preencha todos os campos")

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"

        