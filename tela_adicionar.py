from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

class TelaAdicionar(Screen):
    """Tela para adicionar um livro"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        #Campo de entrada

        layout.add_widget(Label(text="Titulo do livro:", font_size=20))
        self.input_titulo = TextInput(multiline=False)
        layout.add_widget(self.input_titulo)

        layout.add_widget(Label(text="Autor do livro:", font_size=20))
        self.input_autor = TextInput(multiline=False)
        layout.add_widget(self.input_autor)

        #Botão para salvar
        btn_salvar = Button(text="salvar", size_hint=(1, 0.2), font_size=20)
        btn_salvar.bind(on_presss=self.salvar_livro)
        layout.add_widget(btn_salvar)

        #Botão para volta
        btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20)
        btn_voltar.bind(on_press=self.voltar_tela)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def salvar_livro(self, instance):
        """Função par salvar o livro no banco de daods"""

        titulo = self.input_titulo.text
        autor = self.input_autor.text
        print(f"Livro '{titulo}' de {autor} salvo!")

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"

        