# 📊 Clash Royale MongoDB Analyser

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![MongoDB Atlas](https://img.shields.io/badge/MongoDB-Atlas-brightgreen?logo=mongodb)
![Clash Royale API](https://img.shields.io/badge/API-ClashRoyale-blueviolet?logo=cloudflare)
![Projeto Acadêmico](https://img.shields.io/badge/Feito_para-Faculdade-blue)
![Contributions](https://img.shields.io/badge/Contribui%C3%A7%C3%B5es-Bem%20vindas-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)


Este é um projeto acadêmico de banco de dados não relacional com foco em **análise estatística de batalhas do Clash Royale** utilizando a API oficial do jogo, armazenamento no **MongoDB Atlas** e execução via terminal em Python com interface interativa.

---

## 📦 Tecnologias Utilizadas

- Python 3.10+
- MongoDB Atlas (cloud)
- Pymongo
- Dotenv
- VSCode + Bash
- API oficial Clash Royale

---

## 🎯 Objetivo do Projeto

Simular e analisar estatísticas de partidas Clash Royale com:
- Armazenamento estruturado no MongoDB
- Consultas analíticas com foco em estratégia e balanceamento
- Relatórios de cartas, decks e vitórias com desvantagem
- Interface de linha de comando com menu interativo
- Arquitetura modular, limpa e escalável

---

### 🧱 Estrutura de Pastas

```bash
clash_royale_mongo/
│
├── api/                      # Scripts para coleta de dados da API e simulações
│   ├── coletar_cartas.py
│   └── coletar_batalhas.py
│
├── db/                       # Conexão com banco e inserção de dados
│   ├── conexao.py
│   ├── inserir_cartas.py
│   └── inserir_batalhas.py
│
├── consultas/                # Todas as consultas analíticas do projeto
│   ├── porcentagem_carta.py
│   ├── decks_vencedores.py
│   ├── combos_derrota.py
│   ├── vitorias_com_desvantagem.py
│   ├── combos_vencedores_n_cartas.py
│   ├── cartas_mais_usadas_derrotas.py
│   ├── vitorias_rapidas.py
│   └── carta_carregadora.py
│
├── main.py                   # Menu principal para executar todo o projeto
├── .env                      # Variáveis de ambiente (token + Mongo URI)
├── requirements.txt          # Bibliotecas necessárias
└── README.md                 # Este arquivo lindo aqui :)
```

### 🚀 Como Rodar o Projeto
1. Clone o repositório
```bash
git clone https://github.com/Luanacsilva/ClashRoyale.git
cd ClashRoyale
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/Scripts/activate  # ou venv/bin/activate no Linux/macOS
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o .env
   Crie um arquivo .env na raiz com o seguinte conteúdo:
```bash
MONGODB_URI=sua_string_de_conexao_mongo
CLASH_API_TOKEN=seu_token_da_api
```
---


### 🧪 Consultas Implementadas
✅ Requisitos obrigatórios:

1. Porcentagem de vitórias usando uma carta X em um intervalo de tempo

2. Decks que venceram com mais de X% de aproveitamento

3. Derrotas com combo de cartas específico

4. Vitórias com desvantagem em troféus, tempo e torres + carta usada

5. Combos de N cartas com mais de Y% de vitórias

## 💡 Consultas extras criativas:

1. Cartas mais usadas em decks perdedores

2. Vitórias com duração inferior a X segundos

3. Cartas "carregadoras": muito usadas em vitórias, raras nas derrotas
---

### 🖥️ Interface via terminal

Você pode rodar o sistema com:
```bash
python main.py
```
E terá acesso a um menu como este:
```bash
=== PAINEL DE CONTROLE DO CLASH ROYALE MONGO ===
1 - Inserir cartas da API
2 - Gerar e inserir batalhas simuladas
3 - Executar consulta analítica
0 - Sair
```
---

 ### 📈 Exemplo de Consulta (output)
```bash
Escolha a consulta: 1
Digite o nome da carta: Giant
Data de início: 10/04/25
Data de fim: 12/04/25

📊 Resultados da carta 'Giant':
🏆 Vitórias: 14 (63.64%)
💀 Derrotas: 8 (36.36%)
```
---
# ⚠️ Aviso

## Este projeto utiliza dados públicos da API do Clash Royale. Nenhum dado privado ou pessoal foi coletado.
## Recomenda-se o uso de um token pessoal limitado para testes.


---

##  🌟 Possibilidades Futuras

Visualização com Streamlit

Exportação de relatórios em .csv ou .pdf

Comparação de decks entre temporadas

API própria com FastAPI ou Flask

---

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](LICENSE).

