from etl_cards import inserir_cartas
from etl_players import inserir_jogadores
from etl_battles import inserir_batalhas

def rodar_etl():
    print("\n=== PAINEL DE CONTROLE - ETL CLASH ROYALE ===")
    
    print("\n🃏 Inserindo cartas...")
    inserir_cartas()
    print("✅ Cartas inseridas com sucesso!")

    print("\n👤 Inserindo jogadores...")
    inserir_jogadores()
    print("✅ Jogadores inseridos com sucesso!")

    print("\n⚔️ Inserindo batalhas reais...")
    inserir_batalhas()
    print("✅ Batalhas reais inseridas com sucesso!")

    print("\n✨ ETL finalizada!\n")

if __name__ == "__main__":
    rodar_etl()
