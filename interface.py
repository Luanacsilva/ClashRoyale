import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Interface Clash Royale", layout="wide")

# ESTILO
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

        html, body, [class*="css"] {
            font-family: 'UnifrakturCook', cursive;
            background-color: #0a0a0a;
            color: #f0f0f0;
        }

        .stApp {
            text-align: center;
        }

        h1 {
            font-family: 'UnifrakturCook', cursive;
            font-size: 48px;
            font-weight: bold;
            color: #f0f0f0;
        }

        .stButton > button {
            background-color: #0074d9;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 30px;
            font-family: 'UnifrakturCook', cursive;
        }

        .stButton > button:hover {
            background-color: #005bb5;
        }

        .stSlider > div > div > div {
            background: linear-gradient(90deg, #ff4136, #85144b) !important;
            height: 6px !important;
            border-radius: 5px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Clash Royale - Consultas</h1>", unsafe_allow_html=True)
st.markdown("---")

#ENDPOINTS
endpoints = {
    "Cartas mais usadas em derrotas": "/cartas_mais_usadas_em_derrotas",
    "Cartas mais usadas em decks completos": "/cartas_mais_usadas_em_decks_completos",
    "Cartas mais usadas por top players": "/cartas_usadas_por_top_players",
    "Combos de derrota": "/combos_derrota",
    "Combos vencedores (n=3, min 70%)": "/combos_vencedores_n_cartas",
    "Decks vitoriosos": "/decks_vitoriosos",
    "Porcentagem de vitória por carta": "/porcentagem_carta",
    "Vitórias com desvantagem": "/vitorias_com_desvantagem"
}

#INPUTS
opcao = st.selectbox("\U0001F50D Escolha uma consulta:", list(endpoints.keys()))
limite = st.slider("Quantos resultados mostrar?", 1, 20, 10)
params = {"limite": limite}

if opcao == "Combos vencedores (n=3, min 70%)":
    params["n"] = 3
    params["min_taxa"] = 70
#BOTÃO
if st.button("\U0001F50E Buscar"):
    try:
        response = requests.get(f"http://localhost:5000{endpoints[opcao]}", params=params)
        data = response.json()

        st.success("Consulta realizada com sucesso! ✅")

        # Caso especial: vitórias com desvantagem
        if isinstance(data, dict) and "vitorias_com_desvantagem" in data:
            info_geral = {
                "\U0001F3C6 Total de batalhas analisadas": data.get("total_batalhas_analisadas", 0),
                "❌ Removidas por falta de desvantagem de troféus": data.get("removidas_por_falta_de_desvantagem_de_trofeus", 0),
                "\U0001F4C9 Removidas por não ter vencido": data.get("removidas_por_nao_ter_vencido", 0),
                "\U0001F6E1️ Removidas por torres maiores ou iguais a 2": data.get("removidas_por_torres_maiores_ou_iguais_a_2", 0)
            }
            st.subheader("\U0001F4CA Estatísticas gerais")
            st.table(pd.DataFrame(info_geral.items(), columns=["Descrição", "Quantidade"]))

            vitorias = data["vitorias_com_desvantagem"]
            if vitorias:
                st.subheader("\U0001F4C9 Detalhamento das vitórias com desvantagem")
                st.dataframe(pd.DataFrame(vitorias))
            else:
                st.info("Nenhuma vitória com desvantagem encontrada.")

        else:
            st.subheader("\U0001F4CB Resultado")
            if isinstance(data, list):
                st.dataframe(pd.DataFrame(data))
            else:
                st.json(data)

    except Exception as e:
        st.error(f"❌ Erro ao buscar dados: {e}")