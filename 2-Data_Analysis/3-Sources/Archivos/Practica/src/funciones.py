# encoding: utf-8

# Funciones para el ejercicio práctico de lectura y escritura de ficheros con Python. 

# $Version: 1 $, $Fecha: 2026-11-09 (lun, 09 nov 2026). Por Julio Blanco Lorenzo. 


import os
import shutil


def ordenar_fichs(direc, subdirecs, subdirec_otro):
    """
    Mueve ficheros situados en un directorio a subdirectorios 
    especificados. Solo mueve los ficheros situados en el 
    directorio raíz especificado (no los situados en subdirectorios). 
    
    Entradas: 
       direc: directorio de trabajo, donde se encuentran los ficheros a 
              mover. Tipo: str. 
       subdirecs: diccionario en el que las claves son nombres de 
                  subdirectorios, y los valores son listas o tuplas con 
                  extensiones de archivo (str). Los ficheros con extensión 
                  igual a uno de los valores de la lista correspondiente a 
                  una clave subdirec se moverán a la carpeta direc/subdirec. 
                  Esa carpeta se creará si no existe. 
       subdirec_otro: nombre del subdirectorio al que Tipo: str. 
    
    Salidas: None
    
    """
    #
    
    # $Version: 1 $, $Fecha: 2026-11-09 (lun, 09 nov 2026). Por Julio Blanco Lorenzo. 
    
    
    dir_act = os.getcwd()
    
    try:
        os.chdir(direc)
        
        lst_subdirecs = list(subdirecs.keys())
        len_lst_subdirecs = len(lst_subdirecs)
        
        elms = os.listdir(direc)
        
        for elm in elms:
            ruta_elm = os.path.join(direc, elm)
            if os.path.isfile(ruta_elm):
                nom_f, ext = os.path.splitext(ruta_elm)
                sigue = 1
                i = 0
                while sigue == True and i in range(len_lst_subdirecs):
                    if ext in subdirecs[lst_subdirecs[i]]:
                        try:
                            os.mkdir(lst_subdirecs[i])
                        except:
                            pass
                        shutil.move(ruta_elm, f"./{lst_subdirecs[i]}/")
                        sigue = False
                    i += 1
                
                if sigue == True:
                    try:
                        os.mkdir(subdirec_otro)
                    except:
                        pass
                
                    try:
                        shutil.move(ruta_elm, f"./{subdirec_otro}/")
                    except:
                        # No se moverá el fichero si ya existe uno con el mismo nombre en la carpeta de destino 
                        pass
        
        os.chdir(dir_act)
    except Exception as e:
        print(e)


