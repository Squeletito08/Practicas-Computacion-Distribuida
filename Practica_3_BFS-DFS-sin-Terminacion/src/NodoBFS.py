import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra:
        self.hijos = []
        self.padre = -1
        self.distancia = -1

    def bfs(self, env):
        yield env.timeout(TICK)

        if self.id_nodo == 0:
            self.canal_salida.envia([self.id_nodo, 'GO()', -1], [0])

        # El nodo 0 envía un mensaje a su vecino más pequeño
        while True:
            # Esperamos a que nos llegue el mensaje
            mensaje = yield self.canal_entrada.get()
            mensajero = mensaje[0]
            tipo_mensaje = mensaje[1]
            argumento = mensaje[2]

            if 'GO' in tipo_mensaje:  # Mensaje de tipo GO
                d = argumento

                if self.padre == -1:
                    self.padre = mensajero
                    self.hijos = []
                    self.distancia = d + 1
                    self.mensajes_esperados = len(self.vecinos) - 1
                    if self.mensajes_esperados == 0:
                        self.canal_salida.envia(
                            [self.id_nodo, 'BACK()', ['yes', d+1]], [self.padre])
                    else:
                        aux = self.vecinos.copy()
                        try:
                            aux.remove(mensajero)
                        except:
                            pass
                        self.canal_salida.envia(
                            [self.id_nodo, 'GO()', d+1], aux)

                # Si el mensaje viene de un nodo con menor distancia, actualizamos
                elif self.distancia > d + 1:
                    self.padre = mensajero
                    self.hijos = []
                    self.distancia = d + 1
                    self.mensajes_esperados = len(self.vecinos) - 1
                    if self.mensajes_esperados == 0:
                        self.canal_salida.envia(
                            [self.id_nodo, 'BACK()', ['yes', self.distancia]], [self.padre])
                    else:
                        aux = self.vecinos.copy()
                        aux.remove(mensajero)
                        self.canal_salida.envia(
                            [self.id_nodo, 'GO()', d+1], aux)
                else:
                    self.canal_salida.envia(
                        [self.id_nodo, 'BACK()', ['no', d+1]], [mensajero])

            # Mensaje de tipo BACK
            if "BACK" in tipo_mensaje:
                resp = mensaje[0]  # yes o no
                d = mensaje[1]  # distancia

                if d == self.distancia + 1:  # Si el mensaje viene de un nodo con menor distancia, actualizamos
                    if resp == 'yes':  # Si el nodo es parte del BFS, lo agregamos a la lista de hijos
                        self.hijos.append(mensajero)
                    self.mensajes_esperados = self.mensajes_esperados - 1
                    # Si ya recibimos todos los mensajes, enviamos el mensaje BACK a nuestro padre
                    if self.mensajes_esperados == 0:
                        if self.padre != self.id_nodo:  # Si no somos la raíz, enviamos el mensaje a nuestro padre
                            self.canal_salida.envia(
                                [self.id_nodo, 'BACK()', ['yes', self.distancia]], [self.padre])
                        else:  # Si somos la raíz, terminamos el algoritmo
                            print('BFS terminado.')
                            break
