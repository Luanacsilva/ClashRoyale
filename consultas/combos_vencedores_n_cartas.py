from datetime import datetime, date, time
from typing import Optional, List, Dict, Any
from itertools import combinations
from collections import Counter
from pymongo.database import Database


def combos_vencedores_n_cartas(
    db: Database,
    data_inicio: Optional[date | datetime] = None,
    data_fim:    Optional[date | datetime] = None,
    porcentagem_minima: float = 1.0,
    elixir_min:  int = 1,
    tamanho_combo: int = 3,
) -> List[Dict[str, Any]]:
  
    # Normaliza datas para datetime
    if data_inicio is not None and not isinstance(data_inicio, datetime):
        data_inicio = datetime.combine(data_inicio, time.min)
    if data_fim    is not None and not isinstance(data_fim,    datetime):
        data_fim    = datetime.combine(data_fim,    time.max)

    # Prepara filtro de vitórias e datas
    match_filter: Dict[str, Any] = {
        "$expr": {
            "$gt": [
                {"$arrayElemAt": ["$team.crowns", 0]},
                {"$arrayElemAt": ["$opponent.crowns", 0]},
            ]
        }
    }
    if data_inicio or data_fim:
        date_cond: Dict[str, Any] = {}
        if data_inicio:
            date_cond["$gte"] = data_inicio
        if data_fim:
            date_cond["$lte"] = data_fim
        match_filter["battleTimeDate"] = date_cond

    # Conta total de vitórias no período
    total_vitorias = db["battles"].count_documents(match_filter)
    if total_vitorias == 0:
        return []

    # Pipeline de agregação
    pipeline = [
        # Converte battleTime para datetime em campo auxiliar
        {"$addFields": {"battleTimeDate": {"$dateFromString": {
            "dateString": "$battleTime",
            "format": "%Y%m%dT%H%M%S.%LZ",
        }}}},
        # Aplica filtro de vitória e datas
        {"$match": match_filter},
        # Filtra cartas de acordo com elixir_min
        {"$addFields": {"filtered": {
            "$filter": {
                "input": "$team.cards",
                "as": "c",
                "cond": {"$gte": ["$$c.elixirCost", elixir_min]}
            }
        }}},
        # Projeta apenas nomes de cartas
        {"$project": {"combo": {"$map": {
            "input": "$filtered",
            "as": "c",
            "in": "$$c.name"
        }}}},
        # Ordena os nomes para padronizar
        {"$addFields": {"combo": {"$sortArray": {"input": "$combo"}}}},
        # Agrupa por combo e conta ocorrências
        {"$group": {"_id": "$combo", "count": {"$sum": 1}}},
    ]

    docs = list(db["battles"].aggregate(pipeline))

    # Gera combinações de tamanho tamanho_combo
    min_count = max(1, round(total_vitorias * (porcentagem_minima / 100)))
    combo_counter: Counter[tuple[str, ...]] = Counter()
    for doc in docs:
        cards = doc["_id"] or []
        for combo in combinations(cards, tamanho_combo):
            combo_counter[combo] += doc["count"]

    # Formata resultados que atingem o mínimo
    resultados: List[Dict[str, Any]] = []
    for combo, cnt in combo_counter.items():
        if cnt >= min_count:
            resultados.append({
                "combo": list(combo),
                "count": cnt,
                "percent": round(cnt / total_vitorias * 100, 2),
            })

    # Ordena por percentual desc
    resultados.sort(key=lambda x: x["percent"], reverse=True)
    return resultados