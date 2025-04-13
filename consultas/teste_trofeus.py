from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

print("\n📊 TESTE DE TROFÉUS NAS BATALHAS:\n")

amostras = list(battles.find({}, {
    "_id": 0,
    "team.0.name": 1,
    "team.0.startingTrophies": 1,
    "team.0.crowns": 1,
    "opponent.0.name": 1,
    "opponent.0.startingTrophies": 1,
    "opponent.0.crowns": 1
}).limit(5))

for a in amostras:
    print(a)

print("\n✅ Teste finalizado!\n")
