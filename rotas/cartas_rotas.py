
from flask import Blueprint, request, jsonify, current_app
from consultas.cartas_mais_usadas_derrotas import cartas_mais_usadas_em_derrotas
from consultas.cartas_mais_usadas_em_decks_completos import cartas_mais_usadas_em_decks_completos

cartas_bp = Blueprint("cartas_bp", __name__)

# cartas mais usadas em derrotas
@cartas_bp.route("/cartas_mais_usadas_em_derrotas", methods=["GET"])
def rota_cartas_mais_usadas_em_derrotas():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = cartas_mais_usadas_em_derrotas(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# cartas mais usadas em decks completos
@cartas_bp.route("/cartas_mais_usadas_em_decks_completos", methods=["GET"])
def rota_cartas_mais_usadas_em_decks_completos():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = cartas_mais_usadas_em_decks_completos(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

#top players
from consultas.cartas_usadas_por_top_players import cartas_usadas_por_top_players

@cartas_bp.route("/cartas_usadas_por_top_players", methods=["GET"])
def rota_cartas_usadas_por_top_players():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = cartas_usadas_por_top_players(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Combos de derrotas 
from consultas.combos_derrota import combos_derrota

@cartas_bp.route("/combos_derrota", methods=["GET"])
def rota_combos_derrota():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = combos_derrota(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# vencedores n de cartas 
from consultas.combos_vencedores_n_cartas import combos_vencedores_n_cartas

@cartas_bp.route("/combos_vencedores_n_cartas", methods=["GET"])
def rota_combos_vencedores_n_cartas():
    try:
        db = current_app.db
        n = int(request.args.get("n", 3))
        min_taxa = float(request.args.get("min_taxa", 70))
        limite = int(request.args.get("limite", 10))
        resultado = combos_vencedores_n_cartas(db, n, min_taxa, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# decks vitoriosos
from consultas.decks_vitoriosos import decks_vitoriosos

@cartas_bp.route("/decks_vitoriosos", methods=["GET"])
def rota_decks_vitoriosos():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = decks_vitoriosos(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# vitória por carta
from consultas.porcentagem_carta import porcentagem_carta

@cartas_bp.route("/porcentagem_carta", methods=["GET"])
def rota_porcentagem_carta():
    try:
        db = current_app.db
        limite = int(request.args.get("limite", 10))
        resultado = porcentagem_carta(db, limite)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

#Vitórias com desvantagem

from consultas.vitorias_com_desvantagem import vitorias_com_desvantagem

@cartas_bp.route("/vitorias_com_desvantagem", methods=["GET"])
def rota_vitorias_com_desvantagem():
    try:
        db = current_app.db
        resultado = vitorias_com_desvantagem(db)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

