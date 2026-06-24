import sys
from datetime import date

from gerenciador import GerenciadorEncomendas
from algoritmos import ALGORITMOS

_ATRIBUTOS = ["nome", "id", "data_postagem", "peso", "quantidade", "prioridade"]


def _ler_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("  Valor inválido. Informe um inteiro (ex: 3).")


def _ler_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  Valor inválido. Informe um número (ex: 1.5).")


def _ler_data(prompt: str) -> date:
    while True:
        raw = input(prompt).strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  Formato inválido. Use AAAA-MM-DD (ex: 2026-05-10).")


def _exibir(encomendas):
    if not encomendas:
        print("  (nenhuma encomenda cadastrada)")
        return
    print(f"\n  {'ID':<4} {'Nome':<20} {'Data':<12} {'Peso (kg)':>9} {'Qtd':>5} {'Prior':>6}")
    print("  " + "-" * 62)
    for e in encomendas:
        print(
            f"  {e.id:<4} {e.nome:<20} {str(e.data_postagem):<12}"
            f" {e.peso:>9.2f} {e.quantidade:>5} {e.prioridade:>6}"
        )
    print()


def op_criar(g: GerenciadorEncomendas) -> None:
    print("\n-- Nova Encomenda --")
    nome = input("  Nome do produto: ").strip()
    data = _ler_data("  Data de postagem (AAAA-MM-DD): ")
    peso = _ler_float("  Peso (kg): ")
    quantidade = _ler_int("  Quantidade: ")
    prioridade = _ler_int("  Prioridade (1-5): ")
    enc = g.criar(nome, data, peso, quantidade, prioridade)
    print(f"  Encomenda criada com ID {enc.id}.")


def op_listar(g: GerenciadorEncomendas) -> None:
    print("\n-- Encomendas Cadastradas --")
    _exibir(g.listar())


def op_atualizar(g: GerenciadorEncomendas) -> None:
    print("\n-- Atualizar Encomenda --")
    id_ = _ler_int("  ID da encomenda: ")
    enc = g.buscar_por_id(id_)
    if enc is None:
        print(f"  Encomenda ID {id_} não encontrada.")
        return

    print(f"  {enc}")
    print("  (pressione Enter para manter o valor atual)")

    raw = input(f"  Nome [{enc.nome}]: ").strip()
    nome = raw if raw else None

    raw = input(f"  Data [{enc.data_postagem}] (AAAA-MM-DD): ").strip()
    if raw:
        try:
            data = date.fromisoformat(raw)
        except ValueError:
            print("  Data inválida, mantendo o valor atual.")
            data = None
    else:
        data = None

    raw = input(f"  Peso [{enc.peso}]: ").strip()
    try:
        peso = float(raw) if raw else None
    except ValueError:
        print("  Peso inválido, mantendo o valor atual.")
        peso = None

    raw = input(f"  Quantidade [{enc.quantidade}]: ").strip()
    try:
        quantidade = int(raw) if raw else None
    except ValueError:
        print("  Quantidade inválida, mantendo o valor atual.")
        quantidade = None

    raw = input(f"  Prioridade [{enc.prioridade}]: ").strip()
    try:
        prioridade = int(raw) if raw else None
    except ValueError:
        print("  Prioridade inválida, mantendo o valor atual.")
        prioridade = None

    g.atualizar(id_, nome=nome, data_postagem=data, peso=peso,
                quantidade=quantidade, prioridade=prioridade)
    print("  Encomenda atualizada.")


def op_remover(g: GerenciadorEncomendas) -> None:
    print("\n-- Remover Encomenda --")
    id_ = _ler_int("  ID da encomenda: ")
    if g.remover(id_):
        print(f"  Encomenda ID {id_} removida.")
    else:
        print(f"  Encomenda ID {id_} não encontrada.")


def op_ordenar(g: GerenciadorEncomendas) -> None:
    print("\n-- Ordenar Encomendas --")

    algoritmos_lista = list(ALGORITMOS.keys())

    print("  Atributos disponíveis:")
    for i, a in enumerate(_ATRIBUTOS, 1):
        print(f"    {i}. {a}")

    idx_atr = _ler_int("  Escolha o atributo (número): ") - 1
    if not (0 <= idx_atr < len(_ATRIBUTOS)):
        print("  Opção inválida.")
        return
    atributo = _ATRIBUTOS[idx_atr]

    print("  Algoritmos disponíveis:")
    for i, a in enumerate(algoritmos_lista, 1):
        print(f"    {i}. {a}")

    idx_alg = _ler_int("  Escolha o algoritmo (número): ") - 1
    if not (0 <= idx_alg < len(algoritmos_lista)):
        print("  Opção inválida.")
        return
    algoritmo = algoritmos_lista[idx_alg]

    resultado = g.ordenar(atributo, algoritmo)
    print(f"\n  Ordenado por '{atributo}' usando '{algoritmo}':")
    _exibir(resultado)


def op_listar_prioridade(g: GerenciadorEncomendas) -> None:
    print("\n-- Encomendas por Prioridade --")
    _exibir(g.listar_por_prioridade())


def op_proxima_entrega(g: GerenciadorEncomendas) -> None:
    print("\n-- Próxima Entrega --")
    enc = g.proxima_entrega()
    _exibir([enc] if enc else [])


def op_buscar_intervalo(g: GerenciadorEncomendas) -> None:
    print("\n-- Buscar por Intervalo de Datas --")
    inicio = _ler_data("  Data inicial (AAAA-MM-DD): ")
    fim = _ler_data("  Data final (AAAA-MM-DD): ")
    if data_invalida := (inicio > fim):
        print("  Data inicial não pode ser depois da data final.")
        return
    resultado = g.buscar_por_intervalo_data(inicio, fim)
    _exibir(resultado)


_OPCOES = {
    "1": op_criar,
    "2": op_listar,
    "3": op_atualizar,
    "4": op_remover,
    "5": op_ordenar,
    "6": op_listar_prioridade,
    "7": op_proxima_entrega,
    "8": op_buscar_intervalo,
}


def menu() -> None:
    g = GerenciadorEncomendas()

    while True:
        print("\n===== Sistema de Encomendas =====")
        print("  1. Criar encomenda")
        print("  2. Listar encomendas")
        print("  3. Atualizar encomenda")
        print("  4. Remover encomenda")
        print("  5. Ordenar encomendas")
        print("  6. Listar por prioridade")
        print("  7. Próxima entrega (maior prioridade)")
        print("  8. Buscar por intervalo de datas")
        print("  0. Sair")
        print("=================================")

        escolha = input("  Opção: ").strip()

        if escolha == "0":
            print("  Encerrando.")
            sys.exit(0)

        op = _OPCOES.get(escolha)
        if op is None:
            print("  Opção inválida.")
        else:
            op(g)


if __name__ == "__main__":
    menu()
