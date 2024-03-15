operations_table = """ CREATE TABLE IF NOT EXISTS operations (
                        id_operacao SERIAL PRIMARY KEY,
                        data DATE,
                        id_cliente INT,
                        ticker TEXT NOT NULL,
                        operacao CHAR(1),
                        Quant INT NOT NULL,
                        P_Medio NUMERIC NOT NULL,
                        Total NUMERIC )   """

client_table = """ CREATE TABLE IF NOT EXISTS clients (
                   id_cliente SERIAL PRIMARY KEY,
                   nome TEXT NOT NULL,
                   email TEXT NOT NULL,
                   data_nasc DATE NOT NULL,
                   cpf TEXT NOT NULL,
                   senha TEXT NOT NULL )"""

wallets_table = """ CREATE TABLE IF NOT EXISTS wallets (
                    id_carteira SERIAL PRIMARY KEY,
                    id_cliente INT,
                    ticker TEXT NOT NULL,
                    Quant INT,
                    P_Medio NUMERIC,
                    Total NUMERIC
)"""
