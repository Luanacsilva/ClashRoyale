import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles_collection = db["battles"]

def inserir_batalhas():
    tags = [
        "#PCJ29YJJ",
        "#G9YV9GR8R",
        "#JQPLJ9GRP",
        "#290VGG28"
    ]
    
    headers = {
        "Authorization": f"Bearer {os.getenv('CLASH_API_TOKEN')}"
    }

    battles_collection.delete_many({})  # Limpa antes

    for tag in tags:
        tag_url = tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{tag_url}/battlelog"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            batalhas = response.json()
            for batalha in batalhas:
                batalha["playerTag"] = tag  # Adiciona referência
                battles_collection.insert_one(batalha)
            print(f"✅ {len(batalhas)} batalhas do player {tag} inseridas!")
        else:
            print(f"❌ Erro ao buscar batalhas do player {tag}: {response.status_code}")
