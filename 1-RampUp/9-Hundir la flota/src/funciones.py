# encoding: utf-8

# Funciones para HLF. 

# $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 


# funciones: 
# inic_tablero(ncol, nfil)
# colocar_barco(tablero, eslora, ori, x_ini, y_ini). 
#   Devuelve True si ha podido colocar el nuevo barco sin interferencia con los existentes, junto con el tablero actualizado. 
#   Si no, devuelve False, y el tablero tal y como entró. 
# disparar(tablero, x, y)
# viables(tablero, eslora, ori)
#   Devuelve la lista de casillas iniciales viables para un barco de una eslora y orientación determinadas, en un tablero 
#   con otros barcos ya colocados. 
# probables(tablero)
#   Devuelve la lista de casillas donde es más probable que se sitúe un barco en un tablero en el que lo que se conoce son
#   las coordenadas de los disparos previamente efectuados. 


import inspect


def inic_tablero(ncol, nfil):
    """
    Inicializar un tablero 2D rectangular. 
    
    Entradas: 
       ncol: nº de columnas del tablero. Entero positivo. 
       nfil: nº de filas del tablero. Entero positivo. 
    
    Salidas: 
       tablero: lista de listas de ncol columnas y nfil filas (es decir, nfil 
                listas de ncol elementos cada una), en la que cada elemento 
                es un espacio en blanco. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-13 (mar, 13 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    tablero = [[' ' for i in range(ncol)] for j in range(nfil)]
    
    return tablero


def colocar_barco(tablero, eslora, ori, x_ini, y_ini, holg, strs_ocup):
    """
    Colocación de un barco en un tablero, si no hay interferencia con otros barcos 
    o con los bordes del tablero. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos y las posiciones donde 
                debe haber holgura entre barcos marcadas. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. 
       ori: orientación del nuevo barco. String de una letra. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       holg: nº de casillas de holgura entre barcos. Entero positivo (incluyendo 0). 
       x_ini: coordenada x (columna) inicial del nuevo barco. Entero positivo entre 0 y ncol. 
       y_ini: coordenada y (fila) inicial del nuevo barco. Entero positivo entre 0 y nfil. 
       strs_ocup: lista de strings que marcan que una celda está ocupada. 
                  Tiene que tener al menos 2 strings: el primero, el string que marca que hay barco, 
                  y el segundo, el que marca que hay la holgura necesaria entre barcos. 
                  ATENCIÓN: si se quisiera usar esta función cuando ya se han hecho disparos 
                     en el tablero, se debe incluir al menos un string adicional, con lo que se 
                     imprime al acertar un disparo. 
    
    Salidas: 
       cabe: booleano que es True si se ha podido colocar el nuevo barco sin interferencia, 
             y False en caso contrario. 
       tablero: tablero actualizado con el nuevo barco si éste se ha podido colocar sin 
                interferencia. Si no, se devuelve el mismo tablero de entrada (sin incluir 
                el nuevo barco). 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    cabe = True
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    if ori == 'h':
        i_hov = 0
    elif ori == 'v':
        i_hov = 1
    
    x_fin = x_ini + (1 - i_hov) * (eslora - 1)
    y_fin = y_ini + i_hov * (eslora - 1)
    
    # Comprobar si hay interferencia del nuevo barco
    if x_ini in range(ncol) and x_fin in range(ncol) \
     and y_ini in range(nfil) and y_fin in range(nfil):
        i = 0
        while cabe == True and i in range(eslora):
            if tablero[y_ini + i_hov * i][x_ini + (1 - i_hov) * i] in strs_ocup:
                cabe = False
            i += 1
    else:
        cabe = False
    
    # Actualizar tablero con nuevo barco 
    if cabe == True:
        # Holgura alrededor del barco 
        for i in range(eslora + 2*holg):
            ix = x_ini + (1 - i_hov) * (i - holg)
            iy = y_ini + i_hov * (i - holg)
            for j in range(1 + 2*holg):
                iix = ix + i_hov * (j - holg)
                iiy = iy + (1 - i_hov) * (j - holg)
                if iiy in range(nfil) and iix in range(ncol) \
                 and tablero[iiy][iix] not in strs_ocup:
                    tablero[iiy][iix] = strs_ocup[1]
        # Barco 
        for i in range(eslora):
            ix = x_ini + (1 - i_hov) * i
            iy = y_ini + i_hov * i
            tablero[iy][ix] = strs_ocup[0]
    
    return cabe, tablero


def disparar(tablero, x, y, s_barco, s_tocado, s_agua):
    """
    Disparo a un tablero (array 2D) con barcos. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos marcadas. 
       x, y: coordenadas a las que se dispara. 
       x: coordenada x (columna). Entero positivo entre 0 y ncol. 
       y: coordenada y (fila). Entero positivo entre 0 y nfil. 
       s_barco: el string que marca que hay barco en una casilla, 
                sin disparo previo en dicha casilla. 
       s_tocado: string que se escribirá en la casilla a la que se dispara 
                 si el disparo acierta a un barco. 
       s_agua: string que se escribirá en la casilla a la que se dispara 
               si el disparo no acierta a un barco. 
    
    Salidas: 
       acierto: booleano que es True si el disparo ha acertado a un barco. 
       tablero: tablero actualizado con el nuevo disparo. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    acierto = False
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    if x in range(ncol) and y in range(nfil):
        if tablero[y][x] == s_barco:
            tablero[y][x] == s_tocado
            acierto = True
        else:
            tablero[y][x] == s_agua
    
    return acierto, tablero


def viables(tablero, eslora, ori, holg):
    """
    Calcula la lista de casillas iniciales viables para un barco de una eslora 
    y orientación determinadas, en un tablero (array 2D) con otros barcos ya 
    colocados. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos y las posiciones donde 
                debe haber holgura entre barcos marcadas. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. 
       ori: orientación del nuevo barco. String de una letra. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       holg: 
    Salidas: 
       xy_ini_viab: 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    
# viables(tablero, eslora, ori)
#   Devuelve la lista de casillas iniciales viables para un barco de una eslora y orientación determinadas, en un tablero 
#   con otros barcos ya colocados. 