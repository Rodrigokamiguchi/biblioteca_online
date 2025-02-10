import psycopg2
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class TelaDetalhes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campo de busca
        self.input_busca = TextInput(hint_text="Digite o ID ou Nome do Livro")
        btn_buscar = Button(text="Buscar", on_press=self.buscar_livro)

        # Área de exibição dos livros
        self.scroll = ScrollView()
        self.lista_livros = GridLayout(cols=1, size_hint_y=None)
        self.lista_livros.bind(minimum_height=self.lista_livros.setter('height'))
        self.scroll.add_widget(self.lista_livros)

        # Botão de atualizar lista
        btn_atualizar = Button(text="Atualizar Lista", on_press=self.carregar_livros)

        # Botão de voltar
        btn_voltar = Button(text="Voltar", on_press=lambda x: self.manager.current == "tela_principal")

        # Adicionando widgets ao layout
        self.layout.add_widget(Label(text="Lista de Livros", font_size=20))
        self.layout.add_widget(self.input_busca)
        self.layout.add_widget(btn_buscar)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(btn_atualizar)
        self.layout.add_widget(btn_voltar)

        self.add_widget(self.layout)

        # Carregar lista ao iniciar
        self.carregar_livros()

    def carregar_livros(self, instance=None):
        """Carrega todos os livros do banco de dados e exibe na tela."""
        self.lista_livros.clear_widgets()
        try:
            conn = psycopg2.connect(
                dbname="biblioteca",
                user="postegres",
                password="123",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, status FROM livros ORDER BY id")
            livros = cursor.fetchall()
            cursor.close()
            conn.close()

            for livro in livros:
                livro_texto = f"ID: {livro[0]} | {livro[1]} - {livro[2]}"
                self.lista_livros.add_widget(Label(text=livro_texto, size_hint_y=None, height=30))

        except Exception as e:
            print("Erro ao carregar livros:", e)

    def buscar_livro(self, instance):
        """Busca um livro pelo ID ou título."""
        busca = self.input_busca.text.strip()

        if busca:
            self.lista_livros.clear_widgets()
            try:
                conn = psycopg2.connect(
                    dbname="biblioteca",
                    user="postegres",
                    password="123",
                    host="localhost",
                    port="5432"
                )
                cursor = conn.cursor()

                if busca.isdigit():  # Se for número, busca por ID
                    cursor.execute("SELECT id, titulo, status FROM livros WHERE id = %s", (busca,))
                else:  # Se for texto, busca por título
                    cursor.execute("SELECT id, titulo, status FROM livros WHERE titulo ILIKE %s", ('%' + busca + '%',))

                livros = cursor.fetchall()
                cursor.close()
                conn.close()

                if livros:
                    for livro in livros:
                        livro_texto = f"ID: {livro[0]} | {livro[1]} - {livro[2]}"
                        self.lista_livros.add_widget(Label(text=livro_texto, size_hint_y=None, height=30))
                else:
                    self.lista_livros.add_widget(Label(text="Nenhum livro encontrado!", size_hint_y=None, height=30))

            except Exception as e:
                print("Erro ao buscar livro:", e)
        else:
            self.carregar_livros()

def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"