import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]
players_collection = db["players"]

def inserir_jogadores():
    tags = [
    "#PCJ29YJJ",
    "#G9YV9GR8R",
    "#JQPLJ9GRP",
    "#290VGG28"]

  # pode adicionar mais tags aqui
    headers = {
        "Authorization": f"Bearer {os.getenv('CLASH_API_TOKEN')}"
    }

    players_collection.delete_many({})  # limpa antes

    for tag in tags:
        tag_url = tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{tag_url}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            player = response.json()
            players_collection.insert_one(player)
            print(f"✅ Jogador {player['name']} inserido!")
        else:
            print(f"❌ Erro com player {tag}: {response.status_code}")
