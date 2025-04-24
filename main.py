from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Variáveis de ambiente 
MongoDb = os.getenv("MongoDb")
CLASHROYALE_TOKEN = os.getenv("CLASHROYALE_TOKEN")

if MongoDb is None:
    raise EnvironmentError("Variável de ambiente 'MongoDb' não encontrada. Verifique seu .env.")

if CLASHROYALE_TOKEN is None:
    raise EnvironmentError("Variável de ambiente 'CLASHROYALE_TOKEN' não encontrada. Verifique seu .env.")

# Conexão MongoDB
client = MongoClient(MongoDb)
db = client["bd_clashroyale"]


# Cabeçalhos para requisições à API Clash Royale
headers: dict[str, str] = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CLASHROYALE_TOKEN}",
}

battles = db["battles"]
players = db["players"]