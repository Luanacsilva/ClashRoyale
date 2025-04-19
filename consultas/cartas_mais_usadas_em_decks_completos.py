from pymongo import MongoClient
from dotenv import load_dotenv
import os
from collections import Counter

# Carregar variáveis
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n🃏 CARTAS MAIS FREQUENTES EM DECKS COMPLETOS (8 CARTAS):\n")

    cursor = battles.find({}, {"team.cards.name": 1})
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
        print("⚠️ Nenhum deck com 8 cartas foi encontrado.")
    else:
        print(f"🔢 Total de decks completos analisados: {total_decks}\n")
        for carta, qtd in cartas_counter.most_common(10):
            print(f"📌 {carta} - Presente em {qtd} decks")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
