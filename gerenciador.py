from __future__ import annotations
from datetime import date
from encomenda import Encomenda
from algoritmos import ALGORITMOS

from arvore import ArvoreRubroNegra
from grafo.grafo import Grafo
from grafo.semente import grafo_semente, DEPOSITO_ID
from grafo.algoritmos.bfs import bfs
from grafo.algoritmos.dfs import dfs
from grafo.algoritmos.dijkstra import dijkstra
from grafo.algoritmos.kosaraju import componentes_fortemente_conectados

_ATRIBUTOS_VALIDOS = {"nome", "id", "data_postagem", "peso", "quantidade", "prioridade"}


class GerenciadorEncomendas:
    def __init__(self):
        self._arvore_id = ArvoreRubroNegra()
        self._arvore_prioridade = ArvoreRubroNegra()
        self._proximo_id = 1
        self.grafo: Grafo = grafo_semente()  # grafo compartilhado com todos os endpoints


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

    # ------------------------------------------------------------------
    # Integração com o grafo
    # ------------------------------------------------------------------

    def definir_destino(self, id_enc: int, destino_id: int) -> Encomenda | None:
        """Vincula uma encomenda a um Local do grafo. Retorna None se a
        encomenda ou o local não existirem."""
        enc = self.buscar_por_id(id_enc)
        if enc is None:
            return None
        if not self.grafo.existe_local(destino_id):
            return None
        enc.destino_id = destino_id
        return enc

    def analisar_rota(self, id_enc: int) -> dict | None:
        """Roda BFS, DFS, Dijkstra e Kosaraju do depósito até o destino
        da encomenda. Retorna None se a encomenda não existir ou não
        tiver destino definido."""
        enc = self.buscar_por_id(id_enc)
        if enc is None or enc.destino_id is None:
            return None

        origem = DEPOSITO_ID
        destino = enc.destino_id
        g = self.grafo

        # --- entrega direta: existe aresta única origem -> destino? ---
        entrega_direta = g.existe_estrada(origem, destino)

        # --- BFS ---
        resultado_bfs = bfs(g, origem, destino)
        nomes_bfs = [g.buscar_local(v).nome for v in resultado_bfs["caminho"]]

        # --- DFS ---
        resultado_dfs = dfs(g, origem, destino)
        rotas_dfs = [
            [g.buscar_local(v).nome for v in rota]
            for rota in resultado_dfs["rotas"]
        ]

        # --- Dijkstra ---
        resultado_dij = dijkstra(g, origem, destino)
        nomes_dij = [g.buscar_local(v).nome for v in resultado_dij["caminho"]]

        # --- Kosaraju: mesmo SCC? ---
        componentes = componentes_fortemente_conectados(g)
        comp_de: dict[int, int] = {}
        for i, comp in enumerate(componentes):
            for no in comp:
                comp_de[no] = i
        mesmo_scc = comp_de.get(origem) == comp_de.get(destino)

        destino_local = g.buscar_local(destino)

        return {
            "encomenda_id": enc.id,
            "encomenda_nome": enc.nome,
            "destino_id": destino,
            "destino_nome": destino_local.nome if destino_local else str(destino),
            "deposito_id": origem,
            "entrega_direta": entrega_direta,
            "bfs": {
                "alcancavel": resultado_bfs["alcancavel"],
                "distancia_saltos": resultado_bfs["distancia_saltos"],
                "caminho": resultado_bfs["caminho"],
                "caminho_nomes": nomes_bfs,
                "num_caminhos_minimos": resultado_bfs["num_caminhos_minimos"],
            },
            "dfs": {
                "alcancavel": resultado_dfs["alcancavel"],
                "num_rotas": resultado_dfs["num_rotas"],
                "rotas_nomes": rotas_dfs,
            },
            "dijkstra": {
                "alcancavel": resultado_dij["alcancavel"],
                "distancia_km": resultado_dij["distancia_km"],
                "caminho": resultado_dij["caminho"],
                "caminho_nomes": nomes_dij,
            },
            "kosaraju": {
                "mesmo_scc": mesmo_scc,
                "retorno_garantido": mesmo_scc,
            },
        }

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
