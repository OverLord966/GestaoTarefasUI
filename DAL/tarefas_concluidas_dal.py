import json
import os

CAMINHO = "Assets/tarefas_concluidas.json"

def guardar_tarefa_concluida(tarefa):
    # Criar ficheiro se não existir
    if not os.path.exists(CAMINHO):
        with open(CAMINHO, "w") as f:
            json.dump([], f)

    # Ler ficheiro
    with open(CAMINHO, "r") as f:
        dados = json.load(f)

    # Converter prazo para string
    prazo = tarefa["prazo"]
    if hasattr(prazo, "isoformat"):
        prazo = prazo.isoformat()

    # Guardar tudo
    dados.append({
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "prioridade": tarefa["prioridade"],
        "estado": tarefa["estado"],
        "prazo": prazo
    })

    # Escrever novamente
    with open(CAMINHO, "w") as f:
        json.dump(dados, f, indent=4)
