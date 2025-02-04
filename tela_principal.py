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
        botoes = [
            ("Adicionar Livro", self.adicionar_livro),
            ("Emprestar Livro", self.emprestar_livro),
            ("Devolver Livro", self.devolver_livro),
            ("Relatorios", self.relatorios)
        ]

        #Criação dinamica dos botões
        for texto, nome_tela in botoes:
            btn = Button(
                text = texto,
                size_hint=(1, 0.2),
                font_size=20
            )
            btn.bind(
                on_press=lambda instance,
                t=nome_tela: self.mudartela(t)
            )
            layout.add_widget(btn)
        self.add_widget(btn)

    def mudar_tela(self, nome_tela):
        """Alterna para a tela desejada"""

        self.manager.current = nome_tela