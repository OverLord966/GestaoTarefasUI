import tkinter as tk
from tkinter import ttk

class WelcomeUI:
    def __init__(self, frame, abrir_criar_tarefa, abrir_listar_tarefas, abrir_dashboard, sair_callback):
        # Limpar frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Container central
        container = tk.Frame(frame, bg="#FFFFFF")
        container.pack(expand=True)

        card = tk.Frame(container, bg="#FFFFFF", padx=40, pady=40)
        card.pack()

        # Texto de boas-vindas (sem título duplicado)
        texto = tk.Label(
            card,
            text="Uma aplicação simples e intuitiva para gerir as tuas tarefas diárias.\n"
                 "Cria, organiza, acompanha e conclui tarefas de forma rápida e eficiente.",
            bg="#FFFFFF",
            fg="#333333",
            font=("Segoe UI", 13),
            justify="center"
        )
        texto.pack(pady=(0, 30))

        # Botões modernos
        def criar_botao(parent, texto, comando):
            btn = tk.Button(
                parent,
                text=texto,
                command=comando,
                font=("Segoe UI", 11, "bold"),
                bg="#0A66C2",
                fg="white",
                activebackground="#084C8A",
                activeforeground="white",
                relief="flat",
                padx=12,
                pady=6,
                bd=0,
                width=18   # largura fixa → botão mais pequeno
            )
            btn.pack(pady=6)
            return btn


        criar_botao(card, "Criar Tarefa", abrir_criar_tarefa)
        criar_botao(card, "Listar Tarefas", abrir_listar_tarefas)
        criar_botao(card, "Dashboard", abrir_dashboard)

        # Botão sair com estilo diferente
        btn_sair = tk.Button(
            card,
            text="Sair",
            command=sair_callback,
            font=("Segoe UI", 11, "bold"),
            bg="#D9534F",
            fg="white",
            activebackground="#B52F2B",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            bd=0,
            width=18
        )
        btn_sair.pack(pady=(20, 0))

