# 📊 Clash Royale MongoDB Analyser

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![MongoDB Atlas](https://img.shields.io/badge/MongoDB-Atlas-brightgreen?logo=mongodb)
![Clash Royale API](https://img.shields.io/badge/API-ClashRoyale-blueviolet?logo=cloudflare)
![Projeto Acadêmico](https://img.shields.io/badge/Feito_para-Faculdade-blue)
![Contributions](https://img.shields.io/badge/Contribui%C3%A7%C3%B5es-Bem%20vindas-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Backend%20Finalizado-brightgreen)

Este é um projeto acadêmico de banco de dados não relacional com foco em **análise estatística de batalhas do Clash Royale** utilizando a API oficial do jogo, armazenamento no **MongoDB Atlas** e execução via terminal em Python com interface interativa.

---

## 📦 Tecnologias Utilizadas

- Python 3.10+
- MongoDB Atlas (cloud)
- Pymongo
- Dotenv
- VSCode + Git Bash
- API oficial Clash Royale

---

## 🎯 Objetivo do Projeto

Analisar dados reais de partidas do Clash Royale com:
- Coleta e estruturação de dados com ETL
- Armazenamento no MongoDB Atlas
- Consultas analíticas sobre performance de cartas, decks e jogadores
- Interface interativa no terminal
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
│   ├── modelo_batalha.py
│   ├── modelo_carta.py
│   └── modelo_jogador.py
│
├── .env                          # Tokens e URI Mongo (NÃO subir)
├── .gitignore                    # Ignora arquivos sensíveis
├── LICENSE                       # Licença do projeto (MIT)
├── main.py                       # Painel de controle via CLI
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências
└── test_connection.py            # Teste de conexão MongoDB e Clash API
```

---

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

5. Rode o painel principal
```bash
python main.py
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

## 🖥️ Interface Interativa via Terminal

Menu ao executar `main.py`:

```bash
=== PAINEL DE CONTROLE DO CLASH ROYALE MONGO ===
1 - Inserir cartas da API
2 - Inserir jogadores
3 - Inserir batalhas reais
4 - Executar consulta analítica
0 - Sair
```

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

