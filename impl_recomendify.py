from grafo import Grafo
import biblioteca
import csv
import heapq
import sys

class Recomendify():
    def __init__(self):
        self.usuarios = set()
        self.canciones = set()
        self.grafo_usuarios = Grafo()
        self.grafo_canciones = Grafo()
        self.pagerank = []

    def iniciar_grafo_user(self,ruta):
        with open(ruta) as f:
            next(f)#salta la primera linea
            tsv_f = csv.reader(f,delimiter = "\t", quoting = csv.QUOTE_NONE)
            for linea in tsv_f:
                user,playlist,can_ar = biblioteca.parse_spotify(linea)
                self.grafo_usuarios.agregar_vertice(user)
                self.grafo_usuarios.agregar_vertice(can_ar)
                self.grafo_usuarios.agregar_arista(user,can_ar,playlist)
                
                self.canciones.add(can_ar)
                self.usuarios.add(user)

    def _iniciar_grafo_canciones(self):
        if len(self.grafo_canciones.vertices()) != 0:
            return
        self.grafo_canciones.agregar_listado(self.canciones)

        adyacencias = {c : {} for c in self.canciones}
        for c in self.canciones:
            for u in self.grafo_usuarios.adyacentes(c):
                adyacencias[c].update(self.grafo_usuarios.adyacentes(u))    
            adyacencias[c].pop(c)
        self.grafo_canciones.agregar_dict_ady(adyacencias)

    def camino_mas_corto(self,origen,destino):
        _,padres = biblioteca.camino_minimo(self.grafo_usuarios,origen,destino)
        if padres[destino] is None:
            return "No se encontro recorrido"
        canciones_usuarios = biblioteca.reconstruir(padres,origen,destino)
        return self._agregar_playlists_camino(canciones_usuarios)

    def _crear_pagerank(self):
        if len(self.pagerank)==0:
            dict_pagerank = biblioteca.pagerank(self.grafo_usuarios)
            lista_pagerank = []
            for k,v in dict_pagerank.items():
                if k in self.canciones:
                    lista_pagerank.append((k,v))
            self.pagerank = lista_pagerank


    def canciones_mas_importantes(self,tope:int):
        self._crear_pagerank()
        canciones_pedidas = heapq.nlargest(tope,self.pagerank,key = lambda e:e[1])
        importantes = []
        for c in canciones_pedidas:
            importantes.append(c[0])
        return importantes

    def recomendaciones_usuario_canciones(self,listado_vertices,n,opcion):
        recomendaciones = biblioteca.pagerank_personalizado(self.grafo_usuarios,listado_vertices,n,opcion)
        recomendaciones_list = []
        if opcion=="usuarios":
            for k,v in recomendaciones.items():
                if k in self.usuarios:
                    recomendaciones_list.append((k,v))
        else:
            for k,v in recomendaciones.items():
                if k in self.canciones and k not in listado_vertices:
                    recomendaciones_list.append((k,v))
        recomendaciones_list=heapq.nlargest(n,recomendaciones_list, key = lambda e:e[1])
        recomendadas = []
        for c in recomendaciones_list:
            recomendadas.append(c[0])
        return recomendadas

    def rango_canciones(self,cancion,tope:int):
        self._iniciar_grafo_canciones()
        return len(biblioteca.rango_vertice(self.grafo_canciones,cancion,tope))
    
    def ciclo_canciones(self,origen,n):
        self._iniciar_grafo_canciones()
        ciclo = biblioteca.dfs_ciclo(self.grafo_canciones,origen,n)
        return ciclo
    
    def validar_cancion(self,c):
        return c in self.canciones
    
    def _agregar_playlists_camino(self,canciones_usuarios):
        lista_camino_mas_corto = []
        largo = len(canciones_usuarios)
        for i in range(largo // 2):
            index_cancion = i * 2
            index_usuario = (i * 2) + 1
            
            cancion = canciones_usuarios[index_cancion]
            usuario = canciones_usuarios[index_usuario]
            siguiente_cancion = canciones_usuarios[index_usuario + 1]
            
            lista_camino_mas_corto.append(cancion) 
            
            playlist = self.grafo_usuarios.obtener_arista(cancion,usuario)
            lista_camino_mas_corto.append(playlist)

            lista_camino_mas_corto.append(usuario)

            playlist = self.grafo_usuarios.obtener_arista(siguiente_cancion,usuario)
            lista_camino_mas_corto.append(playlist)

        lista_camino_mas_corto.append(canciones_usuarios[largo - 1])

        return lista_camino_mas_corto
