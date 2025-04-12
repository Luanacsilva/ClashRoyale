def validar_carta(carta):
    campos = ["name", "id", "elixirCost", "rarity"]
    for campo in campos:
        if campo not in carta:
            print(f"❌ Carta inválida, campo ausente: {campo}")
            return False
    return True
