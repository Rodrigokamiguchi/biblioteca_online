"""Bliblotecas"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from tela_principal import TelaPrincipal
from tela_adicionar import TelaAdicionar
from tela_emprestar import TelaEmprestar
from tela_devolver import TelaDevolver
from tela_detalhes import TelaDetahes
from tela_remover import TelaRemover


class GerencadorTelas(ScreenManager):
    """Gerencias as telas"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()
        # Adicionando as telas
        self.add_widget(TelaPrincipal(name="tela_principal"))
        self.add_widget(TelaAdicionar(name="tela_adicionar"))
        self.add_widget(TelaEmprestar(name="tela_emprestar"))
        self.add_widget(TelaDevolver(name="tela_devolver"))
        self.add_widget(TelaDetahes(name="tela_detalhes"))
        self.add_widget(TelaRemover(name="tela_remover"))
class BibliotecaApp(App):
    """Classe principal que iniciailiza o aplicavo"""
    def build(self):
        return GerencadorTelas()
    
BibliotecaApp().run()