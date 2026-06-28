from __future__ import annotations

from grafo.grafo import Grafo


def componentes_fortemente_conectados(grafo: Grafo) -> list[list[int]]:
    """Componentes fortemente conectados (SCCs) pelo algoritmo de Kosaraju.
    Faz a questão de percorrer o grafo todo a partir de um nó, depois inverte o grafo e percorre pelo mesmo nó novamente
    """
    # Ordem de término via DFS iterativo 
    visitado: set[int] = set()
    ordem_termino: list[int] = []

    for inicio in grafo.ids():
        if inicio in visitado:
            continue
        pilha = [(inicio, iter(grafo.vizinhos(inicio)))]
        visitado.add(inicio)
        while pilha:
            no, vizinhos = pilha[-1]
            avancou = False
            for (viz, _peso) in vizinhos:
                if viz not in visitado:
                    visitado.add(viz)
                    pilha.append((viz, iter(grafo.vizinhos(viz))))
                    avancou = True
                    break
            if not avancou:
                ordem_termino.append(no)
                pilha.pop()

    # Grafo transposto 
    transposto: dict[int, list[int]] = {v: [] for v in grafo.ids()}
    for u in grafo.ids():
        for (v, _peso) in grafo.vizinhos(u):
            transposto[v].append(u)

    # DFS no transposto na ordem inversa de término 
    visitado.clear()
    componentes: list[list[int]] = []
    for raiz in reversed(ordem_termino):
        if raiz in visitado:
            continue
        comp: list[int] = []
        pilha_t = [raiz]
        visitado.add(raiz)
        while pilha_t:
            no = pilha_t.pop()
            comp.append(no)
            for viz in transposto[no]:
                if viz not in visitado:
                    visitado.add(viz)
                    pilha_t.append(viz)
        componentes.append(sorted(comp))

    return componentes


def _alcancaveis(grafo: Grafo, origem: int) -> set[int]:
    visitado: set[int] = {origem}
    pilha = [origem]
    while pilha:
        no = pilha.pop()
        for (viz, _peso) in grafo.vizinhos(no):
            if viz not in visitado:
                visitado.add(viz)
                pilha.append(viz)
    return visitado


def analisar_rotas(
    grafo: Grafo,
    destinos_ids: list[int],
    deposito_id: int = 0,
) -> dict:
    # decide se as entregas cabem em uma rota ou mais
    componentes = componentes_fortemente_conectados(grafo)

    # Mapeia cada local ao índice do seu componente.
    comp_de: dict[int, int] = {}
    for i, comp in enumerate(componentes):
        for no in comp:
            comp_de[no] = i

    alcancaveis = _alcancaveis(grafo, deposito_id)
    comp_deposito = comp_de.get(deposito_id)

    # Agrupa os destinos válidos por componente, separando inalcançáveis.
    grupos: dict[int, list[int]] = {}
    inalcancaveis: list[int] = []
    inexistentes: list[int] = []
    for d in destinos_ids:
        if not grafo.existe_local(d):
            inexistentes.append(d)
        elif d not in alcancaveis:
            inalcancaveis.append(d)
        else:
            grupos.setdefault(comp_de[d], []).append(d)

    rotas = []
    for idx, destinos in grupos.items():
        rotas.append({
            "componente": idx,
            "locais_do_componente": componentes[idx],
            "destinos": sorted(destinos),
            "mesma_scc_do_deposito": idx == comp_deposito,
        })
    # Coloca a rota do depósito primeiro, depois as demais.
    rotas.sort(key=lambda r: (not r["mesma_scc_do_deposito"], r["componente"]))

    num_rotas = len(rotas)

    if not destinos_ids:
        mensagem = "Nenhuma entrega selecionada."
    elif inexistentes or inalcancaveis:
        partes = []
        if num_rotas:
            partes.append(f"{num_rotas} rota(s) para os destinos alcançáveis")
        if inalcancaveis:
            partes.append(f"{len(inalcancaveis)} destino(s) sem caminho a partir do depósito")
        if inexistentes:
            partes.append(f"{len(inexistentes)} id(s) inexistente(s)")
        mensagem = "Atenção: " + "; ".join(partes) + "."
    elif num_rotas <= 1:
        mensagem = "Todas as entregas podem ser feitas em 1 rota única."
    else:
        mensagem = (
            f"As entregas estão em {num_rotas} regiões desconexas — "
            f"são necessárias {num_rotas} rotas separadas."
        )

    return {
        "deposito_id": deposito_id,
        "num_componentes": len(componentes),
        "componentes": componentes,
        "num_rotas": num_rotas,
        "rotas": rotas,
        "inalcancaveis": sorted(inalcancaveis),
        "inexistentes": sorted(inexistentes),
        "mensagem": mensagem,
    }
