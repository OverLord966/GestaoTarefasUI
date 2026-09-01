import mysql.connector

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # mete a tua password aqui
        database="gestor_tarefas"
    )

def renumerar_ids():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_tarefas"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tarefas ORDER BY id ASC")
    tarefas = cursor.fetchall()

    novo_id = 1
    for (id_antigo,) in tarefas:
        cursor.execute("UPDATE tarefas SET id = %s WHERE id = %s", (novo_id, id_antigo))
        novo_id += 1

    conn.commit()
    conn.close()