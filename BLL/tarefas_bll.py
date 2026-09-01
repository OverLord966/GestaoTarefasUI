from DAL.tarefas_dal import criar_tarefa, listar_tarefas
from datetime import datetime, date
from DAL.tarefas_dal import apagar_tarefa as apagar_tarefa_dal
from DAL.tarefas_dal import editar_tarefa as editar_tarefa_dal
def adicionar_tarefa(titulo, descricao, prioridade, estado, prazo):
    # Validar título
    if not titulo.strip():
        return False, "O título não pode estar vazio."

    # Validar descrição
    if not descricao.strip():
        return False, "A descrição não pode estar vazia."

    # Validar prioridade
    prioridades_validas = ["Baixa", "Média", "Alta"]
    if prioridade not in prioridades_validas:
        return False, "A prioridade é inválida."

    # Validar estado
    estados_validos = ["Pendente", "Em Progresso", "Concluída"]
    if estado not in estados_validos:
        return False, "O estado é inválido."

    # Validar data (formato + não ser anterior a hoje)
    try:
        prazo_dt = datetime.strptime(prazo, "%Y-%m-%d").date()
    except ValueError:
        return False, "A data é inválida."

    if prazo_dt < date.today():
        return False, "A data não pode ser anterior à data de hoje."

    # Se tudo estiver OK → criar tarefa
    criar_tarefa(titulo, descricao, prioridade, estado, prazo)
    return True, "Tarefa criada com sucesso!"

def obter_tarefas():
    return listar_tarefas()
def editar_tarefa(id, titulo, descricao, prioridade, estado, prazo):
    editar_tarefa_dal(id, titulo, descricao, prioridade, estado, prazo)

def apagar_tarefa(id):
    apagar_tarefa_dal(id)