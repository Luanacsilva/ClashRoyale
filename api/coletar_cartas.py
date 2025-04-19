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

def coletar_cartas_usadas():
    cartas_usadas = set()

    for tag in PLAYER_TAGS:
        tag_url = tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{tag_url}/battlelog"

        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            batalhas = response.json()
            print(f"✅ Batalhas para {tag}: {len(batalhas)}")
            for batalha in batalhas:
                team = batalha.get("team", [])
                if team and "cards" in team[0]:
                    for carta in team[0]["cards"]:
                        cartas_usadas.add(carta["name"])
        else:
            print(f"❌ Erro {response.status_code} ao buscar batalhas para {tag}")

    return list(cartas_usadas)

# Teste direto
if __name__ == "__main__":
    cartas = coletar_cartas_usadas()
    print(f"\n🃏 Total de cartas únicas usadas: {len(cartas)}")
    print("Exemplos:", cartas[:10])
