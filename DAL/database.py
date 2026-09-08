import mysql.connector
import json
import os

JSON_FALLBACK = "tarefas_offline.json"


def obter_conexao():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestor_tarefas"
        )

        if conn.is_connected():
            return conn

        return None

    except mysql.connector.Error as err:
        print(f"DEBUG - Erro de Conexão MySQL: {err}")
        return None
    
def carregar_json():
    if not os.path.exists(JSON_FALLBACK):
        return []

    try:
        with open(JSON_FALLBACK, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, OSError):
        return []


def guardar_json(tarefas):
    with open(JSON_FALLBACK, "w", encoding="utf-8") as f:
        json.dump(
            tarefas,
            f,
            indent=4,
            ensure_ascii=False
        )


def renumerar_ids():
    conn = obter_conexao()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tarefas ORDER BY id ASC")
    tarefas = cursor.fetchall()

    novo_id = 1

    for (id_antigo,) in tarefas:
        cursor.execute(
            "UPDATE tarefas SET id = %s WHERE id = %s",
            (novo_id, id_antigo)
        )
        novo_id += 1

    conn.commit()

    cursor.close()
    conn.close()