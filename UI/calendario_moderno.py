import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta


class CalendarioModerno:

    def __init__(self, parent, callback_data):
        """
        Construtor da janela pop-up do calendário.
        :param parent: Widget/Frame pai que invocou o calendário.
        :param callback_data: Função de retorno que receberá a data selecionada pelo utilizador.
        """
        self.parent = parent
        self.callback_data = callback_data

        # -----------------------------
        # DETEÇÃO DO TEMA (Light / Dark)
        # -----------------------------
        # Verifica se o elemento pai (master) define o atributo 'modo_escuro' (padrão: False)
        modo_escuro = getattr(parent.master, "modo_escuro", False)

        # Definição das variáveis de cores para o estilo do calendário
        if modo_escuro:
            fundo = "#1E1E1E"        # Fundo da janela secundária
            card_cor = "#2A2A2A"     # Fundo do cartão/container
            texto = "#FFFFFF"        # Cor do texto em geral
            dia_bg = "#3A3A3A"       # Fundo dos botões dos dias comuns
            dia_fg = "#FFFFFF"       # Cor do texto dos dias comuns
            dia_hover = "#444444"    # Cor ao passar o rato (hover) num dia
            hoje_bg = "#0A66C2"      # Fundo de destaque para o dia atual (Hoje)
            hoje_fg = "#FFFFFF"      # Texto do dia atual
        else:
            fundo = "#F3F3F3"        # Fundo claro da janela
            card_cor = "#FFFFFF"     # Fundo branco para o container
            texto = "#1A1A1A"        # Cor do texto principal
            dia_bg = "#FFFFFF"       # Fundo dos dias normais
            dia_fg = "#000000"       # Cor do número do dia
            dia_hover = "#E6F0FF"    # Cor ao passar o rato (azul claro)
            hoje_bg = "#0A66C2"      # Fundo de destaque para o dia atual
            hoje_fg = "#FFFFFF"      # Texto do dia atual

        # -----------------------------
        # JANELA SECUNDÁRIA (Toplevel)
        # -----------------------------
        # Cria uma nova janela flutuante em cima da aplicação principal
        self.janela = tk.Toplevel(parent)
        self.janela.title("Selecionar data")
        self.janela.configure(bg=fundo)
        self.janela.resizable(False, False)  # Impede o redimensionamento da janela

        # Guarda o mês e ano atualmente visíveis no calendário (inicia na data de hoje)
        self.data_atual = date.today()
        self.mes_atual = self.data_atual.month
        self.ano_atual = self.data_atual.year

        # -----------------------------
        # CONTAINER PRINCIPAL (Card)
        # -----------------------------
        card = tk.Frame(
            self.janela,
            bg=card_cor,
            padx=20,
            pady=20,
            highlightthickness=1,
            highlightbackground="#D0D0D0" # Borda do cartão
        )
        card.pack(padx=20, pady=20)

        # -----------------------------
        # CABEÇALHO (Mês/Ano e Navegação)
        # -----------------------------
        topo = tk.Frame(card, bg=card_cor)
        topo.pack(fill="x")

        # Label que apresenta o Mês e Ano atual (ex: "September 2026")
        self.lbl_mes_ano = tk.Label(
            topo,
            text=self.data_atual.strftime("%B %Y"),
            font=("Segoe UI", 12, "bold"),
            bg=card_cor,
            fg=texto
        )
        self.lbl_mes_ano.pack(side="left")

        # Botão para voltar ao mês anterior
        btn_prev = tk.Button(
            topo,
            text="<",
            command=self.mes_anterior,
            bg=card_cor,
            fg=texto,
            relief="flat"
        )
        btn_prev.pack(side="right", padx=5)

        # Botão para avançar para o próximo mês
        btn_next = tk.Button(
            topo,
            text=">",
            command=self.proximo_mes,
            bg=card_cor,
            fg=texto,
            relief="flat"
        )
        btn_next.pack(side="right", padx=5)

        # -----------------------------
        # GRELHA DOS DIAS (Grid Frame)
        # -----------------------------
        self.grid_frame = tk.Frame(card, bg=card_cor)
        self.grid_frame.pack(pady=10)

        # Cabeçalho dos dias da semana
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for i, d in enumerate(dias_semana):
            tk.Label(
                self.grid_frame,
                text=d,
                font=("Segoe UI", 10, "bold"),
                bg=card_cor,
                fg=texto
            ).grid(row=0, column=i, padx=5, pady=5)

        # Guarda as propriedades visuais na instância para acesso pelos métodos de renderização
        self.dia_bg = dia_bg
        self.dia_fg = dia_fg
        self.dia_hover = dia_hover
        self.hoje_bg = hoje_bg
        self.hoje_fg = hoje_fg
        self.card_cor = card_cor
        self.texto = texto

        # Desenha a grelha de dias do mês atual
        self._criar_calendario()

    def _criar_calendario(self):
        """Gera e posiciona dinamicamente os botões de cada dia na grelha."""
        
        # Limpa todos os botões de dias anteriores mantendo apenas o cabeçalho (row 0)
        for widget in self.grid_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Calcula o primeiro dia do mês visível
        primeiro_dia = date(self.ano_atual, self.mes_atual, 1)
        
        # Determina a coluna onde o 1º dia do mês deve ser desenhado (0=Segunda, ..., 6=Domingo)
        dia_semana = (primeiro_dia.weekday() + 1) % 7

        # Calcula a quantidade de dias no mês atual
        if self.mes_atual != 12:
            # Subtrai 1 dia ao dia 1 do mês seguinte para encontrar o último dia do mês atual
            dias_no_mes = (date(self.ano_atual, self.mes_atual + 1, 1) - timedelta(days=1)).day
        else:
            dias_no_mes = 31

        linha = 1
        coluna = dia_semana

        # Cria um botão para cada dia do mês
        for dia in range(1, dias_no_mes + 1):
            data_atual = date(self.ano_atual, self.mes_atual, dia)

            # Aplica destaque visual caso o dia corresponda ao dia de Hoje
            if data_atual == date.today():
                bg = self.hoje_bg
                fg = self.hoje_fg
            else:
                bg = self.dia_bg
                fg = self.dia_fg

            # Instancia o botão com o número do dia
            btn = tk.Button(
                self.grid_frame,
                text=str(dia),
                width=4,
                bg=bg,
                fg=fg,
                relief="flat",
                # Passa a data selecionada como argumento padrão no lambda para evitar a contaminação da variável do ciclo
                command=lambda d=data_atual: self._selecionar_data(d)
            )
            btn.grid(row=linha, column=coluna, padx=3, pady=3)

            # --- Eventos de Hover (Efeito ao passar o cursor) ---
            def on_enter(e, b=btn):
                # Altera a cor ao passar com o rato se não for o dia de "Hoje"
                if b["bg"] != self.hoje_bg:
                    b.configure(bg=self.dia_hover)

            def on_leave(e, b=btn, original_bg=bg):
                # Restaura a cor original ao retirar o rato do botão
                if b["bg"] != self.hoje_bg:
                    b.configure(bg=original_bg)

            # Atribui os eventos ao botão
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            # Avança a coluna e salta de linha ao chegar ao fim do Domingo (coluna 6)
            coluna += 1
            if coluna > 6:
                coluna = 0
                linha += 1

    def mes_anterior(self):
        """Navega para o mês anterior e redesenha a interface."""
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self._atualizar_mes_ano()
        self._criar_calendario()

    def proximo_mes(self):
        """Navega para o próximo mês e redesenha a interface."""
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self._atualizar_mes_ano()
        self._criar_calendario()

    def _atualizar_mes_ano(self):
        """Atualiza a mensagem de texto do cabeçalho com o mês e ano atualizados."""
        self.lbl_mes_ano.config(text=date(self.ano_atual, self.mes_atual, 1).strftime("%B %Y"))

    def _selecionar_data(self, data):
        """Executa a função de callback enviando a data escolhida e fecha a janela pop-up."""
        self.callback_data(data)
        self.janela.destroy()