# Sistema de Encomendas

Trabalho 3 da disciplina de Estruturas de Dados 2 (EDA2 - 2026.1), ministrada pelo Prof. Maurício Serrano — UnB.

Esse trabalho é uma continuação do Trabalho 2 da disciplina, agora implementando uma **Árvore Rubro-Negra** como estrutura de armazenamento principal do sistema de gerenciamento de encomendas.

## Integrantes

| Nome | Matrícula | GitHub |
|------|-----------|--------|
| Caio Sabino | 231026302 | [@caiomsabino](https://github.com/caiomsabino) |
| João Sapiência | 231026400 | [@JoaoSapiencia](https://github.com/JoaoSapiencia) |

## Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada e menu interativo
├── encomenda.py         # Modelo de dados: classe Encomenda
├── gerenciador.py       # GerenciadorEncomendas: CRUD + ordenação + buscas por árvore
├── arvore/
│   ├── __init__.py      # Expõe ArvoreRubroNegra
│   ├── nodo.py          # Nodo com chave, valor e cor (VERMELHO/PRETO)
│   └── rubro_negra.py   # Árvore Rubro-Negra genérica (CLRS cap. 13)
└── algoritmos/
    ├── __init__.py      # Expõe o dicionário ALGORITMOS
    ├── insertion.py     # Insertion Sort
    ├── selection.py     # Selection Sort
    ├── counting.py      # Counting Sort
    ├── quick.py         # Quick Sort
    ├── radix_lsd.py     # Radix Sort (LSD)
    └── radix_msd.py     # Radix Sort (MSD)
```

## Funcionamento

Cada encomenda cadastrada possui os seguintes atributos:

| Atributo | Descrição |
|----------|-----------|
| `id` | Identificador único (chave primária) |
| `nome` | Nome do produto |
| `data_postagem` | Data de postagem |
| `peso` | Peso do pacote (kg) |
| `quantidade` | Quantidade de itens |
| `prioridade` | Nível de prioridade da entrega (1–5) |

### Árvore Rubro-Negra

O sistema utiliza duas instâncias de `ArvoreRubroNegra` mantidas em sincronia:

| Árvore | Chave | Uso |
|--------|-------|-----|
| `_arvore_id` | `id` | Busca, atualização e remoção em O(log n) |
| `_arvore_prioridade` | `prioridade` | Listagem por urgência e próxima entrega em O(log n) |

A `ArvoreRubroNegra` é genérica e aceita qualquer chave comparável (int, float, date, str). Métodos disponíveis:

| Método | Descrição | Complexidade |
|--------|-----------|--------------|
| `inserir(chave, valor)` | Insere ou atualiza | O(log n) |
| `remover(chave)` | Remove pelo chave | O(log n) |
| `buscar(chave)` | Retorna valor ou None | O(log n) |
| `minimo()` / `maximo()` | Menor/maior chave | O(log n) |
| `traversal_inorder()` | Lista ordenada por chave | O(n) |
| `buscar_intervalo(lo, hi)` | Valores com chave em [lo, hi] | O(log n + k) |

### Operações disponíveis

- **Criar** — cadastra nova encomenda (inserção em ambas as árvores)
- **Listar** — exibe todas as encomendas ordenadas por ID (in-order na `_arvore_id`)
- **Atualizar** — edita atributos de uma encomenda existente
- **Remover** — remove em O(log n) por ID
- **Ordenar** — ordena por qualquer atributo usando os algoritmos clássicos
- **Buscar por intervalo de datas** — retorna encomendas postadas entre duas datas
- **Listar por prioridade** — exibe encomendas da mais urgente à menos urgente
- **Próxima entrega** — retorna a encomenda de maior prioridade em O(log n)

### Algoritmos de ordenação

As encomendas podem ser ordenadas por qualquer atributo usando os algoritmos abaixo:

| Algoritmo | Complexidade (médio) | Complexidade (pior caso) | Estável |
|-----------|----------------------|--------------------------|---------|
| Radix MSD | O(n · k) | O(n · k) | Sim |
| Selection Sort | O(n²) | O(n²) | Não |
| Radix LSD | O(n · k) | O(n · k) | Sim |
| Insertion Sort | O(n²) | O(n²) | Sim |
| Counting Sort | O(n + k) | O(n + k) | Sim |
| Quick Sort | O(n log n) | O(n²) | Não |

> `n` = número de encomendas, `k` = número de dígitos/chaves

## Requisitos

- Python 3.10 ou superior
- FastAPI
- Uvicorn
- Pydantic

## Como executar

1. Instale as dependências executando o comando:
```bash
python -m pip install fastapi uvicorn pydantic
```

2. Inicialize o servidor local:
```bash
python -m uvicorn api:app --reload
```

3. Abra o arquivo `index.html` no seu navegador favorito para visualizar e interagir com o sistema e a Árvore Rubro-Negra!

## Apresentação do Projeto

Confira o vídeo de apresentação demonstrando o funcionamento interno da Árvore Rubro-Negra e a interface interativa:
 [Vídeo de Apresentação no YouTube](https://youtu.be/06MbWmKuyyU)
