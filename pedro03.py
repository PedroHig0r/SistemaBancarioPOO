"""Camada de serviço (regras de negócio).

Atua como **Context** para o padrão Strategy e como cliente das
fábricas (Factory Method) e dos repositórios (Singleton).
"""
from __future__ import annotations

from domain.factories import obter_factory
from domain.models import Beneficiario, Doacao, Doador, Item
from repository.repositorios import (
    BeneficiarioRepository,
    DoacaoRepository,
    DoadorRepository,
    ItemRepository,
)

from .strategies import MatchingStrategy, STRATEGIES, UrgenciaStrategy


class DoadorService:
    def __init__(self) -> None:
        self.repo = DoadorRepository()

    def cadastrar(self, nome: str, cidade: str, contato: str) -> Doador:
        d = Doador(nome=nome, cidade=cidade, contato=contato)
        self.repo.adicionar(d)
        return d

    def listar(self):
        return self.repo.listar()

    def atualizar(self, did: str, **campos) -> bool:
        return self.repo.atualizar(did, **campos)

    def remover(self, did: str) -> bool:
        return self.repo.remover(did)


class BeneficiarioService:
    def __init__(self) -> None:
        self.repo = BeneficiarioRepository()

    def cadastrar(self, nome, cidade, necessidade, urgencia=1) -> Beneficiario:
        b = Beneficiario(nome=nome, cidade=cidade, necessidade=necessidade, urgencia=int(urgencia))
        self.repo.adicionar(b)
        return b

    def listar(self):
        return self.repo.listar()

    def atualizar(self, bid: str, **campos) -> bool:
        return self.repo.atualizar(bid, **campos)

    def remover(self, bid: str) -> bool:
        return self.repo.remover(bid)


class ItemService:
    def __init__(self) -> None:
        self.repo = ItemRepository()

    def cadastrar(self, categoria: str, dados: dict) -> Item:
        factory = obter_factory(categoria)         # Factory Method em ação
        item = factory.criar(dados)
        if not item.validar():
            raise ValueError("Item inválido para a categoria informada.")
        self.repo.adicionar(item)
        return item

    def listar(self):
        return self.repo.listar()

    def remover(self, item_id: str) -> bool:
        return self.repo.remover(item_id)


class DoacaoService:
    """Context do Strategy: orquestra a doação aplicando a estratégia
    selecionada para escolher o beneficiário."""

    def __init__(self, strategy: MatchingStrategy | None = None) -> None:
        self.repo = DoacaoRepository()
        self.itens = ItemRepository()
        self.beneficiarios = BeneficiarioRepository()
        self.doadores = DoadorRepository()
        self._strategy: MatchingStrategy = strategy or UrgenciaStrategy()

    def definir_estrategia(self, nome: str) -> None:
        if nome not in STRATEGIES:
            raise ValueError(f"Estratégia inválida. Use uma de: {list(STRATEGIES)}")
        self._strategy = STRATEGIES[nome]

    @property
    def estrategia_atual(self) -> str:
        return type(self._strategy).__name__

    def registrar(self, doador_id: str, item_id: str) -> Doacao:
        doador = self.doadores.buscar(doador_id)
        item = self.itens.buscar(item_id)
        if not doador:
            raise ValueError("Doador não encontrado.")
        if not item:
            raise ValueError("Item não encontrado.")

        beneficiario = self._strategy.selecionar(
            item, self.beneficiarios.listar(), doador.cidade
        )
        doacao = Doacao(
            doador_id=doador.id,
            item_id=item.id,
            beneficiario_id=beneficiario.id if beneficiario else None,
        )
        self.repo.adicionar(doacao)
        # remove item do estoque após destiná-lo
        self.itens.remover(item.id)
        return doacao

    def listar(self):
        return self.repo.listar()
