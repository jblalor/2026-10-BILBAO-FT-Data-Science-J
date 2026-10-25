# encoding: utf-8

# Fichero de ejecución principal de Hundir La Flota. 

# $Version: 1 $, $Fecha: 2026-10-22 (jue, 22 oct 2026). Por Julio Blanco Lorenzo. 
# $Version: 2 $, $Fecha: 2026-10-26 (dom, 26 oct 2026). Por Julio Blanco Lorenzo. 
#    Cambios para depurar la lógica relacionada con la inteligencia de los disparos 
#    de la máquina (activada cuando intelig_maq==True). 


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
lsts_bar = [None, None]

for i in range(2):
    tableros[i] = inic_tablero(str_ini[i], ncol[i], nfil[i])
    print(f'\n-HLF-: \nTablero {i+1} ({noms_jug[i]}) vacío: \n')
    # pprint.pprint(tableros[i])
    impr_tablero(tableros[i])
# Graficado con matplotlib 
if b_shw_png == True:
    ax_titles = ['', '']
    vds_bar = [[0 for j in range(n_barcos[i])] for i in range(2)]
    for i in range(2):
        ax_titles[i] = f'Tablero de {noms_jug[i]} vacío'
    f_title = 'Inicialización de tableros'
    graf_tableros(tableros, mostrar_barcos, esloras, vds_bar, v_strs, v_colores_rgba, ax_titles, f_title)

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
        caben[1], tableros[1], lsts_sep[1], lsts_bar[1] = rep_colocar_barcos(str_ini[1], ncol[1], nfil[1], esloras[1], seps[1], strs_ocup, maxint_colocar)
        time.sleep(0.5)
        if caben[1] == False:
            print(f'\n-HLF-: \nERROR: no se han podido colocar todos los barcos en el segundo tablero, de {noms_jug[1]}. \n')
        else:
            if modo_juego == 'demo':
                print(f'\n-HLF-: \n[Modo demo] Tablero 2 ({noms_jug[1]}) con los barcos: \n')
                # pprint.pprint(tableros[1])
                impr_tablero(tableros[1])
            # Primer tablero
            print(f'\n-HLF-: \nColocando barcos en tablero 1 ({noms_jug[0]})... \n')
            if b_coloc_auto == True:
                caben[0], tableros[0], lsts_sep[0], lsts_bar[0] = rep_colocar_barcos(str_ini[0], ncol[0], nfil[0], esloras[0], seps[0], strs_ocup, maxint_colocar)
            else:
                # Colocación manual de barcos 
                tableros[0] = inic_tablero(str_ini[0], ncol[0], nfil[0])
                caben[0], tableros[0], lsts_sep[0], lsts_bar[0] = colocar_barcos(tableros[0], esloras[0], seps[0], strs_ocup, modo='man', stri=str_ini[0], opcs=opcs_ori, opc_reiniciar=opc_reiniciar, opc_salir=opc_salir)
            if caben[0] == False:
                print(f'\n-HLF-: \nERROR: no se han podido colocar todos los barcos en el primer tablero, de {noms_jug[0]}. \n')
            else:
                print(f'\n-HLF-: \nTablero 1 ({noms_jug[0]}) con los barcos: \n')
                # pprint.pprint(tableros[0])
                impr_tablero(tableros[0])
                # Graficado con matplotlib 
                if b_shw_png == True:
                    ax_titles = ['', '']
                    for i in range(2):
                        ax_titles[i] = f'Tablero de {noms_jug[i]}'
                    f_title = 'Tableros con los barcos colocados'
                    graf_tableros(tableros, mostrar_barcos, esloras, vidas_barcos, v_strs, v_colores_rgba, ax_titles, f_title)
            

## Inicio del juego 
tableros_shw = tableros.copy()
disparos = [0, 0]
# hay_toc = [False, False]  # Booleanos que indican si hay algún barco tocado y no hundido en cada tablero 
# Lista con las celdas adyacentes a celdas tocadas de barcos no hundidos en el tablero del jugador 1, 
# que la máquina tendrá en cuenta en los niveles i+: 
lst_probables = []
# Lista con las celdas adyacentes a celdas tocadas de barcos no hundidos en el tablero del jugador 1. 
# Cada elemento de la lista es una lista con el índice 1D de la celda tocada como primer elemento, y 
# con un string como segundo elemento que indica la orientación deducida para el barco que pasa 
# por esa celda. 
lst_tocadas = []
icels_tocadas = []

