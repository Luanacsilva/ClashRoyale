import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

def testar_conexao_api():
    token = os.getenv("CLASHROYALE_TOKEN")
    if not token:
        print("❌ Token da API não encontrado no .env")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.clashroyale.com/v1/cards"

    try:
        response = requests.get(url, headers=headers)
        print(f"🌐 API - Status da requisição: {response.status_code}")
        if response.status_code == 200:
            print("✅ Conexão com a API bem-sucedida!")
            data = response.json()
            print(f"🃏 Total de cartas recebidas: {len(data.get('items', []))}")
        elif response.status_code == 403:
            print("🚫 Acesso negado: verifique o token ou o IP autorizado.")
        else:
            print(f"⚠️ Resposta inesperada: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {str(e)}")

def testar_conexao_mongo():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ URI do MongoDB não encontrada no .env")
        return

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")  # Força verificação de conexão
        print("✅ Conexão com o MongoDB estabelecida com sucesso!")
    except ConnectionFailure as e:
        print(f"❌ Erro de conexão com o MongoDB: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado com o MongoDB: {str(e)}")

if __name__ == "__main__":
    print("\n=== 🔍 TESTE DE CONEXÕES ===")
    testar_conexao_api()
    print()
    testar_conexao_mongo()
