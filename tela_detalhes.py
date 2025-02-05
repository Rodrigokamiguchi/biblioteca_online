from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TelaDetahes(Screen):
    def __init__(self, livros=None, **kwargs):
        super().__init__(**kwargs)

        self.livro = livro or {} # Dicionario contendo os detalhes do livro

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # labels para exibir informações do livro
        self.label_titulo = Label(text=f"Título: {self.livro.get("Título", "Não informado")}")
        self.label_autor = Label(text=f"Autor: {self.livro.get("Autor", "Não informado")}")
        self.label_status = Label(text=f"Status: {self.livro.get("Status", "Desconhecido")}")

        self.layout.add_widget(self.label_titulo)
        self.layout.add_widget(self.label_titulo)
        self.layout.add_widget(self.label_titulo)

        # Se o livro estiver emprestado
        if self.livro.get("status") == "Emprestado":
            self.label_responsavel = Label(text=f"Emprestado para: {self.livro.get("responsavel", "Desconhecido")}")
            self.layout.add_widget(self.label_responsavel)

         #Botão para volta
        btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20, on_press=self.voltar_tela)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"