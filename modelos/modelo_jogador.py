def validar_jogador(jogador):
    campos = ["nickname", "trofeus", "nivel", "tempo_jogo_meses"]
    for campo in campos:
        if campo not in jogador:
            print(f"❌ Jogador inválido: faltando campo {campo}")
            return False
    return True
0