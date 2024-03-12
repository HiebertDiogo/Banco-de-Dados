from aplicacao_bd import Bd_postgres
from datetime import datetime as dt

# Instância da classe Bd_postgres
bd = Bd_postgres(
    dbname="Wallet",
    user="Grupo BD",
    password="admin123",
    host="localhost",
    port=5432,
)

def menu_principal():
    print("Bem-vindo à sua carteira de investimentos! Digite o número correspondente ao que deseja fazer:\n")
    print("1. Cadastro")
    print("2. Login")
    print("3. Sair")


def cadastro():
    print("\nCadastro:")
    # Solicita informações do usuário para cadastro no banco
    name = input("Nome: ").upper()
    email = input("Email: ")
  
    data_input = input("Data de Nascimento (DD/MM/AAAA): ")
    try:
        birth = dt.strptime(data_input, "%d/%m/%Y")
    except ValueError:
        print("Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.\n")

    cpf = input("CPF: ")

    senha = input("Senha: ")

    # Insere as informações no banco de dados
    bd.inserir("clients", (name, email, birth, cpf, senha))
    print("Cadastro realizado com sucesso!\n")

    # Após o Cadastro, o cliente entra na sua carteira
    menu_carteira(bd.search_client_id((cpf, senha)))


def login():
    # Solicita as credenciais do cliente para login
    print("\nLogin:")
    cpf = input("CPF: ")
    senha = input("Senha: ")
    id_cliente = bd.search_client_id((cpf, senha))
    if id_cliente != -1:
        print("Login realizado com sucesso!\n")
        return id_cliente
    else:
        print("CPF ou senha incorretos.\n")
        return None
    

def menu_carteira(id_cliente):
    while True:
        print("Você está na sua Carteira de Investimentos. O que deseja fazer?\n")
        print("1. Operação de Compra")
        print("2. Operação de Venda")
        print("3. Histórico de Operações")
        print("4. Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            operacao(id_cliente, opcao)
        elif opcao == 2:
            operacao(id_cliente, opcao)
        elif opcao == 3:
            # wallet(id_cliente)
            mostrar_historico_operacoes(id_cliente)
        elif opcao == 4:
            print("Você saiu da sua carteira com sucesso. Até a próxima!\n")
            break
        else:
            print("Opção inválida. Tente novamente.\n")


def operacao(id_cliente, op):
    operacao = "Compra" if op == 1 else "Venda"

    print(f"\nOperação de {operacao}:")
    ticker = input("Ativo: ").upper()
    quant = int(input("Quantidade: "))
    pMedio = float(input("Preço Médio: "))
    tt = quant * pMedio

    # Inserir operação no banco de dados
    bd.inserir("operations", (dt.now().date(), id_cliente, ticker, operacao[0], quant, pMedio, tt))
    print(f"{operacao} cadastrada com sucesso!\n")


def mostrar_historico_operacoes(id_cliente):
    print("\nResultados:")
    # Mostrar informações da carteira do cliente
    carteira = bd.select_where("operations", "id_cliente", str(id_cliente))
    if carteira:
        print("\nInformações da carteira:")
        for registro in carteira:
            print(f"Ativo: {registro['ticker']}, Quantidade: {registro['Quant']}, Preço Médio: R${registro['P_Medio']}, Total: R${registro['total']}")
    else:
        print("Você não possui ativos na carteira.")


def wallet(id_cliente):
    bd.select_where("operations", "id_cliente", str(id_cliente))

def main():
    bd.create_tables()

    while True:
        menu_principal()
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            cadastro()

        elif opcao == 2:
            id_cliente = login()
            if id_cliente:
                menu_carteira(id_cliente)

        elif opcao == 3:
            print("Finalizando o Programa")
            bd.disconnect()
            break
        
        else:
            print("Opção inválida. Tente novamente.\n")
