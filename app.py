from __future__ import annotations
from datetime import date, datetime, time
from typing import Callable, Union, Optional, List, Dict, Any
import streamlit as st

# CSS
st.markdown('''<style>
  /* Esconde as tabs nativas */
  .stTabs { display: none !important; }

  /* Selectbox como botão-dropdown */
  [data-baseweb="select"] {
    width: auto !important;
    display: inline-block;
    margin: 1rem 0;
  }
  [data-baseweb="select"] .css-1hwfws3,
  [data-baseweb="select"] .css-1u0x6y5 {
    background-color: #ff4b4b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    cursor: pointer;
  }
  [data-baseweb="select"] .css-1uccc91-singleValue {
    color: #fff !important;
    font-weight: 500;
  }
  [data-baseweb="select"] .css-1n76uvr-menu {
    background-color: #1f1f1f !important;
    border: 1px solid #333 !important;
    border-radius: 6px !important;
    margin-top: 0.2rem !important;
  }
  [data-baseweb="select"] .css-1n76uvr-option {
    color: #eee !important;
    padding: 0.5rem 1rem !important;
  }
  [data-baseweb="select"] .css-1n76uvr-option:hover {
    background-color: #333 !important;
  }

  /* Dark theme geral e botões */
  html, body, [class*="css"] {
    background-color: #121212;
    color: #eee;
    font-family: 'Roboto', sans-serif;
  }
  .stButton > button {
    background-color: #ff4b4b;
    color: #fff;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    border: none;
    transition: background-color 0.2s;
  }
  .stButton > button:hover {
    background-color: #e04343;
  }
  .metric-container {
    background-color: #1f1f1f !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 0.8rem !important;
    margin-bottom: 1rem !important;
  }
</style>''', unsafe_allow_html=True)
# FIM CSS 

from main import db 
from consultas.porcentagem_carta import porcentagem_carta
from consultas.decks_vitoriosos import decks_vitoriosos
from consultas.cartas_mais_usadas_derrotas import cartas_mais_usadas_derrotas
from consultas.vitorias_com_desvantagem import vitorias_com_desvantagem
from consultas.combos_vencedores_n_cartas import combos_vencedores_n_cartas
from consultas.cartas_mais_usadas_em_decks_completos import cartas_mais_usadas_em_decks_completos
from consultas.cartas_usadas_por_top_players import cartas_usadas_por_top_players
from consultas.combos_derrota import combos_derrota

def to_datetime(d: date | datetime, start: bool = True) -> datetime:
    if isinstance(d, datetime):
        return d
    t = datetime.min.time() if start else datetime.max.time()
    return datetime.combine(d, t)


def show_metrics(pairs: list[tuple[str, Union[int, float, str]]]) -> None:
    cols = st.columns(min(3, len(pairs)))
    for col, (label, val) in zip(cols, pairs):
        col.metric(label, val)

