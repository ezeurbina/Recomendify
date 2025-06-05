#!/usr/bin/env python3
import sys
from impl_recomendify import Recomendify
import output_recomendify as out_recom


def inicializacion(f):
    r=Recomendify()
    r.iniciar_grafo_user(f)
    comandos={
        "camino":out_recom.camino_mas_corto,
        
        "mas_importantes":out_recom.canciones_mas_importantes,

        "recomendacion":out_recom.recomendacion,

        "ciclo":out_recom.ciclo_canciones,

        "rango":out_recom.rango,  
    }
    return r,comandos



def main():
    f = sys.argv[1]
    (r,comandos)=inicializacion(f)
    
    for linea in sys.stdin:
        linea_formato = linea.lstrip().rstrip()
        comando = linea_formato.split()[0]
        if comando in comandos:
            comandos[comando](r,linea_formato)    
                           
    

main()

