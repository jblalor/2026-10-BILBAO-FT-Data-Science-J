# encoding: utf-8

# Parámetros para HLF. 

# $Version: 1 $, $Fecha: 2026-10-22 (jue, 22 oct 2026). Por Julio Blanco Lorenzo. 


from matplotlib.colors import to_rgba
import numpy as np


# Nombres de los jugadores
nom_jug1 = 'Julio'  # Jugador 1 (persona)
nom_jug2 = 'máquina'  # Jugador 2 (máquina)
noms_jug = [nom_jug1, nom_jug2]

# Entero con el que se fija quién juega primero. Opciones: 
#   0: la persona. 
#   1: la máquina. 
j_primero = 0


# Dimensiones de los tableros 
# Dimensiones del tablero del jugador 1 (humano): 
ncol1 = 10  # Nº de columnas 
nfil1 = 10  # Nº de filas 
# Dimensiones del tablero del jugador 2 (máquina): 
ncol2 = 10  # Nº de columnas 
nfil2 = 10  # Nº de filas 

ncol = [ncol1, ncol2]
nfil = [nfil1, nfil2]

# Lista de barcos 
# Lista de listas. En cada lista anidada, el primer elemento es el nº de barcos de 
# una determinada eslora, y el segundo la eslora. 
# Jugador 1 (humano): 
barcos1 = [[1, 4], [2, 3], [3, 2], [4, 1]]
# Jugador 2 (máquina): 
barcos2 = [[1, 4], [2, 3], [3, 2], [4, 1]]

# Separación mínima entre barcos. Entero positivo, 0 incluído. 
#Si vale 0, los barcos se pueden colocar sin ninguna 
# separación (casilla libre) entre ellos. Si vale 1, tiene que haber al menos una 
# casilla libre entre distintos barcos. 
sep1 = 1  # Jugador 1 (humano) 
sep2 = 1  # Jugador 2 (máquina) 
seps = [sep1, sep2]

# Nº máximo de intentos para colocar los barcos en cada tablero aleatoriamente 
maxint_colocar = 5

# Booleano para controlar si los barcos del jugador 1 (persona) se colocan aleatoriamente o 
# manualmente por el propio jugador. Si vale True, se colocan aleatoriamente. 
b_coloc_auto = True


# Nivel de dificultad del juego. Opciones: 
#   - 1, 2, 3: corresponde al nº máximo de intentos de disparo de la máquina en su turno. 
#   - '1+', '2+', '3+': igual que los correspondientes niveles sin '+', haciendo más 
#     inteligentes los disparos de la máquina. Disparará primero a las celdas adyacentes 
#     a barcos tocados no hundidos. 
nivel = '9+'
intelig_maq = False
if type(nivel) == int:
    nint_maq = nivel
    intelig_maq = False
elif type(nivel) == str:
    nint_maq = int(nivel[0])
    if nivel[-1] == '+':
        intelig_maq = True

# Booleano con el que se controla si la máquina recuerda las celdas que ha sondeado en 
# turnos pasados y que no ha disparado. Relevante para los niveles >1. 
# Si es True, las recuerda, y por lo tanto el nivel de dificultad es mayor. 
b_r_sond = False

# Booleano para controlar si se descubren o no las celdas de separación mínima necesaria 
# alrededor de los barcos hundidos. Si vale True, se descubren, y también se descartan como 
# posibles celdas a disparar. 
b_dsabh = True


# Modo de juego. Opciones: 
#   - normal: no se muestran los barcos del tablero de la máquina. 
#   - demo: se muestran los barcos del tablero de la máquina. 
modo_juego = 'normal'

# Opciones de input de usuario 
opc_salir = 'SAL'
opc_jugar = 'J'
opc_colocar = 'C'
opc_reiniciar = 'R'
opc_h = 'H'
opc_v = 'V'
opcs = {opc_colocar: 'colocar barcos', 
        opc_jugar: 'jugar', 
        opc_salir: 'salir del juego'}
opcs_ori = {opc_h: 'colocar barco en horizontal', 
            opc_v: 'colocar barco en vertical', 
            opc_reiniciar: 'reiniciar colocación de barcos', 
            opc_salir: 'salir del juego'}
