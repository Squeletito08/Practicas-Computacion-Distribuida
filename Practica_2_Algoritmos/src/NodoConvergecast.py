import simpy
import time
from Nodo import *
from Canales.CanalConvergecast import *

#Demora un tiempo para ejemplificar el costo de los pasos que se realizan 
TICK = 1


class NodoConvergecast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, padre, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.padre = padre

    def convergecast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        #Si el nodo es hoja
        if (len(self.vecinos)==0):
            data = "["+ str(self.id_nodo) +", "+ str(self.mensaje) +"]"
            # Mandar mensaje al padre
            self.canal_salida.envia('BACK({})'.format(data), self.padre)
            print(data)
            yield env.timeout(TICK)
        
        while True:
            mensaje = yield self.canal_entrada.get()
            if mensaje.startswith('BACK'):
                #Extraemos el mensaje para mandarlo al siguiente
                data = mensaje[mensaje.index('(') + 1: mensaje.index(')')]
                #Agregamos el mensaje propio
                d = "["+ str(self.id_nodo) +", "+ str(self.mensaje) +"]"
                if d not in data:
                    data += d
                print(data)
                # Mandar mensaje al padre
                if(self.id_nodo != 0):
                    self.canal_salida.envia('BACK({})'.format(data), self.padre)
                    yield env.timeout(TICK)
                else:
                    self.mensaje = data
