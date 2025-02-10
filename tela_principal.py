#Bibliotecas
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class TelaPrincipal(Screen):
    """Tela Principal do Aplicativo"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Adiciona o titulo da tela
        layout.add_widget(Label(
            text="📚 Biblioteca Online",
            font_size=32,
            bold=True,
            size_hint=(1, 0.2)
        ))

        #Lista de botões e suas funções associados
        btn_adicionar = Button(text="Adicionar Livro", size_hint=(0, 0.2), font_size=20)
        btn_adicionar.bind(on_press=self.adicionar_livros)
        layout.add_widget(btn_adicionar)
        
        btn_emprestar = Button(text="Emprestar", size_hint=(0, 0.2), font_size=20)
        btn_adicionar.bind(on_press=self.emprestar_livros)
        layout.add_widget(btn_emprestar)

        btn_detalhes = Button(text="Detalhes", size_hint=(0, 0.2), font_size=20)
        btn_adicionar.bind(on_press=self.detalhes_livros)
        layout.add_widget(btn_detalhes)

        btn_editar = Button(text="Remover", size_hint=(0, 0.2), font_size=20)
        btn_adicionar.bind(on_press=self.editar_livros)
        layout.add_widget(btn_editar)

        btn_adicionarUsuario = Button(text="Remover", size_hint=(0, 0.2), font_size=20)
        btn_adicionar.bind(on_press=self.adicionar_usuario)
        layout.add_widget(btn_adicionarUsuario)

        self.add_widget(layout)

    def adicionar_livros(self, instance):
        """Função para mudar para a tela adicionar livros"""

        self.manager.current = "tela_adicionar"

    def emprestar_livros(self, instance):

        self.manager.current = "tela_emprestar"
     
    def detalhes_livros(self, instance):

        self.manager.current = "tela_detalhes"
    
    def editar_livros(self, instance):

        self.manager.current = "tela_editar"
        
    def adicionar_usuario(self, instance):

        self.manager.current = "adicionar_usuarios"

    
