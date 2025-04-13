from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]

print("Coleções disponíveis:", db.list_collection_names())
print("Total de batalhas:", db["battles"].count_documents({}))
