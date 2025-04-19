import os
from dotenv import load_dotenv

# ETLs
from etl.etl_cards import inserir_cartas
from etl.etl_battles import inserir_batalhas
from etl.etl_players import inserir_jogadores

# CONSULTAS OBRIGATÓRIAS
from consultas.porcentagem_carta import main as consultar_porcentagem_carta
from consultas.decks_vitoriosos import main as consultar_decks_vitoriosos
from consultas.combos_derrota import main as consultar_combos_derrota
from consultas.vitorias_com_desvantagem import main as consultar_vitorias_com_desvantagem
from consultas.combos_vencedores_n_cartas import main as consultar_combos_vencedores

# CONSULTAS EXTRAS
from consultas.cartas_mais_usadas_derrotas import main as consultar_cartas_mais_usadas_derrotas
from consultas.cartas_mais_usadas_em_decks_completos import main as consultar_cartas_em_decks
from consultas.cartas_usadas_por_top_players import main as consultar_top_players

def menu():
    while True:
        print("\n=== 🛠️ PAINEL DE CONTROLE - CLASH ROYALE & MONGODB ===")
        print("1 - Inserir cartas da API")
        print("2 - Inserir batalhas reais")
        print("3 - Inserir jogadores")
        print("4 - Executar consultas analíticas")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            inserir_cartas()
        elif opcao == "2":
            inserir_batalhas()
        elif opcao == "3":
            inserir_jogadores()
        elif opcao == "4":
            print("\n--- 📊 CONSULTAS ANALÍTICAS ---")
            print("OBRIGATÓRIAS:")
            print("  1 - Porcentagem de vitórias por carta")
            print("  2 - Decks com maior taxa de vitórias")
            print("  3 - Combos mais comuns em derrotas")
            print("  4 - Vitórias com desvantagem de troféus")
            print("  5 - Combos com N cartas com mais de Y% de vitórias")
            print("EXTRAS:")
            print("  6 - Cartas mais usadas em derrotas")
            print("  7 - Cartas mais frequentes em decks completos")
            print("  8 - Cartas mais usadas pelos top players")

            sub = input("\nEscolha a consulta desejada: ")

            match sub:
                case "1": consultar_porcentagem_carta()
                case "2": consultar_decks_vitoriosos()
                case "3": consultar_combos_derrota()
                case "4": consultar_vitorias_com_desvantagem()
                case "5": consultar_combos_vencedores()
                case "6": consultar_cartas_mais_usadas_derrotas()
                case "7": consultar_cartas_em_decks()
                case "8": consultar_top_players()
                case _: print("❌ Subopção inválida.")
        elif opcao == "0":
            print("\n👋 Saindo do sistema... Até mais, lenda!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    load_dotenv()
    menu()
