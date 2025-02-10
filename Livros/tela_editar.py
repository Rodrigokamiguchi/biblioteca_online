import psycopg2
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class TelaEditar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Campo para buscar livro por ID
        self.input_id = TextInput(hint_text="Digite o ID do Livro para Editar ou Remover")
        btn_buscar = Button(text="Buscar", on_press=self.buscar_livro)

        # Campos de edição
        self.input_titulo = TextInput(hint_text="Novo Título")
        self.input_status = TextInput(hint_text="Novo Status (Disponível/Emprestado)")

        # Botões
        btn_salvar = Button(text="Salvar Alterações", on_press=self.atualizar_livro)
        btn_remover = Button(text="Remover Livro", on_press=self.remover_livro)
        btn_voltar = Button(text="Voltar", on_press=lambda x: self.manager.current == "tela_principal")

        # Adicionando widgets ao layout
        self.layout.add_widget(Label(text="Editar Livro", font_size=20))
        self.layout.add_widget(self.input_id)
        self.layout.add_widget(btn_buscar)
        self.layout.add_widget(self.input_titulo)
        self.layout.add_widget(self.input_status)
        self.layout.add_widget(btn_salvar)
        self.layout.add_widget(btn_remover)
        self.layout.add_widget(btn_voltar)

        self.add_widget(self.layout)

    def buscar_livro(self, instance):
        """Busca um livro pelo ID e preenche os campos."""
        livro_id = self.input_id.text.strip()
        if not livro_id.isdigit():
            self.mostrar_popup("Erro", "ID inválido!")
            return

        try:
            conn = psycopg2.connect(
                dbname="biblioteca",
                user="postegres",
                password="123",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT titulo, status FROM livros WHERE id = %s", (livro_id,))
            livro = cursor.fetchone()
            cursor.close()
            conn.close()

            if livro:
                self.input_titulo.text = livro[0]
                self.input_status.text = livro[1]
            else:
                self.mostrar_popup("Erro", "Livro não encontrado!")

        except Exception as e:
            print("Erro ao buscar livro:", e)

    def atualizar_livro(self, instance):
        """Atualiza as informações do livro no banco de dados."""
        livro_id = self.input_id.text.strip()
        novo_titulo = self.input_titulo.text.strip()
        novo_status = self.input_status.text.strip()

        if not livro_id.isdigit() or not novo_titulo or not novo_status:
            self.mostrar_popup("Erro", "Preencha todos os campos!")
            return

        try:
            conn = psycopg2.connect(
                dbname="biblioteca",
                user="seu_usuario",
                password="sua_senha",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE livros SET titulo = %s, status = %s WHERE id = %s",
                (novo_titulo, novo_status, livro_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.mostrar_popup("Sucesso", "Livro atualizado com sucesso!")

        except Exception as e:
            print("Erro ao atualizar livro:", e)

    def remover_livro(self, instance):
        """Remove um livro do banco de dados."""
        livro_id = self.input_id.text.strip()
        if not livro_id.isdigit():
            self.mostrar_popup("Erro", "ID inválido!")
            return

        try:
            conn = psycopg2.connect(
                dbname="biblioteca",
                user="seu_usuario",
                password="sua_senha",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM livros WHERE id = %s", (livro_id,))
            conn.commit()
            cursor.close()
            conn.close()

            self.input_id.text = ""
            self.input_titulo.text = ""
            self.input_status.text = ""
            self.mostrar_popup("Sucesso", "Livro removido com sucesso!")

        except Exception as e:
            print("Erro ao remover livro:", e)

    def mostrar_popup(self, titulo, mensagem):
        """Exibe um popup na tela."""
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_layout.add_widget(Label(text=mensagem))
        btn_fechar = Button(text="Fechar", size_hint=(None, None), size=(100, 40))
        popup_layout.add_widget(btn_fechar)

        popup = Popup(title=titulo, content=popup_layout, size_hint=(None, None), size=(300, 200))
        btn_fechar.bind(on_press=popup.dismiss)
        popup.open()
