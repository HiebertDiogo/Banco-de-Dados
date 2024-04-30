import os
import json
import psycopg2
import sql.tables as tables

class Bd_postgres:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def create_connection(self, filename='credentials.json'):
        # Constrói o caminho até o arquivo de credenciais com base no local atual do script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, 'credentials', filename)

        with open(credentials_path, 'r') as file:
            data = json.load(file)

        self.connection = psycopg2.connect(
            dbname=data['NAME_BD'],
            user=data['USERNAME'],
            password=data['PASSWORD'],
            host=data['HOST'],
            port=data['PORT']
        )
        self.cursor = self.connection.cursor()
    

    def disconnect(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def update_wallets_table(self):
        try:
            query = """
            SELECT id_cliente, ticker, SUM(CASE WHEN operacao = 'C' THEN quant ELSE -quant END) AS quant, 
            AVG(p_medio) AS p_medio, SUM(CASE WHEN operacao = 'C' THEN quant * p_medio ELSE -(quant * p_medio) END ) AS total
            FROM operations
            GROUP BY id_cliente, ticker
            """
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            for row in data:
                id_cliente, ticker, quant, p_medio, total = row
                values = (id_cliente, ticker, quant, p_medio, total)
                existing_data = self.select_where("wallets", id_cliente=id_cliente, ticker=ticker)
                if existing_data:
                    self.update_especific("wallets", {"quant": quant, "p_medio": p_medio, "total": total},
                                            {"id_cliente": id_cliente, "ticker": ticker})
                else:
                    self.inserir("wallets", values)
            
            self.connection.commit()
            print("Tabela wallets atualizada com sucesso!")
        except psycopg2.Error as e:
            print(e)


    def create_procedure_truncate(self):
        sql = """
        CREATE OR REPLACE PROCEDURE truncate_table(table_name VARCHAR(100))
        AS $$
        BEGIN
            EXECUTE 'TRUNCATE TABLE ' || table_name;
        END;
        $$ LANGUAGE plpgsql;
        """

        self.cursor.execute(sql)
        self.connection.commit()
        print("procedure criada")

    def truncate_table(self, table_name):
        self.cursor.execute("CALL truncate_table(%s)", (table_name,))
        self.connection.commit()
        print("procedure chamada com sucesso")

    
    def update_wallets_table(self):
        try:
            query = """
            SELECT id_cliente, ticker, SUM(CASE WHEN operacao = 'C' THEN quant ELSE -quant END) AS quant, 
            AVG(p_medio) AS p_medio, SUM(CASE WHEN operacao = 'C' THEN quant * p_medio ELSE -(quant * p_medio) END ) AS total
            FROM operations
            GROUP BY id_cliente, ticker
            """
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            for row in data:
                id_cliente, ticker, quant, p_medio, total = row
                values = (id_cliente, ticker, quant, p_medio, total)
                existing_data = self.select_where("wallets", id_cliente=id_cliente, ticker=ticker)
                if existing_data:
                    self.update_especific("wallets", {"quant": quant, "p_medio": p_medio, "total": total},
                                            {"id_cliente": id_cliente, "ticker": ticker})
                else:
                    self.inserir("wallets", values)
            
            self.connection.commit()
            print("Tabela wallets atualizada com sucesso!")
        except psycopg2.Error as e:
            print(e)


    def create_procedure_truncate(self):
        sql = """
        CREATE OR REPLACE PROCEDURE truncate_table(table_name VARCHAR(100))
        AS $$
        BEGIN
            EXECUTE 'TRUNCATE TABLE ' || table_name;
        END;
        $$ LANGUAGE plpgsql;
        """

        self.cursor.execute(sql)
        self.connection.commit()
        print("procedure criada")

    def truncate_table(self, table_name):
        self.cursor.execute("CALL truncate_table(%s)", (table_name,))
        self.connection.commit()
        print("procedure chamada com sucesso")


    def create_tables(self):
        self.cursor.execute(tables.client_table)
        self.cursor.execute(tables.operations_table)
        self.cursor.execute(tables.wallets_table)

        self.connection.commit()


    def columns_table(self, table_postgres):
        try:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ORDINAL_POSITION"
            self.cursor.execute(query, (table_postgres,))
            columns = [row[0] for row in self.cursor.fetchall()]
            return columns
        
        except psycopg2.Error as e:
            print(e)
            return None


    def inserir(self, table_postgres, values):
        try:
            columns = self.columns_table(table_postgres)[1:]
            query = f"INSERT INTO {table_postgres} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))}) "
            
            self.cursor.execute(query, values)
            self.connection.commit()

        except psycopg2.Error as e:
            print(e)


    def delete(self, table_postgres, **kwargs):
        try:
            conditions = " AND ".join(f"{column} = %s" for column in kwargs.keys())

            query = f"DELETE FROM {table_postgres} WHERE {conditions}"
            values = tuple(kwargs.values())

            self.cursor.execute(query, values)
            self.connection.commit()

        except psycopg2.Error as e:
            print(e)

    # Seleciona tudo, dado as condições impostas.
    def select_where(self, table_postgres, **kwargs):
        try:
            conditions = " AND ".join(f"{column} = %s" for column in kwargs.keys())

            query = f"SELECT * FROM {table_postgres} WHERE {conditions}"
            values = tuple(kwargs.values())

            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            if data:
                return data
            else:
                return None
            
        except psycopg2.Error as e:
            print(e)

    # Busca UM valor em específico, dado as condições impostas.
    def search_especific_where(self, columns, table_postgres, **kwargs):
        try:
            conditions = " AND ".join(f"{column} = %s" for column in kwargs.keys())

            query = f"SELECT {columns} FROM {table_postgres} WHERE {conditions}"
            values = tuple(kwargs.values())

            self.cursor.execute(query, values)
            data = self.cursor.fetchone()
            return data
                
        except psycopg2.Error as e:
            print(e)

    # Seleciona todos os elementos únicos, dado as condições impostas.
    def select_distinct(self, column, table_postgres, **kwargs):
        try:
            conditions = " AND ".join(f"{column} = %s" for column in kwargs.keys())

            query = f"SELECT DISTINCT {column} FROM {table_postgres} WHERE {conditions}"
            values = tuple(kwargs.values())

            self.cursor.execute(query, values)
            data = [info[0] for info in self.cursor.fetchall()]

            if data:
                return data
            else:
                return None

        except psycopg2.Error as e:
            print(e)

    # set_values, where_values são dicionários
    # O primeiro atribui os valores a serem atualizados
    # O segundo atribui as condições para atualizar
    def update_especific(self, tabela, set_values, where_values):
        try:
            set_clause = ", ".join([f'{column} = %s' for column in set_values.keys()])
            where_conditions = " AND ".join([f'{cond} = %s' for cond in where_values.keys()])

            query = f'UPDATE {tabela} SET {set_clause} WHERE {where_conditions}'
            values = tuple(set_values.values()) + tuple(where_values.values())

            self.cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.Error as e:
            print(e)
    
    def update_wallets(self, id_cliente):
        def calculate_new_avg(operations_by_ticker):
            avg_price = quant = 0
            # operation[2] = quantidade ; operation[3] = preco medio
            for operation in operations_by_ticker:
                # Recalculando o novo preço médio e nova quantidade
                if operation[1] == 'C':
                    avg_price = (avg_price * quant + operation[3] * operation[2]) / (quant + operation[2])
                    quant = quant + operation[2]
                elif operation[1] == 'V':
                    # Vende menos do que possui
                    if operation[2] < quant:
                        avg_price = avg_price
                    # Vende tudo o que possui
                    elif operation[2] == quant: 
                        avg_price = 0
                    quant = quant - operation[2]
            return quant, round(avg_price, 2)
        
        try:
            # Seleciona todos os ativos que o usuario investe
            tickers = self.select_distinct("ticker", "operations", id_cliente=id_cliente)

            if tickers == None:
                return

            for ticker in tickers:
                # Filtra-se todas as operações envolvendo o ticker x do usuário
                query = f"SELECT o.ticker, o.operacao, o.quant, o.p_medio FROM operations o WHERE id_cliente = %s AND ticker = %s"
                self.cursor.execute(query, (id_cliente, ticker,))
                operations_by_ticker = self.cursor.fetchall() 

                # Com a lista obtida para todas as operacoes do ticker x, realizamos as contas
                quant_tt, avg = calculate_new_avg(operations_by_ticker)
                total = quant_tt*avg
                
                # Removemos de Wallets caso o Ativo não faça mais parte da carteira
                if quant_tt == 0:
                    self.delete("wallets", ticker=ticker, id_cliente=id_cliente)
                    continue
                # Atualizamos o novo valor para o ativo x
                self.update_especific("wallets",  {"quant":quant_tt, "p_medio":avg, "total":total}, 
                                      {"id_cliente":id_cliente, "ticker":ticker})

        except psycopg2.Error as e:
            print(e)