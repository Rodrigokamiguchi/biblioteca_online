"""Bliblotecas"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from tela_principal import TelaPrincipal
from Livros.tela_adicionar import TelaAdicionar
from Livros.tela_emprestar import TelaEmprestimo
from Livros.tela_editar import TelaEditar
from Livros.tela_detalhes import TelaDetalhes
from Usuarios.adicionar_usuarios import TelaAdicionarUsuario


class GerenciadorTelas(ScreenManager):
    """Gerencias as telas"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()
        # Adicionando as telas
        self.add_widget(TelaPrincipal(name="tela_principal"))
        self.add_widget(TelaAdicionar(name="tela_adicionar"))
        self.add_widget(TelaEmprestimo(name="tela_emprestar"))
        self.add_widget(TelaDetalhes(name="tela_detalhes"))
        self.add_widget(TelaEditar(name="tela_editar"))
        self.add_widget(TelaAdicionarUsuario(name="adicionar_usuarios"))
class BibliotecaApp(App):
    """Classe principal que iniciailiza o aplicavo"""
    def build(self):
        return GerenciadorTelas()
    
BibliotecaApp().run()