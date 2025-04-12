from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
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

def consultar_combos_derrota():
    raw_combo = input("Digite as cartas do combo separadas por vírgula (ex: Mortar, Skeleton Army): ")
    combo = [c.strip() for c in raw_combo.split(",") if c.strip()]
    
    if len(combo) < 2:
        print("⚠️ Por favor, insira pelo menos 2 cartas.")
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

    derrotas_com_combo = []

    for p in partidas:
        vencedor = p["vencedor"]
        perdedor_deck = p["deck_1"] if vencedor == p["jogador_2"]["nickname"] else p["deck_2"]
        if all(carta in perdedor_deck for carta in combo):
            derrotas_com_combo.append(perdedor_deck)

    total = len(derrotas_com_combo)

    if total == 0:
        print("🥳 Nenhuma derrota encontrada com esse combo!")
    else:
        print(f"\n💀 Combo de derrota encontrado em {total} batalha(s):")
        for i, deck in enumerate(derrotas_com_combo, 1):
            print(f"{i}. {deck}")
