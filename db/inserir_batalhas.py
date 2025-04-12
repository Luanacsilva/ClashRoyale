import os
from dotenv import load_dotenv
from pymongo import MongoClient
from api.coletar_batalhas import gerar_lote_batalhas

# Carrega URI do MongoDB
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Conecta ao banco
client = MongoClient(MONGODB_URI)
db = client["bd_clashroyale"]
colecao = db["batalhas"]

def inserir_batalhas(qtd=10):
    batalhas = gerar_lote_batalhas(qtd)

    if not batalhas:
        print("⚠️ Nenhuma batalha gerada.")
        return

    resultado = colecao.insert_many(batalhas)
    print(f"✅ {len(resultado.inserted_ids)} batalhas inseridas com sucesso!")

# Teste direto
if __name__ == "__main__":
    inserir_batalhas(5)
