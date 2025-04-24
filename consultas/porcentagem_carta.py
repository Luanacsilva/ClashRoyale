# consultas/porcentagem_carta.py
from datetime import datetime, date
from pymongo.database import Database

def porcentagem_carta(
    db: Database,
    carta: str,
    data_inicio: date | datetime,
    data_fim: date | datetime,
    limite: int = 10,
) -> list[dict]:
    pipeline = [
        # converte battleTime para datetime
        {
            "$addFields": {
                "battleTimeDate": {
                    "$dateFromString": {
                        "dateString": "$battleTime",
                        "format": "%Y%m%dT%H%M%S.%LZ",
                    }
                }
            }
        },
        # explode arrays para acessar a carta
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        # filtra carta + intervalo
        {
            "$match": {
                "team.cards.name": carta,
                "battleTimeDate": {
                    "$gte": datetime.combine(data_inicio, datetime.min.time()),
                    "$lte": datetime.combine(data_fim,   datetime.max.time()),
                },
            }
        },
        # agrupa por carta
        {
            "$group": {
                "_id": "$team.cards.name",
                "total":   {"$sum": 1},
                "vitorias": {
                    "$sum": {
                        "$cond": [
                            {"$gt": ["$team.crowns", {"$max": "$opponent.crowns"}]},
                            1,
                            0,
                        ]
                    }
                },
            }
        },
        # adiciona derrotas
        {
            "$addFields": {
                "derrotas": {"$subtract": ["$total", "$vitorias"]}
            }
        },
        # calcula percentuais (com round de 1 casa)
        {
            "$project": {
                "_id": 0,
                "carta": "$_id",
                "total": 1,
                "vitorias": 1,
                "derrotas": 1,
                "taxa_vitorias": {
                    "$round": [
                        {"$multiply": [
                            {"$divide": ["$vitorias", "$total"]},
                            100
                        ]},
                        1
                    ]
                },
                "taxa_derrotas": {
                    "$round": [
                        {"$multiply": [
                            {"$divide": ["$derrotas", "$total"]},
                            100
                        ]},
                        1
                    ]
                },
            }
        },
        # ordena e limita
        {"$sort": {"taxa_vitorias": -1}},
        {"$limit": limite},
    ]

    return list(db["battles"].aggregate(pipeline))
