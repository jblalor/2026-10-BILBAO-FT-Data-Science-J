# encoding: utf-8

# Fichero de ejecución principal de Hundir La Flota. 

# $Version: 1 $, $Fecha: 2026-10-21 (mie, 21 oct 2026). Por Julio Blanco Lorenzo. 


import time
import pprint
import numpy as np
import random as rnd
import importlib


# Carga e inicialización de variables y funciones 
from variables import *
from funciones import *


print(f'\n-HLF-: \n¡BIENVENID@ A HUNDIR LA FLOTA, {noms_jug[0].upper()}! \n')

tableros = [[], []]  # El primer tablero corresponde a la persona, y el segundo a la máquina 
# Celdas a las que se puede disparar (no descubiertas): 
cels_no_descub = [list(range(ncol[0]*nfil[0])), list(range(ncol[1]*nfil[1]))]
ncels_no_descub = [len(cels_no_descub[0]), len(cels_no_descub[1])]
lsts_sep = [None, None]

for i in range(2):
    tableros[i] = inic_tablero(str_ini[i], ncol[i], nfil[i])
    print(f'\n-HLF-: \nTablero {i} ({noms_jug[i]}) vacío: \n')
    pprint.pprint(tableros[i])
### Graficar 


## Colocación de barcos en tableros 
caben = [False, False]
opc_slc = opc_colocar
while caben[0] == False or caben[1] == False or opc_slc == opc_colocar:
    # Pedir opción a usuario 
    if caben[0] == False or caben[1] == False:
        opc_slc = pedir_opc(msg_in1, opcs1)
    else:
        opc_slc = pedir_opc(msg_in, opcs)
    
    if opc_slc == opc_salir:
        print(f'\n-HLF-: \nSaliendo del juego. \n')
        time.sleep(0.2)
        quit()
    elif opc_slc == opc_colocar:
        # Colocación de los barcos, empezando por el segundo tablero 
        #Segundo tablero 
        print(f'\n-HLF-: \nColocando barcos en tablero 2 ({noms_jug[1]})... \n')
        caben[1], tableros[1], lsts_sep[1] = rep_colocar_barcos(str_ini[1], ncol[1], nfil[1], esloras[1], seps[1], strs_ocup, maxint_colocar)
        if caben[1] == False:
            print(f'\n-HLF-: \nERROR: no se han podido colocar todos los barcos en el segundo tablero, de {noms_jug[1]}. \n')
        else:
            if modo_juego == 'demo':
                print(f'\n-HLF-: \n[Modo demo] Tablero 2 ({noms_jug[1]}) con los barcos: \n')
                pprint.pprint(tableros[1])
            # Primer tablero
            print(f'\n-HLF-: \nColocando barcos en tablero 1 ({noms_jug[0]})... \n')
            if b_coloc_auto == True:
                caben[0], tableros[0], lsts_sep[0] = rep_colocar_barcos(str_ini[0], ncol[0], nfil[0], esloras[0], seps[0], strs_ocup, maxint_colocar)
            else:
                # Colocación manual de barcos 
                tableros[0] = inic_tablero(str_ini[0], ncol[0], nfil[0])
                caben[0], tableros[0], lsts_sep[0] = colocar_barcos(tableros[0], esloras[0], seps[0], strs_ocup, modo='man', stri=str_ini[0], opcs=opcs_ori, opc_reiniciar=opc_reiniciar, opc_salir=opc_salir)
            if caben[0] == False:
                print(f'\n-HLF-: \nERROR: no se han podido colocar todos los barcos en el primer tablero, de {noms_jug[0]}. \n')
            else:
                print(f'\n-HLF-: \nTablero 1 ({noms_jug[0]}) con los barcos: \n')
                pprint.pprint(tableros[0])
            

## Inicio del juego 
tableros_shw = tableros.copy()
disparos = [0, 0]
hay_toc = [False, False]  # Booleanos que indican si hay algún barco tocado y no hundido en cada tablero 
# Lista con las celdas tocadas de barcos no hundidos en el tablero del jugador 1, 
# que la máquina tendrá en cuenta en los niveles i+: 
lst_probables = []  

if modo_juego != 'demo':
    # Tablero del jugador 2 (máquina) ocultando las posiciones donde hay barco o las reservadas 
    # para separación mínima entre barcos 
    tableros_shw[1] = [[tableros_shw[1][j][i] if tableros_shw[1][j][i][0] not in strs_ocup else str_ini[1] for i in range(len(tableros_shw[1][0]))] for j in range(len(tableros_shw[1]))]

