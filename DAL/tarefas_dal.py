from DAL.database import obter_conexao
import mysql.connector

def criar_tarefa(titulo, descricao, prioridade, estado, prazo):
    conn = obter_conexao()
    cursor = conn.cursor()
    sql = """
        INSERT INTO tarefas (titulo, descricao, prioridade, estado, prazo)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (titulo, descricao, prioridade, estado, prazo))
    conn.commit()
    conn.close()

def listar_tarefas():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tarefas ORDER BY id ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados
def editar_tarefa(id, titulo, descricao, prioridade, estado, prazo):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_tarefas"
    )
    cursor = conn.cursor()

    sql = """
        UPDATE tarefas
        SET titulo = %s,
            descricao = %s,
            prioridade = %s,
            estado = %s,
            prazo = %s
        WHERE id = %s
    """

    cursor.execute(sql, (titulo, descricao, prioridade, estado, prazo, id))
    conn.commit()
    conn.close()
def apagar_tarefa(tarefa_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_tarefas"
    )
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
    conn.commit()
    conn.close()