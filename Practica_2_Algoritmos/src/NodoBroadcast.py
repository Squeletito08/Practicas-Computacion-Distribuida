import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

#Demora un tiempo para ejemplificar el costo de los pasos que se realizan 
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        #Si el nodo es distinguido    
        if self.id_nodo == 0:
            data = self.mensaje
            self.canal_salida.envia('GO({})'.format(data), self.vecinos)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            if mensaje.startswith('GO'):
                #Extraemos el mensaje para mandarlo al siguiente
                data = mensaje[mensaje.index('(') + 1: mensaje.index(')')]
                self.canal_salida.envia('GO({})'.format(data), self.vecinos)
