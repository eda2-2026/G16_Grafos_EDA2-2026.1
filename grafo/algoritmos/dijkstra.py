from __future__ import annotations

from grafo.grafo import Grafo


# ---------------------------------------------------------------------------
# Min-Heap implementada manualmente.
#
# Cada elemento é um par (prioridade, valor).  A heap garante que o par de
# menor prioridade sempre fica na raiz (índice 0), permitindo extração em
# O(log n) e inserção em O(log n).
#
# Operações implementadas:
#   inserir(prioridade, valor)  — adiciona um elemento
#   extrair_minimo()            — remove e devolve (prioridade, valor) menor
#   vazia()                     — True se não há elementos
# ---------------------------------------------------------------------------

class _MinHeap:
    """Fila de prioridade mínima (min-heap binária) implementada sobre lista."""

    def __init__(self) -> None:
        self._dados: list[tuple[float, int]] = []

    # ----- interface pública -----

    def inserir(self, prioridade: float, valor: int) -> None:
        self._dados.append((prioridade, valor))
        self._subir(len(self._dados) - 1)

    def extrair_minimo(self) -> tuple[float, int]:
        if self.vazia():
            raise IndexError("extrair de heap vazia")

        # Troca a raiz com o último elemento e remove o último
        self._trocar(0, len(self._dados) - 1)
        minimo = self._dados.pop()

        # Restaura a propriedade de heap descendo a nova raiz
        if not self.vazia():
            self._descer(0)

        return minimo

    def vazia(self) -> bool:
        return len(self._dados) == 0

    # ----- métodos auxiliares de heap -----

    def _pai(self, i: int) -> int:
        return (i - 1) // 2

    def _filho_esq(self, i: int) -> int:
        return 2 * i + 1

    def _filho_dir(self, i: int) -> int:
        return 2 * i + 2

    def _trocar(self, i: int, j: int) -> None:
        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]

    def _subir(self, i: int) -> None:
        """Sobe o elemento na posição i até restaurar a propriedade de heap."""
        while i > 0:
            p = self._pai(i)
            if self._dados[i][0] < self._dados[p][0]:
                self._trocar(i, p)
                i = p
            else:
                break

    def _descer(self, i: int) -> None:
        """Desce o elemento na posição i até restaurar a propriedade de heap."""
        n = len(self._dados)
        while True:
            menor = i
            esq = self._filho_esq(i)
            dir_ = self._filho_dir(i)

            if esq < n and self._dados[esq][0] < self._dados[menor][0]:
                menor = esq
            if dir_ < n and self._dados[dir_][0] < self._dados[menor][0]:
                menor = dir_

            if menor == i:
                break  # já está na posição correta

            self._trocar(i, menor)
            i = menor


# ---------------------------------------------------------------------------
# Dijkstra principal
# ---------------------------------------------------------------------------

_INF = float("inf")


def dijkstra(grafo: Grafo, origem: int, destino: int) -> dict:
    """Algoritmo de Dijkstra — menor caminho ponderado (por distância em km).

    Retorna um dicionário com:
    - ``alcancavel``  : bool        — destino é alcançável a partir da origem
    - ``distancia_km``: float       — custo total do caminho mínimo
                                      (_INF se inalcançável)
    - ``caminho``     : list[int]   — sequência de ids do caminho mínimo
                                      ([] se inalcançável)
    - ``distancias``  : dict[int, float] — distância mínima de origem até
                                           cada vértice do grafo

    Complexidade: O((V + E) log V) com a min-heap implementada acima.
    """
    if not grafo.existe_local(origem) or not grafo.existe_local(destino):
        return {
            "alcancavel": False,
            "distancia_km": _INF,
            "caminho": [],
            "distancias": {},
        }

    ids = grafo.ids()

    # dist[v] = menor distância conhecida de origem até v
    dist: dict[int, float] = {v: _INF for v in ids}
    dist[origem] = 0.0

    # predecessor[v] = vértice anterior no caminho mínimo até v
    predecessor: dict[int, int | None] = {v: None for v in ids}

    # finalizado[v] = True quando o menor caminho até v já foi determinado
    finalizado: set[int] = set()

    # A heap armazena (distancia_atual, id_vertice)
    heap = _MinHeap()
    heap.inserir(0.0, origem)

    while not heap.vazia():
        dist_atual, no_atual = heap.extrair_minimo()

        # Se já finalizamos este vértice, ignoramos (entrada obsoleta na heap)
        if no_atual in finalizado:
            continue
        finalizado.add(no_atual)

        # Otimização: paramos assim que o destino for extraído da heap,
        # pois nesse momento sua distância já é definitiva
        if no_atual == destino:
            break

        # Relaxamento das arestas que saem de no_atual
        for (vizinho, peso_aresta) in grafo.vizinhos(no_atual):
            if vizinho in finalizado:
                continue

            nova_dist = dist[no_atual] + peso_aresta

            if nova_dist < dist[vizinho]:
                # Distância melhorada: atualiza e re-insere na heap
                dist[vizinho] = nova_dist
                predecessor[vizinho] = no_atual
                heap.inserir(nova_dist, vizinho)

    # Verifica alcançabilidade
    if dist[destino] == _INF:
        return {
            "alcancavel": False,
            "distancia_km": _INF,
            "caminho": [],
            "distancias": dist,
        }

    # Reconstrói o caminho seguindo predecessores de trás para frente
    caminho: list[int] = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = predecessor[no]
    caminho.reverse()

    return {
        "alcancavel": True,
        "distancia_km": dist[destino],
        "caminho": caminho,
        "distancias": dist,
    }
