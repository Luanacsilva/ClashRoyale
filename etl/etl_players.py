from __future__ import annotations
from typing import List
import requests

from main import headers, players

PLAYER_TAGS: List[str] = [
    "#PCJ29YJJ",
    "#G9YV9GR8R",
    "#JQPLJ9GRP",
    "#290VGG28",
    "#PURLRYVJ2",
    "#PP0VL8LC",
    "#9GJ0Q0LGG",
    "#R9QJRCY",
    "#2YGQVGQ9",
    "#202RU2GLC",
    "#8GLURVU2"

]

API_BASE = "https://api.clashroyale.com/v1/players"


def _tag_to_url(tag: str) -> str:
    """Converte tag → URL da API."""
    return f"{API_BASE}/{tag.replace('#', '%23')}"

def inserir_jogadores(tags: List[str] | None = None, *, refresh: bool = True) -> None:
    
    tags = tags or PLAYER_TAGS

    if refresh:
        players.delete_many({})
        print("🧹 Collection 'players' limpa.")

    ok = err = 0
    for tag in tags:
        try:
            resp = requests.get(_tag_to_url(tag), headers=headers, timeout=15)
            resp.raise_for_status()
            data: dict = resp.json() 
            data["_id"] = data.get("tag", tag)
            players.replace_one({"_id": data["_id"]}, data, upsert=True)
            ok += 1
            print(f"✅ {data.get('name', tag)} inserido/atualizado.")
        except requests.exceptions.RequestException as exc:
            err += 1
            print(f"❌ Falha {tag}: {exc}")

    print(f"➜ Concluído: {ok} OK, {err} erro(s).")


if __name__ == "__main__":
    inserir_jogadores()