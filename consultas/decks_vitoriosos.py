from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n📘 DECKS COM MAIOR TAXA DE VITÓRIA:\n")

    pipeline = [
        {"$unwind": "$team"},
        {"$unwind": "$opponent"},

        {"$addFields": {
            "team.vitoria": {"$gt": ["$team.crowns", "$opponent.crowns"]}
        }},

        {"$group": {
            "_id": "$team.cards.name",
            "total": {"$sum": 1},
            "vitorias": {
                "$sum": {
                    "$cond": ["$team.vitoria", 1, 0]
                }
            }
        }},

        {"$project": {
            "_id": 0,
            "deck": "$_id",
            "total": 1,
            "vitorias": 1,
            "taxa_vitorias": {
                "$multiply": [
                    {"$divide": ["$vitorias", "$total"]},
                    100
                ]
            }
        }},

        {"$sort": {"taxa_vitorias": -1}}
    ]

    resultados = list(battles.aggregate(pipeline))

    if not resultados:
        print("⚠️ Nenhum resultado encontrado.")
    else:
        for r in resultados:
            deck_nome = ", ".join(r['deck'])
            print(f"🃏 Deck: [{deck_nome}]\n   - Vitórias: {r['vitorias']} em {r['total']} partidas ({r['taxa_vitorias']:.1f}%)\n")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
