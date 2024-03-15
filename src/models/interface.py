# 1) fazer interface.py virar classe
# 2) chamar classe aplicacao_bd e interface na MAIN.py, o main deve está no arquivo main.py, na classe interfeca apenas as funções da interface
# 3) para operacoes: TEM que colocar o valor do id_operacao e id_cliente PRE DEFINIDO para fazer o update
#       bd.update("operations", 2, (id_operacao, data_nasc, id_cliente,"br", "c", 4, 15.0, value))
# 4) pode modificar os prints das funcoes da classe BD_POSTGRES, Para ficar legal na interface

from .aplicacao_bd import Bd_postgres
from datetime import datetime as dt

class Interface:
    def __init__(self):
        self.bd = Bd_postgres()
        self.bd.create_connection()

    def menu_principal(self):
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
        elif opcao == 3:
            print("Finalizando o Programa")
            self.bd.disconnect()
        else:
            print("Opção inválida. Tente novamente.\n")

    def cadastro(self):
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

        id_cliente = self.bd.search_client_id((cpf, senha))
        if id_cliente != -1:
            self.menu_carteira(id_cliente)

    def login(self):
        print("\nLogin:")
        cpf = input("CPF: ")
        senha = input("Senha: ")
        id_cliente = self.bd.search_client_id((cpf, senha))
        if id_cliente != -1:
            print("Login realizado com sucesso!\n")
            return id_cliente
        else:
            print("CPF ou senha incorretos.\n")
            return None

    def menu_carteira(self, id_cliente):
        while True:
            print("\nVocê está na sua Carteira de Investimentos. O que deseja fazer?\n")
            print("1. Operação de Compra")
            print("2. Operação de Venda")
            print("3. Histórico de Operações")
            print("4. Sair")

            opcao = int(input("Escolha uma opção: "))
            if opcao == 1 or opcao == 2:
                self.operacao(id_cliente, opcao)
            elif opcao == 3:
                self.mostrar_historico_operacoes(id_cliente)
            elif opcao == 4:
                print("Você saiu da sua carteira com sucesso. Até a próxima!\n")
                break
            else:
                print("Opção inválida. Tente novamente.\n")

    def operacao(self, id_cliente, op):
        operacao = "Compra" if op == 1 else "Venda"
        print(f"\nOperação de {operacao}:")
        ticker = input("Ativo: ").upper()
        quant = int(input("Quantidade: "))
        pMedio = float(input("Preço Médio: "))
        tt = quant * pMedio

        self.bd.inserir("operations", (dt.now().date(), id_cliente, ticker, operacao[0], quant, pMedio, tt))
        print(f"{operacao} cadastrada com sucesso!\n")

#Precisa consertar esse método
    # def mostrar_historico_operacoes(id_cliente):
    #     print("\nResultados:")
    #     # Mostrar informações da carteira do cliente
    #     carteira = bd.select_where("operations", "id_cliente", str(id_cliente))
    #     if carteira:
    #         print("\nInformações da carteira:")
    #         for registro in carteira:
    #             print(f"Ativo: {registro['ticker']}, Quantidade: {registro['Quant']}, Preço Médio: R${registro['P_Medio']}, Total: R${registro['total']}")
    #     else:
    #         print("Você não possui ativos na carteira.")

# Esse funciona, mas mostra os dados de forma errada
        
    def mostrar_historico_operacoes(self, id_cliente):
        print("\nResultados:")
        # Mostrar informações da carteira do cliente
        carteira = self.bd.select_where("operations", "id_cliente", str(id_cliente))
        if carteira:
            print("\nInformações da carteira:")
            for registro in carteira:
                # Supondo que a estrutura do resultado seja uma tupla, o acesso deve ser por índices
                # Mas se a estrutura for um dicionário (como parece ser o esperado), então algo está errado na execução ou explicação anterior
                print(f"Ativo: {registro[3]}, Quantidade: {registro[5]}, Preço Médio: R${registro[6]}, Total: R${registro[7]}")
        else:
            print("Você não possui ativos na carteira.")


    
    def atualizar_operacao(self, id_operacao):
        print("Atualizando operação...")
        data = input("Nova data (DD/MM/AAAA): ")
        id_cliente = input("ID do Cliente: ")
        ticker = input("Ticker: ").upper()
        operacao = input("Operação (C/V): ")
        quant = int(input("Quantidade: "))
        p_medio = float(input("Preço Médio: "))
        total = quant * p_medio

        valores = (data, id_cliente, ticker, operacao, quant, p_medio, total)
        self.bd.update("operations", id_operacao, valores)

