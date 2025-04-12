import requests
import os
from dotenv import load_dotenv

# Carregar token do .env
load_dotenv()
TOKEN = os.getenv("CLASH_API_TOKEN")

# Cabeçalhos da requisição
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def coletar_cartas():
    url = "https://api.clashroyale.com/v1/cards"
    try:
        resposta = requests.get(url, headers=HEADERS)
        resposta.raise_for_status()
        cartas = resposta.json().get("items", [])
        print(f"✅ {len(cartas)} cartas coletadas com sucesso!")
        return cartas
    except requests.exceptions.RequestException as erro:
        print("🔴 Erro ao coletar cartas:", erro)
        return []

# Executar diretamente no terminal
if __name__ == "__main__":
    coletar_cartas()
