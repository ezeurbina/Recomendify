import random
class Grafo:
    def __init__(self,es_dirigido=False):
        self.dirigido=es_dirigido
        self.vecinos={}

    def agregar_vertice(self,v):
        if v not in self.vecinos:
            self.vecinos[v]={}

    def agregar_listado(self,listado):
        for v in listado:
            self.agregar_vertice(v)

    def vertices(self):
        return self.vecinos

    def agregar_arista(self,v,w,peso=1):
        if v in self.vecinos and w in self.vecinos:    
            self._unir_vertices(v,w,peso)
            if not self.dirigido:
                self._unir_vertices(w,v,peso)

    def agregar_dict_ady(self,adys):
        for v,a in adys.items():
            if v not in self.vecinos:
                self.agregar_vertice(v)
            self.vecinos[v]=a

    def adyacentes(self,v):
        return self.vecinos[v]
    
    def obtener_arista(self,v,w):
        return self.vecinos[v][w]
    
    def  estan_unidas(self,v,w):
        return w in self.vecinos[v]
    
    def vertice_aleatorio(self):
        return random.choice(self.vertice)
    
    def pertenece(self,v):
        return v in self.vecinos
    
    def _unir_vertices(self,v,w,peso):
        self.vecinos[v][w]=peso
    
