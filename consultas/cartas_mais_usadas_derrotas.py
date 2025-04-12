from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from collections import Counter
import os

# Conecta ao Mongo
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

def consultar_cartas_mais_usadas_derrotas():
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

    cartas_derrota = Counter()

    for p in partidas:
        vencedor = p["vencedor"]
        deck_perdedor = p["deck_1"] if vencedor == p["jogador_2"]["nickname"] else p["deck_2"]
        cartas_derrota.update(deck_perdedor)

    print("\n💀 Cartas mais usadas em decks perdedores:\n")
    for carta, qtd in cartas_derrota.most_common(10):
        print(f"🔸 {carta}: {qtd} ocorrências")
