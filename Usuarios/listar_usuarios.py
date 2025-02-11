from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from database import obter_usuarios, pagar_multa

class TelaListarUsuarios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)
        self.carregar_usuarios()
    
    def carregar_usuarios(self):
        self.layout.clear_widgets()
        usuarios = obter_usuarios()
        
        for usuario in usuarios:
            usuario_box = BoxLayout(orientation='horizontal', spacing=10)
            nome_label = Label(text=f"{usuario['nome']}")
            livros_label = Label(text=f"Livros: {usuario['livros_emprestados']}")
            multa_label = Label(text=f"Multa: R$ {usuario['multa']:.2f}")
            usuario_box.add_widget(nome_label)
            usuario_box.add_widget(livros_label)
            usuario_box.add_widget(multa_label)
            
            if usuario['multa'] > 0:
                btn_pagar = Button(text="Pagar Multa")
                btn_pagar.bind(on_press=lambda instance, id=usuario['id']: self.pagar_multa(id))
                usuario_box.add_widget(btn_pagar)
            
            self.layout.add_widget(usuario_box)
    
    def pagar_multa(self, usuario_id):
        pagar_multa(usuario_id)
        self.carregar_usuarios()
