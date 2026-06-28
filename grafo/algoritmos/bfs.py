from __future__ import annotations

from grafo.grafo import Grafo

class _Fila:
    """Fila FIFO de uso geral implementada sobre lista."""

    def __init__(self) -> None:
        self._dados: list = []
        self._head: int = 0  # índice do próximo elemento a sair

    def enqueue(self, item) -> None:
        self._dados.append(item)

    def dequeue(self):
        if self.vazia():
            raise IndexError("dequeue em fila vazia")
        item = self._dados[self._head]
        self._head += 1
        return item

    def vazia(self) -> bool:
        return self._head >= len(self._dados)


def bfs(grafo: Grafo, origem: int, destino: int) -> dict:
    """Busca em Largura (BFS) de ``origem`` até ``destino``.

    Retorna um dicionário com:
    - ``alcancavel``      : bool — destino é alcançável a partir da origem
    - ``distancia_saltos``: int  — menor número de arestas no caminho
                                   (-1 se inalcançável)
    - ``caminho``         : list[int] — sequência de ids no caminho mais curto
                                   ([] se inalcançável)
    - ``num_caminhos_minimos``: int — quantos caminhos distintos de comprimento
                                      mínimo existem entre origem e destino
    """
    if not grafo.existe_local(origem) or not grafo.existe_local(destino):
        return {
            "alcancavel": False,
            "distancia_saltos": -1,
            "caminho": [],
            "num_caminhos_minimos": 0,
        }

    # Casos triviais
    if origem == destino:
        return {
            "alcancavel": True,
            "distancia_saltos": 0,
            "caminho": [origem],
            "num_caminhos_minimos": 1,
        }

    # dist[v]    = menor número de arestas de origem até v (-1 = não visitado)
    # contagem[v] = quantos caminhos mínimos chegam até v
    # predecessor[v] = vértice anterior no caminho mínimo (para reconstrução)
    dist: dict[int, int] = {v: -1 for v in grafo.ids()}
    contagem: dict[int, int] = {v: 0 for v in grafo.ids()}
    predecessor: dict[int, int | None] = {v: None for v in grafo.ids()}

    dist[origem] = 0
    contagem[origem] = 1

    fila = _Fila()
    fila.enqueue(origem)

    while not fila.vazia():
        no_atual = fila.dequeue()

        # Explora cada vizinho do nó atual
        for (vizinho, _peso) in grafo.vizinhos(no_atual):

            if dist[vizinho] == -1:
                # Primeira vez que chegamos a este vizinho: descoberta
                dist[vizinho] = dist[no_atual] + 1
                contagem[vizinho] = contagem[no_atual]
                predecessor[vizinho] = no_atual
                fila.enqueue(vizinho)

            elif dist[vizinho] == dist[no_atual] + 1:
                # Chegamos ao vizinho pelo mesmo comprimento mínimo:
                # somamos os caminhos, mas não re-enfileiramos
                contagem[vizinho] += contagem[no_atual]

    # Verifica se o destino foi alcançado
    if dist[destino] == -1:
        return {
            "alcancavel": False,
            "distancia_saltos": -1,
            "caminho": [],
            "num_caminhos_minimos": 0,
        }

    # Reconstrói o caminho seguindo os predecessores de trás para frente
    caminho: list[int] = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = predecessor[no]
    caminho.reverse()

    return {
        "alcancavel": True,
        "distancia_saltos": dist[destino],
        "caminho": caminho,
        "num_caminhos_minimos": contagem[destino],
    }
