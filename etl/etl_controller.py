from etl.etl_cards import inserir_cartas
from etl.etl_players import inserir_jogadores
from etl.etl_battles import inserir_batalhas



def rodar_etl():
    print("🔄 Iniciando ETL...")
    inserir_cartas()
    print("✅ ETL de cartas finalizada!")

if __name__ == "__main__":
    rodar_etl()
    inserir_jogadores()
    inserir_batalhas()


