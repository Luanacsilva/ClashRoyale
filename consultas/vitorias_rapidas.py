from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

# Tempo limite para considerar uma vitória "rápida" (em segundos)
LIMITE_SEGUNDOS = 120

def main():
    print("\n⏰ VITÓRIAS EM TEMPO RECORDE:")

    # Pipeline para buscar vitórias com menos de LIMITE_SEGUNDOS de duração
    pipeline = [
        {"$match": {
            "$expr": {
                "$gt": [
                    { "$arrayElemAt": ["$team.crowns", 0] },
                    { "$arrayElemAt": ["$opponent.crowns", 0] }
                ]
            },
            "team": { "$exists": True },
            "opponent": { "$exists": True },
            "battleTime": { "$exists": True },
            "duration": { "$exists": True, "$lte": LIMITE_SEGUNDOS }
        }},
        {"$project": {
            "_id": 0,
            "crowns": "$team.crowns",
            "opponent_crowns": "$opponent.crowns",
            "duration": 1
        }},
        {"$sort": {"duration": 1}}
    ]

    resultados = list(battles.aggregate(pipeline))

    if not resultados:
        print("\n🚨 Nenhuma vitória rápida encontrada!")
    else:
        for r in resultados:
            duracao = r.get("duration", 0)
            time_crowns = r.get("crowns", [0])[0]
            opp_crowns = r.get("opponent_crowns", [0])[0]
            print(f"🚀 Vitória em {duracao} segundos (Coroas: {time_crowns} x {opp_crowns})")

    print("\n🌟 Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
