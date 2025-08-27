# ==============================
#   Sistema Bancário - V2
# ==============================

# Constantes
LIMITE_SAQUES = 3
AGENCIA = "0001"

# Variáveis globais
usuarios = []
contas = []

# ------------------------------
# Funções principais do sistema
# ------------------------------

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza um saque da conta"""
    if valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print("❌ Valor excede o limite por saque.")
    elif valor <= 0:
        print("❌ Valor inválido.")
    elif numero_saques >= limite_saques:
        print("❌ Limite de saques diários atingido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("✅ Saque realizado com sucesso.")
    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):
    """Realiza um depósito na conta"""
    if valor <= 0:
        print("❌ Valor inválido.")
    else:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("✅ Depósito realizado com sucesso.")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """Exibe o extrato da conta"""
    print("\n====== EXTRATO ======")
    if extrato:
        for movimento in extrato:
            print(movimento)
    else:
        print("Nenhuma movimentação registrada.")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=====================\n")


# ------------------------------
# Funções de cadastro
# ------------------------------

def criar_usuario(usuarios):
    """Cadastra um novo usuário"""
    cpf = input("Informe o CPF (apenas números): ")

    # Verifica se já existe usuário com esse CPF
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("❌ Já existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("✅ Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    """Retorna o usuário pelo CPF"""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    """Cria uma nova conta vinculada a um usuário"""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("✅ Conta criada com sucesso!")
    else:
        print("❌ Usuário não encontrado. Cadastre o usuário primeiro.")


def listar_contas(contas):
    """Lista todas as contas cadastradas"""
    for conta in contas:
        usuario = conta["usuario"]
        print(f"""
Agência: {conta['agencia']}
C/C: {conta['numero_conta']}
Titular: {usuario['nome']}
""")


# ------------------------------
# Programa principal
# ------------------------------

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    numero_conta = 1

    menu = """
========= MENU =========

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair
=> """

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(AGENCIA, numero_conta, usuarios)
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("👋 Até mais!")
            break

        else:
            print("❌ Operação inválida, tente novamente.")


main()
