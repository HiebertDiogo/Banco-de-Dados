from aplicacao_bd import Bd_postgres
from datetime import datetime as dt


bd = Bd_postgres(
        dbname="Wallet",
        user="Grupo BD",
        password="admin123",
        host="localhost",
        port=5432,
    )

bd.create_tables()


bd.inserir("clients", ("Diogo", "@gmail.com", "23/09/2001", "048", "123"))




# id_cliente = bd.search_client_id(cpf, senha)


# ticker = input("Ativo: ").upper()
# op = input("Operação (c/v): ").lower()
# quant = input("Quantidade: ")
# pMedio = float(input("Preço Médio: "))
# tt = quant * pMedio


# bd.inserir("operations", (dt.now().strftime("%d/%m/%Y"), id_cliente, ticker, op, quant, pMedio, tt ))





bd.disconnect()


def login(): 
    cpf = input("CPF: ")
    senha = input("Senha: ")
    return (cpf, senha)


def cadatro():
    name = input("NOME: ").upper()
    email = input("EMAIL: ")

    data_input = input("Data de Nascimento (DD/MM/AAAA): ")
    try:
        birth = dt.strptime(data_input, "%d/%m/%Y")
    except ValueError:
        print("Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.")

    return (name, email, birth, login())


def operacao(cpf, senha): 
    data = dt.now().strftime("%d/%m/%Y")
    id_cliente = bd.search_client_id(cpf, senha)
    ticker = input("Ativo: ").upper()
    op = input("Operação (c/v): ").lower()
    quant = input("Quantidade: ")
    pMedio = float(input("Preço Médio: "))
    tt = quant * pMedio

    return (data, id_cliente, ticker, op, quant, pMedio, tt)


def menu_cadastro():
    print(  "\n-------------------------------\n"
            "1- Cadastrar\n"
            "2- Login\n"
            "3- Sair\n"
            "-------------------------------")
    
    
def menu_carteira():
    print( "\n-------------------------------\n"
            "1- Operacao de Compra\n"
            "2- Operacao de Venda\n"
            "3- Mostrar Resultados\n"
            "4- Sair\n" 
            "-------------------------------")


