from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date, timedelta
import random

from gerenciador import GerenciadorEncomendas
from algoritmos import ALGORITMOS

app = FastAPI(title="Sistema de Logística - Árvore Rubro-Negra")
g = GerenciadorEncomendas()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EncomendaIn(BaseModel):
    nome: str
    data_postagem: date
    peso: float
    quantidade: int
    prioridade: int

class EncomendaUpdate(BaseModel):
    nome: str
    data_postagem: date
    peso: float
    quantidade: int
    prioridade: int

class DestinoIn(BaseModel):
    destino_id: int

@app.get("/")
def pagina_principal():
    return FileResponse("index.html")

@app.get("/encomendas")
def listar_todas():
    # Retorna todas as encomendas em ordem de ID
    encomendas = g.listar()
    resultado = []
    for e in encomendas:
        local = g.grafo.buscar_local(e.destino_id) if e.destino_id is not None else None
        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "data_postagem": str(e.data_postagem),
            "peso": e.peso,
            "quantidade": e.quantidade,
            "prioridade": e.prioridade,
            "destino_id": e.destino_id,
            "destino_nome": local.nome if local else None,
        })
    return resultado

@app.get("/encomendas/prioridade")
def listar_por_prioridade():
    # Retorna todas as encomendas em ordem de Prioridade (Maior para menor)
    encomendas = g.listar_por_prioridade()
    return [{"id": e.id, "nome": e.nome, "data_postagem": str(e.data_postagem), "peso": e.peso, "quantidade": e.quantidade, "prioridade": e.prioridade} for e in encomendas]

@app.post("/encomendas")
def criar_nova(enc: EncomendaIn):
    nova = g.criar(enc.nome, enc.data_postagem, enc.peso, enc.quantidade, enc.prioridade)
    return {"mensagem": "Encomenda criada!", "id": nova.id}

@app.put("/encomendas/{id}")
def atualizar_encomenda(id: int, encomenda_dados: EncomendaUpdate):
    resultado = g.atualizar(
        id=id,
        nome=encomenda_dados.nome,
        data_postagem=encomenda_dados.data_postagem,
        peso=encomenda_dados.peso,
        quantidade=encomenda_dados.quantidade,
        prioridade=encomenda_dados.prioridade
    )
    if resultado is None:
        raise HTTPException(status_code=404, detail="Encomenda não encontrada")
    return {"mensagem": "Encomenda atualizada com sucesso!"}

@app.delete("/encomendas/{id}")
def excluir_encomenda(id: int):
    resultado = g.remover(id)
    if not resultado: 
        raise HTTPException(status_code=404, detail="Encomenda não encontrada")
    return {"mensagem": "Encomenda excluída com sucesso!"}

@app.get("/encomendas/proxima")
def proxima_entrega():
    enc = g.proxima_entrega()
    if enc is None:
        raise HTTPException(status_code=404, detail="Nenhuma encomenda pendente")
    return {"id": enc.id, "nome": enc.nome, "prioridade": enc.prioridade}

@app.post("/gerar-teste/{quantidade}")
def gerar_massa_teste(quantidade: int):
    tipos = ["Notebook", "Monitor", "Cadeira", "Teclado", "Mouse", "Mesa", "Gabinete", "Placa", "Cabo"]
    marcas = ["Dell", "Razer", "Logitech", "Corsair", "Asus", "Acer", "LG", "Samsung"]
    data_base = date.today()

    # IDs disponíveis no grafo, excluindo o depósito (id=0) que é sempre a origem
    destinos_possiveis = [local.id for local in g.grafo.locais() if local.id != 0]

    for _ in range(quantidade):
        nome = f"{random.choice(tipos)} {random.choice(marcas)} {random.randint(100, 999)}"
        dt = data_base - timedelta(days=random.randint(0, 365))
        peso = round(random.uniform(0.1, 50.0), 2)
        qtd = random.randint(1, 100)
        prio = random.randint(1, 5)
        enc = g.criar(nome, dt, peso, qtd, prio)
        # Atribui destino aleatório — o usuário pode alterar pelo dropdown
        g.definir_destino(enc.id, random.choice(destinos_possiveis))

    return {"mensagem": f"{quantidade} encomendas criadas com destinos aleatórios!"}


# --- Rota para Visualizar a Árvore  ---
def serializar_nodo(nodo, arvore):
    from arvore.nodo import PRETO, VERMELHO
    if nodo is arvore._nil:
        return None
    return {
        "id": nodo.valor.id if hasattr(nodo.valor, 'id') else str(nodo.chave),
        "chave": str(nodo.chave),
        "cor": "preto" if getattr(nodo, 'cor', None) == PRETO else "vermelho",
        "esq": serializar_nodo(nodo.esq, arvore) if hasattr(nodo, 'esq') else None,
        "dir": serializar_nodo(nodo.dir, arvore) if hasattr(nodo, 'dir') else None
    }

@app.get("/arvore/{tipo}")
def arvore_json(tipo: str):
    # tipo: 'id' ou 'prioridade'
    arvore = g._arvore_id if tipo == 'id' else g._arvore_prioridade
    return serializar_nodo(arvore._raiz, arvore)


# -----------------------------------------------------------------------
# Endpoints do Grafo
# -----------------------------------------------------------------------

@app.get("/grafo")
def grafo_json():
    """Serializa o grafo (locais + estradas) para o frontend D3."""
    return g.grafo.serializar()


@app.patch("/encomendas/{id}/destino")
def definir_destino(id: int, dados: DestinoIn):
    """Vincula um Local do grafo como destino de uma encomenda."""
    enc = g.definir_destino(id, dados.destino_id)
    if enc is None:
        raise HTTPException(
            status_code=404,
            detail="Encomenda não encontrada ou local inválido."
        )
    local = g.grafo.buscar_local(enc.destino_id)
    return {
        "mensagem": "Destino definido com sucesso!",
        "encomenda_id": enc.id,
        "destino_id": enc.destino_id,
        "destino_nome": local.nome if local else None,
    }


@app.get("/encomendas/{id}/analise")
def analisar_rota(id: int):
    """Roda BFS, DFS, Dijkstra e Kosaraju do depósito até o destino
    da encomenda e retorna o resultado consolidado."""
    resultado = g.analisar_rota(id)
    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Encomenda não encontrada ou sem destino definido."
        )
    return resultado
