import simpy
import time
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

# Demora un tiempo para ejemplificar el costo de los pasos que se realizan 
TICK = 1

class NodoBroadcast(Nodo):
    ''' 
    Implementa la interfaz de Nodo para el algoritmo de Broadcast.
    
    Atributos:
        id_nodo: Identificador único del nodo.
        vecinos: Lista de vecinos a los que el nodo puede enviar mensajes.
        canal_entrada: Canal por el que recibe mensajes.
        canal_salida: Canal por el que envía mensajes.
        mensaje: Mensaje inicial que se enviará (opcional).
    '''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        '''
        Inicializa un nodo broadcast.

        Args:
            id_nodo: Identificador único del nodo.
            vecinos: Lista de identificadores de nodos vecinos.
            canal_entrada: Canal de entrada para recibir mensajes.
            canal_salida: Canal de salida para enviar mensajes.
            mensaje: Mensaje inicial que se enviará (opcional).
        '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []

    def broadcast(self, env: simpy.Environment, data="m"):
        ''' 
        Algoritmo de Broadcast.

        Desde el nodo distinguido (id_nodo == 0), se envía un mensaje a todos los demás nodos.
        Cuando recibe un mensaje que comienza con 'GO', lo retransmite a sus vecinos.

        Args:
            env: El entorno de SimPy donde se ejecuta el proceso.
        '''

        # Si el nodo es distinguido    
        if self.id_nodo == 0:
            self.mensaje = data
            yield env.timeout(randint(1, 5))
            for vecino in self.vecinos:
                self.reloj += 1
                self.eventos.append([self.reloj, 'E', data, self.id_nodo, vecino])
            self.canal_salida.envia((data, self.reloj, self.id_nodo), self.vecinos)
                
                
        while True:
            yield env.timeout(randint(1, 5))
            data, reloj, j = yield self.canal_entrada.get()
            self.mensaje = data
            self.reloj = max(self.reloj, reloj) + 1
            self.eventos.append([self.reloj, 'R', data, j, self.id_nodo])
            yield env.timeout(randint(1, 5))
            
            vecinos_sin_j = [vecino for vecino in self.vecinos if vecino != j]
            
            for vecino in vecinos_sin_j:
                self.reloj += 1
                self.eventos.append([self.reloj, 'E', data, self.id_nodo, vecino])

            self.canal_salida.envia((data, self.reloj, self.id_nodo), vecinos_sin_j) 
                
                
            yield env.timeout(randint(1, 5))

