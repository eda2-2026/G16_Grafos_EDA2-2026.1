from __future__ import annotations

from grafo.grafo import Grafo

# Serve para colocar como exemplo as primeiras cidades, representando já grafos fortemente conectados e rotas que exigem mais de um caminho

def grafo_semente() -> Grafo:
    g = Grafo()

    # Locais (a ordem de inserção define os ids
    g.adicionar_local("Depósito Central (SIA)", x=500, y=400)  
    g.adicionar_local("Asa Norte", x=480, y=300)               
    g.adicionar_local("Asa Sul", x=520, y=480)                 
    g.adicionar_local("Lago Norte", x=580, y=240)
    g.adicionar_local("Lago Sul", x=600, y=520)                
    g.adicionar_local("Taguatinga", x=300, y=420)              
    g.adicionar_local("Ceilândia", x=180, y=400)               
    g.adicionar_local("Águas Claras", x=330, y=490)            
    g.adicionar_local("Samambaia", x=220, y=540)               
    g.adicionar_local("Gama", x=440, y=720)                    
    g.adicionar_local("Sobradinho", x=640, y=150)              
    g.adicionar_local("Planaltina", x=760, y=110)              

    # SCC 0: Plano Piloto (vias de mão dupla) 
    g.adicionar_estrada(0, 1, 8, bidirecional=True)
    g.adicionar_estrada(0, 2, 9, bidirecional=True)
    g.adicionar_estrada(1, 2, 5, bidirecional=True)
    g.adicionar_estrada(1, 3, 6, bidirecional=True)
    g.adicionar_estrada(2, 4, 7, bidirecional=True)
    g.adicionar_estrada(3, 4, 12, bidirecional=True)

    # SCC 1: Taguatinga (vias de mão dupla internas) 
    g.adicionar_estrada(5, 6, 8, bidirecional=True)
    g.adicionar_estrada(5, 7, 6, bidirecional=True)
    g.adicionar_estrada(7, 8, 10, bidirecional=True)
    g.adicionar_estrada(6, 8, 9, bidirecional=True)

    # SCC 2: Norte (vias de mão dupla internas) 
    g.adicionar_estrada(10, 11, 12, bidirecional=True)

    #  Pontes de mão única entre regiões (
    g.adicionar_estrada(0, 5, 25)   # Depósito  -> Taguatinga
    g.adicionar_estrada(1, 10, 20)  # Asa Norte -> Sobradinho
    g.adicionar_estrada(2, 9, 30)   # Asa Sul   -> Gama

    return g


# Id do depósito no grafo-semente (origem padrão das rotas).
DEPOSITO_ID = 0
