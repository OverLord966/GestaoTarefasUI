import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta

class CalendarioModerno:

    def __init__(self, parent, callback_data):
        self.parent = parent
        self.callback_data = callback_data

        modo_escuro = getattr(parent.master, "modo_escuro", False)

        if modo_escuro:
            fundo = "#1E1E1E"
            card_cor = "#2A2A2A"
            texto = "#FFFFFF"
            dia_bg = "#3A3A3A"
            dia_fg = "#FFFFFF"
            dia_hover = "#444444"
            hoje_bg = "#0A66C2"
            hoje_fg = "#FFFFFF"
        else:
            fundo = "#F3F3F3"
            card_cor = "#FFFFFF"
            texto = "#1A1A1A"
            dia_bg = "#FFFFFF"
            dia_fg = "#000000"
            dia_hover = "#E6F0FF"
            hoje_bg = "#0A66C2"
            hoje_fg = "#FFFFFF"

        self.janela = tk.Toplevel(parent)
        self.janela.title("Selecionar data")
        self.janela.configure(bg=fundo)
        self.janela.resizable(False, False)

        self.data_atual = date.today()
        self.mes_atual = self.data_atual.month
        self.ano_atual = self.data_atual.year

        card = tk.Frame(
            self.janela,
            bg=card_cor,
            padx=20,
            pady=20,
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )
        card.pack(padx=20, pady=20)

        topo = tk.Frame(card, bg=card_cor)
        topo.pack(fill="x")

        self.lbl_mes_ano = tk.Label(
            topo,
            text=self.data_atual.strftime("%B %Y"),
            font=("Segoe UI", 12, "bold"),
            bg=card_cor,
            fg=texto
        )
        self.lbl_mes_ano.pack(side="left")

        btn_prev = tk.Button(
            topo,
            text="<",
            command=self.mes_anterior,
            bg=card_cor,
            fg=texto,
            relief="flat"
        )
        btn_prev.pack(side="right", padx=5)

        btn_next = tk.Button(
            topo,
            text=">",
            command=self.proximo_mes,
            bg=card_cor,
            fg=texto,
            relief="flat"
        )
        btn_next.pack(side="right", padx=5)

        self.grid_frame = tk.Frame(card, bg=card_cor)
        self.grid_frame.pack(pady=10)

        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for i, d in enumerate(dias_semana):
            tk.Label(
                self.grid_frame,
                text=d,
                font=("Segoe UI", 10, "bold"),
                bg=card_cor,
                fg=texto
            ).grid(row=0, column=i, padx=5, pady=5)

        self.dia_bg = dia_bg
        self.dia_fg = dia_fg
        self.dia_hover = dia_hover
        self.hoje_bg = hoje_bg
        self.hoje_fg = hoje_fg
        self.card_cor = card_cor
        self.texto = texto

        self._criar_calendario()

    def _criar_calendario(self):
        for widget in self.grid_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        primeiro_dia = date(self.ano_atual, self.mes_atual, 1)
        dia_semana = (primeiro_dia.weekday() + 1) % 7
        dias_no_mes = (date(self.ano_atual, self.mes_atual + 1, 1) - timedelta(days=1)).day if self.mes_atual != 12 else 31

        linha = 1
        coluna = dia_semana

        for dia in range(1, dias_no_mes + 1):
            data_atual = date(self.ano_atual, self.mes_atual, dia)

            if data_atual == date.today():
                bg = self.hoje_bg
                fg = self.hoje_fg
            else:
                bg = self.dia_bg
                fg = self.dia_fg

            btn = tk.Button(
                self.grid_frame,
                text=str(dia),
                width=4,
                bg=bg,
                fg=fg,
                relief="flat",
                command=lambda d=data_atual: self._selecionar_data(d)
            )
            btn.grid(row=linha, column=coluna, padx=3, pady=3)

            def on_enter(e, b=btn):
                if b["bg"] != self.hoje_bg:
                    b.configure(bg=self.dia_hover)

            def on_leave(e, b=btn, original_bg=bg):
                if b["bg"] != self.hoje_bg:
                    b.configure(bg=original_bg)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            coluna += 1
            if coluna > 6:
                coluna = 0
                linha += 1

    def mes_anterior(self):
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self._atualizar_mes_ano()
        self._criar_calendario()

    def proximo_mes(self):
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self._atualizar_mes_ano()
        self._criar_calendario()

    def _atualizar_mes_ano(self):
        self.lbl_mes_ano.config(text=date(self.ano_atual, self.mes_atual, 1).strftime("%B %Y"))

    def _selecionar_data(self, data):
        self.callback_data(data)
        self.janela.destroy()
