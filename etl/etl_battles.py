"from __future__ import annotations"
from datetime import datetime
from typing import Iterable, List

import requests
from main import battles, headers

try:
    # Reaproveita a lista definida no ETL de players
    from etl.etl_players import PLAYER_TAGS as _DEFAULT_TAGS 
    PLAYER_TAGS: List[str] = list(_DEFAULT_TAGS)
except Exception:
    PLAYER_TAGS = [
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
        "#8GLURVU2",
    ]

API_BASE = "https://api.clashroyale.com/v1/players"
TIMEOUT = 15  


def _tag_to_url(tag: str) -> str:
    return f"{API_BASE}/{tag.replace('#', '%23')}/battlelog"


def _fetch(url: str) -> list[dict]:
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()  
    except requests.exceptions.RequestException as exc:
        print(f"❌ {url}: {exc}")
        return []


def _flatten(it: Iterable[list[dict]]) -> list[dict]:
    return [b for sub in it for b in sub]


def inserir_batalhas(tags: List[str] | None = None, *, refresh: bool = False) -> None:
   
    tags = tags or PLAYER_TAGS

    if refresh:
        battles.delete_many({})
        print("🧹 Collection 'battles' limpa.")

    urls = [_tag_to_url(t) for t in tags]
    docs = _flatten(_fetch(u) for u in urls)
    if not docs:
        print("⚠️ Nenhum dado obtido.")
        return

    for d in docs:
        tag = d.get("team", [{}])[0].get("tag") or d.get("playerTag")
        bt = d.get("battleTime")
        if not tag or not bt:
            continue
        _id = f"{tag}_{bt}"
        d.update({"_id": _id, "importedAt": datetime.utcnow()})
        battles.replace_one({"_id": _id}, d, upsert=True)

    print(f"✅ Collection 'battles' → {battles.count_documents({})} documentos.")


if __name__ == "__main__":
    inserir_batalhas(refresh=True)