import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

class NodoBroadcast(Nodo):
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        super().__init__(id_nodo,vecinos,canal_entrada,canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []

    def broadcast(self, env: simpy.Environment, data="Mensaje"):
       #Tu implementacion va aqui
