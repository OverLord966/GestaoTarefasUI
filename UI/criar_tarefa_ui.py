import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date, timedelta
from BLL.tarefas_bll import criar_tarefa
from DAL.database import renumerar_ids

class CriarTarefaUI:
    def mostrar_erro(self, card, mensagem):
        erro = tk.Label(card, text=mensagem, fg="#B00020", bg="#FFFFFF",
                        font=("Segoe UI", 11))
        erro.pack(pady=5)

        # Remover automaticamente após 3 segundos
        erro.after(3000, erro.destroy)

    def __init__(self, frame, voltar_menu_callback):

        for widget in frame.winfo_children():
            widget.destroy()

        # Container central
        container = tk.Frame(frame, bg="#F3F3F3")
        container.pack(expand=True)

        # Card estilo Windows 11
        card = tk.Frame(container, bg="#FFFFFF", padx=40, pady=40, bd=1, relief="solid")
        card.pack(pady=20)

        ttk.Label(card, text="Criar Nova Tarefa", font=("Segoe UI", 22)).pack(pady=10)

        # Título
        ttk.Label(card, text="Título:", anchor="w").pack(fill="x")
        titulo_entry = ttk.Entry(card, width=45)
        titulo_entry.pack(pady=5, anchor="w")

        # Descrição (Windows 11 style)
        ttk.Label(card, text="Descrição:", anchor="w").pack(fill="x")

        descricao_frame = tk.Frame(card, bg="#FFFFFF")
        descricao_frame.pack(fill="x", pady=5)

        descricao_text = tk.Text(
            descricao_frame,
            height=6,
            width=45,
            font=("Segoe UI", 11),
            wrap="word",
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        descricao_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(descricao_frame, orient="vertical", command=descricao_text.yview)
        scroll.pack(side="right", fill="y")

        descricao_text.configure(yscrollcommand=scroll.set)

        # Prioridade
        ttk.Label(card, text="Prioridade:", anchor="w").pack(fill="x")
        prioridade_var = tk.StringVar()
        prioridade_combo = ttk.Combobox(
            card,
            textvariable=prioridade_var,
            values=["Alta", "Média", "Baixa"],
            state="readonly",
            width=20
        )
        prioridade_combo.set("Média")
        prioridade_combo.pack(pady=5, anchor="w")

        # Estado
        ttk.Label(card, text="Estado:", anchor="w").pack(fill="x")
        estado_var = tk.StringVar()
        estado_combo = ttk.Combobox(
            card,
            textvariable=estado_var,
            values=["Por fazer", "Em progresso", "Concluída"],
            state="readonly",
            width=20
        )
        estado_combo.set("Por fazer")
        estado_combo.pack(pady=5, anchor="w")

        # Prazo
        ttk.Label(card, text="Prazo:", anchor="w").pack(fill="x")

        maxdate = date.today() + timedelta(days=365)

        prazo_entry = DateEntry(
            card,
            date_pattern="yyyy-mm-dd",
            mindate=date.today(),
            maxdate=maxdate,
            showweeknumbers=False,
            width=18
        )
        prazo_entry.pack(pady=5, anchor="w")

        # Botão Criar
        def submeter():
            titulo = titulo_entry.get().strip()
            descricao = descricao_text.get("1.0", "end").strip()
            prioridade = prioridade_combo.get().strip()
            estado = estado_combo.get().strip()
            prazo = prazo_entry.get().strip()

            # Validações
            if titulo == "":
                self.mostrar_erro(card, "O título não pode estar vazio.")
                return

            if descricao == "":
                self.mostrar_erro(card, "A descrição não pode estar vazia.")
                return

            if prioridade == "":
                self.mostrar_erro(card, "Escolhe uma prioridade.")
                return

            if estado == "":
                self.mostrar_erro(card, "Escolhe um estado.")
                return

            if prazo == "":
                self.mostrar_erro(card, "Escolhe um prazo válido.")
                return

            # Se tudo estiver OK → criar tarefa
            criar_tarefa(titulo, descricao, prioridade, estado, prazo)
            renumerar_ids()
            voltar_menu_callback()


        ttk.Button(card, text="Criar", command=submeter).pack(pady=20)
        ttk.Button(card, text="Voltar ao Menu", command=voltar_menu_callback).pack(pady=10)
