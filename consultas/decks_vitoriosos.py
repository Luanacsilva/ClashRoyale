# consultas/decks_vitoriosos.py
from datetime import datetime, date, time
from typing import List, Dict, Any
from pymongo.database import Database

def decks_vitoriosos(
    db: Database,
    percentual: float,
    data_inicio: date | datetime,
    data_fim: date | datetime,
    limite: int = 10,
) -> List[Dict[str, Any]]:
    """
    Lista decks completos cuja taxa de vitórias ≥ `percentual`
    no intervalo [data_inicio, data_fim].
    Retorna no máximo `limite` decks.
    """
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
        # filtra intervalo de datas
        {
            "$match": {
                "battleTimeDate": {
                    "$gte": datetime.combine(data_inicio, time.min),
                    "$lte": datetime.combine(data_fim,   time.max),
                }
            }
        },
        #  marca vitória
        {
            "$addFields": {
                "vitoria": {
                    "$gt": [
                        { "$arrayElemAt": ["$team.crowns", 0] },
                        { "$max": "$opponent.crowns" }
                    ]
                }
            }
        },
        #  agrupa pelo deck completo
        {
            "$group": {
                "_id": "$team.cards",
                "totalPartidas": { "$sum": 1 },
                "totalVitorias": { "$sum": { "$cond": ["$vitoria", 1, 0] } }
            }
        },
        # calcula taxa de vitórias
        {
            "$addFields": {
                "taxaVitorias": {
                    "$multiply": [
                        { "$divide": ["$totalVitorias", "$totalPartidas"] },
                        100
                    ]
                }
            }
        },
        # filtra por corte mínimo
        { "$match": { "taxaVitorias": { "$gte": percentual } } },
        # projeta resultado final (com rounding)
        {
            "$project": {
                "_id": 0,
                "deck": "$_id",
                "totalPartidas": 1,
                "totalVitorias": 1,
                "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
            }
        },
        # ordena e limita
        { "$sort": { "taxaVitorias": -1 } },
        { "$limit": limite },
    ]

    brutos = list(db["battles"].aggregate(pipeline))

    # ---- transforma cada deck em string legível ----
    resultados: List[Dict[str, Any]] = []
    for r in brutos:
        nomes: List[str] = []
        for carta in r.get("deck", []):
            if isinstance(carta, dict) and "name" in carta:
                nomes.append(carta["name"])
            elif isinstance(carta, list):
                nomes.extend([item["name"] for item in carta if isinstance(item, dict) and "name" in item])

        resultados.append({
            "deck": ", ".join(nomes[:8]) if nomes else "Desconhecido",
            "totalPartidas": r.get("totalPartidas", 0),
            "totalVitorias": r.get("totalVitorias", 0),
            "taxaVitorias": r.get("taxaVitorias", 0.0),
        })

    return resultados
