import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis do .env
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Criar cliente Mongo
client = MongoClient(MONGODB_URI)

# Verificar conexão e listar bancos
try:
    print("🟢 Conectado ao MongoDB com sucesso!")
    print("Bancos disponíveis:")
    print(client.list_database_names())
except Exception as erro:
    print("🔴 Erro ao conectar no MongoDB:", erro)
