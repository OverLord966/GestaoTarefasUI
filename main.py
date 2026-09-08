from UI.janela_principal import JanelaPrincipal
from DAL.tarefas_dal import sincronizar_json_para_mysql
sincronizar_json_para_mysql()


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.update_idletasks()
    app.geometry("")
    app.mainloop()

