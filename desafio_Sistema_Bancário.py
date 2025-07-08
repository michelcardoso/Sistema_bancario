titulo = "MENU"
largura_total = 30
titulo_extrato = "EXTRATO"

menu_extrato = """


[s] Extrato saque
[d] Extrato deposito
=>"""

menu = """

[s] Sacar
[d] Depositar
[e] Extrato
[q] Sair
=>"""

saldo_conta = 0
limite = 500
extrato_saque = []
extrato_deposito = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    print (titulo.center(largura_total, '='))
    opcao = input(menu)
    if opcao == "s":
        if numero_saques < LIMITE_SAQUES:
            valor = float( input("Digite o valor do saque: "))
            if valor > saldo_conta:
                print("Saldo insuficiente")
            elif valor > limite:
                print (" Valor excede o limite por saque.")
            elif valor <= 0:
                print("Valor inválido")
            else:
                saldo_conta -= valor
                extrato_saque.append(valor)
                numero_saques += 1
                print("Saque realizado com sucesso.")
        else:
            print("Limite de saques diarios atingido.")
    elif opcao == "d":
        valor = float (input("Digite o valor do deposito: "))
        if valor <= 0:
            print("Valor inválido")
        else:
            saldo_conta += valor
            extrato_deposito.append(valor)
            print("Deposito realizado com sucesso")
    elif opcao == "e":
        print(titulo_extrato.center(largura_total, "="))
        opcao_extrato = input(menu_extrato)
        if opcao_extrato == "d":
            print("Extratos de depositos")
            if extrato_deposito:
                for valor in extrato_deposito:
                    print(f"Depósito: R${valor:.2f}")
                print(f"\nSaldo atual: R${saldo_conta:.2f}")
            else:
                print("Nenhum depósito realizado.")
        elif opcao_extrato == "s":
            print("Extrato de saque")
            if extrato_saque:
                for valor in extrato_saque:
                    print (f"Saque: R$ {valor:.2f}")
                print(f"\nSaldo atual: R${saldo_conta:.2f}")
            else:
                print("nenhum saque realizado.")
        
    elif opcao == "q":
       print("Até mais !")
       break

    else:
        print("Valor invalido")