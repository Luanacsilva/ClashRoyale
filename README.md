# 📊 Clash Royale MongoDB Analyser

![Made with MongoDB](https://img.shields.io/badge/DB-MongoDB-green?logo=mongodb)
![Made with Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![Made with Streamlit](https://img.shields.io/badge/Interface-Streamlit-ff4b4b?logo=streamlit)
![ETL Ready](https://img.shields.io/badge/ETL-Pronto-blue)
![API Status](https://img.shields.io/badge/API%20Status-Online-brightgreen)
![MongoDB Status](https://img.shields.io/badge/MongoDB%20Status-Conectado-brightgreen)
![Env Protegido](https://img.shields.io/badge/.env-Seguro-important)
![Dados Reais](https://img.shields.io/badge/Dados-Reais-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Projeto acadêmico de banco de dados não relacional com foco em **análise estatística de batalhas do Clash Royale**, utilizando a API oficial do jogo, armazenamento no **MongoDB Atlas** e execução via **Flask, terminal interativo e interface com Streamlit**.

---

## 📦 Tecnologias Utilizadas

- Python 3.10+
- MongoDB Atlas (cloud)
- Pymongo
- Flask + Flask Blueprint
- Dotenv
- Streamlit
- VSCode + Git Bash
- API oficial Clash Royale

---

## 🎯 Objetivo do Projeto

Analisar dados reais de partidas do Clash Royale com:

- Coleta e estruturação de dados com ETL
- Armazenamento no MongoDB Atlas
- Consultas analíticas sobre performance de cartas, decks e jogadores
- Interface interativa no terminal e via Streamlit
- Rotas HTTP para consumo via front-end ou navegador
- Dados reais, sem simulação ou mock

---

## 🧱 Estrutura de Pastas

```bash
ClashRoyale/
│
├── api/                          # Scripts diretos de coleta
│   ├── coletar_cartas.py
│   └── coletar_batalhas.py
│
├── consultas/                    # Consultas analíticas (obrigatórias e extras)
│   ├── porcentagem_carta.py
│   ├── decks_vitoriosos.py
│   ├── combos_derrota.py
│   ├── vitorias_com_desvantagem.py
│   ├── combos_vencedores_n_cartas.py
│   ├── cartas_mais_usadas_derrotas.py
│   ├── cartas_mais_usadas_em_decks_completos.py
│   └── cartas_usadas_por_top_players.py
│
├── etl/                          # Extração, transformação e carga
│   ├── etl_cards.py
│   ├── etl_players.py
│   ├── etl_battles.py
│   └── etl_controller.py
│
├── modelos/                      # Validação de estrutura dos dados recebidos
│  
│
├── rotas/                        # Rotas HTTP com Flask Blueprint
│   └── cartas_rotas.py
│
├── .env                          # Tokens e URI Mongo (NÃO subir)
├── .gitignore                    # Ignora arquivos sensíveis
├── LICENSE                       # Licença do projeto (MIT)
├── app.py                        # Inicializa e executa o backend Flask
├── interface.py                  # Interface gráfica com Streamlit
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências
└── test_connection.py            # Teste de conexão MongoDB e Clash API
```

## 🚀 Como Rodar o Projeto

1. Clone o repositório
```bash
git clone https://github.com/Luanacsilva/ClashRoyale.git
cd ClashRoyale
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/Scripts/activate  # ou venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o .env
```bash
MONGODB_URI=sua_uri_do_mongo
CLASH_API_TOKEN=seu_token_api
```

5. Rode o backend Flask:
```bash
python app.py
```
Acesse no navegador:
```bash
http://localhost:5000
```

6. (Opcional) Rode a interface gráfica com Streamlit:
```bash
streamlit run interface.py
```
Acesse no navegador:
```bash
http://localhost:8501
```

---

# 📡 Rotas HTTP (via Flask)
Todas as consultas analíticas estão disponíveis como rotas GET retornando JSON.

Exemplo de uso:
```bash
http://localhost:5000/porcentagem_carta?limite=5
```

```bash
Endpoint                                                           Descrição

/cartas_mais_usadas_em_derrotas                                  Cartas mais frequentes entre derrotados

/cartas_mais_usadas_em_decks_completos                           Cartas mais frequentes em decks com 8 cartas

/cartas_usadas_por_top_players                                   Cartas mais usadas por jogadores com 6000+ troféus

/combos_derrota                                                   Combos de 2 cartas mais presentes em derrotas

/combos_vencedores_n_cartas                                      Combos de N cartas com X%+ de vitória

/decks_vitoriosos                                                 Decks com maior taxa de vitória

/porcentagem_carta                                                Taxa de vitórias por carta

/vitorias_com_desvantagem                                         Batalhas vencidas com desvantagem de torres e troféus
```

---

## 🧪 Consultas Implementadas

### ✅ Obrigatórias (conforme PDF da disciplina):

1. Porcentagem de vitórias por carta
2. Decks com maior taxa de vitórias
3. Combos mais comuns em derrotas
4. Vitórias com desvantagem (torres e troféus)
5. Combos com N cartas com mais de Y% de vitórias

### 💡 Extras criativas:

6. Cartas mais usadas em derrotas
7. Cartas mais frequentes em decks completos (8 cartas)
8. Cartas mais comuns entre jogadores com +6000 troféus

---

## ⚙️ Teste de Conexão

```bash
python test_connection.py
```
Verifica se a API e o MongoDB estão operando corretamente.

---

## ⚠️ Aviso

Este projeto utiliza dados **públicos** da API oficial Clash Royale. Nenhuma informação privada é acessada. Recomenda-se utilizar tokens limitados para segurança.

---

## 🌟 Possibilidades Futuras

- Front-end com visualização em Streamlit
- Comparativos entre jogadores e decks por temporada

---

## 📄 Licença

Distribuído sob os termos da [Licença MIT](LICENSE).

