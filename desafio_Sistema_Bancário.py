def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, criação de conta encerrada! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 40)
        print(linha)


def selecionar_conta(contas):
    if not contas:
        print("\n@@@ Nenhuma conta encontrada! Cadastre uma conta antes. @@@")
        return None

    if len(contas) == 1:
        return contas[0]

    print("\n=== Selecione a conta para operar ===")
    for i, conta in enumerate(contas, start=1):
        print(f"{i} - Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")

    opcao = int(input("Digite o número da conta: "))
    if 1 <= opcao <= len(contas):
        return contas[opcao - 1]
    else:
        print("\n@@@ Opção inválida! @@@")
        return None


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = input("""
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo usuário
[c] Nova conta
[l] Listar contas
[q] Sair

=> """)

        if opcao == "d":
            conta = selecionar_conta(contas)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

        elif opcao == "s":
            conta = selecionar_conta(contas)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
                    saldo=conta["saldo"],
                    valor=valor,
                    extrato=conta["extrato"],
                    limite=conta["limite"],
                    numero_saques=conta["numero_saques"],
                    limite_saques=conta["limite_saques"],
                )

        elif opcao == "e":
            conta = selecionar_conta(contas)
            if conta:
                exibir_extrato(conta["saldo"], extrato=conta["extrato"])

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                # inicializar dados da conta
                conta["saldo"] = 0
                conta["extrato"] = ""
                conta["numero_saques"] = 0
                conta["limite"] = 500
                conta["limite_saques"] = LIMITE_SAQUES
                contas.append(conta)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()
