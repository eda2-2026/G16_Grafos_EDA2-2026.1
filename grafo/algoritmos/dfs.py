from __future__ import annotations

from grafo.grafo import Grafo


def dfs(grafo: Grafo, origem: int, destino: int) -> dict:
    """Busca em Profundidade (DFS) que enumera **todas** as rotas simples
    de ``origem`` até ``destino``.

    Uma rota *simples* é aquela que não repete vértices.

    Retorna um dicionário com:
    - ``alcancavel``: bool      — existe ao menos uma rota
    - ``rotas``     : list[list[int]] — todas as rotas encontradas (cada
                                        rota é a lista de ids em ordem)
    - ``num_rotas`` : int       — total de rotas distintas encontradas
    """
    if not grafo.existe_local(origem) or not grafo.existe_local(destino):
        return {"alcancavel": False, "rotas": [], "num_rotas": 0}

    if origem == destino:
        return {"alcancavel": True, "rotas": [[origem]], "num_rotas": 1}

    rotas_encontradas: list[list[int]] = []

    # visitado controla quais vértices já estão no caminho atual,
    # evitando ciclos (backtracking manual)
    visitado: set[int] = set()
    caminho_atual: list[int] = []

    _dfs_recursivo(grafo, origem, destino, visitado, caminho_atual, rotas_encontradas)

    return {
        "alcancavel": len(rotas_encontradas) > 0,
        "rotas": rotas_encontradas,
        "num_rotas": len(rotas_encontradas),
    }


def _dfs_recursivo(
    grafo: Grafo,
    no_atual: int,
    destino: int,
    visitado: set[int],
    caminho_atual: list[int],
    rotas_encontradas: list[list[int]],
) -> None:
    # --- entra no nó atual ---
    visitado.add(no_atual)
    caminho_atual.append(no_atual)

    if no_atual == destino:
        # Chegou ao destino: salva uma cópia do caminho atual
        rotas_encontradas.append(list(caminho_atual))
    else:
        # Explora cada vizinho alcançável diretamente
        for (vizinho, _peso) in grafo.vizinhos(no_atual):
            if vizinho not in visitado:
                _dfs_recursivo(
                    grafo,
                    vizinho,
                    destino,
                    visitado,
                    caminho_atual,
                    rotas_encontradas,
                )

    # --- backtrack: sai do nó atual ---
    caminho_atual.pop()
    visitado.discard(no_atual)
