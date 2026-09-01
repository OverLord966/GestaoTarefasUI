import tkinter as tk
from tkinter import ttk
class WelcomeUI:
    def __init__(self, frame, abrir_criar, abrir_listar, abrir_dashboard, sair):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Segoe UI", 12),
                        padding=10)

        style.configure("TLabel",
                        font=("Segoe UI", 14),
                        background="#FFFFFF")
        # Limpar conteúdo
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(frame, text="Gestor de Tarefas", font=("Arial", 28), bg="#FFFFFF").pack(pady=40)

        tk.Label(frame, text="Uma aplicação simples e intuitiva para gerir as tuas tarefas diárias.",
                 font=("Arial", 14), bg="#FFFFFF").pack(pady=20)

        tk.Label(frame, text="Cria, organiza, acompanha e conclui tarefas de forma rápida e eficiente.",
                 font=("Arial", 12), bg="#FFFFFF").pack(pady=10)

        ttk.Button(frame, text="Criar Tarefa", command=abrir_criar).pack(pady=10)
        ttk.Button(frame, text="Listar Tarefas", command=abrir_listar).pack(pady=10)
        ttk.Button(frame, text="Dashboard", command=abrir_dashboard).pack(pady=10)
        ttk.Button(frame, text="Sair", command=sair).pack(pady=10)

