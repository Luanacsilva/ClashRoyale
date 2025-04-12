import os
from dotenv import load_dotenv
from pymongo import MongoClient
from api.coletar_cartas import coletar_cartas

# Carrega variáveis de ambiente
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Conecta ao MongoDB
client = MongoClient(MONGODB_URI)
db = client["bd_clashroyale"]
colecao = db["cards"]

def inserir_cartas():
    cartas = coletar_cartas()
    
    if not cartas:
        print("Nenhuma carta para inserir.")
        return

    for carta in cartas:
        # Substitui ou insere com base no 'id' da carta
        colecao.replace_one({"id": carta["id"]}, carta, upsert=True)

    print(f"✅ Inseridas/atualizadas {len(cartas)} cartas no banco.")

# Teste direto
if __name__ == "__main__":
    inserir_cartas()
