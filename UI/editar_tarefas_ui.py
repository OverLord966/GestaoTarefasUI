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

        # Aplicar tema nativo moderno do sistema
        style = ttk.Style()
        try:
            style.theme_use('vista')
        except tk.TclError:
            try:
                style.theme_use('xpnative')
            except tk.TclError:
                pass

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
        titulo_entry.insert(0, tarefa.get("titulo", ""))
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
        descricao_text.insert("1.0", tarefa.get("descricao", ""))
        descricao_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(descricao_frame, orient="vertical", command=descricao_text.yview)
        scroll.pack(side="right", fill="y")
        descricao_text.configure(yscrollcommand=scroll.set)

        # -----------------------------
        # FUNÇÃO AUXILIAR DE EXTRAÇÃO DE VALORES
        # -----------------------------
        def obter_valor_tarefa(dicionario, *chaves_possiveis):
            for chave in chaves_possiveis:
                if chave in dicionario and dicionario[chave] is not None:
                    return str(dicionario[chave]).strip()
            return ""

        # Função para forçar a atualização visual no mapeamento do widget
        def forcar_render(event, combo, valor):
            combo.set(valor)

        # -----------------------------
        # PRIORIDADE
        # -----------------------------
        ttk.Label(card, text="Prioridade:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        opcoes_prioridade = ["Alta", "Média", "Baixa"]
        val_prio = obter_valor_tarefa(tarefa, "prioridade", "Prioridade", "prioridade_nome")
        prio_selecionada = next((p for p in opcoes_prioridade if p.lower() == val_prio.lower()), opcoes_prioridade[1])

        prioridade_var = tk.StringVar(value=prio_selecionada)
        prioridade_combo = ttk.Combobox(
            card,
            textvariable=prioridade_var,
            values=opcoes_prioridade,
            state="readonly",
            font=("Segoe UI", 10),
            width=22
        )
        prioridade_combo.pack(pady=5, anchor="w")
        prioridade_combo.set(prio_selecionada)
        prioridade_combo.bind("<Map>", lambda e: forcar_render(e, prioridade_combo, prio_selecionada))

        # -----------------------------
        # ESTADO
        # -----------------------------
        ttk.Label(card, text="Estado:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        opcoes_estado = ["Por fazer", "Em progresso", "Quase a terminar", "Concluída"]
        val_estado = obter_valor_tarefa(tarefa, "estado", "Estado", "estado_nome")
        estado_selecionado = next((e for e in opcoes_estado if e.lower() == val_estado.lower()), opcoes_estado[0])

        estado_var = tk.StringVar(value=estado_selecionado)
        estado_combo = ttk.Combobox(
            card,
            textvariable=estado_var,
            values=opcoes_estado,
            state="readonly",
            font=("Segoe UI", 10),
            width=22
        )
        estado_combo.pack(pady=5, anchor="w")
        estado_combo.set(estado_selecionado)
        estado_combo.bind("<Map>", lambda e: forcar_render(e, estado_combo, estado_selecionado))

        # -----------------------------
        # PRAZO
        # -----------------------------
        ttk.Label(card, text="Prazo:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        prazo_var = tk.StringVar()
        prazo_var.set(tarefa.get("prazo", ""))

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
                "id": tarefa.get("id"),
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