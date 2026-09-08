from DAL.database import obter_conexao
# -------------------------------------------------
# SINCRONIZAÇÃO JSON → MYSQL
# -------------------------------------------------

def sincronizar_json_para_mysql():

    conn = obter_conexao()

    if conn is None:
        return

    tarefas_json = carregar_json()

    if not tarefas_json:
        return

    print("BD online → a sincronizar JSON...")

    cursor = conn.cursor()

    for t in tarefas_json:

        status = t.get("sync_status")

        try:

            # -----------------------------
            # CRIAR (Sem passar o 'id' para o MySQL gerar AUTO_INCREMENT)
            # -----------------------------
            # -----------------------------
            # CRIAR (Força o ID gerado offline no MySQL)
            # -----------------------------
            # -----------------------------
            # CRIAR (Insere explicitamente com o ID vago calculado offline)
            # -----------------------------
            if status == "create":

                cursor.execute(
                    """
                    INSERT INTO tarefas
                    (id, titulo, descricao, prioridade, estado, prazo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        t["id"],
                        t["titulo"],
                        t["descricao"],
                        t["prioridade"],
                        t["estado"],
                        str(t["prazo"])
                    )
                )

            # -----------------------------
            # EDITAR
            # -----------------------------
            elif status == "update":

                cursor.execute(
                    """
                    UPDATE tarefas
                    SET titulo=%s,
                        descricao=%s,
                        prioridade=%s,
                        estado=%s,
                        prazo=%s
                    WHERE id=%s
                    """,
                    (
                        t["titulo"],
                        t["descricao"],
                        t["prioridade"],
                        t["estado"],
                        str(t["prazo"]),
                        t["id"]
                    )
                )

            # -----------------------------
            # APAGAR
            # -----------------------------
            elif status == "delete":

                cursor.execute(
                    "DELETE FROM tarefas WHERE id=%s",
                    (t["id"],)
                )

        except Exception as e:
            print(
                f"Erro ao sincronizar tarefa {t.get('id')}:",
                e
            )

    conn.commit()
    cursor.close()
    conn.close()

    print("Sincronização concluída!")