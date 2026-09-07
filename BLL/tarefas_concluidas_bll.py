import datetime
from DAL.tarefas_dal import obter_tarefa_por_id_dal, atualizar_estado_tarefa_dal
from DAL.tarefas_concluidas_dal import guardar_tarefa_concluida

def concluir_tarefa_bll(id_tarefa):
    tarefa = obter_tarefa_por_id_dal(id_tarefa)

    hoje = datetime.date.today()
    prazo = tarefa["prazo"]

    # Verificar atraso
    if prazo < hoje:
        novo_estado = "Concluída com atraso"
    else:
        novo_estado = "Concluída"

    # Atualizar na base de dados
    atualizar_estado_tarefa_dal(id_tarefa, novo_estado)

    # Atualizar objeto para guardar no JSON
    tarefa["estado"] = novo_estado

    # Guardar no histórico JSON
    guardar_tarefa_concluida(tarefa)
