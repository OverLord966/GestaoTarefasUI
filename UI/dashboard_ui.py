import tkinter as tk
from tkinter import ttk
from DAL.tarefas_dal import listar_tarefas
from DAL.database import obter_conexao
from UI.listar_tarefas_ui import ListarTarefasUI
import datetime


class DashboardUI:
    def __init__(self, frame, voltar_menu_callback):
        modo_escuro = getattr(frame.master, "modo_escuro", False)
        frame.master.mostrar_botao_listar = True

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"

        for widget in frame.winfo_children():
            widget.destroy()

        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True, fill="both")

        ttk.Label(
            container,
            text="Dashboard",
            font=("Segoe UI", 24, "bold"),
            background=fundo,
            foreground=texto
        ).pack(pady=20)

        # Aviso modo offline
        if obter_conexao() is None:
            ttk.Label(
                container,
                text="⚠ Modo Offline — Base de dados indisponível (a usar JSON)",
                font=("Segoe UI", 11, "bold"),
                background=fundo,
                foreground="#FF8C00"
            ).pack(pady=5)

        tarefas = listar_tarefas()
        hoje = datetime.date.today()

        total = len(tarefas)
        concluidas = sum(1 for t in tarefas if "conclu" in t["estado"].lower() and "atras" not in t["estado"].lower())
        concluidas_atraso = sum(1 for t in tarefas if "conclu" in t["estado"].lower() and "atras" in t["estado"].lower())
        atrasadas = sum(
            1 for t in tarefas
            if (
                (t["prazo"] if isinstance(t["prazo"], datetime.date)
                 else datetime.datetime.strptime(t["prazo"], "%Y-%m-%d").date()) < hoje
            )
            and "conclu" not in t["estado"].lower()
        )
        alta_prioridade = sum(1 for t in tarefas if t["prioridade"].lower() == "alta")
        quase_terminar = sum(1 for t in tarefas if t["estado"].lower() == "quase a terminar")
        por_fazer = sum(1 for t in tarefas if t["estado"].lower() == "por fazer")

        def card(parent, titulo, valor, cor, comando):
            frame_card = tk.Frame(
                parent,
                bg=cor,
                padx=20,
                pady=20,
                highlightthickness=1,
                highlightbackground="#D0D0D0"
            )
            frame_card.pack(side="left", padx=15, pady=10, expand=True, fill="both")
            frame_card.bind("<Button-1>", lambda e: comando())

            lbl1 = ttk.Label(frame_card, text=titulo, font=("Segoe UI", 14, "bold"), background=cor)
            lbl1.pack(anchor="w")
            lbl1.bind("<Button-1>", lambda e: comando())

            lbl2 = ttk.Label(frame_card, text=str(valor), font=("Segoe UI", 26, "bold"), background=cor)
            lbl2.pack(anchor="center", pady=10)
            lbl2.bind("<Button-1>", lambda e: comando())

        linha1 = tk.Frame(container, bg=fundo)
        linha1.pack(fill="x", pady=10)

        card(linha1, "Total de Tarefas", total, card_cor,
             lambda: ListarTarefasUI(
                 frame, 
                 voltar_menu_callback, 
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback), 
                 mostrar_titulo=False
             ))

        card(linha1, "Concluídas", concluidas, "#2E7D32",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="concluidas",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        card(linha1, "Concluídas com Atraso", concluidas_atraso, "#FF8C00",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="concluidas_atraso",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        linha2 = tk.Frame(container, bg=fundo)
        linha2.pack(fill="x", pady=10)

        card(linha2, "Em Atraso", atrasadas, "#C62828",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="atraso",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        card(linha2, "Alta Prioridade", alta_prioridade, "#FFD966",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="alta",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        card(linha2, "Quase a Terminar", quase_terminar, "#C6E0B4",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="quase",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        card(linha2, "Por Fazer", por_fazer, "#BDD7EE",
             lambda: ListarTarefasUI(
                 frame,
                 voltar_menu_callback,
                 filtro="por_fazer",
                 voltar_dashboard_callback=lambda: DashboardUI(frame, voltar_menu_callback),
                 mostrar_titulo=False
             ))

        tk.Button(
            container,
            text="Voltar ao Menu",
            command=voltar_menu_callback,
            font=("Segoe UI", 11, "bold"),
            bg="#6C757D",
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            width=18
        ).pack(pady=20)
