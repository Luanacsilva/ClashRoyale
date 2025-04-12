import os
from dotenv import load_dotenv

from db.inserir_cartas import inserir_cartas
from db.inserir_batalhas import inserir_batalhas
from consultas.porcentagem_carta import consultar_porcentagem_carta
from consultas.decks_vencedores import consultar_decks_vencedores
from consultas.combos_derrota import consultar_combos_derrota
from consultas.vitorias_com_desvantagem import consultar_vitorias_com_desvantagem
from consultas.combos_vencedores_n_cartas import consultar_combos_vencedores
from consultas.cartas_mais_usadas_derrotas import consultar_cartas_mais_usadas_derrotas
from consultas.vitorias_rapidas import consultar_vitorias_rapidas
from consultas.carta_carregadora import consultar_carta_carregadora

def menu():
    while True:
        print("\n=== PAINEL DE CONTROLE DO CLASH ROYALE MONGO ===")
        print("1 - Inserir cartas da API")
        print("2 - Gerar e inserir batalhas simuladas")
        print("3 - Executar consulta analítica")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            inserir_cartas()
        elif opcao == "2":
            try:
                qtd = int(input("Quantas batalhas deseja gerar? "))
                inserir_batalhas(qtd)
            except ValueError:
                print("❌ Valor inválido. Digite um número inteiro.")
        elif opcao == "3":
            print("\n--- CONSULTAS ANALÍTICAS ---")
            print("1 - Porcentagem de vitórias por carta")
            print("2 - Decks com X% de vitórias")
            print("3 - Derrotas com combo específico de cartas")
            print("4 - Vitórias com desvantagem (carta + troféus + tempo + torres)")
            print("5 - Combos de N cartas com mais de Y% de vitórias")
            print("6 - Cartas mais usadas em decks perdedores")
            print("7 - Vitórias em tempo recorde (menos de X segundos)")
            print("8 - Cartas mais 'carregadoras' dos decks vencedores")
            sub = input("Escolha a consulta: ")

            if sub == "1":
                consultar_porcentagem_carta()
            elif sub == "2":
                consultar_decks_vencedores()
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
            elif sub == "8":
                consultar_carta_carregadora()
            else:
                print("❌ Subopção inválida.")
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    load_dotenv()
    menu()
