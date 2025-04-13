from pymongo import MongoClient
from dotenv import load_dotenv
import os
from itertools import combinations
from collections import Counter

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
battles = db["battles"]

# Configurações
N = 3         # Número de cartas no combo
MIN_TAXA = 70 # Taxa mínima de vitórias em %

def main():
    print("\n🎯 COMBOS DE CARTAS COM MELHOR DESEMPENHO:\n")

    # Pega batalhas com vitória
    vitorias = battles.find({
        "$expr": {
            "$gt": [
                { "$arrayElemAt": ["$team.crowns", 0] },
                { "$arrayElemAt": ["$opponent.crowns", 0] }
            ]
        }
    }, { "team.cards.name": 1 })

    # Pega todas as batalhas
    todas = battles.find({}, { "team.cards.name": 1 })

    # Função para gerar combos
    def gerar_combos(batalhas):
        combos = []
        for b in batalhas:
            try:
                cartas = [c["name"] for c in b["team"][0]["cards"]]
                if len(cartas) >= N:
                    combos += combinations(sorted(cartas), N)
            except:
                pass
        return combos

    # Contagem
    total_combos = Counter(gerar_combos(todas))
    vitoria_combos = Counter(gerar_combos(vitorias))

    # Filtra combos com taxa alta
    resultados = []
    for combo, total in total_combos.items():
        wins = vitoria_combos.get(combo, 0)
        taxa = (wins / total) * 100
        if taxa >= MIN_TAXA:
            resultados.append((combo, wins, total, taxa))

    # Ordena
    resultados.sort(key=lambda x: x[3], reverse=True)

    if not resultados:
        print("⚠️ Nenhum combo com alta taxa de vitória encontrado.")
    else:
        for combo, wins, total, taxa in resultados[:10]:
            print(f"🔗 Combo: {', '.join(combo)} - {taxa:.1f}% de vitórias ({wins} de {total})")

    print("\n✅ Consulta executada com sucesso!\n")

if __name__ == "__main__":
    main()
