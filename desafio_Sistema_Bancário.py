import abc
from abc import ABC, abstractmethod
from datetime import datetime

# ==============================================================================
# Classes de Operações e Transações
# ==============================================================================

class Transacao(ABC):
    """
    Interface para transações bancárias.
    Define o contrato que as classes de transação devem seguir.
    """
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# ==============================================================================
# Classes de Clientes e Contas
# ==============================================================================

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo_excedido = valor > self._saldo
        
        if saldo_excedido:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_hoje = 0

    def sacar(self, valor):
        limite_excedido = valor > self._limite
        saques_excedidos = self._saques_hoje >= self._limite_saques

        if limite_excedido:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif saques_excedidos:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            if super().sacar(valor):
                self._saques_hoje += 1
                return True
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente._nome}
        """

# ==============================================================================
# Funções de interação com o usuário (Main)
# ==============================================================================

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")
    return cliente

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if isinstance(cliente, PessoaFisica) and cliente._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta_bancaria(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, criação de conta encerrada! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")
    return conta

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta encontrada! @@@")
        return

    for conta in contas:
        print("=" * 100)
        print(str(conta))

def selecionar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
    return cliente

def main():
    clientes = []
    contas = []

    while True:
        opcao = input("""
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo cliente
[c] Nova conta
[l] Listar contas
[q] Sair

=> """)

        if opcao == "d":
            cliente = selecionar_cliente(clientes)
            if cliente:
                conta = cliente._contas[0] # Simplificando para a primeira conta
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                cliente.realizar_transacao(conta, transacao)

        elif opcao == "s":
            cliente = selecionar_cliente(clientes)
            if cliente:
                conta = cliente._contas[0]
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)
                cliente.realizar_transacao(conta, transacao)

        elif opcao == "e":
            cliente = selecionar_cliente(clientes)
            if cliente:
                conta = cliente._contas[0]
                print("\n================ EXTRATO ================")
                extrato_str = "Não foram realizadas movimentações."
                if conta.historico.gerar_relatorio():
                    for transacao in conta.historico.gerar_relatorio():
                        extrato_str = f"Tipo: {transacao['tipo']} - Valor: R$ {transacao['valor']:.2f}\n"

                print(extrato_str)
                print(f"\nSaldo: R$ {conta.saldo:.2f}")
                print("==========================================")

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta_bancaria(numero_conta, clientes, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()
