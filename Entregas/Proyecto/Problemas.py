import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from itertools import combinations, product
from types import MethodType
from Logica import *


Nx = 3
Turnos =[0,1,2,3,4,5,6,7,8,9]
Objetos = ["Gallina","Zorro","Maiz"]
objeto_a_numero = {objeto: indice for indice, objeto in enumerate(Objetos)}
Nn = len(objeto_a_numero)
Nt = len(Turnos)
X = list(range(Nx))
T = list(range(Nt))
OenP = Descriptor([Nx, Nt, Nn]) 


def escribir(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    x, t, n  = self.inv(atomo)
    return f" {Objetos[n]}{neg} está en la casilla ({X[x]}) en el tiempo {T[t]}"

    from types import MethodType

    OenP.escribir = MethodType(escribir, OenP)

class Cruce:

    '''
    Clase para representar el problema de poner
    tres caballos en un tablero de ajedrez sin que se
    puedan atacar el uno al otro.
    '''

    def __init__(self):
        self.OenP = Descriptor([Nx, Nt, Nn])
        self.OenP.escribir = MethodType(escribir, OenP)
        r0 = self.r0()
        r1 = self.r1()
        r2 = self.r2()
        r3 = self.r3()
        r4 = self.r4()
        r5 = self.r5()
        r6 = self.r6()
        self.reglas = [r0,r1, r2, r3, r4, r5, r6]
        


    def r0(self):
        formula1 = '(' +'('+ OenP.P([0, 0, 0]) + ')'+'Y' '('+ OenP.P([1, 0, 0]) + ')' + 'Y' + '(' + OenP.P([2, 0, 0]) + ')' + ')' 
        return formula1
    
    def r1(self):
    # Regla 1; La gallina no puede quedar a solas con el maíz (estar en la misma casilla en un turno T sin el zorro).
        formulas = []
        for t in T:
            for objeto in Objetos:
                formula1 = ''  # Mueve la inicialización fuera del bucle X
                inicial = True
                for x in X:
                    if inicial:
                        formula1 = OenP.P([x, t, objeto_a_numero[objeto]])
                        inicial = False
                    else:
                        formula1 = "(" + formula1 + "O" + OenP.P([x, t, objeto_a_numero[objeto]]) + ")"

                if objeto == 'Zorro':
                    formula1 = "(" + OenP.P([x, t, objeto_a_numero[objeto]]) + ">-" + OenP.P([x, t, objeto_a_numero['Gallina']]) + ")"
                    formulas.append(formula1)
                elif objeto == 'Gallina':
                    formula1 = "(" + OenP.P([x, t, objeto_a_numero[objeto]]) + ">-" + OenP.P([x, t, objeto_a_numero['Zorro']]) + ")"
                    formulas.append(formula1)

        return formulas




    def r2(self):
        # Regla 2; La gallina no puede quedar a solas con el maíz (estar en la misma casilla en un turno T sin el zorro).
        formulas = []
        for t in T:
            for objeto in Objetos:
                formula1 = ''  # Mueve la inicialización fuera del bucle X
                inicial = True
                for x in X:
                    if inicial:
                        formula1 = OenP.P([x, t, objeto_a_numero[objeto]])
                        inicial = False
                    else:
                        formula1 = "(" + formula1 + "O" + OenP.P([x, t, objeto_a_numero[objeto]]) + ")"

                if objeto == 'Gallina':
                    formula1 = "(" + OenP.P([x, t, objeto_a_numero[objeto]]) + ">-" + OenP.P([x, t, objeto_a_numero['Maiz']]) + ")"
                    formulas.append(formula1)
                elif objeto == 'Maiz':
                    formula1 = "(" + OenP.P([x, t, objeto_a_numero[objeto]]) + ">-" + OenP.P([x, t, objeto_a_numero['Gallina']]) + ")"
                    formulas.append(formula1)

        return formulas

    def r3(self):
        # Regla 3; Cada O solo puede estar en un lugar a la vez. 
        formulas = []
        for objeto in Objetos:
            for tiempo in T:
                for casilla in X:
                    otras_casillas = [otra_casilla for otra_casilla in X if otra_casilla != casilla]
                    formula_regla = ''
                    inicial = True
                    for otra_casilla in otras_casillas:
                        if inicial:
                            formula_regla = OenP.P([otra_casilla,tiempo, objeto_a_numero[objeto]])
                            inicial = False
                        else:
                            formula_regla = "(" + formula_regla + "O" + OenP.P([otra_casilla,tiempo, objeto_a_numero[objeto]]) + ")"

                    formula_regla = "(" + OenP.P([otra_casilla,tiempo, objeto_a_numero[objeto]]) + ">-" + formula_regla + ")"
                    formulas.append(formula_regla)

        return formulas


    def r4(self):
        # Regla 4: En cada T, debe haber un cambio de posición para algún O.
        formulas = []
        for t in range(len(T) - 1):
            for objeto in Objetos:
                formula4 = ''  # Inicialización dentro del bucle X
                inicial = True
                for x in X:
                    otras_casillas = [otra_casilla for otra_casilla in X if otra_casilla != x]
                    for otra_casilla in otras_casillas:
                        if inicial:
                            formula4 = OenP.P([x, t, objeto_a_numero[objeto]])
                            inicial = False
                        else:
                            formula4 = "(" + formula4 + "O" + OenP.P([x, t, objeto_a_numero[objeto]]) + ")"

                    formula4 = "(" + formula4 + ">" + OenP.P([otra_casilla, max(0, t + 1),objeto_a_numero[objeto]]) + ")"

                formulas.append(formula4)

        return formulas

    def r5(self):
    # Regla 5: Para cada T, el objeto en la casilla 1 debe tener al menos otro objeto en otra casilla.
        formulas = []
        for t in T:
            for objeto in Objetos:
                formula_objeto_en_2 = OenP.P([1, t, objeto_a_numero[objeto]])
                otras_objetos_no_en_2 = [f"{OenP.P([1, t, objeto_a_numero[otro_objeto]])}" for otro_objeto in Objetos if otro_objeto != objeto]

                formula_completa = f"({formula_objeto_en_2}>-({'Y'.join(otras_objetos_no_en_2)}))"
                formulas.append(formula_completa)

        return formulas


    def r6(self):
            # Regla 6: Ningún O puede estar más de un turno en R.
        formulas = []
        for objeto in Objetos:
            for t in range(len(T) - 1):
                formula_regla = ''
                inicial = True
                if inicial:
                    formula_regla = OenP.P([1, t + 1, objeto_a_numero[objeto]])
                    inicial = False
                else:
                    formula_regla = "(" + formula_regla + "O" + OenP.P([1, t, objeto_a_numero[objeto]]) + ")"

                formula_regla = "(" + OenP.P([1, t, objeto_a_numero[objeto]]) + ">-" + formula_regla + ")"
                formulas.append(formula_regla)

        return formulas



        def visualizar(self, I):
            fig, axes = plt.subplots(figsize=(48,24))
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)

            step = 1. / 10
            tangulos = []
            direcciones = {}

            for i in range(3):
                for j in range(10):
                    color = 'lightgreen' if i == 0 or i == 2 else 'lightskyblue'
                    tangulos.append(patches.Rectangle(*[(i * step, j * step), step, step], facecolor=color))
                    direcciones[(i, j)] = [i * step + step / 2, 1 - j * step - step / 2]

            for i in range(10):
                locacion = i * step
                tangulos.append(patches.Rectangle(*[(0, locacion), 3 * step, 0.005], facecolor='black'))
                tangulos.append(patches.Rectangle(*[(i * step, 0), 0.005, 1], facecolor='black'))

            for t in tangulos:
                axes.add_patch(t)

            arr_gallina = plt.imread("./img/gallina.png", format='png')
            arr_fox = plt.imread("./img/zorro.png", format='png')
            arr_corn = plt.imread("./img/maiz.png", format='png')

            imagebox_gallina = OffsetImage(arr_gallina, zoom=0.3)
            imagebox_fox = OffsetImage(arr_fox, zoom=0.3)
            imagebox_corn = OffsetImage(arr_corn, zoom=0.3)

            imagebox_gallina.image.axes = axes
            imagebox_fox.image.axes = axes
            imagebox_corn.image.axes = axes

            for l in I:
                if I[l]:
                    x, objeto, tiempo = self.OenP.inv(l)
                    if tiempo == 0:
                        ab_gallina = AnnotationBbox(imagebox_gallina, direcciones[(x, objeto)], frameon=False)
                        axes.add_artist(ab_gallina)
                    elif tiempo == 1:
                        ab_fox = AnnotationBbox(imagebox_fox, [direcciones[(x, objeto)][0] - step / 4, direcciones[(x, objeto)][1]], frameon=False)
                        axes.add_artist(ab_fox)
                    elif tiempo == 2:
                        ab_corn = AnnotationBbox(imagebox_corn, [direcciones[(x, objeto)][0] + step / 4, direcciones[(x, objeto)][1]], frameon=False)
                        axes.add_artist(ab_corn)

            axes.set_xlim(-step / 2, 3 * step + step / 2)
            axes.set_ylim(-step / 2, 1 + step / 2)
            axes.set_aspect('equal', 'box') 
            plt.show()