if modo_juego != 'demo':
    # Tablero del jugador 2 (máquina) ocultando las posiciones donde hay barco o las reservadas 
    # para separación mínima entre barcos 
    tableros_shw[1] = [[tableros_shw[1][j][i] if tableros_shw[1][j][i][0] not in strs_ocup else str_ini[1] for i in range(len(tableros_shw[1][0]))] for j in range(len(tableros_shw[1]))]

esl_res_2ym = [e for i, e in enumerate(esloras[0]) if (e > 1.1) and (vidas_barcos[0][i] > 0.1)]
if len(esl_res_2ym) > 0.1:
    esl_res_2ym_min = min(esl_res_2ym)
    esl_res_2ym_max = max(esl_res_2ym)

tur = j_primero
nju = 1
while opc_slc == opc_jugar and vidas[0] > 0.1 and vidas[1] > 0.1:
    ncels_no_descub = [len(cels_no_descub[0]), len(cels_no_descub[1])]
    print(f'\n-HLF-: \nJugada nº {nju}. \n')
    print(f'\n-HLF-: \nA {noms_jug[0]} le quedan {vidas[0]} vidas y a {noms_jug[1]} {vidas[1]}.\n')
    print(f'\n-HLF-: \nTurno de {noms_jug[tur]}, disparando al tablero de {noms_jug[1-tur]}. \n')
    if modo_juego == 'demo' and tur == 0:
        print(f'\n-HLF-: \n[MODO DEMO] \n')
    # pprint.pprint(tableros_shw[1-tur])
    impr_tablero(tableros_shw[1-tur])
    # Graficado con matplotlib 
    if b_shw_png == True:
        ax_titles = ['', '']
        for i in range(2):
            ax_titles[i] = f'Tablero de {noms_jug[i]}. Quedan {vidas[i]} vidas'
        f_title = f'Jugada nº {nju}. Turno de {noms_jug[tur]}, disparando al tablero de {noms_jug[1-tur]}'
        graf_tableros(tableros_shw, mostrar_barcos, esloras, vidas_barcos, v_strs, v_colores_rgba, ax_titles, f_title)
    
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
        nint = 0
        tocado = False
        # La máquina sondea un máximo de nint_maq celdas en su turno, hasta que encuentra una con barco 
        cels_no_descub_tmp = [e for e in cels_no_descub[1-tur]]
        lst_probables_tmp = [e for e in lst_probables]
        while tocado == False and nint in range(nint_maq) and len(cels_no_descub_tmp)>0.1:
            if len(lst_probables_tmp) > 0.1:
                icel = lst_probables_tmp[0]
                del lst_probables_tmp[0]
                if b_r_sond == True:
                    del lst_probables[0]
                cels_no_descub_tmp.remove(icel)
            else:
                ind = rnd.randint(0, len(cels_no_descub_tmp) - 1)
                icel = cels_no_descub_tmp[ind]
                cels_no_descub_tmp.remove(icel)
            x, y = ind_1d_a_2d(icel, ncol[1-tur])
            if tableros[1-tur][y][x][0] == s_barco:
                tocado = True
            elif b_r_sond == True:
                cels_no_descub[1-tur].remove(icel)
            nint += 1
    
    # Disparar, y actualizar variables de vidas y vidas_barcos, y celdas disponibles para disparar (no descubiertas). 
    # Seguir disparando hasta que se falle. 
    acierto, hundido, id_barco, tableros[1-tur] = disparar(tableros[1-tur], icel, s_barco, s_tocado, s_agua)
    # Eliminar celda disparada de la lista de celdas disponibles para disparar 
    if icel in cels_no_descub[1-tur]:
        cels_no_descub[1-tur].remove(icel)
    if intelig_maq == True and tur == 1 and icel in lst_probables:
        lst_probables.remove(icel)
    disparos[tur] += 1
    tableros_shw[1-tur][y][x] = tableros[1-tur][y][x]
    
    nom_cel = chr(ord('A') + x) + str(y+1)
    msg_rst_i = f'\n-HLF-: \nResultado del disparo de {noms_jug[tur]} (nº {disparos[tur]}) a la celda {nom_cel} del tablero de {noms_jug[1-tur]}: '
    if acierto == True:
        vidas[1-tur] -= 1
        vidas_barcos[1-tur][id_barco] -= 1
        esloras_np = np.array(esloras[1-tur])
        vidas_barcos_np = np.array(vidas_barcos[1-tur])
        # hay_toc[1-tur] = np.any((vidas_barcos_np < esloras_np - 0.1) & (vidas_barcos_np > 0.1))
        if hundido == True:
            msg_rst_f = f'TOCADO Y HUNDIDO BARCO CON ID {id_barco} \n'
            if b_dsabh == True:
                # Actualizar celdas disponibles para disparar (no descubiertas), eliminando las reservadas para 
                # separación mínima alrededor del barco hundido. Actualizar también tableros para graficar. 
                cels_no_descub[1-tur] = [e for e in cels_no_descub[1-tur] if e not in lsts_sep[1-tur][id_barco]]
                if intelig_maq == True and tur == 1 and len(lst_probables)>0.1:
                    lst_probables = [c for c in lst_probables if c in cels_no_descub[1-tur]]
                
                tablero_np = np.array(tableros[1-tur])
                tablero_shw_np = np.array(tableros_shw[1-tur])
                tablero_flat = tablero_np.ravel()
                tablero_shw_flat = tablero_shw_np.ravel()
                msk = np.array([s[0] == s_sep for s in tablero_flat[lsts_sep[1-tur][id_barco]]])
                tablero_shw_flat[np.array(lsts_sep[1-tur][id_barco])[msk]] = strs_descub[2].ljust(len(str_ini[1-tur]))
                tablero_flat[np.array(lsts_sep[1-tur][id_barco])[msk]] = tablero_shw_flat[np.array(lsts_sep[1-tur][id_barco])[msk]]
                tableros_shw[1-tur] = tablero_shw_np.tolist()
                tableros[1-tur] = tablero_np.tolist()
            if intelig_maq == True and tur == 1:
                lst_tocadas = [e for e in lst_tocadas if e[0] not in lsts_bar[1-tur][id_barco]]
                icels_tocadas = [e[0] for e in lst_tocadas]
                esl_res_2ym = [e for i, e in enumerate(esloras[1-tur]) if (e > 1.1) and (vidas_barcos[1-tur][i] > 0.1)]
                if len(esl_res_2ym) > 0.1: 
                    esl_res_2ym_min = min(esl_res_2ym)
                    esl_res_2ym_max = max(esl_res_2ym)
        else:
            msg_rst_f = 'TOCADO \n'
            if intelig_maq == True and tur == 1:
                lst_tocadas.insert(0, [icel, ''])
                icels_tocadas = [e[0] for e in lst_tocadas]
                for e in lst_tocadas:
                    if e[1] == '':
                        icels_prio1, icels_prio2, icels_descar, e[1] = intelig_disp(tableros[1-tur], e[0], icels_tocadas, seps[1-tur], strs_descub, esl_res_2ym_min, esl_res_2ym_max)
                        lst_probables = [e for e in lst_probables if e not in icels_prio1]
                        lst_probables = icels_prio1 + lst_probables
                        icels_prio2_f = [e for e in icels_prio2 if e not in lst_probables]
                        lst_probables = [e for e in lst_probables if e not in icels_descar]
                        lst_probables = lst_probables + icels_prio2_f
                        cels_no_descub[1-tur] = [e for e in cels_no_descub[1-tur] if e not in icels_descar]
    else:
        msg_rst_f = 'AGUA \n'
        # Pasar turno 
        tur = 1 - tur
        if tur == j_primero:
            nju += 1
    
    print(msg_rst_i + msg_rst_f)
    time.sleep(0.5)
    
    if vidas[1-tur] < 0.1:
        print(f'\n-HLF-: \nTablero de {noms_jug[0]}, tras {disparos[1]} disparos de {noms_jug[1]}. \n')
        # pprint.pprint(tableros[0])
        impr_tablero(tableros[0])
        print(f'\n-HLF-: \nTablero de {noms_jug[1]}, tras {disparos[0]} disparos de {noms_jug[0]}. \n')
        # pprint.pprint(tableros[1])
        impr_tablero(tableros[1])
        print(f'\n-HLF-: \n¡Ha ganado {noms_jug[tur]}! \nFIN DEL JUEGO \n')
        # Graficado con matplotlib 
        if b_shw_png == True:
            ax_titles = ['', '']
            for i in range(2):
                ax_titles[i] = f'Tablero de {noms_jug[i]}, tras {disparos[1-i]} disparos de {noms_jug[1-i]}'
            f_title = f'¡Ha ganado {noms_jug[tur]}! FIN DEL JUEGO'
            graf_tableros(tableros, mostrar_barcos, esloras, vidas_barcos, v_strs, v_colores_rgba, ax_titles, f_title)

