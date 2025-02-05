from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TelaRemover(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="veritcal", padding=10, spacing=10)

        self.lbl_info = Label(text="Bucar Livro")
        layout.add_widget(self.lbl_info)

        self.input_buscar = TextInput(hint_text="Digite o nome do livro ou Id: ")
        layout.add_widget(self.input_buscar)

        self.btn_buscar = Button(text="Buscar", on_press=self.buscar_livro)
        layout.add_widget(self.btn_buscar)

        self.lbl_detalhes = Label(text="Detalhes do Livro")
        layout.add_widget(self.lbl_detalhes)

        self.btn_remover = Button(text="Remover", on_press=self.remover_livro)
        layout.add_widget(self.btn_remover)

        #Botão para volta
        btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20, on_press=self.voltar_tela)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def buscar_livro(self, instance):
        livro_id = self.input_buscar.text
        "Aqui vai a logica"
        "Adicionar o banco de dados"

    def remover_livro(self, instance):
         livro_id = self.input_buscar.text
    
    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"