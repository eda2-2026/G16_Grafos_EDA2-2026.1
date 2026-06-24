from __future__ import annotations

from arvore.nodo import Nodo, VERMELHO, PRETO


class ArvoreRubroNegra:

    def __init__(self) -> None:
        # Sentinela NIL compartilhado por todas as folhas e pela raiz inicial.
        self._nil = Nodo(None, None)
        self._nil.cor = PRETO
        self._nil.pai = self._nil
        self._nil.esq = self._nil
        self._nil.dir = self._nil
        self._raiz: Nodo = self._nil
        self._tamanho: int = 0

    # ------------------------------------------------------------------
    # Interface pública
    # ------------------------------------------------------------------

    def inserir(self, chave, valor) -> None:
        """Insere chave→valor. Se a chave já existe, atualiza o valor."""
        z = Nodo(chave, valor)
        z.esq = self._nil
        z.dir = self._nil
        z.cor = VERMELHO

        y = self._nil
        x = self._raiz
        while x is not self._nil:
            y = x
            if z.chave < x.chave:
                x = x.esq
            elif z.chave > x.chave:
                x = x.dir
            else:
                x.valor = valor  # chave duplicada: só atualiza
                return

        z.pai = y
        if y is self._nil:
            self._raiz = z
        elif z.chave < y.chave:
            y.esq = z
        else:
            y.dir = z

        self._tamanho += 1
        self._fixup_insercao(z)

    def remover(self, chave) -> bool:
        """Remove o nó com a chave dada. Retorna True se encontrado."""
        z = self._buscar_nodo(chave)
        if z is self._nil:
            return False

        y = z
        y_cor_original = y.cor

        if z.esq is self._nil:
            x = z.dir
            self._transplantar(z, z.dir)
        elif z.dir is self._nil:
            x = z.esq
            self._transplantar(z, z.esq)
        else:
            y = self._minimo_nodo(z.dir)
            y_cor_original = y.cor
            x = y.dir
            if y.pai is z:
                x.pai = y
            else:
                self._transplantar(y, y.dir)
                y.dir = z.dir
                y.dir.pai = y
            self._transplantar(z, y)
            y.esq = z.esq
            y.esq.pai = y
            y.cor = z.cor

        if y_cor_original == PRETO:
            self._fixup_remocao(x)

        self._tamanho -= 1
        return True

    def buscar(self, chave):
        """Retorna o valor associado à chave, ou None se não existir."""
        nodo = self._buscar_nodo(chave)
        return nodo.valor if nodo is not self._nil else None

    def minimo(self):
        """Retorna o valor do nó com menor chave, ou None se vazia."""
        if self._raiz is self._nil:
            return None
        return self._minimo_nodo(self._raiz).valor

    def maximo(self):
        """Retorna o valor do nó com maior chave, ou None se vazia."""
        if self._raiz is self._nil:
            return None
        return self._maximo_nodo(self._raiz).valor

    def traversal_inorder(self) -> list:
        """Retorna lista de valores em ordem crescente de chave."""
        resultado: list = []
        self._inorder(self._raiz, resultado)
        return resultado

    def buscar_intervalo(self, chave_min, chave_max) -> list:
        """Retorna valores cujas chaves estejam em [chave_min, chave_max]."""
        resultado: list = []
        self._intervalo(self._raiz, chave_min, chave_max, resultado)
        return resultado

    def vazia(self) -> bool:
        return self._raiz is self._nil

    def __len__(self) -> int:
        return self._tamanho

    # ------------------------------------------------------------------
    # Rotações (CLRS 13.2)
    # ------------------------------------------------------------------

    def _rotacao_esq(self, x: Nodo) -> None:
        y = x.dir
        x.dir = y.esq
        if y.esq is not self._nil:
            y.esq.pai = x
        y.pai = x.pai
        if x.pai is self._nil:
            self._raiz = y
        elif x is x.pai.esq:
            x.pai.esq = y
        else:
            x.pai.dir = y
        y.esq = x
        x.pai = y

    def _rotacao_dir(self, x: Nodo) -> None:
        y = x.esq
        x.esq = y.dir
        if y.dir is not self._nil:
            y.dir.pai = x
        y.pai = x.pai
        if x.pai is self._nil:
            self._raiz = y
        elif x is x.pai.dir:
            x.pai.dir = y
        else:
            x.pai.esq = y
        y.dir = x
        x.pai = y

    # ------------------------------------------------------------------
    # Fixup de inserção (CLRS 13.3)
    # ------------------------------------------------------------------

    def _fixup_insercao(self, z: Nodo) -> None:
        while z.pai.cor == VERMELHO:
            if z.pai is z.pai.pai.esq:
                tio = z.pai.pai.dir
                if tio.cor == VERMELHO:          # caso 1
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.dir:           # caso 2 → transforma em 3
                        z = z.pai
                        self._rotacao_esq(z)
                    z.pai.cor = PRETO            # caso 3
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_dir(z.pai.pai)
            else:                                # simétrico
                tio = z.pai.pai.esq
                if tio.cor == VERMELHO:          # caso 1
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z is z.pai.esq:           # caso 2 → transforma em 3
                        z = z.pai
                        self._rotacao_dir(z)
                    z.pai.cor = PRETO            # caso 3
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_esq(z.pai.pai)
        self._raiz.cor = PRETO

    # ------------------------------------------------------------------
    # Fixup de remoção (CLRS 13.4)
    # ------------------------------------------------------------------

    def _fixup_remocao(self, x: Nodo) -> None:
        while x is not self._raiz and x.cor == PRETO:
            if x is x.pai.esq:
                w = x.pai.dir
                if w.cor == VERMELHO:                          # caso 1
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_esq(x.pai)
                    w = x.pai.dir
                if w.esq.cor == PRETO and w.dir.cor == PRETO:  # caso 2
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.dir.cor == PRETO:                     # caso 3 → transforma em 4
                        w.esq.cor = PRETO
                        w.cor = VERMELHO
                        self._rotacao_dir(w)
                        w = x.pai.dir
                    w.cor = x.pai.cor                          # caso 4
                    x.pai.cor = PRETO
                    w.dir.cor = PRETO
                    self._rotacao_esq(x.pai)
                    x = self._raiz
            else:                                              # simétrico
                w = x.pai.esq
                if w.cor == VERMELHO:                          # caso 1
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_dir(x.pai)
                    w = x.pai.esq
                if w.dir.cor == PRETO and w.esq.cor == PRETO:  # caso 2
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.esq.cor == PRETO:                     # caso 3 → transforma em 4
                        w.dir.cor = PRETO
                        w.cor = VERMELHO
                        self._rotacao_esq(w)
                        w = x.pai.esq
                    w.cor = x.pai.cor                          # caso 4
                    x.pai.cor = PRETO
                    w.esq.cor = PRETO
                    self._rotacao_dir(x.pai)
                    x = self._raiz
        x.cor = PRETO

    # ------------------------------------------------------------------
    # Auxiliares internos
    # ------------------------------------------------------------------

    def _buscar_nodo(self, chave) -> Nodo:
        x = self._raiz
        while x is not self._nil:
            if chave == x.chave:
                return x
            x = x.esq if chave < x.chave else x.dir
        return self._nil

    def _transplantar(self, u: Nodo, v: Nodo) -> None:
        if u.pai is self._nil:
            self._raiz = v
        elif u is u.pai.esq:
            u.pai.esq = v
        else:
            u.pai.dir = v
        v.pai = u.pai

    def _minimo_nodo(self, x: Nodo) -> Nodo:
        while x.esq is not self._nil:
            x = x.esq
        return x

    def _maximo_nodo(self, x: Nodo) -> Nodo:
        while x.dir is not self._nil:
            x = x.dir
        return x

    def _inorder(self, x: Nodo, resultado: list) -> None:
        if x is not self._nil:
            self._inorder(x.esq, resultado)
            resultado.append(x.valor)
            self._inorder(x.dir, resultado)

    def _intervalo(self, x: Nodo, lo, hi, resultado: list) -> None:
        if x is self._nil:
            return
        if lo < x.chave:
            self._intervalo(x.esq, lo, hi, resultado)
        if lo <= x.chave <= hi:
            resultado.append(x.valor)
        if x.chave < hi:
            self._intervalo(x.dir, lo, hi, resultado)
