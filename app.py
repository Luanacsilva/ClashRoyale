from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# Garante que o Python encontre a pasta 'rotas'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa o Blueprint correto da pasta 'rotas'
from rotas.cartas_rotas import cartas_bp

# Carrega variáveis de ambiente
load_dotenv()

# Conecta ao MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bd_clashroyale"]

# Cria app Flask
app = Flask(__name__)
app.db = db  # Agora acessível em current_app.db

# Registra as rotas
app.register_blueprint(cartas_bp)

# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
