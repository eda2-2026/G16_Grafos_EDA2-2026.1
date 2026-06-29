# Sistema de Encomendas - Grafo

Trabalho 4 da disciplina de Estruturas de Dados 2 (EDA2 - 2026.1), ministrada pelo Prof. Maurício Serrano — UnB.

Esse trabalho é uma continuação do Trabalho 3 da disciplina, agora implementando **grafos** como estrutura de armazenamento principal do sistema de gerenciamento de encomendas.

## Integrantes

| Nome | Matrícula | GitHub |
|------|-----------|--------|
| Caio Sabino | 231026302 | [@caiomsabino](https://github.com/caiomsabino) |
| João Sapiência | 231026400 | [@JoaoSapiencia](https://github.com/JoaoSapiencia) |

## Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada e menu interativo
├── api.py               # API FastAPI: endpoints REST de encomendas, análise de rota e CRUD do grafo
├── index.html           # Frontend (árvore, mapa do grafo e CRUD de locais/estradas com D3)
├── encomenda.py         # Modelo de dados: classe Encomenda (com destino_id)
├── gerenciador.py       # GerenciadorEncomendas: CRUD + ordenação + buscas + análise de rota
├── arvore/
│   ├── __init__.py      # Expõe ArvoreRubroNegra
│   ├── nodo.py          # Nodo com chave, valor e cor (VERMELHO/PRETO)
│   └── rubro_negra.py   # Árvore Rubro-Negra genérica 
├── algoritmos/
│   ├── __init__.py      # Expõe o dicionário ALGORITMOS
│   ├── insertion.py     # Insertion Sort
│   ├── selection.py     # Selection Sort
│   ├── counting.py      # Counting Sort
│   ├── quick.py         # Quick Sort
│   ├── radix_lsd.py     # Radix Sort (LSD)
│   └── radix_msd.py     # Radix Sort (MSD)
└── grafo/
    ├── __init__.py      # Expõe Grafo, Local e o grafo-semente
    ├── grafo.py         # Grafo dirigido e ponderado (lista de adjacência)
    ├── local.py         # Local: vértice com nome e coordenadas (x, y)
    ├── semente.py       # grafo_semente(): mapa inicial de locais do DF
    └── algoritmos/
        ├── __init__.py  # Expõe bfs, dfs, dijkstra e Kosaraju
        ├── bfs.py       # Busca em Largura — menor número de saltos
        ├── dfs.py       # Busca em Profundidade — todas as rotas simples
        ├── dijkstra.py  # Dijkstra — menor caminho ponderado (km)
        └── kosaraju.py  # Kosaraju — componentes fortemente conectados
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
| `destino_id` | Id do `Local` no grafo para onde a encomenda será entregue (opcional) |

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

## Grafo de Locais de Entrega

O sistema agora modela a **rede de entrega** como um
**grafo dirigido e ponderado**. Cada encomenda pode ser vinculada a um destino
e o sistema calcula rotas a partir do **Depósito Central** (id `0`, origem padrão).

### Estrutura do grafo

| Componente | Descrição |
|------------|-----------|
| `Local` | Vértice do grafo: um local de entrega com `id`, `nome` e coordenadas `(x, y)` para desenho |
| `Grafo` | Grafo dirigido e ponderado em **lista de adjacência**; cada aresta carrega a distância (km) entre dois locais. Vias de mão dupla são modeladas por duas arestas |
| `grafo_semente()` | Mapa inicial de locais do DF (Plano Piloto, Taguatinga, região Norte…) já conectados, com regiões fortemente conectadas e pontes de mão única entre elas |

O `Grafo` oferece operações de manutenção em tempo constante ou linear: `adicionar_local`,
`remover_local`, `adicionar_estrada` (com opção `bidirecional`), `remover_estrada`,
`vizinhos`, `peso` e `serializar` (exporta locais e estradas em JSON para o frontend D3).

### Algoritmos de grafo

Ao analisar a rota de uma encomenda, o sistema executa quatro algoritmos do
Depósito até o destino e combina os resultados:

| Algoritmo | O que faz | Resposta que entrega | Complexidade |
|-----------|-----------|----------------------|--------------|
| **BFS** (Busca em Largura) | Explora o grafo por camadas a partir da origem | Menor número de **saltos** (estradas) até o destino, o caminho correspondente e quantos caminhos mínimos distintos existem | O(V + E) |
| **DFS** (Busca em Profundidade) | Percorre em profundidade com *backtracking* | **Todas as rotas simples** (sem repetir locais) entre origem e destino | O(V + E) por rota |
| **Dijkstra** | Expande sempre o vértice de menor custo usando uma *min-heap* própria | Menor caminho **ponderado pela distância em km** e a distância mínima até cada local | O((V + E) log V) |
| **Kosaraju** | Duas passagens de DFS (grafo original + transposto) | **Componentes fortemente conectados (SCCs)**: indica se o destino está na mesma região do depósito e se o **retorno é garantido** | O(V + E) |

> `V` = número de locais, `E` = número de estradas

### Análise de rota e agrupamento de entregas

- **Análise de rota individual** — para uma encomenda com destino definido, combina BFS, DFS,
  Dijkstra e Kosaraju, indicando se há **entrega direta** (aresta única origem→destino), o menor
  caminho em saltos, o menor caminho em km, todas as rotas possíveis e se o retorno ao depósito é garantido.
- **Sugestão de pacotes na rota** — para cada rota encontrada pelo DFS, o sistema lista outras
  encomendas pendentes cujo destino esteja em algum ponto do trajeto (exceto o depósito), já que o
  entregador passaria por ali de qualquer forma. As sugestões aparecem ordenadas por prioridade no
  card de DFS do painel de análise .
- **Análise de múltiplas entregas** (`analisar_rotas`) — usa os SCCs de Kosaraju para agrupar
  vários destinos por região e dizer se todas as entregas cabem em **uma rota única** ou se é
  preciso dividir em **rotas separadas**, sinalizando destinos inalcançáveis ou inexistentes.

### Gerenciamento do grafo

O grafo pode ser editado direto pela interface, na seção **"Gerenciar Grafo (Locais e Estradas)"**:
adicionar/remover locais e estradas (com distância e opção de mão dupla). A tabela de encomendas,
os dropdowns de destino e o mapa do grafo se atualizam automaticamente a cada alteração.

### Visualizador estrutural do grafo

O seletor "Visualizador Estrutural" tem uma terceira opção, **Grafo de Locais (Mapa)**, que desenha
com D3 todos os locais nas coordenadas do grafo-semente e as estradas entre eles: linha cinza
contínua com seta nas duas pontas para vias de mão dupla, e linha laranja tracejada com seta única
para as pontes de mão única entre regiões.


## Requisitos

- Python 3.10 ou superior
- FastAPI
- Uvicorn
- Pydantic

## Como executar

1. Crie o ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências executando o comando:
```bash
python -m pip install fastapi uvicorn pydantic
```

3. Inicialize o servidor local:
```bash
python -m uvicorn api:app --reload
```

4. Abra o arquivo `index.html` no seu navegador favorito para visualizar e interagir com o sistema e a Árvore Rubro-Negra!

## Apresentação do Projeto

Confira o vídeo de apresentação demonstrando o funcionamento interno da Árvore Rubro-Negra e a interface interativa:
 [Vídeo de Apresentação no YouTube]()
