import tkinter as tk
from UI.welcome_ui import WelcomeUI
from UI.listar_tarefas_ui import ListarTarefasUI
from UI.criar_tarefa_ui import CriarTarefaUI

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        
        
        super().__init__()

        self.title("Gestor de Tarefas")
        self.minsize(800, 650)

        # Frame de conteúdo
        self.frame_conteudo = tk.Frame(self, bg="#FFFFFF")
        self.frame_conteudo.pack(expand=True, fill="both")

        # Ecrã inicial (menu)
        self._voltar_ao_menu()

    def _voltar_ao_menu(self):
        WelcomeUI(
            self.frame_conteudo,
            self._abrir_criar_tarefa,
            self._abrir_listar_tarefas,
            self._abrir_dashboard,
            self.destroy
        )

    def _abrir_criar_tarefa(self):
        CriarTarefaUI(self.frame_conteudo, self._voltar_ao_menu)

    def _abrir_listar_tarefas(self):
        ListarTarefasUI(self.frame_conteudo, self._voltar_ao_menu)

    def _abrir_dashboard(self):
        DashboardUI(self.frame_conteudo, self._voltar_ao_menu)
