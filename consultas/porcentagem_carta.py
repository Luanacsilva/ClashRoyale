from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

def main():
    pipeline = [
        { "$unwind": "$team" },
        { "$unwind": "$team.cards" },
        {
            "$group": {
                "_id": "$team.cards.name",
                "total": { "$sum": 1 },
                "vitorias": {
                    "$sum": {
                        "$cond": [
                            {
                                "$gt": [
                                    "$team.crowns",
                                    { "$max": "$opponent.crowns" }
                                ]
                            },
                            1, 0
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "carta": "$_id",
                "total": 1,
                "vitorias": 1,
                "taxa_vitorias": {
                    "$multiply": [
                        { "$divide": ["$vitorias", "$total"] },
                        100
                    ]
                }
            }
        },
        { "$sort": { "taxa_vitorias": -1 } }
    ]

    print("\n📊 TAXA DE VITÓRIA POR CARTA:\n")
    resultados = list(battles.aggregate(pipeline))

    if not resultados:
        print("⚠️ Nenhum resultado encontrado.")
    else:
        for r in resultados:
            print(f"{r['carta']}: {r['taxa_vitorias']:.1f}% de vitórias em {r['total']} usos")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
