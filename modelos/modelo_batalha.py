def validar_batalha(batalha):
    campos = [
        "timestamp", "jogador_1", "jogador_2", "deck_1", "deck_2",
        "torres_derrubadas_1", "torres_derrubadas_2", "vencedor", "duracao_segundos"
    ]
    for campo in campos:
        if campo not in batalha:
            print(f"❌ Batalha inválida: faltando campo {campo}")
            return False
    return True
