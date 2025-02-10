from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import psycopg2
from datetime import datetime, timedelta

# Conexão com o PostgreSQL
DATABASE_CONFIG = {
    'dbname': 'biblioteca',
    'user': 'postegres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def conectar_bd():
    return psycopg2.connect(**DATABASE_CONFIG)

class TelaEmprestimo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label_info = Label(text='Emprestar Livro')
        layout.add_widget(self.label_info)
        
        self.input_id_livro = TextInput(hint_text='ID do Livro')
        layout.add_widget(self.input_id_livro)
        
        self.input_usuario = TextInput(hint_text='Nome do Usuário')
        layout.add_widget(self.input_usuario)
        
        self.btn_emprestar = Button(text='Emprestar')
        self.btn_emprestar.bind(on_press=self.emprestar_livro)
        layout.add_widget(self.btn_emprestar)
        
        self.btn_devolver = Button(text='Devolver')
        self.btn_devolver.bind(on_press=self.devolver_livro)
        layout.add_widget(self.btn_devolver)

        self.btn_voltar = Button(text="Tela Principal", on_press=self.tela_principal)
        layout.add_widget(self.btn_voltar)
        
        self.label_mensagem = Label(text='')
        layout.add_widget(self.label_mensagem)
        
        self.add_widget(layout)
    
    def emprestar_livro(self, instance):
        livro_id = self.input_id_livro.text.strip()
        usuario = self.input_usuario.text.strip()
        
        if not livro_id or not usuario:
            self.label_mensagem.text = 'Preencha todos os campos!'
            return
        
        conn = conectar_bd()
        cur = conn.cursor()
        
        # Verificar se o livro existe e está disponível
        cur.execute("SELECT status FROM livros WHERE id = %s", (livro_id,))
        resultado = cur.fetchone()
        
        if not resultado:
            self.label_mensagem.text = 'Livro não encontrado!'
        elif resultado[0] == 'Emprestado':
            self.label_mensagem.text = 'Livro já está emprestado!'
        else:
            # Atualizar o status do livro e salvar o empréstimo
            data_emprestimo = datetime.now()
            data_devolucao = data_emprestimo + timedelta(days=14)  # 14 dias de prazo
            cur.execute("UPDATE livros SET status = %s, usuario = %s, data_emprestimo = %s, data_devolucao = %s WHERE id = %s",
                        ('Emprestado', usuario, data_emprestimo, data_devolucao, livro_id))
            conn.commit()
            self.label_mensagem.text = f'Livro emprestado! Devolução esperada: {data_devolucao.strftime("%d/%m/%Y")}.'
        
        cur.close()
        conn.close()
    
    def devolver_livro(self, instance):
        livro_id = self.input_id_livro.text.strip()
        
        if not livro_id:
            self.label_mensagem.text = 'Informe o ID do livro!'
            return
        
        conn = conectar_bd()
        cur = conn.cursor()
        
        # Verificar se o livro existe e está emprestado
        cur.execute("SELECT status FROM livros WHERE id = %s", (livro_id,))
        resultado = cur.fetchone()
        
        if not resultado:
            self.label_mensagem.text = 'Livro não encontrado!'
        elif resultado[0] == 'Disponível':
            self.label_mensagem.text = 'Este livro já está disponível!'
        else:
            # Atualizar o status para disponível e remover dados de empréstimo
            cur.execute("UPDATE livros SET status = %s, usuario = NULL, data_emprestimo = NULL, data_devolucao = NULL WHERE id = %s",
                        ('Disponível', livro_id))
            conn.commit()
            self.label_mensagem.text = 'Livro devolvido com sucesso!'
        
        cur.close()
        conn.close()


def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"