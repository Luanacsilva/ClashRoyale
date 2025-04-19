from itertools import combinations
from collections import Counter

def combos_vencedores_n_cartas(db, n=3, min_taxa=70, limite=10):
    """
    Retorna combos de N cartas com taxa de vitória maior ou igual a `min_taxa` (%).
    """

    # 1. Pega todas as batalhas (para contar aparições totais)
    todas_batalhas = db["battles"].find({}, {"team.cards.name": 1})

    # 2. Pega apenas batalhas vencidas
    vitorias = db["battles"].find({
        "$expr": {
            "$gt": [
                {"$arrayElemAt": ["$team.crowns", 0]},
                {"$arrayElemAt": ["$opponent.crowns", 0]}
            ]
        }
    }, {"team.cards.name": 1})

    def extrair_combos(cursor):
        contagem = Counter()
        for doc in cursor:
            try:
                cartas = doc["team"][0]["cards"]
                nomes = sorted([c["name"] for c in cartas])
                if len(nomes) >= n:
                    contagem.update(combinations(nomes, n))
            except (KeyError, IndexError, TypeError):
                continue
        return contagem

    total_combos = extrair_combos(todas_batalhas)
    vitoria_combos = extrair_combos(vitorias)

    resultados = []
    for combo, total in total_combos.items():
        wins = vitoria_combos.get(combo, 0)
        taxa = (wins / total) * 100
        if taxa >= min_taxa:
            resultados.append({
                "combo": list(combo),
                "vitorias": wins,
                "total": total,
                "taxa_vitoria": round(taxa, 1)
            })

    resultados.sort(key=lambda x: x["taxa_vitoria"], reverse=True)
    return resultados[:limite]
