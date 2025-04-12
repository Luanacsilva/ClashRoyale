import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Conecta ao MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
cards_collection = db["cards"]

def inserir_cartas():
    token = os.getenv("CLASH_API_TOKEN")
    url = "https://api.clashroyale.com/v1/cards"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json()["items"]
        cards_collection.delete_many({})
        cards_collection.insert_many(dados)
        print(f"✅ {len(dados)} cartas inseridas com sucesso!")
    else:
        print("❌ Erro ao acessar a API:", response.status_code)
