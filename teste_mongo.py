



import sys
import datetime
from pymongo import MongoClient
import certifi

# O SEU LINK DE CONEXÃO
uri = "mongodb+srv://olnairgonzagapereira6_db_user:NXPX4dKglEq0MBqA@cluster0.d6lswau.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("Conectando ao MongoDB Atlas (Modo Termux)...")

try:
    # O segredo está em usar o tlsCAFile e forçar o cliente a não depender do sistema
    client = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        connectTimeoutMS=30000,
        socketTimeoutMS=None,
        connect=True
    )
    
    db = client.olnair_monitor
    colecao = db.logs

    # Criando os dados
    dados = {
        "projeto": "Olnair Monitor",
        "status": "Online",
        "mensagem": "Conexão estabelecida com sucesso!",
        "data_hora": datetime.datetime.now()
    }

    # Tentando inserir
    resultado = colecao.insert_one(dados)
    print(f"✅ SUCESSO! Dados salvos com ID: {resultado.inserted_id}")

except Exception as e:
    print(f"❌ ERRO: {e}")
