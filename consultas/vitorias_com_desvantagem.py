from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

# Conexão
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

def consultar_vitorias_com_desvantagem():
    carta = input("Digite o nome da carta (ex: Giant): ")
    try:
        porcentagem = float(input("Digite a porcentagem de desvantagem em troféus (ex: 20): "))
    except ValueError:
        print("❌ Valor inválido para porcentagem.")
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

    contador = 0

    for p in partidas:
        j1, j2 = p["jogador_1"], p["jogador_2"]
        vencedor = p["vencedor"]

        # Identificar quem venceu e quem perdeu
        if vencedor == j1["nickname"]:
            v, pdd = j1, j2
            deck_v = p["deck_1"]
            torres_p = p["torres_derrubadas_2"]
        else:
            v, pdd = j2, j1
            deck_v = p["deck_2"]
            torres_p = p["torres_derrubadas_1"]

        # Verificações da regra
        trofeus_diff = ((pdd["trofeus"] - v["trofeus"]) / pdd["trofeus"]) * 100
        duracao_ok = p["duracao_segundos"] < 120
        torres_ok = torres_p >= 2
        carta_ok = carta in deck_v

        if trofeus_diff >= porcentagem and duracao_ok and torres_ok and carta_ok:
            contador += 1

    print(f"\n📊 {contador} vitória(s) com desvantagem e uso da carta '{carta}' foram encontradas.")
