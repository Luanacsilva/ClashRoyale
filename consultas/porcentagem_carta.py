def porcentagem_carta(db, limite=10):
    """
    Retorna a taxa de vitória por carta, com base em quantas vezes a carta foi usada
    e quantas vezes resultou em vitória.
    """
    pipeline = [
        {"$unwind": "$team"},
        {"$unwind": "$opponent"},
        {"$unwind": "$team.cards"},
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
                                    "$opponent.crowns"
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
                    "$round": [
                        { "$multiply": [
                            { "$divide": ["$vitorias", "$total"] },
                            100
                        ] },
                        1
                    ]
                }
            }
        },
        { "$sort": { "taxa_vitorias": -1 } },
        { "$limit": limite }
    ]

    return list(db["battles"].aggregate(pipeline))