def aba_consulta1() -> None:
    st.subheader("% de vitórias e derrotas usando uma carta")
    cartas_disponiveis = sorted(db["battles"].distinct("team.cards.name"))
    carta = st.selectbox("Carta:", cartas_disponiveis)
    d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c1s")
    d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c1e")
    if st.button("Executar", key="c1"):
        try:
            res = porcentagem_carta(db, carta, to_datetime(d_ini), to_datetime(d_fim, False))
            if res:
                r = res[0]
                show_metrics([
                    ("Vitórias", r["vitorias"]),
                    ("Derrotas", r["derrotas"]),
                    ("Taxa %",   f"{r['taxa_vitorias']}"),
                ])
            else:
                st.info("Nenhum dado encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta2() -> None:
    st.subheader("Decks com ≥ X% de vitórias")
    pct = st.slider("Percentual mínimo", 1, 100, 60, key="c2pct")
    d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c2s")
    d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c2e")
    if st.button("Executar", key="c2"):
        try:
            res = decks_vitoriosos(db, pct, to_datetime(d_ini), to_datetime(d_fim, False))
            if res:
                for i, d in enumerate(res, 1):
                    st.markdown(f"### Deck {i}")
                    show_metrics([
                        ("Taxa %",   d["taxaVitorias"]),
                        ("Vitórias", d["totalVitorias"]),
                        ("Partidas", d["totalPartidas"]),
                    ])
                    st.write("Cartas:", d["deck"])
                    st.markdown("---")
            else:
                st.warning("Nenhum deck atende ao corte.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta3() -> None:
    st.subheader("Derrotas com combo fixo de cartas")
    combo = ["Musketeer", "Skeletons", "Miner"]
    st.write("Cartas do combo:", ", ".join(combo))
    d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c3s")
    d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c3e")
    if st.button("Executar", key="c3"):
        try:
            res = cartas_mais_usadas_derrotas(db, combo, to_datetime(d_ini), to_datetime(d_fim, False))
            if res:
                r = res[0]
                show_metrics([
                    ("Partidas", r["totalPartidas"]),
                    ("Derrotas", r["totalDerrotas"]),
                    ("Taxa %",   f"{r['taxaDerrotas']}"),
                ])
            else:
                st.info("Nenhum resultado encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta4() -> None:
    st.subheader("Vitórias com desvantagem de troféus")
    carta = st.text_input("Carta", "Golem", key="c4c")
    diff = st.slider("Desvantagem mínima %", 1, 100, 20, key="c4d")
    if st.button("Executar", key="c4"):
        try:
            qtd = vitorias_com_desvantagem(db, carta, diff)
            st.success(f"Vitórias: {qtd}")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta5() -> None:
    st.subheader("Combos de cartas com ≥ X% de vitórias")
    d_ini = st.date_input("Data inicial", date(2025, 4, 1), key="c5s")
    d_fim = st.date_input("Data final",   date(2025, 4, 19), key="c5e")
    pct = st.slider("Porcentagem mínima %", 1, 100, 2, key="c5pct")
    if st.button("Executar", key="c5"):
        try:
            res = combos_vencedores_n_cartas(db, to_datetime(d_ini), to_datetime(d_fim, False), pct)
            if res:
                st.write(f"{len(res)} combos encontrados:")
                for c in res:
                    st.write(f"• {', '.join(c['combo'])} — {c['percent']}% ({c['count']})")
            else:
                st.warning("Nenhum combo atende.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta6() -> None:
    st.subheader("Cartas mais usadas em decks completos")
    limite = st.slider("Limite de cartas", 1, 30, 10, key="c6lim")
    if st.button("Executar", key="c6"):
        try:
            resultados = cartas_mais_usadas_em_decks_completos(db, limite)
            if resultados:
                st.dataframe(resultados)
            else:
                st.info("Nenhum dado encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta7() -> None:
    st.subheader("Cartas mais usadas por top players (6000+ troféus)")
    limite = st.slider("Limite de cartas", 1, 30, 10, key="c7lim")
    if st.button("Executar", key="c7"):
        try:
            resultados = cartas_usadas_por_top_players(db, limite)
            if resultados:
                st.dataframe(resultados)
            else:
                st.info("Nenhum dado encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")


def aba_consulta8() -> None:
    st.subheader("Combos de 2 cartas mais frequentes em derrotas")
    limite = st.slider("Limite de combos", 1, 30, 10, key="c8lim")
    if st.button("Executar", key="c8"):
        try:
            resultados = combos_derrota(db, limite)
            if resultados:
                st.dataframe(resultados)
            else:
                st.info("Nenhum dado encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")


# ------------------------------------------------------------------
# DROPDOWN DE NAVEGAÇÃO
# ------------------------------------------------------------------
CONSULTAS_MAP: dict[str, Callable[[], None]] = {
    "Consulta 1 — Porcentagem de vitória por carta":               aba_consulta1,
    "Consulta 2 — Decks vitoriosos":                  aba_consulta2,
    "Consulta 3 — Derrotas fixas":                    aba_consulta3,
    "Consulta 4 — Vitórias c/ desvantagem":           aba_consulta4,
    "Consulta 5 — Combos vencedores":                 aba_consulta5,
    "Consulta 6 — Decks completos":        aba_consulta6,
    "Consulta 7 — Cartas top players":                aba_consulta7,
    "Consulta 8 — Combos em derrotas ":     aba_consulta8,
}

selecionada = st.selectbox(
    "🔍 Escolha a consulta",
    list(CONSULTAS_MAP.keys()),
    index=0
)
CONSULTAS_MAP[selecionada]()
