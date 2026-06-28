from __future__ import annotations


class Local:
    # Vértices com coordenada

    def __init__(self, id: int, nome: str, x: float = 0.0, y: float = 0.0):
        self.id = id
        self.nome = nome
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Local(id={self.id}, nome='{self.nome}')"
