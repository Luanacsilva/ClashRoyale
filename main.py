import os
from dotenv import load_dotenv

from etl.etl_cards import inserir_cartas
from etl.etl_battles import inserir_batalhas

# Importa as consultas com a função main renomeada
from consultas.porcentagem_carta import main as consultar_porcentagem_carta
from consultas.decks_vitoriosos import main as consultar_decks_vitoriosos
from consultas.combos_derrota import main as consultar_combos_derrota
from consultas.vitorias_com_desvantagem import main as consultar_vitorias_com_desvantagem
from consultas.combos_vencedores_n_cartas import main as consultar_combos_vencedores
from consultas.cartas_mais_usadas_derrotas import main as consultar_cartas_mais_usadas_derrotas
from consultas.vitorias_rapidas import main as consultar_vitorias_rapidas

def menu():
    while True:
        print("\n=== 🛠️ PAINEL DE CONTROLE DO CLASH ROYALE MONGO ===")
        print("1 - Inserir cartas da API")
        print("2 - Inserir batalhas reais")
        print("3 - Executar consulta analítica")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            inserir_cartas()
        elif opcao == "2":
            inserir_batalhas()
        elif opcao == "3":
            print("\n--- 📊 CONSULTAS ANALÍTICAS ---")
            print("1 - Porcentagem de vitórias por carta")
            print("2 - Decks com maior taxa de vitórias")
            print("3 - Combos mais comuns em derrotas")
            print("4 - Vitórias com desvantagem de troféus")
            print("5 - Combos com N cartas com mais de Y% de vitórias")
            print("6 - Cartas mais usadas em derrotas")
            print("7 - Vitórias em tempo recorde")
            sub = input("Escolha a consulta: ")

            if sub == "1":
                consultar_porcentagem_carta()
            elif sub == "2":
                consultar_decks_vitoriosos()
            elif sub == "3":
                consultar_combos_derrota()
            elif sub == "4":
                consultar_vitorias_com_desvantagem()
            elif sub == "5":
                consultar_combos_vencedores()
            elif sub == "6":
                consultar_cartas_mais_usadas_derrotas()
            elif sub == "7":
                consultar_vitorias_rapidas()
            else:
                print("❌ Subopção inválida.")
        elif opcao == "0":
            print("\n👋 Saindo do sistema... Até mais, lenda!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    load_dotenv()
    menu()
