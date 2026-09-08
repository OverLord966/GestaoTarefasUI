import tkinter as tk
from tkinter import ttk
from UI.calendario_moderno import CalendarioModerno
from DAL.tarefas_dal import editar_tarefa_dal

class EditarTarefaUI:

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
            entrada_bg = "#3A3A3A"
            entrada_fg = "#FFFFFF"
            cor_botao = "#0A3A66"
            cor_hover = "#06294A"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            entrada_bg = "#FFFFFF"
            entrada_fg = "#1A1A1A"
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

        ttk.Label(
            card,
            text="Editar Tarefa",
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
        titulo_entry.insert(0, tarefa["titulo"])
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
        descricao_text.insert("1.0", tarefa["descricao"])
        descricao_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(descricao_frame, orient="vertical", command=descricao_text.yview)
        scroll.pack(side="right", fill="y")
        descricao_text.configure(yscrollcommand=scroll.set)

        # -----------------------------
        # PRIORIDADE
        # -----------------------------
        ttk.Label(card, text="Prioridade:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        prioridade_var = tk.StringVar(value=tarefa["prioridade"])
        prioridade_combo = ttk.Combobox(
            card,
            textvariable=prioridade_var,
            values=["Alta", "Média", "Baixa"],
            state="readonly",
            width=20
        )
        prioridade_combo.pack(pady=5, anchor="w")

        # -----------------------------
        # ESTADO
        # -----------------------------
        ttk.Label(card, text="Estado:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        estado_var = tk.StringVar(value=tarefa["estado"])
        estado_combo = ttk.Combobox(
            card,
            textvariable=estado_var,
            values=["Por fazer", "Em progresso", "Quase a terminar", "Concluída"],
            state="readonly",
            width=20
        )
        estado_combo.pack(pady=5, anchor="w")

        # -----------------------------
        # PRAZO (Calendário Moderno)
        # -----------------------------
        ttk.Label(card, text="Prazo:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        prazo_var = tk.StringVar()
        prazo_var.set(tarefa["prazo"])

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

        def guardar():
            tarefa_editada = {
                "id": tarefa["id"],
                "titulo": titulo_entry.get().strip(),
                "descricao": descricao_text.get("1.0", "end").strip(),
                "prioridade": prioridade_combo.get().strip(),
                "estado": estado_combo.get().strip(),
                "prazo": prazo_var.get().strip()
            }

            editar_tarefa_dal(tarefa_editada)
            voltar_callback()

        criar_botao(card, "Guardar Alterações", guardar)
        criar_botao(card, "Voltar", voltar_callback, cor="#6C757D", hover="#5A6268")
