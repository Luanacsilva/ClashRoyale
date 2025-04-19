def cartas_mais_usadas_em_derrotas(db, limite=10):
    """
    Retorna as cartas mais usadas nos decks de jogadores derrotados.
    """
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
        {"$limit": limite},
        {"$project": {
            "_id": 0,
            "carta": "$_id",
            "quantidade": 1
        }}
    ]

    return list(db["battles"].aggregate(pipeline))
