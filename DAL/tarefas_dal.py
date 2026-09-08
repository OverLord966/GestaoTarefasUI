from DAL.database import obter_conexao, carregar_json, guardar_json
from datetime import datetime, date


# -------------------------------------------------
# LISTAR TAREFAS
# -------------------------------------------------

def listar_tarefas():

    conn = obter_conexao()

    # -----------------------------
    # BD ONLINE
    # -----------------------------
    if conn is not None:

        try:
            # 1. Sincronizar qualquer alteração/criação feita offline
            sincronizar_json_para_mysql()

            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM tarefas ORDER BY id"
            )

            tarefas = cursor.fetchall()

            cursor.close()
            conn.close()

            # Converter campos de data/hora para string simples (JSON serializable)
            for t in tarefas:
                for chave, valor in t.items():
                    if isinstance(valor, (date, datetime)):
                        t[chave] = valor.strftime('%Y-%m-%d')

            # Atualizar a cópia local do JSON com a verdade absoluta do MySQL
            guardar_json(tarefas)

            return tarefas

        except Exception as e:
            print("Erro ao consultar BD:", e)

            try:
                conn.close()
            except:
                pass

    # -----------------------------
    # BD OFFLINE → JSON
    # -----------------------------

    print("BD offline → a utilizar JSON")

    # Retorna todas as tarefas excepto as marcadas para apagar enquanto offline
    tarefas = carregar_json()
    return [t for t in tarefas if t.get("sync_status") != "delete"]


# -------------------------------------------------
# OBTER TAREFA POR ID
# -------------------------------------------------

def obter_tarefa_por_id(id_tarefa):

    conn = obter_conexao()

    if conn is not None:

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM tarefas WHERE id = %s",
                (id_tarefa,)
            )

            tarefa = cursor.fetchone()

            cursor.close()
            conn.close()

            if tarefa:
                for chave, valor in tarefa.items():
                    if isinstance(valor, (date, datetime)):
                        tarefa[chave] = valor.strftime('%Y-%m-%d')

            return tarefa

        except Exception:
            try:
                conn.close()
            except:
                pass

    # JSON (Offline)
    tarefas = carregar_json()

    for t in tarefas:
        if t["id"] == id_tarefa:
            return t

    return None


# -------------------------------------------------
# CRIAR TAREFA
# -------------------------------------------------

