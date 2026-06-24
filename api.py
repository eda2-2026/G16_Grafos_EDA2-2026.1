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

@app.get("/")
def pagina_principal():
    return FileResponse("index.html")

@app.get("/encomendas")
def listar_todas():
    # Retorna todas as encomendas em ordem de ID
    encomendas = g.listar()
    return [{"id": e.id, "nome": e.nome, "data_postagem": str(e.data_postagem), "peso": e.peso, "quantidade": e.quantidade, "prioridade": e.prioridade} for e in encomendas]

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

    for _ in range(quantidade):
        nome = f"{random.choice(tipos)} {random.choice(marcas)} {random.randint(100, 999)}"
        dt = data_base - timedelta(days=random.randint(0, 365))
        peso = round(random.uniform(0.1, 50.0), 2)
        qtd = random.randint(1, 100)
        prio = random.randint(1, 5)
        g.criar(nome, dt, peso, qtd, prio)

    return {"mensagem": f"{quantidade} encomendas criadas e indexadas nas Árvores Rubro-Negras!"}

# --- Rota para Visualizar a Árvore (bônus!) ---
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
