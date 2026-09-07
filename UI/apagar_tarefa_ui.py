import tkinter as tk
from tkinter import ttk
from BLL.tarefas_bll import apagar_tarefa

class ApagarTarefaUI:

    def __init__(self, frame, tarefa, voltar_callback):

        # Limpar frame
        for widget in frame.winfo_children():
            widget.destroy()

        self.frame = frame

        # -----------------------------
        # TEMA (Light / Dark)
        # -----------------------------
        modo_escuro = getattr(frame.master, "modo_escuro", False)

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
            cor_botao = "#0A3A66"
            cor_hover = "#06294A"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            cor_botao = "#0A66C2"
            cor_hover = "#084C8A"

        # Container central
        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True)

        # Card moderno estilo Windows 11
        card = tk.Frame(
            container,
            bg=card_cor,
            padx=40,
            pady=40,
            bd=0,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card.pack(pady=20)

        # Título
        ttk.Label(
            card,
            text="Apagar Tarefa",
            font=("Segoe UI", 22, "bold"),
            foreground=texto,
            background=card_cor
        ).pack(pady=(0, 20))

        # Título da tarefa
        ttk.Label(
            card,
            text=f"Título: {tarefa['titulo']}",
            font=("Segoe UI", 12),
            foreground=texto,
            background=card_cor
        ).pack(anchor="w", pady=5)

        # Descrição da tarefa
        ttk.Label(
            card,
            text=f"Descrição: {tarefa['descricao']}",
            font=("Segoe UI", 12),
            wraplength=400,
            foreground=texto,
            background=card_cor
        ).pack(anchor="w", pady=5)

        # Pergunta de confirmação
        ttk.Label(
            card,
            text="Tens a certeza que queres apagar esta tarefa?",
            font=("Segoe UI", 12, "bold"),
            foreground="#B00020",
            background=card_cor
        ).pack(pady=20)

        # -----------------------------
        # BOTÕES MODERNOS
        # -----------------------------
        def criar_botao(parent, texto_btn, comando, cor=cor_botao, hover=cor_hover):
            btn = tk.Button(
                parent,
                text=texto_btn,
                command=comando,
                font=("Segoe UI", 11, "bold"),
                bg=cor,
                fg="white",
                activebackground=hover,
                activeforeground="white",
                relief="flat",
                padx=12,
                pady=6,
                bd=0,
                width=18
            )
            btn.pack(pady=6)
            return btn

        # Função apagar
        def confirmar_apagar():
            apagar_tarefa(tarefa["id"])
            voltar_callback()

        # Botões
        criar_botao(card, "Apagar", confirmar_apagar, cor="#B00020", hover="#8A0018")
        criar_botao(card, "Cancelar", voltar_callback, cor="#6C757D", hover="#5A6268")
