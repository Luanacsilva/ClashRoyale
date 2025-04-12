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

def consultar_vitorias_rapidas():
    try:
        tempo_limite = int(input("Mostrar vitórias com duração menor que (segundos): "))
    except ValueError:
        print("❌ Valor inválido.")
        return

    partidas = list(colecao.find({
        "duracao_segundos": {"$lt": tempo_limite}
    }))

    if not partidas:
        print("⚠️ Nenhuma batalha rápida encontrada com esse critério.")
        return

    print(f"\n⚡ Vitórias com duração menor que {tempo_limite} segundos:\n")

    for p in partidas:
        vencedor = p["vencedor"]
        if vencedor == p["jogador_1"]["nickname"]:
            oponente = p["jogador_2"]["nickname"]
        else:
            oponente = p["jogador_1"]["nickname"]
        tempo = p["duracao_segundos"]

        print(f"🏆 {vencedor} venceu {oponente} em {tempo} segundos")