def criar_tarefa_dal(
    titulo,
    descricao,
    prioridade,
    estado,
    prazo
):

    conn = obter_conexao()

    # Tratar data para formato string
    prazo_str = prazo.strftime('%Y-%m-%d') if isinstance(prazo, (date, datetime)) else str(prazo)

    # -----------------------------
    # OFFLINE (Sem conexão)
    # -----------------------------
    if conn is None:
        tarefas = carregar_json()

        # Guarda todos os IDs atualmente em uso no JSON
        ids_existentes = {t["id"] for t in tarefas if "id" in t}

        # Procura o primeiro ID livre a começar do 1
        novo_id = 1
        while novo_id in ids_existentes:
            novo_id += 1

        nova_tarefa = {
            "id": novo_id,
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "estado": estado,
            "prazo": prazo_str,
            "sync_status": "create"
        }

        tarefas.append(nova_tarefa)
        guardar_json(tarefas)

        print(f"Tarefa criada no JSON (offline) com o ID livre: {novo_id}")
        return

    # -----------------------------
    # ONLINE (Com conexão à BD)
    # -----------------------------
    try:
        cursor = conn.cursor()

        # 1. Procurar os IDs ocupados no MySQL
        cursor.execute("SELECT id FROM tarefas")
        ids_usados = {row[0] for row in cursor.fetchall()}

        # 2. Encontrar o menor ID livre
        proximo_id = 1
        while proximo_id in ids_usados:
            proximo_id += 1

        # 3. Inserir na BD com o ID vago calculado
        cursor.execute(
            """
            INSERT INTO tarefas
            (id, titulo, descricao, prioridade, estado, prazo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                proximo_id,
                titulo,
                descricao,
                prioridade,
                estado,
                prazo_str
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Tarefa criada na BD com sucesso com o ID: {proximo_id}")

    except Exception as e:
        print("Erro ao criar na BD, a guardar offline:", e)

        try:
            conn.close()
        except:
            pass

        # Se falhou durante a execução, guarda offline
        conn = None
        criar_tarefa_offline(titulo, descricao, prioridade, estado, prazo)


def criar_tarefa_offline(titulo, descricao, prioridade, estado, prazo_str):

    tarefas = carregar_json()

    # Extrai todos os IDs atualmente em uso no JSON
    ids_existentes = {t["id"] for t in tarefas if "id" in t}

    # Procura o primeiro ID disponível a começar em 1
    novo_id = 1
    while novo_id in ids_existentes:
        novo_id += 1

    nova_tarefa = {
        "id": novo_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "estado": estado,
        "prazo": prazo_str,
        "sync_status": "create"
    }

    tarefas.append(nova_tarefa)
    guardar_json(tarefas)

    print(f"Tarefa criada no JSON (offline")


# -------------------------------------------------
# ATUALIZAR ESTADO
# -------------------------------------------------

def atualizar_estado_tarefa(id_tarefa, novo_estado):

    conn = obter_conexao()

    # OFFLINE
    if conn is None:

        tarefas = carregar_json()

        for t in tarefas:
            if t["id"] == id_tarefa:
                t["estado"] = novo_estado
                if t.get("sync_status") != "create":
                    t["sync_status"] = "update"
                break

        guardar_json(tarefas)
        print("Estado atualizado no JSON (offline)")
        return

    # ONLINE
    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE tarefas
            SET estado = %s
            WHERE id = %s
            """,
            (
                novo_estado,
                id_tarefa
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        print("Erro ao atualizar BD:", e)

        try:
            conn.close()
        except:
            pass


# -------------------------------------------------
# EDITAR TAREFA
# -------------------------------------------------

def editar_tarefa_dal(tarefa):

    conn = obter_conexao()

    # Tratar data
    if isinstance(tarefa.get("prazo"), (date, datetime)):
        tarefa["prazo"] = tarefa["prazo"].strftime('%Y-%m-%d')

    # OFFLINE
    if conn is None:

        tarefas = carregar_json()

        for t in tarefas:
            if t["id"] == tarefa["id"]:
                t.update(tarefa)
                if t.get("sync_status") != "create":
                    t["sync_status"] = "update"
                break

        guardar_json(tarefas)
        print("Tarefa editada no JSON (offline)")
        return

    # ONLINE
    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE tarefas
            SET titulo = %s,
                descricao = %s,
                prioridade = %s,
                estado = %s,
                prazo = %s
            WHERE id = %s
            """,
            (
                tarefa["titulo"],
                tarefa["descricao"],
                tarefa["prioridade"],
                tarefa["estado"],
                str(tarefa["prazo"]),
                tarefa["id"]
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        print("Erro ao editar BD:", e)

        try:
            conn.close()
        except:
            pass


# -------------------------------------------------
# APAGAR TAREFA
# -------------------------------------------------

def apagar_tarefa_dal(id_tarefa):

    conn = obter_conexao()

    # OFFLINE
    if conn is None:

        tarefas = carregar_json()
        nova_lista = []

        for t in tarefas:
            if t["id"] == id_tarefa:
                # Se foi criada offline e ainda não foi para a BD, basta removê-la
                if t.get("sync_status") == "create":
                    continue

                # Caso contrário, marca para apagar na BD
                t["sync_status"] = "delete"

            nova_lista.append(t)

        guardar_json(nova_lista)
        print("Tarefa marcada para apagar offline")
        return

    # ONLINE
    try:

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tarefas WHERE id = %s",
            (id_tarefa,)
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        print("Erro ao apagar da BD:", e)

        try:
            conn.close()
        except:
            pass


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

    # Filtrar apenas as tarefas que têm pendências de sincronização
    tarefas_pendentes = [t for t in tarefas_json if t.get("sync_status") in ("create", "update", "delete")]

    if not tarefas_pendentes:
        return

    print("BD online → a sincronizar alterações pendentes do JSON...")

    cursor = conn.cursor()

    for t in tarefas_json:

        status = t.get("sync_status")

        if not status:
            continue

        try:

            # -----------------------------
            # CRIAR
            # -----------------------------
            if status == "create":

                cursor.execute(
                    """
                    INSERT INTO tarefas
                    (titulo, descricao, prioridade, estado, prazo)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
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
            print(f"Erro ao sincronizar tarefa {t.get('id')}:", e)

    conn.commit()

    cursor.close()
    conn.close()

    print("Sincronização concluída com sucesso!")