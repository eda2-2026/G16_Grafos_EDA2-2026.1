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
    ):
        self.id = id
        self.nome = nome
        self.data_postagem = data_postagem
        self.peso = peso
        self.quantidade = quantidade
        self.prioridade = prioridade

    def __repr__(self) -> str:
        return (
            f"Encomenda(id={self.id}, nome='{self.nome}', "
            f"data_postagem={self.data_postagem}, peso={self.peso}, "
            f"quantidade={self.quantidade}, prioridade={self.prioridade})"
        )
