from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from collections import defaultdict, Counter

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
        print("❌ Data em formato inválido. Use dd/mm/aa.")
        return None

def consultar_decks_vencedores():
    try:
        limite = float(input("Porcentagem mínima de vitórias (ex: 60): "))
    except ValueError:
        print("❌ Valor inválido.")
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

    total_decks = 0
    decks_vitoriosos = Counter()

    for p in partidas:
        vencedor = p["vencedor"]
        deck = p["deck_1"] if vencedor == p["jogador_1"]["nickname"] else p["deck_2"]
        deck_key = tuple(sorted(deck))
        decks_vitoriosos[deck_key] += 1
        total_decks += 1

    print("\n📊 DECKS COM MAIS DE", limite, "% DE VITÓRIAS:\n")

    for deck, vitorias in decks_vitoriosos.items():
        porcentagem = (vitorias / total_decks) * 100
        if porcentagem >= limite:
            print(f"🏆 Deck: {deck}")
            print(f"   Vitórias: {vitorias}  ({porcentagem:.2f}%)\n")
