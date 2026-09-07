import tkinter as tk
from tkinter import ttk
from datetime import date
from BLL.tarefas_bll import criar_tarefa
from DAL.database import renumerar_ids
from UI.calendario_moderno import CalendarioModerno

class CriarTarefaUI:

    def mostrar_erro(self, card, mensagem):
        erro = tk.Label(
            card,
            text=mensagem,
            fg="#B00020",
            bg=card["bg"],
            font=("Segoe UI", 11)
        )
        erro.pack(pady=5)
        erro.after(3000, erro.destroy)

    def __init__(self, frame, voltar_menu_callback):

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
            entrada_bg = "#3A3A3A"
            entrada_fg = "#FFFFFF"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            cor_botao = "#0A66C2"
            cor_hover = "#084C8A"
            entrada_bg = "#FFFFFF"
            entrada_fg = "#1A1A1A"

        # -----------------------------
        # CONTAINER
        # -----------------------------
        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True)

        # -----------------------------
        # CARD
        # -----------------------------
        card = tk.Frame(
            container,
            bg=card_cor,
            padx=40,
            pady=40,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card.pack(pady=20)

        ttk.Label(
            card,
            text="Criar Nova Tarefa",
            font=("Segoe UI", 22, "bold"),
            foreground=texto,
            background=card_cor
        ).pack(pady=10)

        # -----------------------------
        # TÍTULO
        # -----------------------------
        ttk.Label(card, text="Título:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        titulo_entry = tk.Entry(card, width=45, bg=entrada_bg, fg=entrada_fg,
                                relief="solid", bd=1, font=("Segoe UI", 11))
        titulo_entry.pack(pady=5, anchor="w")

        # -----------------------------
        # DESCRIÇÃO
        # -----------------------------
        ttk.Label(card, text="Descrição:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        descricao_frame = tk.Frame(card, bg=card_cor)
        descricao_frame.pack(fill="x", pady=5)

        descricao_text = tk.Text(
            descricao_frame,
            height=6,
            width=45,
            font=("Segoe UI", 11),
            wrap="word",
            bd=1,
            relief="solid",
            highlightthickness=0,
            bg=entrada_bg,
            fg=entrada_fg
        )
        descricao_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(descricao_frame, orient="vertical", command=descricao_text.yview)
        scroll.pack(side="right", fill="y")
        descricao_text.configure(yscrollcommand=scroll.set)

        # -----------------------------
        # PRIORIDADE
        # -----------------------------
        ttk.Label(card, text="Prioridade:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

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

        # -----------------------------
        # ESTADO
        # -----------------------------
        ttk.Label(card, text="Estado:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        estado_var = tk.StringVar()
        estado_combo = ttk.Combobox(
            card,
            textvariable=estado_var,
            values=["Por fazer", "Em progresso"],
            state="readonly",
            width=20
        )
        estado_combo.set("Por fazer")
        estado_combo.pack(pady=5, anchor="w")

        # -----------------------------
        # PRAZO (Calendário moderno)
        # -----------------------------
        ttk.Label(card, text="Prazo:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        prazo_var = tk.StringVar()
        prazo_var.set(date.today().strftime("%Y-%m-%d"))

        def abrir_calendario():
            CalendarioModerno(self.frame, lambda data: prazo_var.set(data.strftime("%Y-%m-%d")))

        btn_prazo = tk.Button(
            card,
            textvariable=prazo_var,
            font=("Segoe UI", 11),
            bg=entrada_bg,
            fg=entrada_fg,
            relief="solid",
            bd=1,
            padx=10,
            pady=5,
            command=abrir_calendario
        )
        btn_prazo.pack(pady=5, anchor="w")

        # -----------------------------
        # BOTÕES
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

        # Função submeter
        def submeter():
            titulo = titulo_entry.get().strip()
            descricao = descricao_text.get("1.0", "end").strip()
            prioridade = prioridade_combo.get().strip()
            estado = estado_combo.get().strip()
            prazo = prazo_var.get().strip()

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

            criar_tarefa(titulo, descricao, prioridade, estado, prazo)
            renumerar_ids()
            voltar_menu_callback()

        criar_botao(card, "Criar", submeter)
        criar_botao(card, "Voltar ao Menu", voltar_menu_callback, cor="#6C757D", hover="#5A6268")
