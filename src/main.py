from models.interface import Interface
from models.aplicacao_bd import Bd_postgres

def main():
    #Cria uma instância da classe Interface
    interface = Interface()
    # Chama o menu principal para iniciar a aplicação
    interface.menu_principal()
    # bd = Bd_postgres()
    # bd.create_connection()  # Certifique-se de criar a conexão antes de chamar update_wallets_table()
    # bd.update_wallets_table()
    # bd.disconnect()
if __name__ == "__main__":
    main()
