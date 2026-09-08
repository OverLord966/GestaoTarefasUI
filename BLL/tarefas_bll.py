from DAL.tarefas_dal import (
    criar_tarefa_dal,
    listar_tarefas,
    obter_tarefa_por_id,
    atualizar_estado_tarefa,
    editar_tarefa_dal,
    apagar_tarefa_dal
)

from datetime import datetime, date


# -------------------------------------------------
# ADICIONAR
# -------------------------------------------------

def adicionar_tarefa(
    titulo,
    descricao,
    prioridade,
    estado,
    prazo
):

    if not titulo.strip():
        return False, "O título não pode estar vazio."

    if not descricao.strip():
        return False, "A descrição não pode estar vazia."

    prioridades_validas = [
        "Baixa",
        "Média",
        "Alta"
    ]

    if prioridade not in prioridades_validas:
        return False, "A prioridade é inválida."

    estados_validos = [
        "Pendente",
        "Em Progresso",
        "Concluída"
    ]

    if estado not in estados_validos:
        return False, "O estado é inválido."

    try:

        prazo_dt = datetime.strptime(
            prazo,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return False, "A data é inválida."

    if prazo_dt < date.today():

        return False, (
            "A data não pode ser anterior "
            "à data de hoje."
        )

    criar_tarefa_dal(
        titulo,
        descricao,
        prioridade,
        estado,
        prazo
    )

    return True, "Tarefa criada com sucesso!"


# -------------------------------------------------
# LISTAR
# -------------------------------------------------

def obter_tarefas():

    return listar_tarefas()


# -------------------------------------------------
# EDITAR
# -------------------------------------------------

def editar_tarefa(
    id,
    titulo,
    descricao,
    prioridade,
    estado,
    prazo
):

    tarefa = {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "estado": estado,
        "prazo": prazo
    }

    editar_tarefa_dal(tarefa)


# -------------------------------------------------
# APAGAR
# -------------------------------------------------

def apagar_tarefa(id):

    apagar_tarefa_dal(id)


# -------------------------------------------------
# CONCLUIR
# -------------------------------------------------

def concluir_tarefa_bll(id_tarefa):

    tarefa = obter_tarefa_por_id(id_tarefa)

    if not tarefa:
        return

    hoje = date.today()

    prazo = tarefa["prazo"]

    if isinstance(prazo, str):

        prazo = datetime.strptime(
            prazo,
            "%Y-%m-%d"
        ).date()

    if prazo < hoje:

        novo_estado = "Concluída com atraso"

    else:

        novo_estado = "Concluída"

    atualizar_estado_tarefa(
        id_tarefa,
        novo_estado
    )