from __future__ import annotations

VERMELHO = 0
PRETO = 1


class Nodo:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.cor: int = VERMELHO
        self.pai: Nodo | None = None
        self.esq: Nodo | None = None
        self.dir: Nodo | None = None
