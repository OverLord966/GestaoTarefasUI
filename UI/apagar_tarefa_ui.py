import tkinter as tk
from tkinter import ttk
from DAL.tarefas_dal import apagar_tarefa_dal

class ApagarTarefaUI:

    def __init__(self, frame, tarefa, voltar_callback):

        # Limpar frame
        for widget in frame.winfo_children():
            widget.destroy()

        self.frame = frame

        # Tema Dark/Light
        modo_escuro = getattr(frame.master, "modo_escuro", False)

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
            subtexto = "#CCCCCC"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            subtexto = "#555555"

        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True)

        card = tk.Frame(
            container,
            bg=card_cor,
            padx=40,
            pady=30,
            bd=0,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card.pack(pady=20)

        # Título da tela
        ttk.Label(
            card,
            text="Apagar Tarefa",
            font=("Segoe UI", 22, "bold"),
            foreground=texto,
            background=card_cor
        ).pack(pady=(0, 15))

        # Detalhes da Tarefa (Título e Descrição)
        ttk.Label(
            card,
            text=f"Título: {tarefa.get('titulo', '')}",
            font=("Segoe UI", 11, "bold"),
            foreground=texto,
            background=card_cor,
            anchor="w"
        ).pack(fill="x", pady=3)

        ttk.Label(
            card,
            text=f"Descrição: {tarefa.get('descricao', '')}",
            font=("Segoe UI", 11),
            foreground=subtexto,
            background=card_cor,
            anchor="w",
            wraplength=350
        ).pack(fill="x", pady=3)

        # NOVOS CAMPOS: Prioridade, Estado e Prazo
        ttk.Label(
            card,
            text=f"Prioridade: {tarefa.get('prioridade', 'N/A')}",
            font=("Segoe UI", 10),
            foreground=subtexto,
            background=card_cor,
            anchor="w"
        ).pack(fill="x", pady=2)

        ttk.Label(
            card,
            text=f"Estado: {tarefa.get('estado', 'N/A')}",
            font=("Segoe UI", 10),
            foreground=subtexto,
            background=card_cor,
            anchor="w"
        ).pack(fill="x", pady=2)

        ttk.Label(
            card,
            text=f"Prazo: {tarefa.get('prazo', 'N/A')}",
            font=("Segoe UI", 10),
            foreground=subtexto,
            background=card_cor,
            anchor="w"
        ).pack(fill="x", pady=(2, 15))

        # Mensagem de Aviso em Vermelho
        tk.Label(
            card,
            text="Tens a certeza que queres apagar esta tarefa?",
            font=("Segoe UI", 11, "bold"),
            fg="#D9534F",
            bg=card_cor
        ).pack(pady=10)

        # Botão Apagar (Vermelho)
        tk.Button(
            card,
            text="Apagar",
            font=("Segoe UI", 11, "bold"),
            bg="#A90022",
            fg="white",
            activebackground="#800019",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=20,
            pady=6,
            command=lambda: [apagar_tarefa_dal(tarefa.get("id")), voltar_callback()]
        ).pack(pady=5)

        # Botão Cancelar (Cinzento)
        tk.Button(
            card,
            text="Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=20,
            pady=6,
            command=voltar_callback
        ).pack(pady=5)