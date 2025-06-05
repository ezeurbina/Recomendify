import sys
from impl_recomendify import Recomendify

_SIN_RECORRIDO = "  No se encontro recorrido"
_NO_SON_CANCIONES = "  Tanto el origen como el destino deben ser canciones"
_SEPARACION_CANCIONES = " >>>> "
_COMANDO_CAMINO = "camino "
_COMANDO_RECOMENDACION = "recomendacion "
_INDEX_PLAYLIST = 1
_INDEX_USUARIO = 2

def imprimir_camino(canciones_usuarios):
    if type(canciones_usuarios)!=list:
        print(_SIN_RECORRIDO)
        return
    
    cadena = ""
    largo = len(canciones_usuarios)
    for i in range(largo // 4):
        cancion = 4 * i
        usuario = cancion + _INDEX_USUARIO
        cadena += canciones_usuarios[cancion] + " --> aparece en playlist --> " + str(canciones_usuarios[cancion + _INDEX_PLAYLIST]) + " --> de --> " + str(canciones_usuarios[usuario]) + " --> tiene una playlist --> " + canciones_usuarios[usuario + _INDEX_PLAYLIST] + " --> donde aparece --> "
    print("  " + cadena + canciones_usuarios[largo-1])

def imprimir_canciones(canciones):
    cadena = ""
    for cancion in canciones:
        cadena += cancion + "; "
    print("  " + cadena.rstrip("; "))

def imprimir_ciclo(canciones):
    if type(canciones) != list:
        print(_SIN_RECORRIDO)
        return
    cadena = ""
    for cancion in canciones:
        cadena += cancion + " --> "
    print("  " + cadena.rstrip(" --> "))

def listado_canciones(linea):
    canciones = linea.split(_SEPARACION_CANCIONES)
    return canciones

def linea_simple(linea):
    datos = linea.split(" ",2)
    return datos[1],datos[2]

def camino_mas_corto(r:Recomendify,linea):
    linea_lmp = linea.lstrip(_COMANDO_CAMINO)
    canciones = listado_canciones(linea_lmp)
    cancion1 = canciones[0]
    cancion2 = canciones[1]

    if r.validar_cancion(cancion1) and r.validar_cancion(cancion2):
        imprimir_camino(r.camino_mas_corto(cancion1,cancion2))
    else:
        print(_NO_SON_CANCIONES)

def canciones_mas_importantes(r:Recomendify,linea):
    tope = linea.split()[1]
    
    imprimir_canciones(r.canciones_mas_importantes(int(tope)))

def recomendacion(r:Recomendify,linea):
    linea_lmp=linea.lstrip(_COMANDO_RECOMENDACION)
    opcion=linea_lmp.split(" ",2)[0]
    linea_lmp=linea_lmp.lstrip(opcion + " ")
    tope=linea_lmp.split(" ",2)[0]
    linea_lmp=linea_lmp.lstrip(tope + " ")
    canciones=listado_canciones(linea_lmp)

    imprimir_canciones(r.recomendaciones_usuario_canciones(canciones,int(tope),opcion))

def ciclo_canciones(r:Recomendify,linea):
    iter,cancion=linea_simple(linea)
    imprimir_ciclo(r.ciclo_canciones(cancion,int(iter)))

def rango(r:Recomendify,linea):
    n,cancion=linea_simple(linea)
    print("  " + str(r.rango_canciones(cancion,int(n))))