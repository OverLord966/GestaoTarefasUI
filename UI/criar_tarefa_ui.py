import tkinter as tk
from tkinter import ttk
from datetime import date

# Importações dos módulos internos do projeto (Data Access Layer e UI)
from DAL.database import renumerar_ids
from UI.calendario_moderno import CalendarioModerno
from DAL.tarefas_dal import criar_tarefa_dal, listar_tarefas


class CriarTarefaUI:
    
    def mostrar_erro(self, card, mensagem):
        """
        Exibe uma mensagem de erro temporária no ecram (dura 3 segundos).
        :param card: Onde o label de erro será desenhado.
        :param mensagem: O texto de erro a exibir.
        """
        erro = tk.Label(
            card,
            text=mensagem,
            fg="#B00020",         # Cor vermelha para indicar erro
            bg=card["bg"],        # Usa a mesma cor de fundo do card para integração visual
            font=("Segoe UI", 11)
        )
        erro.pack(pady=5)
        # Remove a mensagem de erro automaticamente após 3000ms (3 segundos)
        erro.after(3000, erro.destroy)

    def __init__(self, frame, voltar_menu_callback):
        """
        Construtor da interface de criação de tarefas.
        :param frame: Frame principal da janela onde a UI será construída.
        :param voltar_menu_callback: Função para navegar de volta ao menu principal.
        """
        
        # Clean up: Remove todos os componentes antigos existentes no frame antes de desenhar a nova UI
        for widget in frame.winfo_children():
            widget.destroy()

        self.frame = frame

        # -----------------------------
        # TEMA (Light / Dark)
        # -----------------------------
        # Verifica se o container pai tem a propriedade 'modo_escuro' ativa (padrão: False)
        modo_escuro = getattr(frame.master, "modo_escuro", False)

        # Definição das paletas de cores dinâmicas baseadas no tema selecionado
        if modo_escuro:
            fundo = "#1E1E1E"       # Fundo escuro para a janela
            card_cor = "#2A2A2A"    # Fundo do card central
            texto = "#FFFFFF"       # Cor do texto em branco
            cor_botao = "#0A3A66"   # Azul escuro para o botão principal
            cor_hover = "#06294A"   # Azul mais escuro para efeito hover
            entrada_bg = "#3A3A3A"  # Fundo dos campos de texto/inputs
            entrada_fg = "#FFFFFF"  # Cor do texto dos inputs
        else:
            fundo = "#F3F3F3"       # Fundo claro
            card_cor = "#FFFFFF"    # Card em branco
            texto = "#1A1A1A"       # Texto em cinza escuro
            cor_botao = "#0A66C2"   # Azul vibrante para o botão
            cor_hover = "#084C8A"   # Azul ligeiramente escuro para hover
            entrada_bg = "#FFFFFF"  # Fundo dos inputs
            entrada_fg = "#1A1A1A"  # Cor do texto dos inputs

        # -----------------------------
        # CONTAINER PRINCIPAL
        # -----------------------------
        # Frame de fundo que ocupa a janela e centraliza o formulário
        container = tk.Frame(frame, bg=fundo)
        container.pack(expand=True)

        # -----------------------------
        # CARD (Cartão Centralizado)
        # -----------------------------
        # Bloco visual central contendo todos os elementos do formulário
        card = tk.Frame(
            container,
            bg=card_cor,
            padx=40, pady=40,            # Margem interna (padding)
            highlightthickness=1,        # Espessura da borda
            highlightbackground="#D0D0D0" # Cor da borda
        )
        card.pack(pady=20)

        # Título principal do formulário
        ttk.Label(
            card,
            text="Criar Nova Tarefa",
            font=("Segoe UI", 22, "bold"),
            foreground=texto,
            background=card_cor
        ).pack(pady=10)

        # -----------------------------
        # CAMPO: TÍTULO
        # -----------------------------
        ttk.Label(card, text="Título:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        # Caixas de texto simples (linha única) para inserir o título
        titulo_entry = tk.Entry(card, width=45, bg=entrada_bg, fg=entrada_fg,
                                relief="solid", bd=1, font=("Segoe UI", 11))
        titulo_entry.pack(pady=5, anchor="w")

        # -----------------------------
        # CAMPO: DESCRIÇÃO
        # -----------------------------
        ttk.Label(card, text="Descrição:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        # Frame secundário para alinhar a caixa de texto multilinha e a scrollbar
        descricao_frame = tk.Frame(card, bg=card_cor)
        descricao_frame.pack(fill="x", pady=5)

        # Campo multilinhas (tk.Text) para a descrição da tarefa
        descricao_text = tk.Text(
            descricao_frame,
            height=6,
            width=45,
            font=("Segoe UI", 11),
            wrap="word",                # Quebra de linha por palavras inteiras
            bd=1,
            relief="solid",
            highlightthickness=0,
            bg=entrada_bg,
            fg=entrada_fg
        )
        descricao_text.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical associada ao campo de descrição
        scroll = ttk.Scrollbar(descricao_frame, orient="vertical", command=descricao_text.yview)
        scroll.pack(side="right", fill="y")
        descricao_text.configure(yscrollcommand=scroll.set)

        # -----------------------------
        # CAMPO: PRIORIDADE
        # -----------------------------
        ttk.Label(card, text="Prioridade:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        # Menu de seleção estilo "Dropdown" / ComboBox
        prioridade_var = tk.StringVar()
        prioridade_combo = ttk.Combobox(
            card,
            textvariable=prioridade_var,
            values=["Alta", "Média", "Baixa"],
            state="readonly", # Impede que o utilizador escreva opções personalizadas
            width=20
        )
        prioridade_combo.set("Média") # Valor por defeito
        prioridade_combo.pack(pady=5, anchor="w")

        # -----------------------------
        # CAMPO: ESTADO
        # -----------------------------
        ttk.Label(card, text="Estado:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        # Dropdown para estado da tarefa
        estado_var = tk.StringVar()
        estado_combo = ttk.Combobox(
            card,
            textvariable=estado_var,
            values=["Por fazer", "Em progresso"],
            state="readonly",
            width=20
        )
        estado_combo.set("Por fazer") # Valor por defeito
        estado_combo.pack(pady=5, anchor="w")

        # -----------------------------
        # CAMPO: PRAZO (Calendário)
        # -----------------------------
        ttk.Label(card, text="Prazo:", anchor="w", font=("Segoe UI", 11),
                  foreground=texto, background=card_cor).pack(fill="x")

        # Define a data por defeito para o dia de hoje no formato AAAA-MM-DD
        prazo_var = tk.StringVar()
        prazo_var.set(date.today().strftime("%Y-%m-%d"))

        def abrir_calendario():
            """Abre o pop-up do calendário e atualiza a variável com a data escolhida."""
            CalendarioModerno(self.frame, lambda data: prazo_var.set(data.strftime("%Y-%m-%d")))

        # Botão interativo que mostra a data selecionada e abre o calendário quando clicado
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
        # GERADOR DE BOTÕES
        # -----------------------------
        def criar_botao(parent, texto_btn, comando, cor=cor_botao, hover=cor_hover):
            """Função auxiliar para criar botões com estilo padronizado."""
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

        # -----------------------------
        # LÓGICA DE VALIDAÇÃO E SUBMISSÃO
        # -----------------------------
        def submeter():
            """Obtém os dados do formulário, valida os campos e guarda no banco de dados."""
            
            # .strip() remove espaços vazios acidentais no início e fim das strings
            titulo = titulo_entry.get().strip()
            descricao = descricao_text.get("1.0", "end").strip() # Lê da linha 1 até ao fim do Text
            prioridade = prioridade_combo.get().strip()
            estado = estado_combo.get().strip()
            prazo = prazo_var.get().strip()

            # Validações de obrigatoriedade dos campos
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

            # Se todos os dados passarem na validação:
            # 1. Guarda a tarefa na base de dados através da camada DAL
            criar_tarefa_dal(titulo, descricao, prioridade, estado, prazo)
            # 2. Mantém a ordenação limpa dos IDs
            renumerar_ids()
            # 3. Executa a função callback para retornar à listagem/menu
            voltar_menu_callback()

        # Instanciação dos botões da interface
        criar_botao(card, "Criar", submeter)
        criar_botao(card, "Voltar ao Menu", voltar_menu_callback, cor="#6C757D", hover="#5A6268")