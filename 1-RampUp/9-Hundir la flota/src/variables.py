# encoding: utf-8

# Constantes para HLF. 

# $Version: 1 $, $Fecha: 2026-10-13 (mar, 13 oct 2026). Por Julio Blanco Lorenzo. 


# Dimensiones de los tableros 
# Dimensiones del tablero del jugador 1 (humano): 
ncol1 = 12  # Nº de columnas 
nfil1 = 10  # Nº de filas 
# Dimensiones del tablero del jugador 2 (máquina): 
ncol2 = ncol1  # Nº de columnas 
nfil2 = nfil1  # Nº de filas 

# Lista de barcos 
# Lista de listas. En cada lista anidada, el primer elemento es el nº de barcos de 
# una determinada eslora, y el segundo la eslora. 
# Jugador 1 (humano): 
barcos1 = [[1, 4], [2, 3], [3, 2], [4, 1]]
# Jugador 2 (máquina): 
barcos2 = [[1, 4], [2, 3], [3, 2], [4, 1]]

# Holgura entre barcos. Si vale 0, los barcos se pueden colocar sin ninguna separación 
# (casilla libre) entre ellos. Si vale 1, tiene que haber al menos una casilla libre 
# entre distintos barcos. 
holg1 = 1  # Jugador 1 (humano) 
holg2 = 1  # Jugador 2 (máquina) 
