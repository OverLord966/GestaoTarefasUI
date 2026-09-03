import tkinter as tk
from tkinter import ttk, messagebox
from BLL.tarefas_bll import apagar_tarefa as apagar_bll
from DAL.database import renumerar_ids

class ApagarTarefaUI:
    def __init__(self, tarefa, callback_recarregar):
        self.tarefa = tarefa
        self.callback_recarregar = callback_recarregar

        janela = tk.Toplevel()
        janela.title("Apagar Tarefa")
        janela.configure(bg="#F3F3F3")
        janela.geometry("400x400")

        card = tk.Frame(janela, bg="#FFFFFF", padx=20, pady=20, bd=1, relief="solid")
        card.pack(fill="both", expand=True, pady=20)

        ttk.Label(card, text="Apagar Tarefa", font=("Segoe UI", 18)).pack(pady=10)

        ttk.Label(card, text=f"Título: {tarefa['titulo']}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(card, text=f"Descrição: {tarefa['descricao']}", font=("Segoe UI", 10)).pack(pady=5)

        ttk.Label(card, text="Tens a certeza que queres apagar esta tarefa?",
                  font=("Segoe UI", 11)).pack(pady=10)

        btn_frame = tk.Frame(card, bg="#FFFFFF")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Cancelar", width=12,
                   command=janela.destroy).pack(side="left", padx=10)

        ttk.Button(btn_frame, text="Apagar", width=12,
                   command=lambda: self.apagar(janela)).pack(side="left", padx=10)

    def apagar(self, janela):
        apagar_bll(self.tarefa["id"])
        renumerar_ids()
        janela.destroy()
        self.callback_recarregar()
