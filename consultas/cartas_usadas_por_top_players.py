# consultas/cartas_usadas_por_top_players.py

from typing import List, Dict, Any
from pymongo.database import Database

def cartas_usadas_por_top_players(
    db: Database,
    limite: int = 10,
) -> List[Dict[str, Any]]:
  
    pipeline = [
        # filtra por troféus 
        {"$match": {
            "$and": [
                {"team.0.startingTrophies": {"$gte": 6000}},
                {"$expr": {
                    "$eq": [
                        {"$size": {"$arrayElemAt": ["$team.cards", 0]}},
                        8
                    ]
                }}
            ]
        }},
        # explode o array de cards
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        # conta frequência por nome
        {"$group": {
            "_id": "$team.cards.name",
            "quantidade": {"$sum": 1}
        }},
        # ordena e limita
        {"$sort": {"quantidade": -1}},
        {"$limit": limite},
        # projeta o formato final
        {"$project": {
            "_id": 0,
            "carta": "$_id",
            "quantidade": 1
        }},
    ]
    return list(db["battles"].aggregate(pipeline))