tur = j_primero
nju = 1
while opc_slc == opc_jugar and vidas[0] > 0.1 and vidas[1] > 0.1:
    ncels_no_descub = [len(cels_no_descub[0]), len(cels_no_descub[1])]
    print(f'\n-HLF-: \nJugada nº {nju}. \n')
    print(f'\n-HLF-: \nTurno de {noms_jug[tur]}, disparando al tablero de {noms_jug[1-tur]}. \n')
    if modo_juego == 'demo' and tur == 0:
        print(f'\n-HLF-: \n[MODO DEMO] \n')
    pprint.pprint(tableros_shw[1-tur])
    # Pedir/obtener aleatoriamente coordenada de disparo 
    if tur == 0:
        # Pedir celda al usuario 
        celda_ok = False
        salir = False
        while celda_ok == False and salir == False:
            msg_in_c = f'\n-HLF-: \nSelecciona casilla a la que disparar, o introduce {opc_salir} para salir del juego. '
            icel, salir = pedir_celda(msg_in_c, ncol[1-tur], nfil[1-tur], opc_salir)
            if salir == True:
                print(f'\n-HLF-: \nSaliendo del juego. \n')
                time.sleep(0.2)
                quit()
            else:
                # Chequear si la celda introducida por el usuario está las disponibles (no ya descubiertas) 
                if icel in cels_no_descub[1-tur]:
                    celda_ok = True
                    x, y = ind_1d_a_2d(icel, ncol[1-tur])
                else:
                    print(f'\n-HLF-: \nATENCIÓN: La casilla seleccionada ya está descubierta. Dispara a una casilla no descubierta. ')
    elif tur == 1:
        # Seleccionar aleatoriamente celda entre las disponibles 
        #### Pendiente calcular celdas probables si intelig_maq == True. 
        nint = 0
        tocado = False
        # La máquina sondea un máximo de nint_maq celdas en su turno, hasta que encuentra una con barco 
        while tocado == False and nint in range(nint_maq):
            ind = rnd.randint(0, ncels_no_descub[1-tur] - 1)
            icel = cels_no_descub[1-tur][ind]
            x, y = ind_1d_a_2d(icel, ncol[1-tur])
            if tableros[1-tur][y][x][0] == s_barco:
                tocado = True
            elif b_r_sond == True:
                del cels_no_descub[1-tur][ind]
            nint += 1
    
    # Disparar, y actualizar variables de vidas y vidas_barcos, y celdas disponibles para disparar (no descubiertas). 
    # Seguir disparando hasta que se falle. 
    acierto, hundido, id_barco, tableros[1-tur] = disparar(tableros[1-tur], icel, s_barco, s_tocado, s_agua)
    # Eliminar celda disparada de la lista de celdas disponibles para disparar 
    if icel in cels_no_descub[1-tur]:
        cels_no_descub[1-tur].remove(icel)
    disparos[tur] += 1
    tableros_shw[1-tur][y][x] = tableros[1-tur][y][x]
    
    nom_cel = chr(ord('A') + x) + str(y+1)
    msg_rst_i = f'\n-HLF-: \nResultado del disparo de {noms_jug[tur]} (nº {disparos[tur]}) a la celda {nom_cel} del tablero de {noms_jug[1-tur]}: '
    if acierto == True:
        vidas[1-tur] -= 1
        vidas_barcos[1-tur][id_barco] -= 1
        esloras_np = np.array(esloras[1-tur])
        vidas_barcos_np = np.array(vidas_barcos[1-tur])
        hay_toc[1-tur] = np.any((vidas_barcos_np < esloras_np - 0.1) & (vidas_barcos_np > 0.1))
        if hundido == True:
            msg_rst_f = f'TOCADO Y HUNDIDO BARCO CON ID {id_barco} \n'
            if b_dsabh == True:
                # Actualizar celdas disponibles para disparar (no descubiertas), eliminando las reservadas para 
                # separación mínima alrededor del barco hundido. Actualizar también tableros para graficar. 
                cels_no_descub[1-tur] = [e for e in cels_no_descub[1-tur] if e not in lsts_sep[1-tur][id_barco]]
                
                tablero_np = np.array(tableros[1-tur])
                tablero_shw_np = np.array(tableros_shw[1-tur])
                tablero_flat = tablero_np.ravel()
                tablero_shw_flat = tablero_shw_np.ravel()
                msk = np.array([s[0] == s_sep for s in tablero_flat[lsts_sep[1-tur][id_barco]]])
                tablero_shw_flat[np.array(lsts_sep[1-tur][id_barco])[msk]] = strs_descub[2].ljust(len(str_ini[1-tur]))
                tablero_flat[np.array(lsts_sep[1-tur][id_barco])[msk]] = tablero_shw_flat[np.array(lsts_sep[1-tur][id_barco])[msk]]
                tableros_shw[1-tur] = tablero_shw_np.tolist()
                tableros[1-tur] = tablero_np.tolist()
        else:
            msg_rst_f = 'TOCADO \n'
    else:
        msg_rst_f = 'AGUA \n'
        # Pasar turno 
        tur = 1 - tur
        if tur == j_primero:
            nju += 1
    
    print(msg_rst_i + msg_rst_f)
    
    if vidas[1-tur] < 0.1:
        print(f'\n-HLF-: \n¡Ha ganado {noms_jug[tur]}! \nFIN DEL JUEGO \n')

