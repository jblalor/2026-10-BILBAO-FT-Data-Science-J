# encoding: utf-8

# Funciones para HLF. 

# $Version: 1 $, $Fecha: 2026-10-21 (mie, 21 oct 2026). Por Julio Blanco Lorenzo. 


# funciones: 
# probables(tablero)
#   Devuelve la lista de casillas donde es más probable que se sitúe un barco en un tablero en el que lo que se conoce son
#   las coordenadas de los disparos previamente efectuados. 


import inspect
import random as rnd
import time
import pprint
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgba
from matplotlib.colors import ListedColormap
import os
import platform
import subprocess


def hov(s_hov):
    """
    Función que devuelve 0 si s_hov es "h", y 1 si s_hov es "v". 
    
    Entradas: 
    s_hov: "h" ó "v". Tipo: str. 
    
    Salidas: 
    i_hov: 0 ó 1. Tipo: int. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    i_hov = None
    
    if s_hov == 'h':
        i_hov = 0
    elif s_hov == 'v':
        i_hov = 1
    
    return i_hov


def ind_2d_a_1d(col, fil, ncol):
    """
    Convierte un índice 2D (fila, columna) de la celda de una matriz 2D 
    a 1D. 
    
    Entradas:
       col: nº de columna. Entero no negativo, incluyendo 0. Tipo: int. 
       fil: nº de fila. Entero no negativo, incluyendo 0. Tipo: int. 
       ncol: Nº de columnas de la matriz. Entero positivo. 
             Debe ser mayor que col. Tipo: int. 
       
    Salidas:
       ind1d: índice 1D. Entero no negativo, incluyendo 0. Tipo: int. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    ind1d = None
    
    if not (isinstance(fil, int) and isinstance(col, int) and isinstance(ncol, int)):
        print(f'\n-{nomfun}-: \nERROR: fil ({fil}), col ({col}), y ncol ({ncol}) deben ser enteros. \n')
        raise TypeError(f'\n-{nomfun}-: \nERROR: fil ({fil}), col ({col}), y ncol ({ncol}) deben ser enteros. \n')
    elif fil < -0.1 or col < -0.1:
        print(f'\n-{nomfun}-: \nERROR: Los índices de fila ({fil}) y columna ({col}) deben ser no negativos. \n')
        raise ValueError(f'\n-{nomfun}-: \nERROR: Los índices de fila ({fil}) y columna ({col}) deben ser no negativos. \n')
    elif ncol - col < 0.1:
        print(f'\n-{nomfun}-: \nERROR: El índice de columna excede el nº de columnas. \n')
        raise ValueError(f'\n-{nomfun}-: \nERROR: El índice de columna excede el nº de columnas. \n')
    else:
        ind1d = fil * ncol + col
    
    return ind1d


