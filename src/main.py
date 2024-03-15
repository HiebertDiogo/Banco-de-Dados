from models.aplicacao_bd import Bd_postgres
import models.interface ##TRANSFORMAR EM CLASSE
from datetime import datetime as dt


def main():
    
    bd = Bd_postgres()
    bd.create_connection()
    bd.disconnect()


if __name__ == "__main__":
    main()
