import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint


class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, num_nodos):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = self.id_nodo
        self.hijos = []
        self.eventos = []
        self.reloj = [0] * num_nodos

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aquí
