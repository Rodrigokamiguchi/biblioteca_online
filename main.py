"""Bliblotecas"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from tela_principal import TelaPrincipal
from tela_adicionar import TelaAdicionar
from tela_emprestar import TelaEmprestar
from tela_devolver import TelaDevolver
from tela_relatorios import TelaRelatorios

class GerencadorTelas(ScreenManager):
    """Gerencias as telas"""
    def __init__(self, **kwargs):
        
        #Adicionando as telas
        self.add_widget(TelaPrincipal(name="tela_principal"))
        self.add_widget(TelaAdicionar(name="tela_principal"))
        self.add_widget(TelaEmprestar(name="tela_principal"))
        self.add_widget(TelaDevolver(name="tela_principal"))
        self.add_widget(TelaRelatorios(name="tela_principal"))
class BibliotecaApp(App):
    """Classe principal que iniciailiza o aplicavo"""
    def build(self):
        return GerencadorTelas()
    
if __name__ == "__main__":
    BibliotecaApp().run()