import random
import datetime
from api.coletar_cartas import coletar_cartas

def gerar_nickname():
    prefixos = ["Dark", "Pro", "Mega", "Fire", "Ultra", "King", "Noob", "Wizard"]
    sufixos = ["X", "007", "BR", "Lord", "Slayer", "Master", "YT"]
    return random.choice(prefixos) + random.choice(sufixos)

def gerar_jogador():
    return {
        "nickname": gerar_nickname(),
        "trofeus": random.randint(2000, 7000),
        "nivel": random.randint(8, 14),
        "tempo_jogo_meses": random.randint(3, 60)
    }

def gerar_deck(cartas):
    return random.sample([c["name"] for c in cartas], 8)

def gerar_batalha_simulada(cartas):
    jogador_1 = gerar_jogador()
    jogador_2 = gerar_jogador()
    deck_1 = gerar_deck(cartas)
    deck_2 = gerar_deck(cartas)

    torres_1 = random.randint(0, 3)
    torres_2 = random.randint(0, 3)

    vencedor = jogador_1["nickname"] if torres_1 > torres_2 else jogador_2["nickname"]

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "jogador_1": jogador_1,
        "jogador_2": jogador_2,
        "deck_1": deck_1,
        "deck_2": deck_2,
        "torres_derrubadas_1": torres_1,
        "torres_derrubadas_2": torres_2,
        "vencedor": vencedor,
        "duracao_segundos": random.randint(60, 360)
    }

def gerar_lote_batalhas(qtd=10):
    cartas = coletar_cartas()
    return [gerar_batalha_simulada(cartas) for _ in range(qtd)]

# Teste direto
if __name__ == "__main__":
    batalhas = gerar_lote_batalhas(5)
    for b in batalhas:
        print(f"{b['timestamp']} | Vencedor: {b['vencedor']} | Torres: {b['torres_derrubadas_1']} x {b['torres_derrubadas_2']}")
