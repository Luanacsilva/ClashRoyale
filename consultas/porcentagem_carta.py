from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

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
        print("❌ Data em formato inválido. Use dd/mm/aa.")
        return None

def consultar_porcentagem_carta():
    carta = input("Digite o nome da carta (ex: Giant): ")

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

    vitorias = 0
    derrotas = 0

    for p in partidas:
        if carta in p["deck_1"] or carta in p["deck_2"]:
            if carta in (p["deck_1"] if p["vencedor"] == p["jogador_1"]["nickname"] else p["deck_2"]):
                vitorias += 1
            else:
                derrotas += 1

    total = vitorias + derrotas

    if total == 0:
        print(f"⚠️ A carta '{carta}' não apareceu em nenhuma batalha no período.")
        return

    print(f"📊 Resultados da carta '{carta}':")
    print(f"🏆 Vitórias: {vitorias} ({vitorias / total * 100:.2f}%)")
    print(f"💀 Derrotas: {derrotas} ({derrotas / total * 100:.2f}%)")




