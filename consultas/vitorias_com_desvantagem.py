from pymongo import MongoClient
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["bd_clashroyale"]
    battles = db["battles"]

    print("\n🏅 VITÓRIAS COM DESVANTAGEM (MENOS TROFÉUS, <2 TORRES):\n")

    print("💡 O campo 'duration' não está presente nas batalhas reais fornecidas pela API oficial do Clash Royale.")
    print("   Por isso, a verificação de tempo foi desabilitada nesta consulta.\n")

    filtro_torres = 0
    filtro_trofeus = 0
    filtro_vitoria = 0
    total_candidatas = 0
    resultados = []

    batalhas = list(battles.find())

    for b in batalhas:
        try:
            team = b["team"][0]
            opponent = b["opponent"][0]

            total_candidatas += 1

            if team["crowns"] >= 2:
                filtro_torres += 1
                continue

            if team["startingTrophies"] >= opponent["startingTrophies"]:
                filtro_trofeus += 1
                continue

            if team["crowns"] <= opponent["crowns"]:
                filtro_vitoria += 1
                continue

            resultados.append({
                "trofeus_time": team["startingTrophies"],
                "trofeus_oponente": opponent["startingTrophies"],
                "crowns_time": team["crowns"],
                "crowns_oponente": opponent["crowns"],
            })

        except Exception as e:
            continue

    if not resultados:
        print("⚠️ Nenhuma vitória com desvantagem completa encontrada.\n")
        print("🧠 Filtros que eliminaram resultados:")
        print(f"🔺 torres_destruídas >= 2: {filtro_torres} batalhas")
        print(f"📉 não tinha desvantagem de troféus: {filtro_trofeus} batalhas")
        print(f"❌ não venceu a partida: {filtro_vitoria} batalhas")
    else:
        for r in resultados:
            print(f"🎯 Vitória com {r['trofeus_time']} troféus contra {r['trofeus_oponente']} "
                  f"(Coroas: {r['crowns_time']} x {r['crowns_oponente']})")

    print(f"\n🔍 Total de batalhas analisadas: {total_candidatas}")
    print("\n✅ Consulta executada com sucesso!\n")

# Isso evita execução acidental se importado em outros arquivos
if __name__ == "__main__":
    main()
