operations_table = """ CREATE TABLE IF NOT EXISTS operations (
                        id_compra SERIAL PRIMARY KEY,
                        data DATE,
                        id_cliente INT,
                        ticker CHAR(10) NOT NULL,
                        operacao CHAR(1),
                        Quant INT,
                        P_Medio NUMERIC,
                        Total NUMERIC )   """

client_table = """ CREATE TABLE IF NOT EXISTS clients (
                   id_cliente SERIAL PRIMARY KEY,
                   nome CHAR(80),
                   email CHAR(30),
                   data_nasc DATE,
                   cpf CHAR(12),
                   senha CHAR(20) )"""

wallets_table = """ CREATE TABLE IF NOT EXISTS wallets (
                    id_carteira SERIAL PRIMARY KEY,
                    id_cliente INT,
                    ticker CHAR(10) NOT NULL,
                    Quant INT,
                    P_Medio NUMERIC,
                    Total NUMERIC
)"""
