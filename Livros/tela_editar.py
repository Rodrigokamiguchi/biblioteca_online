from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TelaEditar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Campo de busca
        self.input_busca = TextInput(hint_text='Digite o título ou ID do livro')
        layout.add_widget(self.input_busca)

        self.btn_buscar = Button(text='Buscar Livro', on_press=self.buscar_livro)
        layout.add_widget(self.btn_buscar)

        # Campos editáveis
        self.input_titulo = TextInput(hint_text='Título do Livro')
        self.input_autor = TextInput(hint_text='Autor')
        self.input_status = TextInput(hint_text='Status (Disponível/Emprestado)')
        
        layout.add_widget(Label(text='Título:'))
        layout.add_widget(self.input_titulo)
        layout.add_widget(Label(text='Autor:'))
        layout.add_widget(self.input_autor)
        layout.add_widget(Label(text='Status:'))
        layout.add_widget(self.input_status)
        
        # Botões
        self.btn_salvar = Button(text='Salvar Alterações', on_press=self.salvar_alteracoes)
        self.btn_cancelar = Button(text='Cancelar', on_press=self.cancelar)
         #Botão para volta
        self.btn_voltar = Button(text="Voltar", size_hint=(1, 0.2), font_size=20, on_press=self.voltar_tela)
        
        layout.add_widget(self.btn_salvar)
        layout.add_widget(self.btn_cancelar)
        layout.add_widget(self.btn_voltar)


        self.add_widget(layout)

    def buscar_livro(self, instance):
        # Aqui entraria a lógica para buscar o livro no banco de dados
        print(f'Buscando livro: {self.input_busca.text}')
        
    def salvar_alteracoes(self, instance):
        # Aqui entraria a lógica para salvar as alterações no banco de dados
        print(f'Salvando alterações para: {self.input_titulo.text}')
        
    def cancelar(self, instance):
        # Voltar para a tela anterior
        self.manager.current = 'tela_listagem'

    def voltar_tela(self, instance):
        """Retorna a tela principal"""

        self.manager.current = "tela_principal"