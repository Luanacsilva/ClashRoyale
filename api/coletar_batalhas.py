import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": f"Bearer {os.getenv('CLASHROYALE_TOKEN')}"
}

PLAYER_TAGS = [
    "#PCJ29YJJ",
    "#G9YV9GR8R",
    "#JQPLJ9GRP",
    "#290VGG28"
]

def coletar_batalhas_reais():
    batalhas = []

    for tag in PLAYER_TAGS:
        tag_url = tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{tag_url}/battlelog"

        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            dados = response.json()
            print(f"✅ Batalhas coletadas para {tag}: {len(dados)}")
            batalhas.extend(dados)
        else:
            print(f"❌ Erro {response.status_code} ao buscar batalhas para {tag}")

    return batalhas

# Teste rápido
if __name__ == "__main__":
    batalhas = coletar_batalhas_reais()
    print(f"\n📊 Total de batalhas coletadas: {len(batalhas)}")
    for b in batalhas[:3]:  # Mostra só as 3 primeiras pra não lotar o terminal
        print(f"{b['type']} - {b['battleTime']} - {b['team'][0]['name']} vs {b['opponent'][0]['name']}")
