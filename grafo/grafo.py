from __future__ import annotations

from grafo.local import Local


class Grafo:
    """Grafo dirigido e ponderado de locais de entrega.

    Implementado com lista de adjacência: cada local aponta para uma lista
    de pares (id_destino, distancia_km). Por ser dirigido, uma estrada de
    mão dupla é representada por duas arestas (uma em cada sentido).
    """

    def __init__(self) -> None:
        self._locais: dict[int, Local] = {}
        self._adj: dict[int, list[tuple[int, float]]] = {}
        self._proximo_id: int = 0

    def adicionar_local(self, nome: str, x: float = 0.0, y: float = 0.0) -> Local:
        """Cria um novo local com id auto-incrementado."""
        local = Local(id=self._proximo_id, nome=nome, x=x, y=y)
        self._locais[local.id] = local
        self._adj[local.id] = []
        self._proximo_id += 1
        return local

    def remover_local(self, id: int) -> bool:
        """Remove o local e todas as estradas que entram ou saem dele."""
        if id not in self._locais:
            return False
        del self._locais[id]
        del self._adj[id]
        # Remove as arestas que apontavam para o local removido.
        for origem in self._adj:
            self._adj[origem] = [
                (dst, peso) for (dst, peso) in self._adj[origem] if dst != id
            ]
        return True

    def buscar_local(self, id: int) -> Local | None:
        return self._locais.get(id)

    def locais(self) -> list[Local]:
        """Lista todos os locais ordenados por id."""
        return [self._locais[i] for i in sorted(self._locais)]

    def ids(self) -> list[int]:
        return sorted(self._locais)

    def existe_local(self, id: int) -> bool:
        return id in self._locais

    def adicionar_estrada(
        self,
        origem_id: int,
        destino_id: int,
        distancia: float,
        bidirecional: bool = False,
    ) -> bool:
        # Adiciona uma estrada origem→destino com a distância em km.
    
        if origem_id not in self._locais or destino_id not in self._locais:
            return False
        if distancia <= 0:
            return False

        self._inserir_aresta(origem_id, destino_id, distancia)
        if bidirecional:
            self._inserir_aresta(destino_id, origem_id, distancia)
        return True

    def remover_estrada(self, origem_id: int, destino_id: int) -> bool:
        # Remove a aresta origem→destino. Retorna True se existia.
        if origem_id not in self._adj:
            return False
        antes = len(self._adj[origem_id])
        self._adj[origem_id] = [
            (dst, peso) for (dst, peso) in self._adj[origem_id] if dst != destino_id
        ]
        return len(self._adj[origem_id]) < antes

    def vizinhos(self, id: int) -> list[tuple[int, float]]:
        # Pares (id_vizinho, distancia) alcançáveis diretamente a partir de `id`.
        return self._adj.get(id, [])

    def existe_estrada(self, origem_id: int, destino_id: int) -> bool:
        return any(dst == destino_id for (dst, _) in self._adj.get(origem_id, []))

    def peso(self, origem_id: int, destino_id: int) -> float | None:
        for (dst, p) in self._adj.get(origem_id, []):
            if dst == destino_id:
                return p
        return None

    def serializar(self) -> dict:
        # Renderizaçãio pro front
        nos = [
            {"id": l.id, "nome": l.nome, "x": l.x, "y": l.y}
            for l in self.locais()
        ]
        arestas = [
            {"origem": u, "destino": v, "distancia": peso}
            for u in self.ids()
            for (v, peso) in self._adj[u]
        ]
        return {"locais": nos, "estradas": arestas}

    def __len__(self) -> int:
        return len(self._locais)

    def _inserir_aresta(self, origem_id: int, destino_id: int, distancia: float) -> None:
        # Atualiza o peso se a aresta já existir, senão adiciona.
        for i, (dst, _) in enumerate(self._adj[origem_id]):
            if dst == destino_id:
                self._adj[origem_id][i] = (destino_id, distancia)
                return
        self._adj[origem_id].append((destino_id, distancia))
