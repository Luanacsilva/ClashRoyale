def vitorias_com_desvantagem(db):
    """
    Retorna as vitórias em que o jogador tinha menos troféus e fez menos de 2 coroas,
    mas ainda assim venceu a partida.
    """
    resultados = []

    filtro_torres = 0
    filtro_trofeus = 0
    filtro_vitoria = 0
    total_candidatas = 0

    batalhas = db["battles"].find()

    for b in batalhas:
        try:
            team = b["team"][0]
            opponent = b["opponent"][0]
            total_candidatas += 1

            if team["crowns"] >= 2:
                filtro_torres += 1
                continue

            if team["startingTrophies"] >= opponent["startingTrophies"]:
                filtro_trofeus += 1
                continue

            if team["crowns"] <= opponent["crowns"]:
                filtro_vitoria += 1
                continue

            resultados.append({
                "trofeus_time": team["startingTrophies"],
                "trofeus_oponente": opponent["startingTrophies"],
                "crowns_time": team["crowns"],
                "crowns_oponente": opponent["crowns"],
            })

        except (KeyError, IndexError, TypeError):
            continue

    return {
        "total_batalhas_analisadas": total_candidatas,
        "removidas_por_torres_maiores_ou_iguais_a_2": filtro_torres,
        "removidas_por_falta_de_desvantagem_de_trofeus": filtro_trofeus,
        "removidas_por_nao_ter_vencido": filtro_vitoria,
        "vitorias_com_desvantagem": resultados
    }
