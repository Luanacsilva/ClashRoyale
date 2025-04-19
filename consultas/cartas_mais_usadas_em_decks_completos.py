def cartas_mais_usadas_em_decks_completos(db, limite=10):
    """
    Retorna as cartas mais frequentes em decks completos (com exatamente 8 cartas).
    """
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
