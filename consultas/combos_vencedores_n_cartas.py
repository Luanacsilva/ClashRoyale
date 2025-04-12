from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from itertools import combinations
from collections import Counter
import os

# Conecta ao MongoDB
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["bd_clashroyale"]
colecao = db["batalhas"]

def formatar_data(data_str, final=False):
    try:
        dt = datetime.strptime(data_str, "%d/%m/%y")
        if final:
            dt = dt.replace(hour=23, minute=59, second=59)
        return dt.isoformat()
    except ValueError:
        print("❌ Data inválida. Use o formato dd/mm/aa.")
        return None

def consultar_combos_vencedores():
    try:
        n = int(input("Tamanho do combo (N): "))
        if n < 2 or n > 8:
            print("❌ O combo deve ter entre 2 e 8 cartas.")
            return
        perc_min = float(input("Porcentagem mínima de vitórias (Y): "))
    except ValueError:
        print("❌ Valor inválido para combo ou porcentagem.")
        return

    data_inicio = input("Data de início (dd/mm/aa): ")
    data_fim = input("Data de fim (dd/mm/aa): ")

    dt_inicio = formatar_data(data_inicio)
    dt_fim = formatar_data(data_fim, final=True)

    if not dt_inicio or not dt_fim:
        return

    partidas = list(colecao.find({
        "timestamp": {"$gte": dt_inicio, "$lte": dt_fim}
    }))

    if not partidas:
        print("⚠️ Nenhuma batalha encontrada no intervalo.")
        return

    total_batalhas = 0
    contador_combos = Counter()

    for p in partidas:
        vencedor = p["vencedor"]
        deck = p["deck_1"] if vencedor == p["jogador_1"]["nickname"] else p["deck_2"]
        combos = combinations(sorted(deck), n)
        for c in combos:
            contador_combos[c] += 1
        total_batalhas += 1

    print(f"\n📊 Combos de {n} cartas com mais de {perc_min}% de vitórias:\n")

    encontrou = False
    for combo, freq in contador_combos.items():
        perc = (freq / total_batalhas) * 100
        if perc >= perc_min:
            encontrou = True
            print(f"🔥 Combo: {combo} — {freq} vitórias ({perc:.2f}%)")

    if not encontrou:
        print("😶 Nenhum combo com os critérios foi encontrado.")
