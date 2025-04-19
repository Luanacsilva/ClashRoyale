def cartas_usadas_por_top_players(db, limite=10):
    """
    Retorna as cartas mais usadas por jogadores com 6000 ou mais troféus.
    Considera apenas decks com exatamente 8 cartas.
    """
    pipeline = [
        # Filtra batalhas de jogadores com 6000+ troféus e 8 cartas
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
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        {"$group": {
            "_id": "$team.cards.name",
            "quantidade": {"$sum": 1}
        }},
        {"$sort": {"quantidade": -1}},
        {"$limit": limite},
        {"$project": {
            "_id": 0,
            "carta": "$_id",
            "quantidade": 1
        }}
    ]

    return list(db["battles"].aggregate(pipeline))
