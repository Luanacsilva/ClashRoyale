from pymongo import MongoClient
from dotenv import load_dotenv
import os
from collections import Counter

# Carregar variáveis de ambiente
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n👑 CARTAS MAIS USADAS PELOS JOGADORES TOP (6000+ TROFÉUS):\n")

    filtro = {
        "team.0.startingTrophies": {"$gte": 6000}
    }

    cursor = battles.find(filtro, {"team.cards.name": 1, "team.startingTrophies": 1})
    cartas_counter = Counter()
    total_decks = 0

    for batalha in cursor:
        try:
            deck = batalha["team"][0]["cards"]
            if len(deck) == 8:
                nomes_cartas = [c["name"] for c in deck]
                cartas_counter.update(nomes_cartas)
                total_decks += 1
        except:
            continue

    if total_decks == 0:
        print("⚠️ Nenhum deck de jogador com 6000+ troféus foi encontrado.")
    else:
        print(f"🎯 Total de decks de top players analisados: {total_decks}\n")
        for carta, qtd in cartas_counter.most_common(10):
            print(f"🏆 {carta} - Usada em {qtd} decks")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
