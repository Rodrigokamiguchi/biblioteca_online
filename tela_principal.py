#Bibliotecas
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class TelaPrincipal(BoxLayout):
    """Tela Principal do Aplicativo"""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        # Adiciona o titulo da tela
        self.add_widget(Label(
            text="📚 Biblioteca Online",
            font_size=32,
            bold=True,
            size_hint=(1, 0.2)
        ))

        #Lista de botões e suas funções associados
        botoes = [
            ("Adicionar Livro", self.adicionar_livro),
            ("Emprestar Livro", self.emprestar_livro),
            ("Devolver Livro", self.devolver_livro),
            ("Relatorios", self.relatorios)
        ]

        #Criação dinamica dos botões
        for texto, funcao in botoes:
            btn = Button(
                text = texto,
                size_hint=(1, 0.2),
                font_size=20
            )
            btn.bind(on_press=funcao) # Associa a função do botão
            self.add_widget(btn)

    #Metodos chados do pressionar os botões
    def adicionar_livro(self, instance):
        print("Ação: Adicionar livro")

    def emprestar_livro(self, instance):
        print("Ação: Emprestar livro")

    def devolver_livro(self, instance):
        print("Ação: Devolver livro")
    
    def relatorios(self, instance):
        print("Ação: Ver Relatorios")