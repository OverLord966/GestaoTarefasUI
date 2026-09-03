import tkinter as tk
from tkinter import ttk, messagebox
from BLL.tarefas_bll import editar_tarefa as editar_bll

class EditarTarefaUI:
    def __init__(self, tarefa, callback_recarregar):
        self.tarefa = tarefa
        self.callback_recarregar = callback_recarregar

        janela = tk.Toplevel()
        janela.title("Editar Tarefa")
        janela.configure(bg="#F3F3F3")
        janela.geometry("700x700")

        card = tk.Frame(janela, bg="#FFFFFF", padx=20, pady=20, bd=1, relief="solid")
        card.pack(fill="both", expand=True, pady=20)

        ttk.Label(card, text="Editar Tarefa", font=("Segoe UI", 18)).pack(pady=10)

        # Título
        ttk.Label(card, text="Título:").pack(anchor="w")
        self.titulo_entry = ttk.Entry(card)
        self.titulo_entry.pack(fill="x")
        self.titulo_entry.insert(0, tarefa["titulo"])

        # Descrição
        ttk.Label(card, text="Descrição:").pack(anchor="w", pady=5)
        self.descricao_text = tk.Text(card, height=5)
        self.descricao_text.pack(fill="x")
        self.descricao_text.insert("1.0", tarefa["descricao"])

        # Prioridade
        ttk.Label(card, text="Prioridade:").pack(anchor="w", pady=5)
        self.prioridade_combo = ttk.Combobox(card, values=["Alta", "Média", "Baixa"])
        self.prioridade_combo.pack(fill="x")
        self.prioridade_combo.set(tarefa["prioridade"])

        # Estado
        ttk.Label(card, text="Estado:").pack(anchor="w", pady=5)
        self.estado_combo = ttk.Combobox(card, values=["Quase a terminar", "Em progresso", "Pendente"])
        self.estado_combo.pack(fill="x")
        self.estado_combo.set(tarefa["estado"])

        # Prazo
        ttk.Label(card, text="Prazo (AAAA-MM-DD):").pack(anchor="w", pady=5)
        self.prazo_entry = ttk.Entry(card)
        self.prazo_entry.pack(fill="x")
        self.prazo_entry.insert(0, tarefa["prazo"])

        ttk.Button(card, text="Guardar Alterações", command=lambda: self.guardar(janela)).pack(pady=20)

    def guardar(self, janela):
        novo_titulo = self.titulo_entry.get()
        nova_descricao = self.descricao_text.get("1.0", "end").strip()
        nova_prioridade = self.prioridade_combo.get()
        novo_estado = self.estado_combo.get()
        novo_prazo = self.prazo_entry.get()

        editar_bll(
            self.tarefa["id"],
            novo_titulo,
            nova_descricao,
            nova_prioridade,
            novo_estado,
            novo_prazo
        )

        janela.destroy()
        self.callback_recarregar()
