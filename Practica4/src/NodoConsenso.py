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
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.
        self.fallo = math.inf

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Escoger cuando fallarán los nodos, entre la rondas 0 y f.
        if self.id_nodo < f:
            self.fallo = randint(0, f)
            self.fallare = True
        # Algoritmo de consenso.
        while True:
            while env.now <= f: # Comienzo de una ronda, desde 0 a f.
                # Mandan mensaje los nodos que no han fallado y con algo en New.
                if self.New != set() and env.now < self.fallo:
                    self.canal_salida.envia((self.New, self.id_nodo), self.vecinos)
                # Guardamos lo recibido en rec_from.
                (rec, j) = yield self.canal_entrada.get()
                self.rec_from[j] = rec
                # Agregamos los mensajes nuevos en V y los guardamos en New.
                self.New = set()
                for i in self.rec_from[j]:
                    if self.V[i] == None:
                        self.V[i] = i
                        self.New.add(i)
                yield env.timeout(TICK) # Fin de la ronda.
            # Escogemos al líder.
            for v in self.V:
                if v != None:
                    self.lider = v
                    return self.lider
