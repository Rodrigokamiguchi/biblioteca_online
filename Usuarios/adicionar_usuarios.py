from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    'dbname': 'biblioteca',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

class TelaAdicionarUsuario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label_nome = Label(text='Nome:')
        self.input_nome = TextInput()
        
        self.label_cpf = Label(text='CPF:')
        self.input_cpf = TextInput()

        self.label_email = Label(text='Email:')
        self.input_email = TextInput()

        self.label_telefone = Label(text='Telefone:')
        self.input_telefone = TextInput()
        
        self.btn_adicionar = Button(text='Adicionar Usuário', on_press=self.adicionar_usuario)
        self.btn_voltar = Button(text='Voltar', on_press=self.voltar)
        
        layout.add_widget(self.label_nome)
        layout.add_widget(self.input_nome)
        layout.add_widget(self.label_cpf)
        layout.add_widget(self.input_cpf)
        layout.add_widget(self.input_email)
        layout.add_widget(self.input_email)
        layout.add_widget(self.input_telefone)
        layout.add_widget(self.input_telefone)
        layout.add_widget(self.btn_adicionar)
        layout.add_widget(self.btn_voltar)
        
        self.add_widget(layout)
    
    def adicionar_usuario(self, instance):
        nome = self.input_nome.text
        cpf = self.input_cpf.text
        email = self.input_email.text
        telefone = self.input_telefone.text
        
        if nome and cpf:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nome, cpf, email, telefone) VALUES (%s, %s)", (nome, cpf, telefone, email))
                conn.commit()
                cursor.close()
                conn.close()
                print("Usuário adicionado com sucesso!")
            except Exception as e:
                print(f"Erro ao adicionar usuário: {e}")
        else:
            print("Preencha todos os campos!")
    
    def voltar(self, instance):
        self.manager.current = 'tela_principal'
