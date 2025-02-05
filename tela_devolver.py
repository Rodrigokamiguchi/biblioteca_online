from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

class TelaDevolver(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.lbl_info = Label(text="Digite o ID ou Nome do livro para devolução: ")
        layout.add_widget(self.lbl_info)

        self.input_buscar = TextInput(hint_text="ID ou nome do livro")
        layout.add_widget(self.input_buscar)

        self.btn_buscar = Button(text="Buscar Livro", on_press=self.buscar_livro)
        layout.add_widget(self.btn_buscar)

        self.lbl_detalhes = Label(text="detalhes do livro: ")
        layout.add_widget(self.lbl_detalhes)

        self.btn_devolver = Button(text="Devolver Livro", disabled=True, on_press=self.devolver_livro)
        layout.add_widget(self.btn_devolver)

        #Botão para volta
        btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20, on_press=self.voltar_tela)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def buscar_livro(self, instance):
        livro_id = self.input_buscar.text.strip()
        if livro_id:
            sucesso = self.consultar_banco(livro_id)
            if sucesso:
                self.lbl_detalhes.text = "Livro devolvido com sucesso!"
                self.btn_devolver.disabled = True
            else:
                self.lbl_detalhes.text = "Erro ao devolver livro"

    def consultar_banco(self, livro_id):
        dados_fake = {f"1": {"titulo" : "Python Avançado", "Emprestado_para": "Rodrigo"}}
        return dados_fake.get(livro_id)
    
    def atualizar_banco(self, livro_id):
        return True
    
    def devolver_livro(self, instance):
        print("Livro devolvido")

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"