def ind_1d_a_2d(ind1d, ncol):
    """
    Convierte un índice 1D a 2D (fila, columna). 
    
    Entradas:
       ind1d: índice 1D. Entero no negativo, incluyendo 0. Tipo: int. 
       ncol: Nº de columnas de la matriz. Entero positivo. 
    
    Salidas:
       xy: lista [x, y] con las coordenadas x (columna) e y (fila) correspondientes 
           a ind1d. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    xy = None
    
    if not (isinstance(ind1d, int) and isinstance(ncol, int)):
        print(f'\n-{nomfun}-: \nERROR: ind1d ({ind1d}) y ncol ({ncol}) deben ser enteros. \n')
        raise TypeError(f'\n-{nomfun}-: \nERROR: ind1d ({ind1d}) y ncol ({ncol}) deben ser enteros. \n')
    elif ind1d < -0.1:
        print(f'\n-{nomfun}-: \nERROR: ind1d ({ind1d}) debe ser no negativo. \n')
        raise ValueError(f'\n-{nomfun}-: \nERROR: ind1d ({ind1d}) debe ser no negativo. \n')
    elif ncol < 0.1:
        print(f'\n-{nomfun}-: \nERROR: ncol ({ncol}) debe ser mayor que 0. \n')
        raise ValueError(f'\n-{nomfun}-: \nERROR: ncol ({ncol}) debe ser mayor que 0. \n')
    else:
        fil = ind1d // ncol
        col = ind1d % ncol
        xy = [col, fil]
    
    return xy


def inic_tablero(stri, ncol, nfil):
    """
    Inicializar un tablero 2D rectangular. 
    
    Entradas: 
       stri: string con el que se inicializan todas las celdas del tablero. 
             Tipo: str. 
       ncol: nº de columnas del tablero. Entero positivo. 
       nfil: nº de filas del tablero. Entero positivo. 
    
    Salidas: 
       tablero: lista de listas de ncol columnas y nfil filas (es decir, nfil 
                listas de ncol elementos cada una), en la que cada elemento 
                es el string dado en stri. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-13 (mar, 13 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    tablero = [[stri for i in range(ncol)] for j in range(nfil)]
    
    return tablero


def impr_tablero(tablero):
    """
    Imprimir en pantalla un tablero 2D rectangular, incluyendo letras como 
    etiquetas de columnas y nºs como etiquetas de filas. 
    La primera celda estará identificada como A1. 
    
    Entradas: 
       tablero: string con el que se inicializan todas las celdas del tablero. 
             Tipo: str. 
       ncol: nº de columnas del tablero. Entero positivo. 
       nfil: nº de filas del tablero. Entero positivo. 
    
    Salidas: None 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-21 (mie, 21 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    nchr = len(tablero[0][0])
    stri = ' ' * nchr
    
    tabl_impr = [[stri for i in range(ncol+2)] for j in range(nfil+2)]
    
    tabl_impr[0][1] = '|'.ljust(nchr)
    for i in range(ncol):
        tabl_impr[0][2+i] = chr(ord('A') + i).ljust(nchr)
        tabl_impr[1][2+i] = '_'.ljust(nchr)
    
    tabl_impr[1][0] = '_'.ljust(nchr)
    tabl_impr[1][1] = '_'.ljust(nchr)
    
    for j in range(nfil):
        tabl_impr[j+2][0] = str(j + 1).ljust(nchr)
        tabl_impr[j+2][1] = '|'.ljust(nchr)
    
    tabl_impr[0][1] = '|'.ljust(nchr)
    tabl_impr[1][1] = '|'.ljust(nchr)
    
    for i in range(ncol):
        for j in range(nfil):
            tabl_impr[j+2][i+2] = tablero[j][i]
    
    pprint.pprint(tabl_impr)
    
    return None


def pedir_celda(msg_in, ncol, nfil, opc_salir):
    """
    Recoge celda como input del usuario. 
    El input del usuario esperado es una letra seguida de un nº entero, sin espacios 
    ni otros caracteres entre ambos. La letra designa la columna, y el nº la fila 
    del tablero. 
    El ordinal de la letra debe estar dentro del rango del nº de columnas del 
    tablero, y el nº debe estar dentro del rango del nº de filas del tablero. 
    Notas: 
       - La primera fila es la nº 1, y la primera columna la A. 
       - No se distingue entre mayúsculas y minúsculas. 
       - Se excluye la letra ñ. 
    
    Entradas: 
       msg_in: mensaje que se muestra al usuario al pedirle el dato. Tipo: str. 
       ncol: nº de columnas del tablero. Entero positivo mayor que 0. Tipo: int. 
       nfil: nº de filas del tablero. Entero positivo mayor que 0. Tipo: int. 
       opc_salir: cadena de caracteres para salir del programa. Sin espacios y en 
                  mayúsculas. Tipo: str. 
    
    Salidas: 
       icel: índice 1D de la celda seleccionada. Entero no negativo, empezando en 0. Tipo: int. 
             Para más información, ver funciones ind_1d_a_2d y ind_2d_a_1d. 
       salir: booleano que vale True si se ha introducido la opción de salir (opc_salir). 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-20 (mar, 20 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    celda_ok = False
    salir = False
    
    celda_min = 'A1'
    celda_max = chr(ord('A') + ncol - 1) + str(nfil)
    
    icel = []
    
    while not (celda_ok or salir):
        # print(f'\n-{nomfun}-: \n{msg_in}\n')
        inp = input(msg_in).strip().upper()
        print(f'\n-{nomfun}-: \nDato introducido: {inp}\n')
        if inp == opc_salir.strip().upper():
            salir = True
        else:
            try:
                col, fil = re.findall('\d+|\D+', inp)
                x = ord(col) - ord('A')
                y = int(fil) - 1
                if x in range(ncol) and y in range(nfil):
                    icel = ind_2d_a_1d(x, y, ncol)
                    celda_ok = True
                else:
                    print(f'\n-{nomfun}-: \nERROR: Dato introducido incorrecto. \
                          \n   Introduce una casilla entre {celda_min} y {celda_max}, o \'{opc_salir}\' para salir del juego. \n')
            except Exception as e:
                print(f'\n-{nomfun}-: \nERROR: Dato introducido incorrecto. \
                      \n   Introduce una casilla entre {celda_min} y {celda_max}, o \'{opc_salir}\' para salir del juego. ')
                print(f'ERROR: {e}\n')
    
    return icel, salir


def pedir_opc(msg_in, opcs):
    """
    Recoge un input del usuario entre una lista de opciones posibles. 
    
    Entradas: 
       msg_in: mensaje que se muestra al usuario al pedirle el dato. Tipo: str. 
       opcs: diccionario con opciones a escoger disponibles. Cada clave y valor 
             son strings. 
    
    Salidas: 
       opc: opción escogida por el usuario. Tipo: str. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-20 (mar, 20 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    opc_ok = False
    opc = None
    
    opcs_u = {k.strip().upper(): v for k, v in opcs.items()}
    
    while not opc_ok:
        # print(f'\n-{nomfun}-: \n{msg_in}\n')
        inp = input(msg_in).strip().upper()
        print(f'\n-{nomfun}-: \nDato introducido: {inp}\n')
        if inp in opcs_u:
            opc = inp
            opc_ok = True
            print(f'\n-{nomfun}-: \nHas escogido la opción {opc} ({opcs_u[opc]}). \n')
        else:
            print(f'\n-{nomfun}-: \nERROR: Opción no reconocida. ')
            print('   Introduce una de las opciones disponibles: ')
            for k, v in opcs_u.items():
                print(f'      - {k}: {v}')
            print()
    
    return opc


def cabe_barco(tablero, eslora, ori, icel_ini, strs_ocup):
    """
    Comprueba si un barco cabe en un tablero (array 2D). 
    El barco cabe en el tablero si no hay interferencia con otros barcos o con los bordes del tablero. 
    
    Entradas: 
       tablero: array 2D (lista de listas, siendo todas las listas anidadas de la misma longitud) 
                con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
                Debe contener strings en todas sus posiciones. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. Tipo: int. 
       ori: orientación del nuevo barco. String de una letra. Tipo: str. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       icel_ini: índice 1D de la celda inicial del nuevo barco. Entero no negativo. Tipo: int. 
                 Para más información, ver funciones ind_1d_a_2d y ind_2d_a_1d. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings, cada uno de un único caracter: 
                  el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la separación necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
    
    Salidas: 
       cabe: booleano que es True si el nuevo barco cabe sin interferencia, y False en caso contrario. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    cabe = True
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    i_hov = hov(ori)
    
    x_ini, y_ini = ind_1d_a_2d(icel_ini, ncol)
    
    x_fin = x_ini + (1 - i_hov) * (eslora - 1)
    y_fin = y_ini + i_hov * (eslora - 1)
    
    # Comprobar si hay interferencia del nuevo barco
    if x_ini in range(ncol) and x_fin in range(ncol) \
     and y_ini in range(nfil) and y_fin in range(nfil):
        i = 0
        while cabe == True and i in range(eslora):
            if tablero[y_ini + i_hov * i][x_ini + (1 - i_hov) * i][0] in strs_ocup:
                cabe = False
            i += 1
    else:
        cabe = False
    
    return cabe


def colocar_barco(tablero, n_barco, eslora, ori, icel_ini, sep, strs_ocup):
    """
    Colocación de un barco en un tablero (array 2D), si no hay interferencia con otros barcos 
    o con los bordes del tablero. 
    
    Entradas: 
       tablero: array 2D (lista de listas, siendo todas las listas anidadas de la misma longitud) 
                con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
                Debe contener strings en todas sus posiciones. 
       n_barco: ID del barco. Nº entero positivo (incluyendo 0). Tipo: int. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. Tipo: int. 
       ori: orientación del nuevo barco. String de una letra. Tipo: str. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       sep: nº de casillas de separación mínima entre barcos. Entero positivo (incluyendo 0). 
            Tipo: int. 
       icel_ini: índice 1D de la celda inicial del nuevo barco. Entero no negativo. Tipo: int. 
                 Para más información, ver funciones ind_1d_a_2d y ind_2d_a_1d. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings, cada uno de un único caracter: 
                  el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la separación necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
    
    Salidas: 
       cabe: booleano que es True si el nuevo barco cabe sin interferencia, y False en caso contrario. 
       tablero: tablero actualizado con el nuevo barco si éste se ha podido colocar sin 
                interferencia. Si no, se devuelve el mismo tablero de entrada (sin incluir 
                el nuevo barco). 
       lst_sep: lista de las celdas correspondientes a la separación mínima alrededor del nuevo 
                barco. Cada elemento de la lista es el índice 1D de una celda (para más información, 
                ver funciones ind_1d_a_2d y ind_2d_a_1d). 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    cabe = True
    lst_sep = []
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    nchr = len(tablero[0][0])
    
    i_hov = hov(ori)
    
    x_ini, y_ini = ind_1d_a_2d(icel_ini, ncol)
    
    # Comprobar si hay interferencia del nuevo barco
    cabe = cabe_barco(tablero, eslora, ori, icel_ini, strs_ocup)
    
    if cabe == True:
        # Actualizar tablero con nuevo barco 
        # Separación alrededor del barco 
        for i in range(eslora + 2*sep):
            x = x_ini + (1 - i_hov) * (i - sep)
            y = y_ini + i_hov * (i - sep)
            for j in range(1 + 2*sep):
                xx = x + i_hov * (j - sep)
                yy = y + (1 - i_hov) * (j - sep)
                if yy in range(nfil) and xx in range(ncol):
                    ind1 = ind_2d_a_1d(xx, yy, ncol)
                    lst_sep.append(ind1)
                    if tablero[yy][xx][0] not in strs_ocup:
                        tablero[yy][xx] = strs_ocup[1].ljust(nchr)
        # Barco 
        for i in range(eslora):
            x = x_ini + (1 - i_hov) * i
            y = y_ini + i_hov * i
            tablero[y][x] = (strs_ocup[0] + str(n_barco)).ljust(nchr)
            ind1 = ind_2d_a_1d(x, y, ncol)
            lst_sep.remove(ind1)
    
    return cabe, tablero, lst_sep


def viables(tablero, eslora, ori, sep, strs_ocup):
    """
    Devuelve la lista de casillas iniciales viables para un barco de una eslora 
    y orientación determinadas, en un tablero (array 2D) con otros barcos ya 
    colocados, respetando una separación mínima dada entre los barcos. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. 
       ori: orientación del nuevo barco. String de una letra. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       sep: nº de casillas de separación mínima entre barcos. Entero positivo (incluyendo 0). 
            Tipo: int. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings, cada uno de un único caracter: 
                  el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la separación necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
    
    Salidas: 
       icel_ini_viab: lista con los índices 1D de las celdas viables donde puede situarse 
                      la casilla inicial de un barco con una eslora y orientación determinada 
                      en un tablero con otros barcos ya colocados. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-18 (dom, 18 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    icel_ini_viab = []
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    i_hov = hov(ori)
    
    for i in range(nfil + (1 - eslora) * i_hov):
        for j in range(ncol + (1 - eslora) * (1 - i_hov)):
            ind1 = ind_2d_a_1d(j, i, ncol)
            cabe_b = cabe_barco(tablero, eslora, ori, ind1, strs_ocup)
            if cabe_b == True: 
                icel_ini_viab.append(ind1)
    
    return icel_ini_viab


def colocar_barcos(tablero, esloras, sep, strs_ocup, modo='auto', stri=None, opcs=None, opc_reiniciar=None, opc_salir=None):
    """
    Colocación aleatoria o manual de varios barcos en un tablero (array 2D), si no hay interferencia 
    con otros barcos o con los bordes del tablero. 
    
    Entradas: 
       tablero: array 2D (lista de listas, siendo todas las listas anidadas de la misma longitud) 
                con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
                Debe contener strings en todas sus posiciones. 
                Normalmente esta función se ejecutará dándole como entrada un tablero vacío. 
       esloras: lista de longitud igual al nº de barcos a colocar en el tablero, con las esloras 
                de todos los barcos. Cada elemento de la lista es un entero mayor que 0. 
       sep: nº de casillas de separación mínima entre barcos. Entero positivo (incluyendo 0). 
            Tipo: int. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings, cada uno de un único caracter: 
                  el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la separación necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
       modo: modo de colocación de los barcos. Opciones: 
          - 'auto': se intenta colocar todos los barcos automáticamente. 
          - 'man': se colocan los barcos manualmente, uno a uno, pidiendo al usuario 
                   la orientación y casilla inicial de cada uno. 
                   En este caso, cada vez que se coloca un nuevo barco se actualiza el gráfico 
                   del tablero. 
       tri: string con el que se inicializan todas las celdas del tablero. 
             Tipo: str. Valor por defecto: None. 
       opcs: diccionario con las opciones que se muestran al usuario cada vez que se le pide la 
             orientación de un nuevo barco. Tanto los keys como los values son strings. 
             Valor por defecto: None. 
       opc_reiniciar: key de opcs correspondiente a la opción de reiniciar la colocación de 
                      barcos. Tipo: str. 
                      Valor por defecto: None. 
       opc_salir: key de opcs correspondiente a la opción de salir del juego. Tipo: str. 
                  Valor por defecto: None. 
    
    Salidas: 
       caben: booleano que vale True si se han conseguido colocar todos los barcos de la lista 
              de esloras. 
       tablero: tablero actualizado con los nuevos barcos que se han podido colocar. Los barcos 
                se colocan en el orden de la lista esloras, y si uno no se puede colocar, todos 
                los posteriores de la lista tampoco se colocan. 
       lsts_sep: Lista con la lista lst_sep que devuelve la función colocar_barco para cada barco 
                 (ver descripción de lst_sep en doc de función colocar_barco). 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-21 (mie, 21 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    caben = True
    
    oris = ['h', 'v']
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    nchr = len(tablero[0][0])
    
    n_barcos = len(esloras)
    lsts_sep = [[] for i in range(n_barcos)]
    
    if modo=='auto':
        opc_slc = oris[0]
    
    id_barco = 0
    while caben == True and id_barco in range(n_barcos):
        eslora = esloras[id_barco]
        if modo == 'man':
            # Pedir al usuario la orientación del nuevo barco 
            msg_in = f'\n-{nomfun}-: \nSiguiente barco a colocar: barco {id_barco+1} de {n_barcos} (eslora={eslora}). \
                     \nSelecciona la orientación del barco o alguna otra de las opciones disponibles: \n'
            for k, v in opcs.items():
                msg_in += f'   - {k}: {v}\n'
            print(f'\n-{nomfun}-: \nColocando barcos en tablero: \n')
            # pprint.pprint(tablero)
            impr_tablero(tablero)
            ##### PENDIENTE graficar en fig matplotlib tablero con barcos colocados hasta el momento 
            opc_slc = pedir_opc(msg_in, opcs)
            if opc_slc.lower() in oris:
                ori = opc_slc.lower()
                i_hov = oris.index(ori)
        elif modo == 'auto':
            # Obtener aleatoriamente la orientación del nuevo barco 
            i_hov = rnd.randint(0, 1)
            ori = oris[i_hov]
        
        if opc_slc.lower() in oris:
            # Lista de celdas viables como celda inicial del nuevo barco 
            icel_i_viab = viables(tablero, eslora, ori, sep, strs_ocup)
            if len(icel_i_viab) < 0.1:
                # Si no hay celdas viables con esa orientación, se prueba con la otra 
                i_hov = 1 - i_hov
                ori = oris[i_hov]
                icel_i_viab = viables(tablero, eslora, ori, sep, strs_ocup)
                if modo == 'man':
                    print(f'\n-{nomfun}-: \nATENCIÓN: No cabe en el tablero el barco con ID {id_barco} (eslora={eslora}) \
                          y la orientación seleccionada ({opc_slc}). \nSe tratará de colocar con la otra orientación. \n')
            if len(icel_i_viab) < 0.1:
                if modo == 'auto':
                    caben = False
                    print(f'\n-{nomfun}-: \nATENCIÓN: No cabe en el tablero el barco con ID {id_barco} (eslora={eslora}). \n')
                elif modo == 'man':
                    print(f'\n-{nomfun}-: \nATENCIÓN: No cabe en el tablero el barco con ID {id_barco} (eslora={eslora}). \
                          \nSe recomienda reiniciar. \n')
            else:
                if modo == 'auto':
                    # Seleccionar aleatoriamente celda inicial del nuevo barco entre las viables 
                    icel_i = icel_i_viab[rnd.randint(0, len(icel_i_viab)-1)]
                elif modo == 'man':
                    # Pedir al usuario la celda inicial del nuevo barco entre las viables 
                    celda_viable = False
                    salir = False
                    # Imprimir celdas viables en tablero 
                    tablero_viab = np.array(tablero)
                    tablero_viab.flat[icel_i_viab] = 'V'.ljust(nchr)
                    tablero_viab = tablero_viab.tolist()
                    print(f'\n-{nomfun}-: \nCasillas iniciales viables para barco con ID {id_barco} (eslora={eslora}) y orientación {ori}: \n')
                    # pprint.pprint(tablero_viab)
                    impr_tablero(tablero_viab)
                    ##### Pendiente graficar en fig matplotlib tablero con celdas viables coloreadas en verde 
                    while celda_viable == False and salir == False:
                        msg_in_c = f'\n-{nomfun}-: \nSelecciona casilla inicial para el barco con ID {id_barco} (eslora={eslora}) y orientación {ori} \
                                   \nentre las viables (señaladas con V/coloreadas en verde), o introduce {opc_salir} para salir del juego. '
                        icel_i, salir = pedir_celda(msg_in_c, ncol, nfil, opc_salir)
                        if salir == True:
                            print(f'\n-{nomfun}-: \nSaliendo del juego. \n')
                            time.sleep(0.2)
                            quit()
                        else:
                            # Chequear si la celda introducida por el usuario está entre las viables 
                            if icel_i in icel_i_viab:
                                celda_viable = True
                            else:
                                print(f'\n-{nomfun}-: \nATENCIÓN: La casilla seleccionada no está entre las viables. ')
                    
                # Colocar el nuevo barco 
                cabe_b, tablero, lst_sep_b = colocar_barco(tablero, id_barco, eslora, ori, icel_i, sep, strs_ocup)
                xi, yi = ind_1d_a_2d(icel_i, ncol)
                if cabe_b == False:
                    caben = False
                    print(f'\n-{nomfun}-: \nERROR: No se ha podido colocar el barco con ID {id_barco} (eslora={eslora}). \
                            \n   con orientación {ori} empezando en la casilla {chr(ord("A") + xi) + str(yi+1)}, supuestamente viable. \
                            \n   Revisar código. \n')
                else:
                    lsts_sep[id_barco] = lst_sep_b
                id_barco += 1
        elif opc_slc == opc_reiniciar:
            id_barco = 0
            tablero = inic_tablero(stri, ncol, nfil)
            caben = True
            print(f'\n-{nomfun}-: \nSe reinicia la colocación de barcos. \n')
        elif opc_slc == opc_salir:
            print(f'\n-{nomfun}-: \nSaliendo del juego. \n')
            time.sleep(0.2)
            quit()
    
    if caben == False:
        print(f'\n-{nomfun}-: \nTablero con los barcos anteriores colocados: ')
        # pprint.pprint(tablero)
        impr_tablero(tablero)
        #### PENDIENTE crear también figura de matplotlib 
        print()
    
    return caben, tablero, lsts_sep


def rep_colocar_barcos(stri, ncol, nfil, esloras, sep, strs_ocup, maxint):
    """
    Repetición de la función colocar_barcos en modo auto como máximo maxint veces, 
    reiniciando el tablero cada vez. Se detiene cuando se consiguen colocar 
    todos los barcos o cuando se llega al nº máximo de intentos maxint. 
    
    Entradas: 
       stri: string con el que se inicializan todas las celdas del tablero. 
             Tipo: str. 
       ncol: nº de columnas del tablero. Entero positivo. 
       nfil: nº de filas del tablero. Entero positivo. 
       esloras: lista de longitud igual al nº de barcos a colocar en el tablero, con las esloras 
                de todos los barcos. Cada elemento de la lista es un entero mayor que 0. 
       sep: nº de casillas de separación mínima entre barcos. Entero positivo (incluyendo 0). 
            Tipo: int. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings, cada uno de un único caracter: 
                  el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la separación necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
        maxint: nº máximo de intentos para colocar todos los barcos en el tablero. 
    
    Salidas: 
       caben: booleano que vale True si se han conseguido colocar todos los barcos de la lista 
              de esloras. 
       tablero: array 2D (lista de listas, siendo todas las listas anidadas de la misma longitud) 
                con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
       lsts_sep: Lista con la lista lst_sep que devuelve la función colocar_barco para cada barco 
                 (ver descripción de lst_sep en doc de función colocar_barco). 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-19 (lun, 19 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    caben = False
    
    tablero = []
    
    n_barcos = len(esloras)
    lsts_sep = [[] for i in range(n_barcos)]
    
    i_colocar = 0
    
    while i_colocar < maxint - 0.1 and caben == False:
        print(f'\n-{nomfun}-: \nIntento {i_colocar+1}... ')
        tablero = inic_tablero(stri, ncol, nfil)
        caben, tablero, lsts_sep = colocar_barcos(tablero, esloras, sep, strs_ocup)
        if caben == True:
            print(f'\n-{nomfun}-: \nSe han conseguido colocar todos los barcos en el tablero en el intento {i_colocar+1}. ')
        i_colocar += 1
    
    return caben, tablero, lsts_sep


def disparar(tablero, icel, s_barco, s_tocado, s_agua):
    """
    Disparo a un tablero (array 2D) con barcos. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos marcadas. 
       icel: índice 1D de la casilla a la que se dispara. 
             Entero no negativo, incluyendo 0. Tipo: int. 
             Para más información, ver funciones ind_1d_a_2d y ind_2d_a_1d. 
       s_barco: inicio del string que marca que hay barco en una casilla, 
                sin disparo previo en dicha casilla. 
       s_tocado: inicio del string que se escribirá en la casilla a la que 
                 se dispara si el disparo acierta a un barco. 
       s_agua: inicio del string que se escribirá en la casilla a la que 
               se dispara si el disparo no acierta a un barco. 
    
    Salidas: 
       acierto: booleano que es True si el disparo ha acertado a un barco 
                (en una casilla previamente no acertada). 
       hundido: booleano que es True si el disparo ha hundido a un barco. 
       id_barco: entero correspondiente al barco al que se ha acertado. Si 
                 no se ha acertado a ningún barco, devuelve -1. 
       tablero: tablero actualizado con el nuevo disparo. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-20 (mar, 20 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    acierto = False
    hundido = False
    id_barco = -1
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    nchr = len(tablero[0][0])
    
    x, y = ind_1d_a_2d(icel, ncol)
    
    if x in range(ncol) and y in range(nfil):
        if tablero[y][x][0] == s_barco:
            nom_barco = tablero[y][x]
            lst_nom_barco = re.findall('\d+|\D+', nom_barco.strip())
            id_barco = int(lst_nom_barco[1])
            tablero[y][x] = s_tocado.ljust(nchr)
            acierto = True
            # Conteo de las celdas no tocadas que quedan de este barco 
            vidas_b = sum([f.count(nom_barco) for f in tablero])
            if vidas_b < 0.1:
                hundido = True
        else:
            tablero[y][x] = s_agua.ljust(nchr)
    
    return acierto, hundido, id_barco, tablero


def intelig_disp(tablero, icel, sep, strs_descub, esl_res_2ym_min, esl_res_2ym_max):
    """
    Función que da inteligencia a los disparos de la máquina, priorizando 
    (y posiblemente descartando) celdas adyacentes a una celda en la que 
    se ha tocado pero no hundido un barco. 
    
    Entradas: 
       tablero: array 2D con las posiciones descubiertas del tablero marcadas. 
       icel: índice 1D de una celda a la que se ha disparado en el tablero, en la que se ha 
             tocado pero no hundido un barco. Entero no negativo. Tipo: int. 
             Para más información, ver funciones ind_1d_a_2d y ind_2d_a_1d. 
       sep: nº de casillas de separación mínima entre barcos. Entero positivo (incluyendo 0). 
            Tipo: int. 
       strs_descub: lista de strings que marcan que una celda está ocupada. 
                    Cada string de la lista tiene que tener un único caracter. 
                    El primer string de la lista debe corresponder a las celdas 
                    tocadas (celdas disparadas en las que hay barco). 
       esl_res_2ym_min, esl_res_2ym_max: esloras mínima y máxima de los barcos que quedan 
               por hundir con eslora de 2 y más. Entero positivo. Tipo: int. 
       
    
    Salidas: 
       icels_prio1: lista con índices 1D de celdas que se priorizarán para 
                    disparos posteriores. Fuera de esta función, estas celdas se 
                    podrán colocar por delante de celdas priorizadas en llamadas 
                    previas a esta función. 
       icels_prio2: lista con índices 1D de celdas que se priorizarán para 
                    disparos posteriores. Fuera de esta función, estas celdas se 
                    podrán colocar por detrás de celdas priorizadas en llamadas 
                    previas a esta función. 
       icels_descar: lista con índices 1D de celdas en las que se descarta que pueda 
                     haber barco. Fuera de esta función, estas celdas se podrán 
                     eliminar de la lista de celdas disponibles para disparar 
                     del tablero. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-21 (mie, 21 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    icels_prio1 = []
    icels_prio2 = []
    icels_descar = []
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    x, y = ind_1d_a_2d(icel, ncol)
    
    # Celdas adyacentes a la celda icel dentro del radio sep en cada orientación 
    # no previamente descubiertas 
    dic_icels_prio = {'h': [], 'v': []}
    if sep>0.1:
        if x+1 in range(ncol):
            if tablero[y][x+1][0] not in strs_descub:
                dic_icels_prio['h'].append(ind_2d_a_1d(x+1, y, ncol))
        if x-1 in range(ncol):
            if tablero[y][x-1][0] not in strs_descub:
                dic_icels_prio['h'].append(ind_2d_a_1d(x-1, y, ncol))
        if y+1 in range(nfil):
            if tablero[y+1][x][0] not in strs_descub:
                dic_icels_prio['v'].append(ind_2d_a_1d(x, y+1, ncol))
        if y-1 in range(nfil):
            if tablero[y-1][x][0] not in strs_descub:
                dic_icels_prio['v'].append(ind_2d_a_1d(x, y-1, ncol))
    
    # Se intenta determinar la orientación del barco tocado y no hundido 
    # que pasa por la celda icel, mirando si: 
    # 1. Hay celdas tocadas dentro del radio sep. 
    # 2. El barco de eslora máxima que pasa por icel que podría caber 
    #    en cada orientación, teniendo en cuenta las celdas previamente 
    #    descubiertas del tablero. 
    #    - Si la eslora máxima que cabe en una dirección es menor que el 
    #      menor barco que queda por hundir con eslora a partir de 2, se 
    #      determina que no es posible que el barco tocado esté colocado 
    #      en esa orientación. En este caso, las celdas asociadas a esa 
    #      orientación de dic_icels_prio se descartan, y las de la otra 
    #      orientación se pasan a icels_prio1. 
    #    - Si la eslora máxima que cabe en una dirección es menor que el 
    #      mayor barco que queda por hundir con eslora a partir de 2 
    #      (y mayor que el menor barco que queda por hundir con eslora 
    #      a partir de 2), en el vector icels_prio2 se ponen primero 
    #      las celdas correspondientes a la otra dirección de dic_icels_prio 
    #      en icels_prio2, y posteriormente se ponen las de la otra dirección. 
    ori_def = False
    ori = ''
    # 1. 
    i = 0
    while ori_def == False and i in range(sep):
        if x+1+i in range(ncol) and ori_def == False:
            if tablero[y][x+1+i][0] == strs_descub[0]:
                ori_def = True
                ori = 'h'
                no_ori = 'v'
        if x-1-i in range(ncol) and ori_def == False:
            if tablero[y][x-1-i][0] == strs_descub[0]:
                ori_def = True
                ori = 'h'
                no_ori = 'v'
        if y+1+i in range(nfil) and ori_def == False:
            if tablero[y+1+i][x][0] == strs_descub[0]:
                ori_def = True
                ori = 'v'
                no_ori = 'h'
        if y-1-i in range(nfil) and ori_def == False:
            if tablero[y-1-i][x][0] == strs_descub[0]:
                ori_def = True
                ori = 'v'
                no_ori = 'h'
        i += 1
    
    # 2. 
    if ori_def == False:
        esl_max_h = 1
        esl_max_v = 1
        stop_n = False
        stop_s = False
        stop_e = False
        stop_o = False
        i = 0
        while (min(esl_max_h, esl_max_v) < esl_res_2ym_max - 0.1) and (stop_n == False or stop_s == False or stop_e == False or stop_o == False):
            if x+1+i in range(ncol):
                if tablero[y][x+1+i][0] not in strs_descub[1:] and stop_e == False:
                    esl_max_h += 1
                else:
                    stop_e = True
            else:
                stop_e = True
            if x-1-i in range(ncol):
                if tablero[y][x-1-i][0] not in strs_descub[1:] and stop_o == False:
                    esl_max_h += 1
                else:
                    stop_o = True
            else:
                stop_o = True
            if y+1+i in range(nfil):
                if tablero[y+1+i][x][0] not in strs_descub[1:] and stop_s == False:
                    esl_max_v += 1
                else:
                    stop_s = True
            else:
                stop_s = True
            if y-1-i in range(nfil):
                if tablero[y-1-i][x][0] not in strs_descub[1:] and stop_n == False:
                    esl_max_v += 1
                else:
                    stop_n = True
            else:
                stop_n = True
            
            i += 1
            
        if esl_max_h < esl_res_2ym_min - 0.1:
            ori_def = True
            ori = 'v'
            no_ori = 'h'
        if esl_max_v < esl_res_2ym_min - 0.1:
            ori_def = True
            ori = 'h'
            no_ori = 'v'
    
    if ori_def == True:
        if sep > 0.1: 
            icels_prio1 = dic_icels_prio[ori]
            icels_descar = dic_icels_prio[no_ori]
        else:
            icels_prio2 = dic_icels_prio[ori] + dic_icels_prio[no_ori]
    elif esl_max_h < esl_res_2ym_max - 0.1:
        if esl_max_v < esl_res_2ym_max - 0.1:
            if esl_max_h < esl_max_v:
                icels_prio2 = dic_icels_prio['v'] + dic_icels_prio['h']
            else:
                icels_prio2 = dic_icels_prio['h'] + dic_icels_prio['v']
        else:
            icels_prio2 = dic_icels_prio['v'] + dic_icels_prio['h']
    elif esl_max_v < esl_res_2ym_max - 0.1:
        if esl_max_h < esl_res_2ym_max - 0.1:
            if esl_max_h < esl_max_v:
                icels_prio2 = dic_icels_prio['v'] + dic_icels_prio['h']
            else:
                icels_prio2 = dic_icels_prio['h'] + dic_icels_prio['v']
        else:
            icels_prio2 = dic_icels_prio['h'] + dic_icels_prio['v']
    else:
        icels_prio2 = dic_icels_prio['h'] + dic_icels_prio['v']
    
    return icels_prio1, icels_prio2, icels_descar


def graf_tablero(ax, tablero, mostrar_barcos, strs, rgba_cels, txt, title):
    """
    Función para graficar un tablero. 
    """
    
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    # Conversión a NumPy array para más fácil procesado 
    tablero_np = np.array(tablero)
    
    # Ocultar barcos en caso de que no se vayan a mostrar 
    if mostrar_barcos == False:
        msk = np.char.startswith(tablero_np, strs[1][0])
        tablero_np[msk] = strs[0]
    
    # Máscara numérica de los colores: 
    num_data = np.zeros(tablero_np.shape, dtype=int)
    for i, e in enumerate(strs):
        msk = np.char.startswith(tablero_np, e[0])
        num_data[msk] = i
    
    # Colormap de las celdas 
    cmap = ListedColormap(rgba_cels)
    
    # Ploteo 
    if ax == None:
        fig, ax = plt.subplots()
    ax.imshow(num_data, cmap=cmap, vmin=0, vmax=len(rgba_cels)-1)
    
    # Tick labels
    x_labels = [chr(ord('A') + i) for i in range(num_data.shape[1])]
    y_labels = np.arange(1, num_data.shape[0] + 1)
    ax.set_xticks(np.arange(num_data.shape[1]))
    ax.set_xticklabels(x_labels)
    ax.set_yticks(np.arange(num_data.shape[0]))
    ax.set_yticklabels(y_labels)
    
    # Enable ticks on top and right
    ax.tick_params(top=True, right=True, labeltop=True, labelright=True)
    
    # Grid lines
    ax.hlines(np.arange(-0.5, num_data.shape[0], 1), xmin=-0.5, xmax=num_data.shape[1]-0.5,
              color="black", linewidth=1)
    ax.vlines(np.arange(-0.5, num_data.shape[1], 1), ymin=-0.5, ymax=num_data.shape[0]-0.5,
              color="black", linewidth=1)
    
    # Superponer el ID de los barcos en las celdas con barco no tocado 
    for i in range(num_data.shape[0]):
        for j in range(num_data.shape[1]):
            if tablero_np[i, j][0] == strs[1][0]:
                ax.text(j, i, tablero_np[i, j], ha="center", va="center",
                        fontsize=14, color="white", fontweight="bold")

    ax.set_title(title, fontsize=12)

    # --- FIX: Textbox relative to axes coordinates ---
    # Position (-0.2, 0.5) means left of the axes center vertically
    ax.text(-0.15, 0.5, txt,
            fontsize=12, va="center", ha="right",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.5"),
            transform=ax.transAxes)


def graf_tableros(tableros, mostrar_barcos, esloras, vidas_barcos, v_strs, v_colores_rgba, ax_titles, f_title):
    """
    Función para crear y mostrar figura (png) con dos tableros. 
    """
    
    
    # --- Create figure with two subplots horizontally ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # Increased width
    
    # Textos con el estado de los barcos para las leyendas 
    txts = ['', '']
    for i in range(2):
        v_esl = esloras[i]
        n_barc = len(v_esl)
        v_vid = vidas_barcos[i]
        v_str_barcos = ['' for i in range(n_barc)]
        for j in range(n_barc):
            if mostrar_barcos[i] == True:
                v_str_barcos[j] = 'o' * v_vid[j] + 'x' * (v_esl[j] - v_vid[j])
            else:
                v_str_barcos[j] = 'o' * (1 - ((v_esl[j] - v_vid[j]) // v_esl[j])) * v_esl[j] + 'x' * ((v_esl[j] - v_vid[j]) // v_esl[j]) * v_esl[j]
        txts[i] = '\n'.join(v_str_barcos)
    
    # Plot first array
    graf_tablero(axes[0], tableros[0], mostrar_barcos[0], v_strs[0], v_colores_rgba[0], txts[0], ax_titles[0])
    
    # Plot second array
    graf_tablero(axes[1], tableros[1], mostrar_barcos[1], v_strs[1], v_colores_rgba[1], txts[1], ax_titles[1])
    
    # --- Shrink axes size slightly ---
    for ax in axes:
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0 + 0.05, pos.width * 0.8, pos.height * 0.8])
    
    # --- Overall title ---
    fig.suptitle(f_title, fontsize=16, fontweight="bold")
    
    # Adjust layout spacing — increased wspace for more separation
    plt.subplots_adjust(left=0.05, wspace=0.3, top=0.8)
    
    # --- Save figure to PNG ---
    ### PENDIENTE añadir timestamp u otro nº secuencial en el nombre del fichero, para poder guardar todas las figuras 
    png_path = "..\png\HLF.png"
    # png_path = "HLF.png"
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    
    # --- Open PNG in default viewer without blocking ---
    system_name = platform.system()
    try:
        if system_name == "Windows":
            os.startfile(png_path)
        elif system_name == "Darwin":  # macOS
            subprocess.Popen(["open", png_path])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", png_path])
    except Exception as e:
        print(f"⚠️ Could not open image automatically: {e}")


