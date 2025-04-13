from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

print("\n🕵️ Testando vitórias com desvantagem de troféus...\n")

resultados = list(battles.find({
    "$expr": {
        "$and": [
            { "$lt": [ { "$arrayElemAt": ["$team.startingTrophies", 0] }, { "$arrayElemAt": ["$opponent.startingTrophies", 0] } ] },
            { "$gt": [ { "$arrayElemAt": ["$team.crowns", 0] }, { "$arrayElemAt": ["$opponent.crowns", 0] } ] }
        ]
    }
}, {
    "team.startingTrophies": 1,
    "opponent.startingTrophies": 1,
    "team.crowns": 1,
    "opponent.crowns": 1
}))

if not resultados:
    print("⚠️ Nenhuma vitória com desvantagem confirmada...")
else:
    print(f"✅ {len(resultados)} vitórias com desvantagem encontradas!\n")
    for r in resultados[:5]:
        print(r)

print("\n🔍 Teste finalizado!\n")
