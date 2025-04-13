from pymongo import MongoClient
from dotenv import load_dotenv
import os
from itertools import combinations
from collections import Counter

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n💥 COMBOS DE CARTAS MAIS PRESENTES EM DERROTAS:\n")

    # Buscar batalhas perdidas
    batalhas = list(battles.find({
        "$expr": {
            "$lt": [
                { "$arrayElemAt": ["$team.crowns", 0] },
                { "$arrayElemAt": ["$opponent.crowns", 0] }
            ]
        }
    }))

    # Gerar combos de 2 cartas
    contagem_combos = Counter()
    for batalha in batalhas:
        for player in batalha.get("team", []):
            cartas = [c["name"] for c in player.get("cards", [])]
            if len(cartas) >= 2:
                combos = combinations(sorted(cartas), 2)
                contagem_combos.update(combos)

    # Mostrar os 10 mais comuns
    mais_comuns = contagem_combos.most_common(10)

    if not mais_comuns:
        print("⚠️ Nenhum combo encontrado.")
    else:
        for combo, count in mais_comuns:
            print(f"🃏 Combo: {combo[0]} + {combo[1]} - Apareceu em {count} derrotas")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
