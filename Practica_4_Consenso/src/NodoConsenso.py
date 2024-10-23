import simpy
from random import randint
from Nodo import *
from Canales.CanalRecorridos import *
import math

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set()
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.
        self.fallo = math.inf
        self.New.add((0, id_nodo))

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Escoger cuando fallarán los nodos.
        if self.id_nodo < f:
            self.fallo = randint(0, f)
            self.fallare = True

        while env.now <= f:
            if self.New != set() and env.now < self.fallo:
                #print(self.New)
                #print(self.id_nodo)
                self.canal_salida.envia([self.New, self.id_nodo], self.vecinos)
            [rec, p] = yield self.canal_entrada.get()
            #print(rec)
            #print(p)
            self.rec_from[p] = rec
            self.New = set()
            for j in self.vecinos:
                if self.rec_from[j] != None:
                    for i in self.rec_from[j]:
                        [v,k] = i
                        if self.V[k] == None:
                            self.V[k] = v
                            self.New.add((v, k))
            yield env.timeout(TICK)

        for v in self.V:
            if v != None:
                self.lider = v
        self.lider = None
