# 3) para operacoes: TEM que colocar o valor do id_operacao e id_cliente PRE DEFINIDO para fazer o update
#       bd.update("operations", 2, (id_operacao, data_nasc, id_cliente,"br", "c", 4, 15.0, value))
# 4) pode modificar os prints das funcoes da classe BD_POSTGRES, Para ficar legal na interface

import os
import time
from tabulate import tabulate
from .aplicacao_bd import Bd_postgres
from datetime import datetime as dt

class Interface:
    def __init__(self):
        self.bd = Bd_postgres()
        self.bd.create_connection()
        self.bd.create_tables()

    def menu_principal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Bem-vindo à sua carteira de investimentos! Digite o número correspondente ao que deseja fazer:\n")
        print("1. Cadastro")
        print("2. Login")
        print("3. Sair")

        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            self.cadastro()
        elif opcao == 2:
            id_cliente = self.login()
            if id_cliente:
                self.menu_carteira(id_cliente)
            else:
                self.menu_principal()
        elif opcao == 3:
            print("Finalizando o Programa")
            self.bd.disconnect()
        else:
            print("Opção inválida. Tente novamente.\n")
            time.sleep(1.5)
            self.menu_carteira()

    def cadastro(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\nCadastro:")
        name = input("Nome: ").upper()
        email = input("Email: ")

        data_input = input("Data de Nascimento (DD/MM/AAAA): ")
        try:
            birth = dt.strptime(data_input, "%d/%m/%Y")
        except ValueError:
            print("Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.\n")
            return

        cpf = input("CPF: ")
        senha = input("Senha: ")

        self.bd.inserir("clients", (name, email, birth, cpf, senha))
        print("Cadastro realizado com sucesso!\n")

        time.sleep(1.5)
        os.system("cls" if os.name == 'nt' else 'clear')

        id_cliente = self.bd.search_client_id((cpf, senha))
        if id_cliente != -1:
            self.menu_carteira(id_cliente)

    def login(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nLogin:")
        cpf = input("CPF: ")
        senha = input("Senha: ")
        id_cliente = self.bd.search_client_id((cpf, senha))
        if id_cliente:
            print("Login realizado com sucesso!\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return id_cliente
        else:
            print("CPF ou senha incorretos.\n")
            time.sleep(1.5)
            return None

    def menu_carteira(self, id_cliente):
        while True:
            print("\nVocê está na sua Carteira de Investimentos. O que deseja fazer?\n")

            print("1. Operação de Compra")
            print("2. Operação de Venda")
            print("3. Histórico de Operações")
            print("4. Mostrar Carteira Resumida")
            print("5. Mostrar Perfil")
            print("6. Sair")

            opcao = int(input("Escolha uma opção: "))
            if opcao == 1 or opcao == 2:
                self.operacao(id_cliente, opcao)
            elif opcao == 3:
                self.mostrar_historico_operacoes(id_cliente)
            elif opcao == 4:
                print("EM ANDAMENTO\n")
            elif opcao == 5:
                self.mostrar_cliente(id_cliente)
            elif opcao == 6:
                print("Você saiu da sua carteira com sucesso. Até a próxima!\n")
                time.sleep(1.5)
                self.menu_principal()
                break
            else:
                print("Opção inválida. Tente novamente.\n")

    def operacao(self, id_cliente, op):
        os.system('cls' if os.name == 'nt' else 'clear')
        operacao = "Compra" if op == 1 else "Venda"
        print(f"\nOperação de {operacao}:")
        ticker = input("Ativo: ").upper()
        quant = int(input("Quantidade: "))
        pMedio = float(input("Preço Médio: "))
        tt = quant * pMedio

        self.bd.inserir("operations", (dt.now().date(), id_cliente, ticker, operacao[0], quant, pMedio, tt))
        print(f"{operacao} cadastrada com sucesso!\n")

        time.sleep(1.5)
        os.system('cls' if os.name == 'nt' else 'clear')

        
    def mostrar_historico_operacoes(self, id_cliente):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Resultados:\n")
        # Mostrar informações da carteira do cliente
        carteira = self.bd.select_where("operations", id_cliente=str(id_cliente))
        if carteira != None:
            columns = list(self.bd.columns_table("operations"))
            print(tabulate(carteira, headers=columns, tablefmt="grid"))

            # for registro in carteira:
            #     print(f"ID: {registro[0]}, Data: {registro[1]}, Ativo: {registro[3]}, Quantidade: {registro[5]}, Preço Médio: R${registro[6]}, Total: R${registro[7]}")

            upd = input("\nDeseja alterar alguma Operação (y/n)? ").lower()

            if upd == "y":
                upd = input("\nDeseja Atualizar(A) ou Deletar(D): ").upper()

                if upd == "A" or upd == ("D"):

                    id_operacao = int(input("Operação (ID): "))

                    if self.bd.select_where("operations", id_cliente=str(id_cliente), id_operacao=str(id_operacao)):
                        if upd == "A":
                            self.atualizar_operacao(id_cliente, id_operacao)
                            print("Ativo atualizado com sucesso")
                        elif upd == "D":
                            self.bd.delete("operations", "id_operacao", id_operacao)
                            print("Ativo removido com sucesso")
                    else:
                        print("Esse ID não existe\n")
                else:
                    print("Opção Inválida")
        else:
            print("Você não possui ativos na carteira.\n")

        time.sleep(1.5)
        os.system('cls' if os.name == 'nt' else 'clear')

    
    def atualizar_operacao(self, id_cliente, id_operacao):
        print("\nAtualizando operação...")
        data_input = input("Nova data (DD/MM/AAAA): ")
        try:
            data = dt.strptime(data_input, "%d/%m/%Y")
        except ValueError:
            print("Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.\n")
            return
        ticker = input("Ticker: ").upper()
        operacao = input("Operação (C/V): ").upper()
        quant = int(input("Quantidade: "))
        p_medio = float(input("Preço Médio: "))
        total = quant * p_medio

        valores = {"data":data,"ticker":ticker,"operacao":operacao,"quant":quant,"p_medio":p_medio,"total":total}

        self.bd.update_especific("operations", valores, {"id_operacao":id_operacao})        

    def mostrar_cliente(self, id_cliente):
        os.system('cls' if os.name == 'nt' else 'clear')

        info_clinte = self.bd.select_where("clients", id_cliente=str(id_cliente))[0]

        print(f"""Número da Conta: {info_clinte[0]} \nNome: {info_clinte[1]} \nEmail: {info_clinte[2]} \nData Nascimento: {info_clinte[3]}\n""")
        
        upd = input("Deseja alterar alguma Infomação (y/n)? ").lower()
        
        if upd == 'y':
            print("\nEditar Cadastro:")
            email = input("Email: ")
            data_input = input("Data de Nascimento (DD/MM/AAAA): ")
            try:
                birth = dt.strptime(data_input, "%d/%m/%Y")
            except ValueError:
                print("Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.\n")
                return
            senha = input("Nova Senha: ")

            self.bd.update_especific("clients", {"email":email,"data_nasc":birth,"senha":senha}, {"id_cliente":id_cliente})

            time.sleep(1.5)
        

