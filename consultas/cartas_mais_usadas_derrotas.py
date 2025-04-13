from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n📉 CARTAS MAIS USADAS EM DERROTAS:\n")

    pipeline = [
        {"$match": {
            "$expr": {
                "$lt": [
                    { "$arrayElemAt": ["$team.crowns", 0] },
                    { "$arrayElemAt": ["$opponent.crowns", 0] }
                ]
            }
        }},
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        {"$group": {
            "_id": "$team.cards.name",
            "quantidade": {"$sum": 1}
        }},
        {"$sort": {"quantidade": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "carta": "$_id",
            "quantidade": 1
        }}
    ]

    resultados = list(battles.aggregate(pipeline))

    if not resultados:
        print("⚠️ Nenhuma carta encontrada em derrotas.")
    else:
        for r in resultados:
            print(f"❌ {r['carta']} - Apareceu em {r['quantidade']} derrotas")

    print("\n✅ Consulta executada com sucesso!")

if __name__ == "__main__":
    main()
