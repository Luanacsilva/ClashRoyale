from __future__ import annotations
from datetime import date, datetime
from typing import Callable, Union, List, Dict, Any
import streamlit as st

# CSS
st.markdown('''<style>
  /* Esconde as tabs nativas */
  .stTabs { display: none !important; }

  /* Importa fontes */
  @import url('https://fonts.googleapis.com/css2?family=Playwrite+AU+SA:wght@100..400&family=MedievalSharp&display=swap');

  /* Banner principal */
  .banner {
    font-family: 'MedievalSharp', cursive;
    font-size: 2.5rem;
    text-align: center;
    margin: 1rem 0;
    color: #ffcc00;
  }

  /* Subheaders das consultas */
  .subheader {
    font-family: 'Playwrite AU SA', sans-serif;
    font-size: 1.4rem !important;
    color: #fff !important;
    margin-top: 1rem;
  }

  /* Inputs de texto e data com largura fixa */
  .stTextInput > div, .stDateInput > div {
    max-width: 300px;
  }

  /* Centraliza botões */
  .button-center .stButton > button {
    margin: 1rem auto;
    display: block;
    width: 40%;
  }

  /* Dropdown estilizado */
  [data-baseweb="select"] {
    width: auto !important;
    display: inline-block;
    margin: 1rem 0 2rem;
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

  /* Botões customizados */
  .stButton > button {
    background-color: #ff4b4b;
    color: #fff;
    border-radius: 6px;
    padding: 0.6rem 1.2rem;
    border: none;
    transition: background-color 0.2s;
  }
  .stButton > button:hover {
    background-color: #e04343;
  }

  /* Tema escuro geral */
  html, body, [class*="css"] {
    background-color: #121212;
    color: #eee;
    font-family: 'Roboto', sans-serif;
  }

  /* Cards de métricas */
  .metric-container {
    background-color: #1f1f1f !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 0.8rem !important;
    margin-bottom: 1rem !important;
  }
</style>''', unsafe_allow_html=True)
# ---- FIM DO CSS ----

st.markdown('<div class="banner">🤴⚔️ Interface Clash Royale ⚔️🤴</div>', unsafe_allow_html=True)

# IMPORTAÇÃO DAS CONSULTAS
from main import db  
from consultas.porcentagem_carta import porcentagem_carta
from consultas.decks_vitoriosos import decks_vitoriosos
from consultas.cartas_mais_usadas_derrotas import cartas_mais_usadas_derrotas
from consultas.vitorias_com_desvantagem import vitorias_com_desvantagem
from consultas.combos_vencedores_n_cartas import combos_vencedores_n_cartas
from consultas.cartas_mais_usadas_em_decks_completos import cartas_mais_usadas_em_decks_completos
from consultas.cartas_usadas_por_top_players import cartas_usadas_por_top_players
from consultas.combos_derrota import combos_derrota

# HELPERS
def to_datetime(d: date | datetime, start: bool = True) -> datetime:
    if isinstance(d, datetime):
        return d
    return datetime.combine(d, datetime.min.time() if start else datetime.max.time())


def show_metrics(pairs: list[tuple[str, Union[int, float, str]]]) -> None:
    cols = st.columns(min(3, len(pairs)))
    for col, (label, val) in zip(cols, pairs):
        col.metric(label, val)

