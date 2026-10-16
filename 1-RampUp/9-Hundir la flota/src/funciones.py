# encoding: utf-8

# Funciones para HLF. 

# $Version: 1 $, $Fecha: 2026-10-15 (jue, 15 oct 2026). Por Julio Blanco Lorenzo. 


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


def cabe_barco(tablero, eslora, ori, x_ini, y_ini, strs_ocup):
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
       x_ini, y_ini: coordenadas x (columna) e y (fila) de la celda inicial del nuevo barco. 
                     Entero positivo entre 0 y ncol. Tipo: int. 
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
    
    # $Version: 1 $, $Fecha: 2026-10-15 (jue, 15 oct 2026). Por Julio Blanco Lorenzo. 
    
    
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
            if tablero[y_ini + i_hov * i][x_ini + (1 - i_hov) * i][0] in strs_ocup:
                cabe = False
            i += 1
    else:
        cabe = False
    
    return cabe


def colocar_barco(tablero, n_barco, eslora, ori, x_ini, y_ini, sep, strs_ocup):
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
       x_ini, y_ini: coordenadas x (columna) e y (fila) de la celda inicial del nuevo barco. 
                     Entero positivo entre 0 y ncol. Tipo: int. 
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
                barco. Cada elemento de la lista es una lista [x, y], con las posiciones x e y 
                de cada una de esas celdas. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-15 (jue, 15 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    cabe = True
    lst_sep = []
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    if ori == 'h':
        i_hov = 0
    elif ori == 'v':
        i_hov = 1
    
    # Comprobar si hay interferencia del nuevo barco
    cabe = cabe_barco(tablero, eslora, ori, x_ini, y_ini, strs_ocup)
    
    if cabe == True:
        # Actualizar tablero con nuevo barco 
        # Separación alrededor del barco 
        for i in range(eslora + 2*sep):
            ix = x_ini + (1 - i_hov) * (i - sep)
            iy = y_ini + i_hov * (i - sep)
            for j in range(1 + 2*sep):
                iix = ix + i_hov * (j - sep)
                iiy = iy + (1 - i_hov) * (j - sep)
                if iiy in range(nfil) and iix in range(ncol):
                    lst_sep.append([iix, iiy])
                    if tablero[iiy][iix][0] not in strs_ocup:
                        tablero[iiy][iix] = strs_ocup[1]
        # Barco 
        for i in range(eslora):
            ix = x_ini + (1 - i_hov) * i
            iy = y_ini + i_hov * i
            tablero[iy][ix] = strs_ocup[0] + str(n_barco)
            lst_sep.remove([ix, iy])
    
    return cabe, tablero, lst_sep


def disparar(tablero, x, y, s_barco, s_tocado, s_agua):
    """
    Disparo a un tablero (array 2D) con barcos. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos marcadas. 
       x, y: coordenadas a las que se dispara. 
       x: coordenada x (columna). Entero positivo entre 0 y ncol. 
       y: coordenada y (fila). Entero positivo entre 0 y nfil. 
       s_barco: inicio del string que marca que hay barco en una casilla, 
                sin disparo previo en dicha casilla. 
       s_tocado: string que se escribirá en la casilla a la que se dispara 
                 si el disparo acierta a un barco. 
       s_agua: string que se escribirá en la casilla a la que se dispara 
               si el disparo no acierta a un barco. 
    
    Salidas: 
       acierto: booleano que es True si el disparo ha acertado a un barco 
                (en una casilla previamente no acertada). 
       hundido: booleano que es True si el disparo ha hundido a un barco. 
       tablero: tablero actualizado con el nuevo disparo. 
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    acierto = False
    hundido = False
    
    nfil = len(tablero)
    ncol = len(tablero[0])
    
    if x in range(ncol) and y in range(nfil):
        if tablero[y][x][0] == s_barco:
            nom_barco = tablero[y][x]
            tablero[y][x] == s_tocado
            acierto = True
            # Conteo de las celdas no tocadas que quedan de este barco 
            vidas_b = sum([f.count(nom_barco) for f in tablero])
            if vidas_b < 0.1:
                hundido = True
        else:
            tablero[y][x] == s_agua
    
    return acierto, hundido, tablero


def viables(tablero, eslora, ori, sep):
    """
    Calcula la lista de casillas iniciales viables para un barco de una eslora 
    y orientación determinadas, en un tablero (array 2D) con otros barcos ya 
    colocados. 
    
    Entradas: 
       tablero: array 2D con las posiciones donde hay barcos y las posiciones donde 
                debe haber separación entre barcos marcadas. 
       eslora: longitud del nuevo barco (nº de casillas que ocupa). 
               Entero positivo mayor que 0. 
       ori: orientación del nuevo barco. String de una letra. 
            Valores posibles: "h" (horizontal), "v" (vertical). 
            El nuevo barco se intenta colocar de izquierda a derecha en caso de ori="h", 
            y de arriba a abajo en caso de ori="v". 
       sep: 
    Salidas: 
       xy_ini_viab: lista de listas, con las coordenadas [x, y] viables donde pueda situarse 
                    la casilla inicial de un barco con una eslora y orientación determinada xxxxxxxxxxseguir aquíempezar 
                    un barco
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-10-14 (mie, 14 oct 2026). Por Julio Blanco Lorenzo. 
    
    
    nomfun = inspect.currentframe().f_code.co_name
    
    
# viables(tablero, eslora, ori)
#   Devuelve la lista de casillas iniciales viables para un barco de una eslora y orientación determinadas, en un tablero 
#   con otros barcos ya colocados. 


# PENDIENTES: 
#     - Función colocar_barco: sacar fuera la parte de verificar si un barco cabe. 
#          Se va a llamar también fuera, para calcular las casillas viables. **HECHO. 
#     - Función colocar_barco: añadir como entrada el id del barco, y donde haya barco, imprimir 'B' + su id. **HECHO. 
#     - Función colocar_barco: añadir como salida los índices de las casillas de separación alrededor del barco. **HECHO. 
#     - Función disparar: añadir como salida booleano que indique si un barco acertado se ha hundido. **HECHO. 
#     - Función genérica para pedir y validar input de usuario. 
#     - Función para colocar todos los barcos. 
#     - ¿Crear funciones para pasar índices de 2D a 1D y viceversa? 
