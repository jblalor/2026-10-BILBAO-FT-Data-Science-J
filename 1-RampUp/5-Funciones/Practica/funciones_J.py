# encoding: utf-8

# Funciones para cálculo de áreas. 

# $Version: 1 $, $Fecha: 2026-10-13 (mar, 13 oct 2026). Por Julio Blanco Lorenzo. 


import math


def area_cuadrado(lado):
    return lado**2

def area_triang(base, altura):
    return base * altura / 2

def area_circ(radio):
    return math.pi * radio**2