# renderização
def aba_consulta1() -> None:
    st.markdown('<div class="subheader">🏰 Consulta 1 — % vitória por carta</div>', unsafe_allow_html=True)
    cartas = sorted(db["battles"].distinct("team.cards.name"))
    carta = st.selectbox("Carta:", cartas)
    col1, col2 = st.columns(2)
    with col1:
        d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c1_s")
    with col2:
        d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c1_e")
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c1_btn"):
        with st.spinner("Carregando..."):
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
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta2() -> None:
    st.markdown('<div class="subheader">🛡️ Consulta 2 — Decks vitoriosos</div>', unsafe_allow_html=True)
    pct = st.slider("% mínimo vitórias", 1, 100, 60, key="c2_pct")
    col1, col2 = st.columns(2)
    with col1:
        d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c2_s")
    with col2:
        d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c2_e")
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c2_btn"):
        with st.spinner("Carregando..."):
            res = decks_vitoriosos(db, pct, to_datetime(d_ini), to_datetime(d_fim, False))
        if res:
            for i, d in enumerate(res, 1):
                st.markdown(f"#### Deck {i}")
                show_metrics([
                    ("Taxa %",   d["taxaVitorias"]),
                    ("Vitórias", d["totalVitorias"]),
                    ("Partidas", d["totalPartidas"]),
                ])
            st.markdown('---')
        else:
            st.warning("Nenhum deck atende.")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta3() -> None:
    st.markdown('<div class="subheader">⚔️ Consulta 3 — Derrotas fixas</div>', unsafe_allow_html=True)
    combo = ["Musketeer", "Skeletons", "Miner"]
    st.write("Cartas do combo:", ", ".join(combo))
    col1, col2 = st.columns(2)
    with col1:
        d_ini = st.date_input("Data inicial", date(2025, 1, 1), key="c3_s")
    with col2:
        d_fim = st.date_input("Data final",   date(2025, 12, 31), key="c3_e")
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c3_btn"):
        with st.spinner("Carregando..."):
            res = cartas_mais_usadas_derrotas(db, combo, to_datetime(d_ini), to_datetime(d_fim, False))
        if res:
            r = res[0]
            show_metrics([
                ("Partidas",   r["totalPartidas"]),
                ("Derrotas",   r["totalDerrotas"]),
                ("Taxa %",     f"{r['taxaDerrotas']}"),
            ])
        else:
            st.info("Nenhum resultado.")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta4() -> None:
    st.markdown('<div class="subheader">🔥 Consulta 4 — Vitórias c/ desvantagem</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        carta = st.text_input("Carta", "Golem", key="c4_card")
    with col2:
        diff = st.slider("Desvantagem %", 1, 100, 20, key="c4_diff")
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c4_btn"):
        with st.spinner("Carregando..."):
            qtd = vitorias_com_desvantagem(db, carta, diff)
        st.success(f"Vitórias: {qtd}")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta5() -> None:
    st.markdown('<div class="subheader">💎 Consulta 5 — Combos vencedores</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        d_ini = st.date_input("Data inicial", date(2025, 4, 1), key="c5_s")
    with col2:
        d_fim = st.date_input("Data final",   date(2025, 4, 19), key="c5_e")
    with col3:
        pct = st.slider("% mínimo", 1, 100, 2, key="c5_pct")
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c5_btn"):
        with st.spinner("Carregando..."):
            res = combos_vencedores_n_cartas(db, to_datetime(d_ini), to_datetime(d_fim, False), pct)
        if res:
            for c in res:
                st.write(f"• {', '.join(c['combo'])} — {c['percent']}% ({c['count']})")
        else:
            st.warning("Nenhum combo.")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta6() -> None:
    st.markdown('<div class="subheader">🔮 Consulta 6 — Decks completos (8 cartas)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: pass
    with col2:
        limite = st.slider("Limite", 1, 30, 10, key="c6_lim")
    with col3: pass
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c6_btn"):
        with st.spinner("Carregando..."):
            resultados = cartas_mais_usadas_em_decks_completos(db, limite)
        if resultados:
            st.dataframe(resultados)
        else:
            st.info("Nenhum dado.")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta7() -> None:
    st.markdown('<div class="subheader">🏹 Consulta 7 — Cartas top players</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: pass
    with col2:
        limite = st.slider("Limite", 1, 30, 10, key="c7_lim")
    with col3: pass
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c7_btn"):
        with st.spinner("Carregando..."):
            resultados = cartas_usadas_por_top_players(db, limite)
        if resultados:
            st.dataframe(resultados)
        else:
            st.info("Nenhum dado.")
    st.markdown('</div>', unsafe_allow_html=True)


def aba_consulta8() -> None:
    st.markdown('<div class="subheader">💥 Consulta 8 — Combos em derrotas (2 cartas)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: pass
    with col2:
        limite = st.slider("Limite", 1, 30, 10, key="c8_lim")
    with col3: pass
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button("Executar", key="c8_btn"):
        with st.spinner("Carregando..."):
            resultados = combos_derrota(db, limite)
        if resultados:
            st.dataframe(resultados)
        else:
            st.info("Nenhum dado.")
    st.markdown('</div>', unsafe_allow_html=True)

# DROPDOWN DE NAVEGAÇÃO
CONSULTAS_MAP: Dict[str, Callable[[], None]] = {
    "🏰 Consulta 1 — % vitória por carta":           aba_consulta1,
    "🛡️ Consulta 2 — Decks vitoriosos":             aba_consulta2,
    "⚔️ Consulta 3 — Derrotas fixas":               aba_consulta3,
    "🔥 Consulta 4 — Vitórias c/ desvantagem":      aba_consulta4,
    "💎 Consulta 5 — Combos vencedores":            aba_consulta5,
    "🔮 Consulta 6 — Decks completos (8 cartas)":   aba_consulta6,
    "🏹 Consulta 7 — Cartas top players":           aba_consulta7,
    "💥 Consulta 8 — Combos em derrotas (2 cartas)": aba_consulta8,
}

selecionada = st.selectbox(
    "🔍 Escolha a consulta",
    list(CONSULTAS_MAP.keys()),
    index=0,
)
CONSULTAS_MAP[selecionada]()

# RODAPÉ
st.markdown(
    "<div style='text-align:center; margin-top:2rem;'>"
    "<a href='https://github.com/Luanacsilva/ClashRoyale' "
    "style='color:#ffcc00; text-decoration:none;'>"
    "🔗 Repositório no GitHub"  
    "</a></div>",
    unsafe_allow_html=True
)
