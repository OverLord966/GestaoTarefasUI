import tkinter as tk
from tkinter import ttk, messagebox
from DAL.tarefas_dal import listar_tarefas
from BLL.tarefas_bll import concluir_tarefa_bll
from UI.editar_tarefas_ui import EditarTarefaUI
from UI.apagar_tarefa_ui import ApagarTarefaUI
import datetime

class ListarTarefasUI:
    def __init__(self, frame, voltar_menu_callback, filtro=None, voltar_dashboard_callback=None, mostrar_titulo=True):
        modo_escuro = getattr(frame.master, "modo_escuro", False)
        frame.master.mostrar_botao_listar = False

        self.voltar_dashboard_callback = voltar_dashboard_callback
        self.mostrar_titulo = mostrar_titulo

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
            tabela_bg = "#2A2A2A"
            tabela_fg = "#FFFFFF"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            tabela_bg = "#FFFFFF"
            tabela_fg = "#000000"
        # Tags diferentes para modo claro e escuro
        if modo_escuro:
            linha_bg = "#2A2A2A"       # fundo escuro
            linha_alt_bg = "#1E1E1E"   # fundo ainda mais escuro
            linha_fg = "#FFFFFF"       # texto branco
        else:
            linha_bg = "#F9F9F9"       # fundo claro
            linha_alt_bg = "#FFFFFF"   # fundo branco
            linha_fg = "#000000"       # texto preto

        self.frame = frame
        self.voltar_menu_callback = voltar_menu_callback

        for widget in frame.winfo_children():
            widget.destroy()

        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True, fill="both")

        card = tk.Frame(container, bg=card_cor, padx=30, pady=30,
                        highlightthickness=1, highlightbackground="#D0D0D0")
        card.pack(pady=20, expand=True, fill="both")

        if self.mostrar_titulo:
            ttk.Label(
                card,
                text="Lista de Tarefas",
                font=("Segoe UI", 20, "bold"),
                foreground=texto,
                background=card_cor
            ).pack(pady=(0, 15))

        colunas = ("id", "titulo", "descricao", "prioridade", "estado", "prazo")
        tree = ttk.Treeview(card, columns=colunas, show="headings", height=12)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=tabela_bg, fieldbackground=tabela_bg,
                        foreground=tabela_fg, rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"),
                        background=card_cor, foreground=texto)

        for col in colunas:
            tree.heading(col, text=col.capitalize())

        tree.column("id", width=50)
        tree.column("titulo", width=150)
        tree.column("descricao", width=300)
        tree.column("prioridade", width=90)
        tree.column("estado", width=150)
        tree.column("prazo", width=100)

        tree.pack(pady=10, fill="both", expand=True)
        tree.bind("<Double-1>", lambda event: self._abrir_detalhes(tree, event))

        tree.tag_configure("linha", background=linha_bg, foreground=linha_fg)
        tree.tag_configure("linha_alt", background=linha_alt_bg, foreground=linha_fg)
        tree.tag_configure("concluida", background="#2E7D32", foreground="white")
        tree.tag_configure("concluida_atraso", background="#FF8C00", foreground="white")
        tree.tag_configure("atraso", background="#C62828", foreground="white")
    

        tarefas = listar_tarefas()
        # Ordenar por ID
        tarefas = sorted(tarefas, key=lambda t: t["id"])

        hoje = datetime.date.today()

        # -----------------------------
        # FILTROS CORRIGIDOS
        # -----------------------------
        if filtro == "concluidas":
            tarefas = [t for t in tarefas if "conclu" in t["estado"].lower() and "atras" not in t["estado"].lower()]

        elif filtro == "concluidas_atraso":
            tarefas = [t for t in tarefas if "conclu" in t["estado"].lower() and "atras" in t["estado"].lower()]

        elif filtro == "atraso":
            tarefas = [
                t for t in tarefas
                if ((t["prazo"] if isinstance(t["prazo"], datetime.date)
                     else datetime.datetime.strptime(t["prazo"], "%Y-%m-%d").date()) < hoje)
                and "conclu" not in t["estado"].lower()
            ]

        elif filtro == "alta":
            tarefas = [t for t in tarefas if t["prioridade"].lower() == "alta"]

        elif filtro == "quase":
            tarefas = [t for t in tarefas if t["estado"].lower() == "quase a terminar"]

        elif filtro == "por_fazer":
            tarefas = [t for t in tarefas if t["estado"].lower() == "por fazer"]

        # -----------------------------
        # INSERIR LINHAS
        # -----------------------------
        for i, tarefa in enumerate(tarefas):
            prazo_data = tarefa["prazo"] if isinstance(tarefa["prazo"], datetime.date) \
                else datetime.datetime.strptime(tarefa["prazo"], "%Y-%m-%d").date()

            estado_lower = tarefa["estado"].lower()

            if "conclu" in estado_lower and "atras" in estado_lower:
                tag = "concluida_atraso"

            elif "conclu" in estado_lower:
                tag = "concluida"

            elif prazo_data < hoje:
                tag = "atraso"

            else:
                tag = "linha_alt" if i % 2 == 0 else "linha"

            tree.insert("", "end", values=(
                tarefa["id"],
                tarefa["titulo"],
                tarefa["descricao"],
                tarefa["prioridade"],
                tarefa["estado"],
                prazo_data.strftime("%Y-%m-%d")
            ), tags=(tag,))

        def voltar():
            if self.voltar_dashboard_callback:
                self.voltar_dashboard_callback()
            else:
                self.voltar_menu_callback()

        tk.Button(
            card,
            text="Voltar ao Dashboard" if self.voltar_dashboard_callback else "Voltar ao Menu",
            command=voltar,
            font=("Segoe UI", 11, "bold"),
            bg="#6C757D",
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            width=18
        ).pack(pady=10)

    # -----------------------------
    # DOUBLE CLICK
    # -----------------------------
    def _abrir_detalhes(self, tree, event):
        item = tree.identify_row(event.y)
        if not item:
            return

        values = tree.item(item, "values")
        tarefa = {
            "id": int(values[0]),
            "titulo": values[1],
            "descricao": values[2],
            "prioridade": values[3],
            "estado": values[4],
            "prazo": values[5]
        }

        self.abrir_detalhes_tarefa(tarefa)

    # -----------------------------
    # CONCLUIR
    # -----------------------------
    def concluir_tarefa(self, id_tarefa, janela):
        concluir_tarefa_bll(id_tarefa)
        messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
        janela.destroy()
        self.recarregar_lista()

    def recarregar_lista(self):
        self.__init__(self.frame, self.voltar_menu_callback)

    # -----------------------------
    # DETALHES
    # -----------------------------
    def abrir_detalhes_tarefa(self, tarefa):
        detalhes = tk.Toplevel()
        modo_escuro = getattr(self.frame.master, "modo_escuro", False)

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
            desc_bg = "#3A3A3A"
            desc_fg = "#FFFFFF"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            desc_bg = "#FFFFFF"
            desc_fg = "#000000"
        # Tags diferentes para modo claro e escuro
        if modo_escuro:
            linha_bg = "#2A2A2A"       # fundo escuro
            linha_alt_bg = "#1E1E1E"   # fundo ainda mais escuro
            linha_fg = "#FFFFFF"       # texto branco
        else:
            linha_bg = "#F9F9F9"       # fundo claro
            linha_alt_bg = "#FFFFFF"   # fundo branco
            linha_fg = "#000000"       # texto preto

        detalhes.title("Detalhes da Tarefa")
        detalhes.configure(bg=fundo)
        detalhes.geometry("750x750")
        detalhes.minsize(750, 750)

        card = tk.Frame(
            detalhes,
            bg=card_cor,
            padx=30,
            pady=30,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card.pack(fill="both", expand=True, pady=20, padx=20)

        ttk.Label(card, text="Detalhes da Tarefa",
                    font=("Segoe UI", 20, "bold"),
                    foreground=texto,
                    background=card_cor).pack(pady=(0, 20))

        def campo(label, valor):
            ttk.Label(card, text=label, font=("Segoe UI", 11, "bold"),
                        foreground=texto, background=card_cor).pack(anchor="w")
            ttk.Label(card, text=valor, font=("Segoe UI", 11),
                        foreground=texto, background=card_cor).pack(anchor="w", pady=(0, 10))

        campo("ID:", tarefa["id"])
        campo("Título:", tarefa["titulo"])

        ttk.Label(card, text="Descrição:", font=("Segoe UI", 11, "bold"),
                    foreground=texto, background=card_cor).pack(anchor="w")

        desc_frame = tk.Frame(card, bg=card_cor)
        desc_frame.pack(fill="x", pady=5)

        desc_text = tk.Text(
            desc_frame,
            height=6,
            width=60,
            font=("Segoe UI", 11),
            wrap="word",
            bd=1,
            relief="solid",
            highlightthickness=0,
            bg=desc_bg,
            fg=desc_fg
        )
        desc_text.insert("1.0", tarefa["descricao"])
        desc_text.config(state="disabled")
        desc_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(desc_frame, orient="vertical", command=desc_text.yview)
        scroll.pack(side="right", fill="y")
        desc_text.configure(yscrollcommand=scroll.set)

        linha_status = tk.Frame(card, bg=card_cor)
        linha_status.pack(fill="x", pady=10)

        def badge(parent, label, valor, cor):
            box = tk.Frame(parent, bg=cor, padx=10, pady=10)
            box.pack(side="left", padx=10, fill="x", expand=True)
            ttk.Label(box, text=label, font=("Segoe UI", 11, "bold"), background=cor).pack(anchor="w")
            ttk.Label(box, text=valor, font=("Segoe UI", 11), background=cor).pack(anchor="w")

        cor_prioridade = {
            "Alta": "#FFD966",
            "Média": "#FFE699",
            "Baixa": "#FFF2CC"
        }.get(tarefa["prioridade"], "#FFF2CC")

        cor_estado = {
            "Concluída": "#A9D08E",
            "Concluída com atraso": "#FF8C00",
            "Quase a terminar": "#C6E0B4",
            "Em progresso": "#F4B084",
            "Por fazer": "#BDD7EE"
        }.get(tarefa["estado"], "#BDD7EE")

        badge(linha_status, "Prioridade:", tarefa["prioridade"], cor_prioridade)
        badge(linha_status, "Estado:", tarefa["estado"], cor_estado)

        prazo_box = tk.Frame(card, bg="#DDEBF7", padx=10, pady=10)
        prazo_box.pack(fill="x", pady=5)

        ttk.Label(prazo_box, text="Prazo:", font=("Segoe UI", 11, "bold"),
                    background="#DDEBF7").pack(anchor="w")
        ttk.Label(prazo_box, text=tarefa["prazo"], font=("Segoe UI", 11),
                    background="#DDEBF7").pack(anchor="w")

        btn_frame = tk.Frame(card, bg=card_cor)
        btn_frame.pack(pady=15)

        def criar_botao(parent, texto_btn, comando, cor="#0A66C2", hover="#084C8A"):
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
                width=15
            )
            btn.pack(side="left", padx=10)
            return btn

        # ------------------------------------------
        # SE VEIO DO DASHBOARD → ESCONDER BOTÕES
        # ------------------------------------------
        if self.voltar_dashboard_callback:
            # Não cria nenhum botão
            pass

        # ------------------------------------------
        # SE VEIO DO MENU → BOTÕES NORMAIS
        # ------------------------------------------
        else:
            if "conclu" in tarefa["estado"].lower():
                # Tarefa concluída → bloquear botões
                criar_botao(btn_frame, "Editar", None, cor="#E0E0E0", hover="#E0E0E0").config(state="disabled", fg="Black")
                criar_botao(btn_frame, "Apagar", None, cor="#E0E0E0", hover="#E0E0E0").config(state="disabled", fg="Black")
                criar_botao(btn_frame, "Concluir", None, cor="#E0E0E0", hover="#E0E0E0").config(state="disabled", fg="Black")
            else:
                criar_botao(btn_frame, "Editar",
                            lambda: (detalhes.destroy(), self.editar_tarefa(tarefa)))
                criar_botao(btn_frame, "Apagar",
                            lambda: (detalhes.destroy(), self.apagar_tarefa(tarefa)),
                            cor="#D9534F", hover="#B52F2B")
                criar_botao(btn_frame, "Concluir",
                            lambda: self.concluir_tarefa(tarefa["id"], detalhes),
                            cor="#198754", hover="#146C43")


        fechar_frame = tk.Frame(card, bg=card_cor)
        fechar_frame.pack(pady=10, anchor="center")
        criar_botao(fechar_frame, "Fechar",
                    detalhes.destroy,
                    cor="#6C757D",
                    hover="#6C757D")

    def editar_tarefa(self, tarefa):
        EditarTarefaUI(self.frame, tarefa, self.recarregar_lista)

    def apagar_tarefa(self, tarefa):
        ApagarTarefaUI(self.frame, tarefa, self.recarregar_lista)
