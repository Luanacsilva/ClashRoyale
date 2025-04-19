import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
cards_collection = db["cards"]

def inserir_cartas():
    token = os.getenv("CLASHROYALE_TOKEN")
    if not token:
        print("❌ Token da API não encontrado no .env.")
        return
    
    url = "https://api.clashroyale.com/v1/cards"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json().get("items", [])
        if not dados:
            print("⚠️ Nenhuma carta retornada pela API.")
            return

        cards_collection.delete_many({})
        cards_collection.insert_many(dados)
        print(f"✅ {len(dados)} cartas inseridas com sucesso!")
    else:
        print(f"❌ Erro ao acessar a API: {response.status_code}")
        print("Detalhes:", response.text)

# Execução direta
if __name__ == "__main__":
    inserir_cartas()
