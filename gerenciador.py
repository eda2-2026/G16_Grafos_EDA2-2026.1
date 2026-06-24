from __future__ import annotations
from datetime import date
from encomenda import Encomenda
from algoritmos import ALGORITMOS

from arvore import ArvoreRubroNegra

_ATRIBUTOS_VALIDOS = {"nome", "id", "data_postagem", "peso", "quantidade", "prioridade"}


class GerenciadorEncomendas:
    def __init__(self):
        self._arvore_id = ArvoreRubroNegra()
        self._arvore_prioridade = ArvoreRubroNegra()
        self._proximo_id = 1


    def criar(
        self,
        nome: str,
        data_postagem: date,
        peso: float,
        quantidade: int,
        prioridade: int,
    ) -> Encomenda:
        encomenda = Encomenda(
            id=self._proximo_id,
            nome=nome,
            data_postagem=data_postagem,
            peso=peso,
            quantidade=quantidade,
            prioridade=prioridade,
        )
        self._arvore_id.inserir(encomenda.id, encomenda)
        self._arvore_prioridade.inserir((encomenda.prioridade, encomenda.id), encomenda)
        self._proximo_id += 1
        return encomenda


    def listar(self) -> list[Encomenda]:
        return self._arvore_id.traversal_inorder()

    def buscar_por_id(self, id: int) -> Encomenda | None:
        return self._arvore_id.buscar(id)


    def atualizar(
        self,
        id: int,
        nome: str | None = None,
        data_postagem: date | None = None,
        peso: float | None = None,
        quantidade: int | None = None,
        prioridade: int | None = None,
    ) -> Encomenda | None:
        enc = self.buscar_por_id(id)
        if enc is None:
            return None

        if prioridade is not None and prioridade != enc.prioridade:
            self._arvore_prioridade.remover((enc.prioridade, enc.id))
            enc.prioridade = prioridade
            self._arvore_prioridade.inserir((enc.prioridade, enc.id), enc)

        if nome is not None:
            enc.nome = nome
        if data_postagem is not None:
            enc.data_postagem = data_postagem
        if peso is not None:
            enc.peso = peso
        if quantidade is not None:
            enc.quantidade = quantidade

        return enc


    def remover(self, id: int) -> bool:
        enc = self.buscar_por_id(id)
        if enc is None:
            return False
            
        self._arvore_prioridade.remover((enc.prioridade, enc.id))
        self._arvore_id.remover(id)
        return True


    def proxima_entrega(self) -> Encomenda | None:
        return self._arvore_prioridade.maximo()

    def listar_por_prioridade(self) -> list[Encomenda]:
        return list(reversed(self._arvore_prioridade.traversal_inorder()))

    def buscar_por_intervalo_data(self, inicio: date, fim: date) -> list[Encomenda]:
        return [enc for enc in self._arvore_id.traversal_inorder()
                if inicio <= enc.data_postagem <= fim]

    def ordenar(self, atributo: str, algoritmo: str) -> list[Encomenda]:
        if atributo not in _ATRIBUTOS_VALIDOS:
            raise ValueError(
                f"Atributo inválido: '{atributo}'. Escolha entre: {_ATRIBUTOS_VALIDOS}"
            )
        if algoritmo not in ALGORITMOS:
            raise ValueError(
                f"Algoritmo inválido: '{algoritmo}'. Escolha entre: {set(ALGORITMOS)}"
            )

        encomendas = self.listar()
        n = len(encomendas)
        if n == 0:
            return []

        chaves = [getattr(enc, atributo) for enc in encomendas]
        sorted_unique = sorted(set(chaves))
        rank = {k: r for r, k in enumerate(sorted_unique)}
        codificado = [rank[chaves[i]] * n + i for i in range(n)]

        ALGORITMOS[algoritmo](codificado)

        # Decodifica: posição original = valor % n
        return [encomendas[v % n] for v in codificado]
