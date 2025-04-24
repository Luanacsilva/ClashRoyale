from typing import List, Dict, Any
from pymongo.database import Database


def cartas_mais_usadas_em_decks_completos(
    db: Database,
    limite: int = 10,
) -> List[Dict[str, Any]]:
  
    pipeline = [
        # Seleciona batalhas onde o jogador tem exatamente 8 cartas
        {"$match": {
            "$expr": {
                "$eq": [
                    {"$size": {"$arrayElemAt": ["$team.cards", 0]}},
                    8
                ]
            }
        }},
        # Desmembra cada carta do deck
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        # Agrupa por nome da carta e conta aparições
        {"$group": {
            "_id": "$team.cards.name",
            "quantidade": {"$sum": 1}
        }},
        # Ordena pelo mais frequente
        {"$sort": {"quantidade": -1}},
        # Limita resultados
        {"$limit": limite},
        # Projeta formato final
        {"$project": {
            "_id": 0,
            "carta": "$_id",
            "quantidade": 1
        }}
    ]
    return list(db["battles"].aggregate(pipeline))
