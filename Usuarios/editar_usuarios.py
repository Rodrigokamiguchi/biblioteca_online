from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import psycopg2

class TelaEditarUsuario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.layout.add_widget(Label(text="Editar Usuário"))

        self.layout.add_widget(Label(text="ID Usuário"))
        self.input_id = TextInput(multiline=False)
        self.layout.add_widget(self.input_id)

        self.layout.add_widget(Label(text="Novo Usuário"))
        self.input_name = TextInput(multiline=False)
        self.layout.add_widget(self.input_name)

        self.layout.add_widget(Label(text="Novo Email"))
        self.input_email = TextInput(multiline=False)
        self.layout.add_widget(self.input_email)

        self.layout.add_widget(Label(text="Novo Telefone"))
        self.input_telefone = TextInput(multiline=False)
        self.layout.add_widget(self.input_telefone)

        self.btn_editar = Button(text="Salvar alterações", on_press=self.editar_usuario)
        self.layout.add_widget(self.btn_editar)

        self.btn_remover = Button(text="Remover usuário", on_press=self.remover_usuario)
        self.layout.add_widget(self.btn_remover)

        self.btn_voltar = Button(text="Voltar", on_press=self.voltar)
        self.layout.add_widgert(self.btn_voltar)

        self.add_widget(self.layout)

    def editar_usuario(self, intance):
        user_id = self.input_id.text
        novo_nome = self.input_id.text
        novo_email = self.input_id.text
        novo_telefone = self.input_id.text

        if user_id and (novo_nome or novo_email or novo_telefone):
            try:
                conexao = psycopg2.connect(
                    dbname='biblioteca',
                    user='postgres',
                    password='123',
                    host='localhost',
                    port='5432'
                )
                cursor = conexao.cursor()

                if novo_nome:
                    cursor.execute("UPDATE usuario SET nome = %s WHERE id = %s", (novo_nome, user_id))
                if novo_email:
                    cursor.execute("UPDATE usuario SET email = %s WHERE id = %s", (novo_email, user_id))
                if novo_telefone:
                    cursor.execute("UPDATE usuario SET telefone = %s WHERE id = %s", (novo_telefone, user_id))

                conexao.commit()
                cursor.close()
                conexao.close()

                print("Usuario atualizado com sucesso!")
            except Exception as e:
                print("Erroa ao atualizar usuário", e)

    def remover_usuario(self, intance):
        user_id = self.input_id.text.strip()

        if not user_id:
            self.label_status.text = "Por favor, insira um ID valido."
            return
        try:
            conn = psycopg2.connect(
                dbname='biblioteca',
                user='postgres',
                password='123',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id))
            conn.commit()

            if cursor.rowcount > 0:
                self.label_status.text = "Usuário removido com sucesso."
            else:
                self.label_status.text = "Usuário não encontrado."

            cursor.close()
            conn.close()
        except Exception as e:
            self.label_status.text = f"Erro ao remover usário: {e}"
    def voltar(self, intance):
        self.manager.current = "tela_principal"