import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        self.padre = id_nodo if id_nodo == 0 else None
        self.hijos = []
        self.mensajes_esperados = len(vecinos)
        
    def genera_arbol(self, env):
        if self.id_nodo == 0:
            self.canal_salida.envia('GO({})'.format(self.id_nodo), self.vecinos)

        while True:
            msj = yield self.canal_entrada.get()

            if msj.startswith('GO'):
                emisor = int(msj[msj.index('(') + 1 : msj.index(')')])
                if self.padre is None:
                    self.padre = emisor
                    self.mensajes_esperados = len(self.vecinos) - 1

                    if self.mensajes_esperados == 0:
                        msj_hijo = [self.id_nodo]
                        self.canal_salida.envia('BACK({})'.format(msj_hijo), [emisor])
                        yield env.timeout(TICK)
                    else:
                        vecinos_sin_emisor = list(filter(lambda vecino: vecino != emisor, self.vecinos))
                        self.canal_salida.envia('GO({})'.format(self.id_nodo), vecinos_sin_emisor)
                else:
                    msj_hijo = []
                    self.canal_salida.envia('BACK({})'.format(msj_hijo), [emisor])

            if msj.startswith('BACK'):
                self.mensajes_esperados -= 1
                nuevos_hijos = msj[msj.index('[') + 1 : msj.index(']')]
                nuevos_hijos = nuevos_hijos.split(', ') if nuevos_hijos else []
                nuevos_hijos = [int(hijo) for hijo in nuevos_hijos if hijo]  

                self.hijos.extend(nuevos_hijos)

                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        msj_hijo = [self.id_nodo]
                        self.canal_salida.envia('BACK({})'.format(msj_hijo), [self.padre])

