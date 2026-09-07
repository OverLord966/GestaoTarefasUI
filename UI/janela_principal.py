import tkinter as tk
from tkinter import ttk
from UI.criar_tarefa_ui import CriarTarefaUI
from UI.listar_tarefas_ui import ListarTarefasUI
from UI.dashboard_ui import DashboardUI

class JanelaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gestor de Tarefas")
        self.geometry("900x600")
        self.modo_escuro = False

        self.frame_conteudo = tk.Frame(self, bg="#F3F3F3")
        self.frame_conteudo.pack(expand=True, fill="both")

        self.mostrar_home()

    def toggle_tema(self):
        self.modo_escuro = not self.modo_escuro
        self.mostrar_home()

    def aplicar_fundo(self):
        self.frame_conteudo.configure(bg="#1E1E1E" if self.modo_escuro else "#F3F3F3")

    def mostrar_home(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        fundo = "#1E1E1E" if self.modo_escuro else "#F3F3F3"
        card = "#2A2A2A" if self.modo_escuro else "#FFFFFF"
        texto = "#FFFFFF" if self.modo_escuro else "#1A1A1A"
        lampada = "🔆" if self.modo_escuro else "💡"

        self.frame_conteudo.configure(bg=fundo)

        card_frame = tk.Frame(
            self.frame_conteudo,
            bg=card,
            padx=40,
            pady=40,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card_frame.pack(expand=True)

        titulo_frame = tk.Frame(card_frame, bg=card)
        titulo_frame.pack(fill="x")

        tk.Label(
            titulo_frame,
            text="Gestor de Tarefas",
            font=("Segoe UI", 26, "bold"),
            bg=card,
            fg=texto
        ).pack(side="left")

        tk.Button(
            titulo_frame,
            text=lampada,
            font=("Segoe UI Emoji", 22),
            bg=card,
            fg=texto,
            relief="flat",
            bd=0,
            command=self.toggle_tema
        ).pack(side="right")

        tk.Label(
            card_frame,
            text="Uma aplicação simples e intuitiva para gerir as tuas tarefas diárias.\n"
                 "Cria, organiza, acompanha e conclui tarefas de forma rápida e eficiente.",
            font=("Segoe UI", 12),
            bg=card,
            fg=texto
        ).pack(pady=20)

        def criar_botao(texto, comando, cor="#0A66C2", hover="#084C8A"):
            btn = tk.Button(
                card_frame,
                text=texto,
                command=comando,
                font=("Segoe UI", 12, "bold"),
                bg=cor,
                fg="white",
                activebackground=hover,
                activeforeground="white",
                relief="flat",
                padx=12,
                pady=8,
                bd=0,
                width=20
            )
            btn.pack(pady=6)
            return btn

        criar_botao(
            "Criar Tarefa",
            lambda: (
                self.aplicar_fundo(),
                CriarTarefaUI(self.frame_conteudo, self.mostrar_home)
            )
        )

        criar_botao(
            "Listar Tarefas",
            lambda: (
                self.aplicar_fundo(),
                ListarTarefasUI(self.frame_conteudo, self.mostrar_home)
            )
        )

        criar_botao("Dashboard", lambda: DashboardUI(self.frame_conteudo, self.mostrar_home))


        criar_botao("Sair", self.destroy, cor="#B00020", hover="#8A0018")
