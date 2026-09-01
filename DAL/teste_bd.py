from database import obter_conexao

conn = obter_conexao()
print("Ligação OK!")
conn.close()
