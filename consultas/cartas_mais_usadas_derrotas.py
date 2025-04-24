from datetime import datetime, date, time
from typing import List, Union, Optional
from pymongo.database import Database


def cartas_mais_usadas_derrotas(
    db: Database,
    cartas: List[str],
    data_inicio: Optional[Union[date, datetime]] = None,
    data_fim:    Optional[Union[date, datetime]] = None,
) -> list[dict]:
    
    # normaliza e converte datas se fornecidas
    if data_inicio is not None and not isinstance(data_inicio, datetime):
        data_inicio = datetime.combine(data_inicio, time.min)
    if data_fim    is not None and not isinstance(data_fim,    datetime):
        data_fim    = datetime.combine(data_fim,    time.max)

    pipeline: list[dict] = [
        # converte battleTime para datetime em campo auxiliar
        {
            "$addFields": {
                "battleTimeDate": {
                    "$dateFromString": {
                        "dateString": "$battleTime",
                        "format": "%Y%m%dT%H%M%S.%LZ",
                    }
                }
            }
        }
    ]

    # constrói filtro principal
    match_filter: dict = {"team.cards.name": {"$all": cartas}}
    if data_inicio is not None or data_fim is not None:
        range_filter: dict = {}
        if data_inicio is not None:
            range_filter["$gte"] = data_inicio
        if data_fim is not None:
            range_filter["$lte"] = data_fim
        match_filter["battleTimeDate"] = range_filter

    pipeline.append({"$match": match_filter})

    # calcula flags e agrupa
    pipeline += [
        {
            "$addFields": {
                "isDerrota": {
                    "$lt": [
                        {"$arrayElemAt": ["$team.crowns", 0]},
                        {"$arrayElemAt": ["$opponent.crowns", 0]},
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "totalPartidas": {"$sum": 1},
                "totalDerrotas": {"$sum": {"$cond": ["$isDerrota", 1, 0]}},
            }
        },
        {
            "$project": {
                "_id": 0,
                "totalPartidas": 1,
                "totalDerrotas": 1,
                "taxaDerrotas": {
                    "$cond": [
                        {"$eq": ["$totalPartidas", 0]},
                        0,
                        {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$totalDerrotas", "$totalPartidas"]},
                                        100,
                                    ]
                                },
                                2
                            ]
                        }
                    ]
                }
            }
        }
    ]

    # executa e retorna lista vazia se não houver partidas
    return list(db["battles"].aggregate(pipeline))