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

    
    def create_tables(self):
        self.cursor.execute(tables.operations_table)
        self.cursor.execute(tables.client_table)
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


    def delete(self, table_postgres, column_name, column_value):
        try:
            query = f"DELETE FROM {table_postgres} WHERE {column_name} = %s"
            self.cursor.execute(query, (column_value,))
            self.connection.commit()
            print("Registro removido com sucesso!")

        except psycopg2.Error as e:
            print(e)


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
            
        except Exception as e:
            print(e)


    def update(self, tabela, id_registro, valores):
        try:
            columns = self.columns_table(tabela)
            set_clause = ", ".join(f"{column} = %s" for column in columns)
            query = f"UPDATE {tabela} SET {set_clause} WHERE id_operacao = %s"
            self.cursor.execute(query, valores)
            self.connection.commit()
            print("Registro alterado com sucesso!")

        except psycopg2.Error as e:
            print(e)

    def search_client_id(self, values):
        try:
            query = f"SELECT id_cliente FROM clients WHERE cpf = %s AND senha = %s"
            self.cursor.execute(query, values)
            data = self.cursor.fetchone()
            if data:
                return data[0]
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
        except Exception as e:
            print(e)

