def combos_derrota(db, limite=10):
    """
    Retorna os combos de 2 cartas mais frequentes em derrotas.
    """
    pipeline = [
        # Filtra batalhas perdidas
        {"$match": {
            "$expr": {
                "$lt": [
                    {"$arrayElemAt": ["$team.crowns", 0]},
                    {"$arrayElemAt": ["$opponent.crowns", 0]}
                ]
            }
        }},
        {"$unwind": "$team"},
        {"$project": {
            "cartas": "$team.cards.name"
        }},
        {"$match": {
            "$expr": {"$gte": [{"$size": "$cartas"}, 2]}
        }},
        # Gera todas as combinações de 2 cartas com $reduce + $concatArrays
        {"$project": {
            "combos": {
                "$map": {
                    "input": {"$range": [0, {"$subtract": [{"$size": "$cartas"}, 1]}]},
                    "as": "i",
                    "in": {
                        "$map": {
                            "input": {"$range": [{"$add": ["$$i", 1]}, {"$size": "$cartas"}]},
                            "as": "j",
                            "in": {
                                "$cond": [
                                    {
                                        "$lt": [
                                            {"$arrayElemAt": ["$cartas", "$$i"]},
                                            {"$arrayElemAt": ["$cartas", "$$j"]}
                                        ]
                                    },
                                    {
                                        "$concat": [
                                            {"$arrayElemAt": ["$cartas", "$$i"]},
                                            " + ",
                                            {"$arrayElemAt": ["$cartas", "$$j"]}
                                        ]
                                    },
                                    {
                                        "$concat": [
                                            {"$arrayElemAt": ["$cartas", "$$j"]},
                                            " + ",
                                            {"$arrayElemAt": ["$cartas", "$$i"]}
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }},
        {"$unwind": "$combos"},
        {"$unwind": "$combos"},
        {"$group": {
            "_id": "$combos",
            "quantidade": {"$sum": 1}
        }},
        {"$sort": {"quantidade": -1}},
        {"$limit": limite},
        {"$project": {
            "_id": 0,
            "combo": "$_id",
            "quantidade": 1
        }}
    ]

    return list(db["battles"].aggregate(pipeline))
