from abc import ABC, abstractmethod
from datetime import datetime


# =========================
# HISTÓRICO
# =========================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


# =========================
# CONTA
# =========================
class Conta:
    AGENCIA = "0001"

    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = Conta.AGENCIA
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):

        if valor > self.saldo:
            print("Saldo insuficiente!")
            return False

        elif valor > 0:
            self.saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado!")
            return True

        else:
            print("Valor inválido!")
            return False

    def depositar(self, valor):

        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado!")
            return True

        else:
            print("Valor inválido!")
            return False


# =========================
# CONTA CORRENTE
# =========================
class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


# =========================
# CLIENTE
# =========================
class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# =========================
# PESSOA FÍSICA
# =========================
class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)

        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# =========================
# INTERFACE TRANSAÇÃO
# =========================
class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# =========================
# DEPÓSITO
# =========================
class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):

        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)


# =========================
# SAQUE
# =========================
class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):

        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)


# =========================
# TESTE DO SISTEMA
# =========================

cliente = PessoaFisica(
    nome="Pedro",
    data_nascimento="01-01-2000",
    cpf="12345678900",
    endereco="Fortaleza - CE"
)

conta = ContaCorrente.nova_conta(cliente, 1)

cliente.adicionar_conta(conta)

deposito = Deposito(1000)
cliente.realizar_transacao(conta, deposito)

saque = Saque(200)
cliente.realizar_transacao(conta, saque)

print("\nSaldo atual:", conta.saldo)

print("\nHistórico:")
for transacao in conta.historico.transacoes:
    print(transacao)