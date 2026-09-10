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
            # CRIAR
            # -----------------------------
            if status == "create":

                # Garante que enviado o ID de utilizador existente (ex: 1)
                criado_por_id = t.get("criado_por")
                if not criado_por_id:
                    criado_por_id = 1

                cursor.execute(
                    """
                    INSERT INTO tarefas
                    (id, titulo, descricao, prioridade, estado, prazo, criado_por)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        t["id"],
                        t["titulo"],
                        t["descricao"],
                        t["prioridade"],
                        t["estado"],
                        str(t["prazo"]),
                        criado_por_id  # <--- ADICIONADO AQUI
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

    # Opcional: Limpar o ficheiro JSON após sincronizar para não tentar reenviar
    salvar_json([])

    print("Sincronização concluída com sucesso!")