def decks_vitoriosos(db, limite=10):
    """
    Retorna os decks com maior taxa de vitória.
    """
    pipeline = [
        {"$unwind": "$team"},
        {"$unwind": "$opponent"},
        {"$addFields": {
            "team.vitoria": {"$gt": ["$team.crowns", "$opponent.crowns"]}
        }},
        {"$group": {
            "_id": "$team.cards.name",
            "total": {"$sum": 1},
            "vitorias": {
                "$sum": {
                    "$cond": ["$team.vitoria", 1, 0]
                }
            }
        }},
        {"$project": {
            "_id": 0,
            "deck": "$_id",
            "total": 1,
            "vitorias": 1,
            "taxa_vitorias": {
                "$round": [
                    {"$multiply": [
                        {"$divide": ["$vitorias", "$total"]},
                        100
                    ]},
                    1
                ]
            }
        }},
        {"$sort": {"taxa_vitorias": -1}},
        {"$limit": limite}
    ]

    return list(db["battles"].aggregate(pipeline))
