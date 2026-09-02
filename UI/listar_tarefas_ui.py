import tkinter as tk
from tkinter import ttk, messagebox
from DAL.database import renumerar_ids
from DAL.tarefas_dal import listar_tarefas
from BLL.tarefas_bll import apagar_tarefa as apagar_tarefa_bll
from DAL.tarefas_concluidas_dal import guardar_tarefa_concluida
from BLL.tarefas_bll import concluir_tarefa_bll

class ListarTarefasUI:
    def __init__(self, frame, voltar_menu_callback):
        self.frame = frame
        self.voltar_menu_callback = voltar_menu_callback

        # Limpar frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Container
        container = tk.Frame(frame, bg="#F3F3F3")
        container.pack(expand=True)

        card = tk.Frame(container, bg="#FFFFFF", padx=20, pady=20, bd=1, relief="solid")
        card.pack(pady=20)

        ttk.Label(card, text="Lista de Tarefas", font=("Segoe UI", 20)).pack(pady=10)

        # Tabela
        colunas = ("id", "titulo", "descricao", "prioridade", "estado", "prazo")
        tree = ttk.Treeview(card, columns=colunas, show="headings", height=10)

        for col in colunas:
            tree.heading(col, text=col.capitalize())

        tree.column("id", width=40)
        tree.column("titulo", width=150)
        tree.column("descricao", width=200)
        tree.column("prioridade", width=80)
        tree.column("estado", width=100)
        tree.column("prazo", width=100)

        tree.pack(pady=10)

        # Carregar tarefas da BD (já ordenadas por ID ASC)
        tarefas = listar_tarefas()

        for tarefa in tarefas:
            tree.insert("", "end", values=(
                tarefa["id"],
                tarefa["titulo"],
                tarefa["descricao"],
                tarefa["prioridade"],
                tarefa["estado"],
                tarefa["prazo"]
            ))

        # Ajustar coluna descrição
        if tarefas:
            max_len = max(len(t["descricao"]) for t in tarefas)
            tree.column("descricao", width=min(max_len * 7, 400))

        # Duplo clique → abrir detalhes
        def on_click(event):
            item = tree.identify_row(event.y)
            if item:
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

        tree.bind("<Double-1>", on_click)

        ttk.Button(card, text="Voltar ao Menu", command=voltar_menu_callback).pack(pady=10)


    # ---------------------------------------------------------
    # Apagar tarefa
    # ---------------------------------------------------------
    def apagar_tarefa(self, tarefa_id, janela):
        resposta = messagebox.askyesno(
            "Confirmar eliminação",
            "Tens a certeza que queres apagar esta tarefa?"
        )

        if resposta:
            apagar_tarefa_bll(tarefa_id)   # chama BLL → DAL → BD
            renumerar_ids()            # renumera IDs
            janela.destroy()
            self.recarregar_lista()


    # ---------------------------------------------------------
    # Editar tarefa
    # ---------------------------------------------------------
    def editar_tarefa(self, tarefa):
        janela = tk.Toplevel()
        janela.title("Editar Tarefa")
        janela.configure(bg="#F3F3F3")
        janela.geometry("700x700")

        card = tk.Frame(janela, bg="#FFFFFF", padx=20, pady=20, bd=1, relief="solid")
        card.pack(fill="both", expand=True, pady=20)

        ttk.Label(card, text="Editar Tarefa", font=("Segoe UI", 18)).pack(pady=10)

        # -----------------------------
        # CAMPOS
        # -----------------------------
        ttk.Label(card, text="Título:").pack(anchor="w")
        titulo_entry = ttk.Entry(card)
        titulo_entry.pack(fill="x")
        titulo_entry.insert(0, tarefa["titulo"])

        ttk.Label(card, text="Descrição:").pack(anchor="w", pady=5)
        descricao_text = tk.Text(card, height=5)
        descricao_text.pack(fill="x")
        descricao_text.insert("1.0", tarefa["descricao"])

        ttk.Label(card, text="Prioridade:").pack(anchor="w", pady=5)
        prioridade_combo = ttk.Combobox(card, values=["Alta", "Média", "Baixa"])
        prioridade_combo.pack(fill="x")
        prioridade_combo.set(tarefa["prioridade"])

        ttk.Label(card, text="Estado:").pack(anchor="w", pady=5)
        estado_combo = ttk.Combobox(card, values=["Quase a terminar", "Em progresso", "Pendente"])
        estado_combo.pack(fill="x")
        estado_combo.set(tarefa["estado"])

        ttk.Label(card, text="Prazo (AAAA-MM-DD):").pack(anchor="w", pady=5)
        prazo_entry = ttk.Entry(card)
        prazo_entry.pack(fill="x")
        prazo_entry.insert(0, tarefa["prazo"])

        # -----------------------------
        # BOTÃO GUARDAR
        # -----------------------------
        def guardar():
            novo_titulo = titulo_entry.get()
            nova_descricao = descricao_text.get("1.0", "end").strip()
            nova_prioridade = prioridade_combo.get()
            novo_estado = estado_combo.get()
            novo_prazo = prazo_entry.get()

            from BLL.tarefas_bll import editar_tarefa as editar_bll
            editar_bll(
                tarefa["id"],
                novo_titulo,
                nova_descricao,
                nova_prioridade,
                novo_estado,
                novo_prazo
            )

            janela.destroy()
            self.recarregar_lista()
            
                
        ttk.Button(card, text="Guardar Alterações", command=guardar).pack(pady=20)

    def concluir_tarefa(self, id_tarefa, janela):
        concluir_tarefa_bll(id_tarefa)
        messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
        self.recarregar_lista()
        janela.destroy()
        
    # ---------------------------------------------------------
    # Recarregar tabela (CORRIGIDO)
    # ---------------------------------------------------------
    def recarregar_lista(self):
        # Apenas reinicia a UI com os mesmos parâmetros
        self.__init__(self.frame, self.voltar_menu_callback)


    # ---------------------------------------------------------
    # Janela de detalhes
    # ---------------------------------------------------------
    def abrir_detalhes_tarefa(self, tarefa):
        detalhes = tk.Toplevel()
        detalhes.title("Detalhes da Tarefa")
        detalhes.configure(bg="#F3F3F3")

        descricao_len = len(tarefa["descricao"])
        extra_height = min(descricao_len // 7, 180)
        altura_final = 560 + extra_height

        detalhes.geometry(f"600x{altura_final}")
        detalhes.minsize(800, 600)

        card = tk.Frame(detalhes, bg="#FFFFFF", padx=25, pady=20, bd=1, relief="solid")
        card.pack(fill="both", expand=True, pady=15)

        ttk.Label(card, text="Detalhes da Tarefa", font=("Segoe UI", 18)).pack(pady=5)

        ttk.Label(card, text="Título:", font=("Segoe UI", 12)).pack(anchor="w")
        ttk.Label(card, text=tarefa["titulo"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=3)

        ttk.Label(card, text="Descrição:", font=("Segoe UI", 12)).pack(anchor="w")

        desc_frame = tk.Frame(card, bg="#FFFFFF")
        desc_frame.pack(fill="x", pady=5)

        desc_frame.grid_columnconfigure(0, weight=1)
        desc_frame.grid_rowconfigure(0, weight=1)

        desc_text = tk.Text(
            desc_frame,
            height=6,
            width=50,
            font=("Segoe UI", 11),
            wrap="word",
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        desc_text.insert("1.0", tarefa["descricao"])
        desc_text.config(state="disabled")
        desc_text.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(desc_frame, orient="vertical", command=desc_text.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        desc_text.configure(yscrollcommand=scroll.set)

        linha_status = tk.Frame(card, bg="#FFFFFF")
        linha_status.pack(fill="x", pady=10)

        def criar_quadrado(parent, label, valor, cor):
            box = tk.Frame(parent, bg=cor, padx=10, pady=10)
            box.pack(side="left", padx=10, fill="x", expand=True)
            ttk.Label(box, text=label, font=("Segoe UI", 11, "bold"), background=cor).pack(anchor="w")
            ttk.Label(box, text=valor, font=("Segoe UI", 11), background=cor).pack(anchor="w")

        cor_prioridade = "#FFD966" if tarefa["prioridade"] == "Alta" else "#FFE699" if tarefa["prioridade"] == "Média" else "#FFF2CC"
        cor_estado = "#A9D08E"   # verde concluída
        if tarefa["estado"] == "Concluída":
            cor_estado = "#A9D08E"   # verde concluída
        elif tarefa["estado"] == "Quase a terminar":
            cor_estado = "#C6E0B4"
        elif tarefa["estado"] == "Em progresso":
            cor_estado = "#F4B084"
        else:
            cor_estado = "#BDD7EE"   # pendente ou outro estado



        criar_quadrado(linha_status, "Prioridade:", tarefa["prioridade"], cor_prioridade)
        criar_quadrado(linha_status, "Estado:", tarefa["estado"], cor_estado)

        prazo_box = tk.Frame(card, bg="#DDEBF7", padx=10, pady=10)
        prazo_box.pack(fill="x", pady=5)

        ttk.Label(prazo_box, text="Prazo:", font=("Segoe UI", 11, "bold"), background="#DDEBF7").pack(anchor="w")
        ttk.Label(prazo_box, text=tarefa["prazo"], font=("Segoe UI", 11), background="#DDEBF7").pack(anchor="w")

        btn_frame = tk.Frame(card, bg="#FFFFFF")
        btn_frame.pack(pady=15)

        # Se a tarefa está concluída → bloquear ações
        if tarefa["estado"].lower() == "concluída":
            ttk.Button(btn_frame, text="Editar", width=15, state="disabled").pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Apagar", width=15, state="disabled").pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Concluir", width=15, state="disabled").pack(side="left", padx=10)
        else:
            ttk.Button(btn_frame, text="Editar", width=15,
                command=lambda: (detalhes.destroy(), self.editar_tarefa(tarefa))).pack(side="left", padx=10)

            ttk.Button(btn_frame, text="Apagar", width=15,
                command=lambda: self.apagar_tarefa(tarefa["id"], detalhes)).pack(side="left", padx=10)

            ttk.Button(btn_frame, text="Concluir", width=15,
                command=lambda: self.concluir_tarefa(tarefa["id"], detalhes)).pack(side="left", padx=10)
                    
    
        ttk.Button(card, text="Voltar ao Menu", width=20,
                   command=lambda: (detalhes.destroy(), self.recarregar_lista())).pack(pady=10)



