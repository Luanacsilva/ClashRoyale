import requests 
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

# Carrega variáveis de ambiente
load_dotenv()

# Conecta ao MongoDB
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["bd_clashroyale"]
    battles_collection = db["battles"]
    print("💚 Conexão com MongoDB estabelecida com sucesso!")
except ConnectionFailure as e:
    print(f"❌ Erro de conexão com o MongoDB: {e}")
    exit()

def inserir_batalhas():
    tags = [
        "#PCJ29YJJ",
        "#G9YV9GR8R",
        "#JQPLJ9GRP",
        "#290VGG28"
    ]
    
    headers = {
        "Authorization": f"Bearer {os.getenv('CLASHROYALE_TOKEN')}"
    }

    # Limpa a coleção antes de inserir
    battles_collection.delete_many({})
    print("🧹 Coleção 'battles' limpa.")

    for tag in tags:
        tag_url = tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{tag_url}/battlelog"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                batalhas = response.json()
                count = 0
                for batalha in batalhas:
                    if "startingTrophies" in batalha.get("team", [{}])[0]:
                        batalha["playerTag"] = tag
                        try:
                            battles_collection.insert_one(batalha)
                            count += 1
                        except DuplicateKeyError:
                            print("⚠️ Batalha duplicada ignorada.")
                    else:
                        print("⚠️ Batalha ignorada (sem startingTrophies)")
                print(f"✅ {count} batalhas inseridas do player {tag}")
            else:
                print(f"❌ Erro {response.status_code} ao buscar batalhas do player {tag}")
        except Exception as e:
            print(f"🔥 Erro durante a requisição ou inserção: {e}")

# Executa se rodar diretamente
if __name__ == "__main__":
    inserir_batalhas()
