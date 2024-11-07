import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

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
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje

    def broadcast(self, env):
        ''' 
        Algoritmo de Broadcast.

        Desde el nodo distinguido (id_nodo == 0), se envía un mensaje a todos los demás nodos.
        Cuando recibe un mensaje que comienza con 'GO', lo retransmite a sus vecinos.

        Args:
            env: El entorno de SimPy donde se ejecuta el proceso.
        '''
        # Si el nodo es distinguido    
        if self.id_nodo == 0:
            data = self.mensaje
            self.canal_salida.envia('GO({})'.format(data), self.vecinos)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            if mensaje.startswith('GO'):
                # Extraemos el mensaje para mandarlo al siguiente
                data = mensaje[mensaje.index('(') + 1: mensaje.index(')')]
                self.canal_salida.envia('GO({})'.format(data), self.vecinos)

            yield env.timeout(TICK)
