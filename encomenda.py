from __future__ import annotations

from datetime import date


class Encomenda:
    def __init__(
        self,
        id: int,
        nome: str,
        data_postagem: date,
        peso: float,
        quantidade: int,
        prioridade: int,
        destino_id: int | None = None,
    ):
        self.id = id
        self.nome = nome
        self.data_postagem = data_postagem
        self.peso = peso
        self.quantidade = quantidade
        self.prioridade = prioridade
        self.destino_id = destino_id  # id do Local no grafo (None = sem destino definido)

    def __repr__(self) -> str:
        return (
            f"Encomenda(id={self.id}, nome='{self.nome}', "
            f"data_postagem={self.data_postagem}, peso={self.peso}, "
            f"quantidade={self.quantidade}, prioridade={self.prioridade}, "
            f"destino_id={self.destino_id})"
        )
