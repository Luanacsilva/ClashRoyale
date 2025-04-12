from pymongo import MongoClient
from dotenv import load_dotenv
from collections import Counter
import os

# Conexão com o Mongo
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["bd_clashroyale"]
colecao = db["batalhas"]

def consultar_carta_carregadora():
    try:
        top_n = int(input("Mostrar top quantas cartas carregadoras? "))
    except ValueError:
        print("❌ Valor inválido.")
        return

    partidas = list(colecao.find({}))
    if not partidas:
        print("⚠️ Nenhuma batalha encontrada.")
        return

    vencedoras = Counter()
    perdedoras = Counter()

    for p in partidas:
        vencedor = p["vencedor"]

        deck_v = p["deck_1"] if vencedor == p["jogador_1"]["nickname"] else p["deck_2"]
        deck_p = p["deck_2"] if vencedor == p["jogador_1"]["nickname"] else p["deck_1"]

        vencedoras.update(deck_v)
        perdedoras.update(deck_p)

    diferenca = {}

    for carta, vitorias in vencedoras.items():
        derrotas = perdedoras.get(carta, 0)
        if vitorias > derrotas:
            diferenca[carta] = vitorias - derrotas

    top_cartas = sorted(diferenca.items(), key=lambda x: x[1], reverse=True)[:top_n]

    print(f"\n🏅 Top {top_n} cartas mais presentes em decks vencedores (vs derrotas):\n")
    for carta, dif in top_cartas:
        print(f"🔥 {carta} — {dif} vitórias a mais que derrotas")
