"""Camada de apresentação: interface de linha de comando (CLI)."""
from __future__ import annotations

from service.servicos import (
    BeneficiarioService,
    DoacaoService,
    DoadorService,
    ItemService,
)
from service.strategies import STRATEGIES


class App:
    def __init__(self) -> None:
        self.doadores = DoadorService()
        self.beneficiarios = BeneficiarioService()
        self.itens = ItemService()
        self.doacoes = DoacaoService()

    # ------------------------------------------------------------------
    def run(self) -> None:
        acoes = {
            "1": ("Cadastrar doador",       self._cad_doador),
            "2": ("Listar doadores",        self._list_doadores),
            "3": ("Cadastrar beneficiário", self._cad_benef),
            "4": ("Listar beneficiários",   self._list_benef),
            "5": ("Cadastrar item",         self._cad_item),
            "6": ("Listar itens",           self._list_itens),
            "7": ("Registrar doação",       self._reg_doacao),
            "8": ("Listar doações",         self._list_doacoes),
            "9": ("Trocar estratégia de matching", self._trocar_estrategia),
            "10": ("Remover doador",        self._rem_doador),
            "11": ("Remover beneficiário",  self._rem_benef),
            "0": ("Sair",                   None),
        }
        while True:
            print("\n=== Plataforma de Doações (ODS 12) ===")
            print(f"Estratégia atual: {self.doacoes.estrategia_atual}")
            for k, (txt, _) in acoes.items():
                print(f"  {k}. {txt}")
            op = input("Escolha: ").strip()
            if op == "0":
                print("Até logo!")
                return
            if op in acoes and acoes[op][1]:
                try:
                    acoes[op][1]()
                except Exception as e:  # noqa: BLE001
                    print(f"[erro] {e}")
            else:
                print("Opção inválida.")

    # ------------------------------------------------------------------
    def _cad_doador(self):
        nome = input("Nome: ")
        cidade = input("Cidade: ")
        contato = input("Contato: ")
        d = self.doadores.cadastrar(nome, cidade, contato)
        print(f"Doador cadastrado: {d.id}")

    def _list_doadores(self):
        for d in self.doadores.listar():
            print(f"  {d.id} | {d.nome} | {d.cidade} | {d.contato}")

    def _rem_doador(self):
        did = input("ID do doador: ")
        print("Removido." if self.doadores.remover(did) else "Não encontrado.")

    def _cad_benef(self):
        nome = input("Nome: ")
        cidade = input("Cidade: ")
        necessidade = input("Necessidade (alimento/roupa/medicamento): ")
        urgencia = input("Urgência (1-5): ") or "1"
        b = self.beneficiarios.cadastrar(nome, cidade, necessidade, urgencia)
        print(f"Beneficiário cadastrado: {b.id}")

    def _list_benef(self):
        for b in self.beneficiarios.listar():
            print(f"  {b.id} | {b.nome} | {b.cidade} | {b.necessidade} | urg={b.urgencia}")

    def _rem_benef(self):
        bid = input("ID do beneficiário: ")
        print("Removido." if self.beneficiarios.remover(bid) else "Não encontrado.")

    def _cad_item(self):
        categoria = input("Categoria (alimento/roupa/medicamento): ").strip().lower()
        descricao = input("Descrição: ")
        quantidade = input("Quantidade: ")
        dados = {"descricao": descricao, "quantidade": quantidade}
        if categoria == "alimento":
            dados["validade"] = input("Validade (YYYY-MM-DD): ")
        elif categoria == "roupa":
            dados["tamanho"] = input("Tamanho (PP/P/M/G/GG/XG): ")
        elif categoria == "medicamento":
            dados["validade"] = input("Validade (YYYY-MM-DD): ")
            dados["receita"] = input("Exige receita? (s/n): ").lower().startswith("s")
        item = self.itens.cadastrar(categoria, dados)
        print(f"Item cadastrado: {item}")

    def _list_itens(self):
        for it in self.itens.listar():
            print(f"  {it}")

    def _reg_doacao(self):
        did = input("ID do doador: ")
        iid = input("ID do item: ")
        d = self.doacoes.registrar(did, iid)
        print(f"Doação {d.id} registrada. Beneficiário: {d.beneficiario_id or '(sem match)'}")

    def _list_doacoes(self):
        for d in self.doacoes.listar():
            print(f"  {d.id} | doador={d.doador_id} | item={d.item_id} | benef={d.beneficiario_id} | {d.data}")

    def _trocar_estrategia(self):
        print(f"Estratégias disponíveis: {', '.join(STRATEGIES)}")
        nome = input("Nome da estratégia: ").strip().lower()
        self.doacoes.definir_estrategia(nome)
        print(f"Estratégia agora: {self.doacoes.estrategia_atual}")


if __name__ == "__main__":
    App().run()
