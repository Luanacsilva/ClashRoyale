from __future__ import annotations
import os
from typing import Any, Dict
import pandas as pd
import requests
import streamlit as st

BASE_URL = os.getenv("Interface Clash Royale", "http://127.0.0.1:5000")

ENDPOINTS: Dict[str, Dict[str, Any]] = {
    "Porcentagem de vitória por carta": {
        "path": "/porcentagem_carta",
        "params": {"carta": "Tornado", "limite": 8},
        "needs_dates": True,
    },
    "Decks vitoriosos (> X% vitórias)": {
        "path": "/decks_vitoriosos",
        "params": {"percentual": 60, "limite": 10},
        "needs_dates": True,
    },
    "Cartas mais usadas em derrotas": {
        "path": "/cartas_mais_usadas_derrotas",
        "params": {"limite": 10},
        "needs_dates": True,
    },
    "Vitórias com desvantagem": {
        "path": "/vitorias_com_desvantagem",
        "params": {"carta": "Golem", "desvantagem_minima": 20},
        "needs_dates": False,
    },
    "Combos de cartas com ≥ X% de vitórias": {
        "path": "/combos_vencedores_n_cartas",
        "params": {
            "porcentagem_minima": 2,
            "elixir_min": 1,
            "tamanho_combo": 3,
        },
        "needs_dates": True,
    },
}

st.set_page_config(page_title="Clash Royale Dashboard", layout="wide")
st.title("📊 Clash Royale – Consultas API")


with st.form("consulta_form"):
    opt = st.selectbox("🔍 Escolha a consulta", list(ENDPOINTS))
    cfg = ENDPOINTS[opt]
    params = cfg["params"].copy()

    if cfg.get("needs_dates", False):
        d1 = st.date_input("Data inicial", value=pd.to_datetime("2025-01-01").date(), key=f"{opt}-d1")
        d2 = st.date_input("Data final",   value=pd.to_datetime("2025-12-31").date(), key=f"{opt}-d2")
        # converter pro formato ISO que o back-end espera
        params["data_inicio"] = d1.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        params["data_fim"]    = d2.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # limites e percentuais
    if "limite" in params:
        params["limite"] = st.slider("Limite", 1, 30, params["limite"], key=f"{opt}-lim")
    if "percentual" in params:
        params["percentual"] = st.slider("% mínimo vitórias", 1, 100, params["percentual"], key=f"{opt}-pct")
    if "porcentagem_minima" in params:
        params["porcentagem_minima"] = st.slider("% mínimo vitórias", 1, 100, params["porcentagem_minima"], key=f"{opt}-pct2")

    # carta / desvantagem
    if "carta" in params:
        params["carta"] = st.text_input("Carta", params["carta"], key=f"{opt}-carta")
    if "desvantagem_minima" in params:
        params["desvantagem_minima"] = st.slider("Desvantagem %", 1, 100, params["desvantagem_minima"], key=f"{opt}-desv")

    # elixir_min e tamanho_combo (Consulta 5)
    if "elixir_min" in params:
        params["elixir_min"] = st.number_input("Elixir mínimo por carta", min_value=1, value=params["elixir_min"], key=f"{opt}-elixir")
    if "tamanho_combo" in params:
        params["tamanho_combo"] = st.number_input("Tamanho do combo", min_value=1, value=params["tamanho_combo"], key=f"{opt}-tcombo")

    submitted = st.form_submit_button("Executar consulta")

if submitted:
    url = f"{BASE_URL}{cfg['path']}"
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        st.success("✅ Consulta realizada com sucesso!")

        if isinstance(data, list):
            st.dataframe(pd.DataFrame(data))
        elif isinstance(data, dict):
            st.json(data)
        else:
            st.write(data)

    except requests.exceptions.RequestException as exc:
        st.error(f"Erro na requisição: {exc}")
