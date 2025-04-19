import os
import requests
from dotenv import load_dotenv

load_dotenv()

def testar_conexao_api():
    token = os.getenv("CLASHROYALE_TOKEN")
    if not token:
        print("❌ Token não encontrado no .env")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.clashroyale.com/v1/cards"

    try:
        response = requests.get(url, headers=headers)
        print(f"Status da requisição: {response.status_code}")
        if response.status_code == 200:
            print("✅ Conexão com a API bem-sucedida!")
            data = response.json()
            print(f"Total de cartas recebidas: {len(data.get('items', []))}")
        elif response.status_code == 403:
            print("🚫 Acesso negado: verifique o token ou o IP autorizado.")
        else:
            print(f"⚠️ Resposta inesperada: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {str(e)}")

if __name__ == "__main__":
    testar_conexao_api()
