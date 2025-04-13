from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    print("\n🏅 VITÓRIAS COM DESVANTAGEM (MENOS TROFÉUS):\n")

    pipeline = [
        {"$match": {
            "$expr": {
                "$and": [
                    { "$lt": [ { "$arrayElemAt": ["$team.startingTrophies", 0] }, { "$arrayElemAt": ["$opponent.startingTrophies", 0] } ] },
                    { "$gt": [ { "$arrayElemAt": ["$team.crowns", 0] }, { "$arrayElemAt": ["$opponent.crowns", 0] } ] }
                ]
            }
        }},
        {"$project": {
            "_id": 0,
            "trofeus_time": { "$arrayElemAt": ["$team.startingTrophies", 0] },
            "trofeus_oponente": { "$arrayElemAt": ["$opponent.startingTrophies", 0] },
            "crowns_time": { "$arrayElemAt": ["$team.crowns", 0] },
            "crowns_oponente": { "$arrayElemAt": ["$opponent.crowns", 0] }
        }}
    ]

    resultados = list(battles.aggregate(pipeline))

    if not resultados:
        print("⚠️ Nenhuma vitória com desvantagem encontrada.")
    else:
        for r in resultados:
            print(f"🎯 Vitória com {r['trofeus_time']} troféus contra {r['trofeus_oponente']} troféus (Coroas: {r['crowns_time']} x {r['crowns_oponente']})")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
