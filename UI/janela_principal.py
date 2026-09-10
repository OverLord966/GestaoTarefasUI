import tkinter as tk
from tkinter import ttk

# Importação das visões (UI) dos restantes ecrãs da aplicação
from UI.criar_tarefa_ui import CriarTarefaUI
from UI.listar_tarefas_ui import ListarTarefasUI
from UI.dashboard_ui import DashboardUI


class JanelaPrincipal(tk.Tk):
    """
    Classe principal que herda de tk.Tk. 
    Funciona como a janela principal (root) e gestora de navegação do programa.
    """

    def __init__(self):
        super().__init__()  # Inicializa a janela Tkinter base

        # -----------------------------
        # CONFIGURAÇÃO DA JANELA
        # -----------------------------
        self.title("Gestor de Tarefas")
        self.geometry("900x600")
        
        # Variável de estado global para controlar o tema (Light = False, Dark = True)
        self.modo_escuro = False

        # Container (Frame) principal onde todas as restantes UIs serão desenhadas dinamicamente
        self.frame_conteudo = tk.Frame(self, bg="#F3F3F3")
        self.frame_conteudo.pack(expand=True, fill="both")

        # Carrega o ecrã inicial (Home/Menu Principal) ao iniciar
        self.mostrar_home()

    def toggle_tema(self):
        """Alterna o estado do modo escuro (True/False) e recarrega o menu principal."""
        self.modo_escuro = not self.modo_escuro
        self.mostrar_home()

    def aplicar_fundo(self):
        """Atualiza a cor de fundo do frame principal consoante o tema ativo."""
        self.frame_conteudo.configure(bg="#1E1E1E" if self.modo_escuro else "#F3F3F3")

    def mostrar_home(self):
        """Desenha o ecrã inicial (Menu Principal) com opções de navegação."""
        
        # Limpa todos os widgets presentes no frame antes de redesenhar
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Definição das cores consoante o tema ativo
        fundo = "#1E1E1E" if self.modo_escuro else "#F3F3F3"
        card = "#2A2A2A" if self.modo_escuro else "#FFFFFF"
        texto = "#FFFFFF" if self.modo_escuro else "#1A1A1A"
        lampada = "🔆" if self.modo_escuro else "💡"  # Ícone do botão do tema

        self.frame_conteudo.configure(bg=fundo)

        # -----------------------------
        # CARD CENTRAL
        # -----------------------------
        card_frame = tk.Frame(
            self.frame_conteudo,
            bg=card,
            padx=40,
            pady=40,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card_frame.pack(expand=True)

        # -----------------------------
        # CABEÇALHO DO CARD (Título + Botão Tema)
        # -----------------------------
        titulo_frame = tk.Frame(card_frame, bg=card)
        titulo_frame.pack(fill="x")

        # Título da aplicação
        tk.Label(
            titulo_frame,
            text="Gestor de Tarefas",
            font=("Segoe UI", 26, "bold"),
            bg=card,
            fg=texto
        ).pack(side="left")

        # Botão para alternar entre Modo Claro e Escuro
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

        # Texto explicativo/boas-vindas
        tk.Label(
            card_frame,
            text="Uma aplicação simples e intuitiva para gerir as tuas tarefas diárias.\n"
                 "Cria, organiza, acompanha e conclui tarefas de forma rápida e eficiente.",
            font=("Segoe UI", 12),
            bg=card,
            fg=texto
        ).pack(pady=20)

        # -----------------------------
        # GERADOR DE BOTÕES DO MENU
        # -----------------------------
        def criar_botao(texto, comando, cor="#0A66C2", hover="#084C8A"):
            """Função utilitária interna para padronizar os botões do menu."""
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

        # -----------------------------
        # NAVEGAÇÃO E AÇÕES DOS BOTÕES
        # -----------------------------
        
        # Botão para o ecrã "Criar Tarefa"
        criar_botao(
            "Criar Tarefa",
            lambda: (
                self.aplicar_fundo(),
                CriarTarefaUI(self.frame_conteudo, self.mostrar_home)
            )
        )

        # Botão para o ecrã "Listar Tarefas"
        criar_botao(
            "Listar Tarefas",
            lambda: (
                self.aplicar_fundo(),
                ListarTarefasUI(self.frame_conteudo, self.mostrar_home)
            )
        )

        # Botão para o ecrã "Dashboard"
        criar_botao(
            "Dashboard", 
            lambda: DashboardUI(self.frame_conteudo, self.mostrar_home)
        )

        # Botão para encerrar a aplicação
        criar_botao("Sair", self.destroy, cor="#B00020", hover="#8A0018")