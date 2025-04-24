# consultas/vitorias_com_desvantagem.py
from pymongo.database import Database

def vitorias_com_desvantagem(
    db: Database,
    carta: str,
    desvantagem_minima: float,
) -> int:
  
    # calcula o fator de corte
    fator_desvantagem = 1 - (desvantagem_minima / 100)

    pipeline = [
        # filtra partidas com a carta em qualquer lado
        {
            "$match": {
                "$or": [
                    {"team.cards.name": carta},
                    {"opponent.cards.name": carta},
                ]
            }
        },
        #  extrai troféus iniciais e quem venceu
        {
            "$addFields": {
                "teamTrophies":     {"$arrayElemAt": ["$team.startingTrophies", 0]},
                "opponentTrophies": {"$arrayElemAt": ["$opponent.startingTrophies", 0]},
                "teamWon":          {"$gt": [
                                        {"$arrayElemAt": ["$team.crowns", 0]},
                                        {"$arrayElemAt": ["$opponent.crowns", 0]}
                                    ]},
                "opponentWon":      {"$gt": [
                                        {"$arrayElemAt": ["$opponent.crowns", 0]},
                                        {"$arrayElemAt": ["$team.crowns", 0]}
                                    ]},
            }
        },
        # mantém só as vitórias com desvantagem de troféus ≥ corte
        {
            "$match": {
                "$or": [
                    {
                        "teamWon": True,
                        "$expr": {
                            "$lt": [
                                "$teamTrophies",
                                {"$multiply": ["$opponentTrophies", fator_desvantagem]}
                            ]
                        }
                    },
                    {
                        "opponentWon": True,
                        "$expr": {
                            "$lt": [
                                "$opponentTrophies",
                                {"$multiply": ["$teamTrophies", fator_desvantagem]}
                            ]
                        }
                    }
                ]
            }
        },
        # filtra vitórias sem derrubar 2 torres (0 ou 1 coroa)
        {
            "$match": {
                "$or": [
                    {
                        "teamWon": True,
                        "$expr": {
                            "$lt": [
                                {"$size": {"$ifNull": ["$opponent.princessTowersHitPoints", []]}},
                                2
                            ]
                        }
                    },
                    {
                        "opponentWon": True,
                        "$expr": {
                            "$lt": [
                                {"$size": {"$ifNull": ["$team.princessTowersHitPoints", []]}},
                                2
                            ]
                        }
                    }
                ]
            }
        },
        # conta quantas atenderam a todos os critérios
        {"$count": "quantidadeVitorias"},
    ]

    resultado = list(db["battles"].aggregate(pipeline))
    return resultado[0].get("quantidadeVitorias", 0) if resultado else 0
