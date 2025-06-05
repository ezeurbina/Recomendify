from grafo import Grafo
from collections import deque
import random
AMORTIGUACION = 0.85
TOLERANCIA = 0.00001
ITERACIONES = 100
ITERACIONES_PRP = 90


def camino_minimo(g: Grafo, origen, destino):
    visitados = set()
    distancias = {}
    padres = {}
    for v in g.vertices():
        padres[v] = None
        distancias[v] = float('inf')

    distancias[origen] = 0
    padres[origen] = None
    cola = deque()

    cola.append(origen)
    while len(cola) > 0:
        desencolado = cola.popleft()
        visitados.add(desencolado)
        for ady in g.adyacentes(desencolado):
            if ady not in visitados:
                padres[ady] = desencolado
                distancias[ady] = distancias[desencolado]+1
                cola.append(ady)
                visitados.add(ady)
                if ady == destino:
                    break

    return distancias, padres


def pagerank_personalizado(g: Grafo, listado_vertices: list, n: int, opcion):
    ranking = {v: 0 for v in g.vertices()}

    for _ in range(ITERACIONES_PRP):
        for v in listado_vertices:
            origen=random.choice(listado_vertices)
            ran_walk(g,origen,ranking)

    return ranking

def ran_walk(g:Grafo,origen,ranking:dict):
    pg = 1
    act = origen
    for i in range(ITERACIONES_PRP):
        vecino = random.choice(list(g.adyacentes(act)))
        n_pg = pg / len(g.adyacentes(act))
        pg = n_pg
        ranking[act] += n_pg
        act = vecino


def parse_spotify(linea):
    user = linea[1]
    cancion = linea[2]
    artista = linea[3]
    playlist = linea[5]
    canar = f"{cancion} - {artista}"
    return user, playlist, canar


def rango_vertice(grafo: Grafo, vertice_inicial, tope):
    cola = deque()
    cola.append(vertice_inicial)
    distancia = {vertice_inicial: 0}
    visitados = set()
    visitados.add(vertice_inicial)
    vertices_a_distancia = []
    while len(cola) > 0:
        v = cola.popleft()
        if distancia[v] > tope:
            break
        for w in grafo.adyacentes(v):
            if w not in visitados:
                distancia[w] = distancia[v]+1
                cola.append(w)
                visitados.add(w)
                if distancia[w] == tope:
                    vertices_a_distancia.append(w)

    return vertices_a_distancia

def reconstruir(padres: dict, origen, destino) -> list:
    lista = [destino]
    act = destino
    while act != origen:
        act = padres[act]
        lista.append(act)

    return lista[::-1]

def dfs_ciclo(g: Grafo, origen, n):
    visitados = set()
    recorrido = []
    destino = recu_dfs_ciclo(g, origen, origen, 1, n,recorrido, visitados)
    if destino is not None:
        return recorrido + [origen]
    return "No se encontro ciclo"


def recu_dfs_ciclo(g: Grafo, origen, v, pos, tope,recorrido, visitados):
    visitados.add(v)
    recorrido.append(v)
    if pos == tope:  # llega al tope n y si encuentra un ciclo devuelve el recorrido
        if origen in g.adyacentes(v):
            return recorrido
        else:
            visitados.remove(v)
            recorrido.pop()
            return None
    
    for a in g.adyacentes(v):
        if a not in visitados:
            destino = recu_dfs_ciclo(g, origen, a, pos+1, tope, recorrido, visitados)
            if destino is not None:
                return recorrido  # ya se encontró el ciclo y vuelve en la recursion
    # recorrió a todos sus adyacentes y no llegó a un ciclo n
    visitados.remove(v)
    recorrido.pop()
    return None  # Si no hay ciclo devuelve None


def pagerank(g:Grafo):
    vertices = g.vertices()
    n = len(vertices)
    rnk_inicial = 1 /n
    ranking = {v: rnk_inicial for v in vertices}


    for _ in range(ITERACIONES):
        nuevo_ranking = ranking.copy()
        for v in vertices:
            suma = 0
            for a in g.adyacentes(v):
                adj_a = len(g.adyacentes(a))
                suma += ranking[a] / adj_a
        
            nuevo_ranking[v] = ((1 - AMORTIGUACION) / n) + AMORTIGUACION * suma
        
        cambio = 0
        for v in ranking:
            cambio += abs(nuevo_ranking[v]-ranking[v])
        if cambio < TOLERANCIA:
            break        
        ranking = nuevo_ranking

    return ranking
