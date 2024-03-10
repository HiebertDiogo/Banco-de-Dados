operations_table = """ CREATE TABLE IF NOT EXISTS operations (
                        id_compra SERIAL PRIMARY KEY,
                        data DATE,
                        id_cliente INT,
                        ticker TEXT NOT NULL,
                        operacao TEXT,
                        Quant INT,
                        P_Medio NUMERIC,
                        Total NUMERIC )   """

client_table = """ CREATE TABLE IF NOT EXISTS clients (
                   id_cliente SERIAL PRIMARY KEY,
                   nome TEXT,
                   email TEXT,
                   data_nasc DATE,
                   cpf TEXT,
                   senha TEXT )"""

wallets_table = """ CREATE TABLE IF NOT EXISTS wallets (
                    id_carteira SERIAL PRIMARY KEY,
                    id_cliente INT,
                    ticker TEXT NOT NULL,
                    Quant INT,
                    P_Medio NUMERIC,
                    Total NUMERIC
)"""
