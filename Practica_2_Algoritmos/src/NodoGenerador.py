import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoGenerador(Nodo):
    ''' 
    Implementa la interfaz de Nodo para el algoritmo de flooding.
    
    Atributos:
        id_nodo: Identificador único del nodo.
        vecinos: Lista de vecinos a los que el nodo puede enviar mensajes.
        canal_entrada: Canal por el que recibe mensajes.
        canal_salida: Canal por el que envía mensajes.
        padre: Nodo padre del árbol generador.
        hijos: Lista de hijos del nodo.
        mensajes_esperados: Contador de mensajes que se esperan recibir.
    '''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' 
        Inicializa un nodo generador.

        Args:
            id_nodo: Identificador único del nodo.
            vecinos: Lista de identificadores de nodos vecinos.
            canal_entrada: Canal de entrada para recibir mensajes.
            canal_salida: Canal de salida para enviar mensajes.
        '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        self.padre = id_nodo if id_nodo == 0 else None
        self.hijos = []
        self.mensajes_esperados = len(vecinos)
        
    def genera_arbol(self, env):
        """ 
        Implementación del algoritmo para crear un árbol generador.

        Este método permite que el nodo defina su estructura de árbol
        en función de los mensajes que recibe de sus vecinos.

        Args:
            env: Ambiente en el que se ejecutarán los procesos.
        """
        # Si el proceso es el nodo distinguido (0), envía el mensaje inicial
        if self.id_nodo == 0:
            self.canal_salida.envia('GO({})'.format(self.id_nodo), self.vecinos)

        # Simulamos el tiempo que tarda lo anterior 
        yield env.timeout(TICK)

        while True:
            msj = yield self.canal_entrada.get()  # Espera hasta que llegue un mensaje al canal de entrada  

            if msj.startswith('GO'):
                emisor = int(msj[msj.index('(') + 1 : msj.index(')')])  # Obtiene el mensaje enviado dentro del GO()

                # Define al emisor como padre si aún no tiene uno
                if self.padre is None:
                    self.padre = emisor 
                    self.mensajes_esperados = len(self.vecinos) - 1

                    # Informa al nuevo padre que este proceso será su hijo si no se esperan más mensajes
                    if self.mensajes_esperados == 0:
                        msj_hijo = [self.id_nodo]
                        self.canal_salida.envia('BACK({})'.format(msj_hijo), [emisor])
                    else:
                        # Envía mensajes a los vecinos para definir el padre
                        vecinos_sin_emisor = list(filter(lambda vecino: vecino != emisor, self.vecinos))
                        self.canal_salida.envia('GO({})'.format(self.id_nodo), vecinos_sin_emisor)

                else:
                    # Informa al emisor que este proceso no será su hijo
                    msj_hijo = []
                    self.canal_salida.envia('BACK({})'.format(msj_hijo), [emisor])

            if msj.startswith('BACK'):
                self.mensajes_esperados -= 1
                nuevos_hijos = msj[msj.index('[') + 1 : msj.index(']')]  # Obtiene el mensaje enviado dentro del BACK()

                # Convierte el mensaje a una lista 
                nuevos_hijos = nuevos_hijos.split(', ') if nuevos_hijos else []
                nuevos_hijos = [int(hijo) for hijo in nuevos_hijos if hijo]  

                # Añade nuevos hijos
                self.hijos.extend(nuevos_hijos)

                # Informa al padre que este proceso es su hijo si ya no se esperan más mensajes
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        msj_hijo = [self.id_nodo]
                        self.canal_salida.envia('BACK({})'.format(msj_hijo), [self.padre])

            # Simula el tiempo que tarda en procesar lo anterior 
            yield env.timeout(TICK)