opcs1 = opcs.copy()
del opcs1[opc_jugar]

# Mensajes que se muestran en los diálogos de input de usuario: 
msg_in1 = '\n-HLF-: \nEscoge una de las siguentes opciones: \n'
msg_in = '\n-HLF-: \nEscoge una de las siguentes opciones: \n'
for k, v in opcs1.items():
    msg_in1 += f'   - {k}: {v}\n'
for k, v in opcs.items():
    msg_in += f'   - {k}: {v}\n'


# Strings con los que se marcan las celdas de los tableros 
# Strings que marcan que una celda no está disponible para su ocupación por un barco 
# (por estar ocupada por otro barco, o por estar reservada para la separación necesaria 
# entre barcos). 
# El primero marca que hay barco, y el segundo, la separación necesaria entre barcos. 
# Cada string debe tener un único caracter. 
strs_ocup = ['B', 'S']
s_barco = strs_ocup[0]
s_sep = strs_ocup[1]

# Strings que marcan las celdas descubiertas de los tableros. 
# Descripción de las celdas que marca cada uno: 
# 1: celdas a las que se ha disparado y tocado a algún barco. 
# 2: celdas a las que se ha disparado y no se ha acertado a ningún barco (agua). 
# 3: celdas no disparadas correspondientes a la separación mínima entre barcos, descubiertas 
#    tras hundir algún barco si b_dsabh = True. 
# Cada string debe tener un único caracter. 
strs_descub = ['X', 'O', 'a']
s_tocado = strs_descub[0]
s_agua = strs_descub[1]


# Booleano que controla si se crean figuras con los dos tableros, además de las impresiones 
# de los tableros que se muestran por pantalla. Si es True, se crean y se muestran las 
# figuras con matplotlib, y se muestran sus pngs. 
# Los siguientes parámetros se usan en la creación de las figuras. 
b_shw_png = True
# Colores para graficar los tableros, siendo el primero el correspondiente a las celdas vacías, 
# y los siguientes a los elementos de las listas strs_ocup y strs_descub, por orden. 
# Ver nomenclaturas admitidas en doc de matplotlib.colors. 
colores = ['ivory', 'grey', 'ivory', 'red', 'blue', 'cyan']  # Colores de las celdas 
alfas = [0.9, 0.6, 0.9, 0.6, 0.5, 0.5]  # Nivel de opacidad de los colores de las celdas 
colores_bordes = ['ivory', 'grey', 'ivory', 'red', 'blue', 'cyan']  # Colores de los bordes de las celdas 
alfas_bordes = [0.99, 0.99, 0.99, 0.99, 0.99, 0.99]  # Nivel de opacidad de los colores de los bordes de las celdas 

mostrar_barcos = [True, False]
if modo_juego == 'demo':
    mostrar_barcos[1] = True



### Datos derivados 
# Listas de esloras. Cada una de longitud igual al nº total de barcos de cada jugador. 
esloras1 = [elm[1] for elm in barcos1 for i in range(elm[0])]
esloras2 = [elm[1] for elm in barcos2 for i in range(elm[0])]
esloras = [esloras1, esloras2]
n_barcos = [len(esloras1), len(esloras2)]
vidas = [sum(esloras1), sum(esloras2)]
# vidas_barcos = esloras.copy()
vidas_barcos1 = esloras1.copy()
vidas_barcos2 = esloras2.copy()
vidas_barcos = [vidas_barcos1, vidas_barcos2]

str_ini = [' ' * (1 + len(str(n_barcos[0]-1))), ' ' * (1 + len(str(n_barcos[0]-1)))]

strs = [' '] + strs_ocup + strs_descub
v_strs = [strs, strs]

# Colores y alfas en formato RGBA 
colores_rgba = [to_rgba(c, alpha=a) for c, a in zip(colores, alfas)]
v_colores_rgba = [colores_rgba, colores_rgba]
colores_bordes_rgba = [to_rgba(c, alpha=a) for c, a in zip(colores_bordes, alfas_bordes)]

oris = ['h', 'v']

