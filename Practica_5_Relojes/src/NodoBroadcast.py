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
        Algoritmo de Broadcast con reloj de Lamport.

        Este método implementa el algoritmo de broadcast, permitiendo que un nodo envíe un mensaje 
        a todos los demás nodos en la red, y utiliza el reloj de Lamport para llevar un control 
        del orden de los eventos.

        Desde el nodo distinguido (id_nodo == 0), se envía un mensaje inicial a todos sus vecinos.
        Cuando cualquier nodo recibe un mensaje, actualiza su reloj de acuerdo al reloj de Lamport 
        y retransmite el mensaje a todos sus vecinos excepto al nodo del cual recibió el mensaje.

        Args:
            env: El entorno de SimPy donde se ejecuta el proceso de simulación.
            data: El mensaje inicial que se enviará a través de la red (es nuestro caso es "m" como ejemplo).

        Notas:
            - El reloj de Lamport se actualiza en cada evento local de acuerdo a la lógica del 
            algoritmo de relojes de Lamport, garantizando que cada evento tenga una marca temporal 
            secuencialmente consistente en el sistema distribuido.
        '''
    
        # Si el nodo es distinguido (id_nodo == 0), envía el mensaje inicial a todos sus vecinos
        if self.id_nodo == 0:
            self.mensaje = data 
            yield env.timeout(randint(1, 5))  # Espera un tiempo aleatorio simulado antes de enviar
            
            for vecino in self.vecinos:
                self.reloj += 1  # Incrementa el reloj de Lamport antes de cada envío
                # Registra el evento de envío en la lista de eventos
                self.eventos.append([self.reloj, 'E', data, self.id_nodo, vecino])
            
            # Enviar el mensaje a todos los vecinos mediante el canal de salida
            self.canal_salida.envia((data, self.reloj, self.id_nodo), self.vecinos)
                    
        # Bucle infinito para recibir y retransmitir mensajes
        while True:
            yield env.timeout(randint(1, 5))  # Simula un tiempo de espera aleatorio para recibir
            
            # Espera un mensaje en el canal de entrada; se recibe el contenido del mensaje,
            # el valor del reloj remoto, y el ID del nodo remitente
            data, reloj, j = yield self.canal_entrada.get()
            
            self.mensaje = data 

            # Actualiza el reloj de Lamport tomando el máximo entre el reloj actual y el remoto,
            # y luego lo incrementa en 1 para reflejar el evento de recepción
            self.reloj = max(self.reloj, reloj) + 1

            # Registra el evento de recepción en la lista de eventos
            self.eventos.append([self.reloj, 'R', data, j, self.id_nodo])
            
            yield env.timeout(randint(1, 5))  # Simula un tiempo de espera aleatorio antes de retransmitir
            
            # Filtra la lista de vecinos para excluir el nodo que envió el mensaje (j)
            vecinos_sin_j = [vecino for vecino in self.vecinos if vecino != j]
            
            for vecino in vecinos_sin_j:
                self.reloj += 1  # Incrementa el reloj de Lamport antes de cada envío
                # Registra el evento de envío en la lista de eventos
                self.eventos.append([self.reloj, 'E', data, self.id_nodo, vecino])

            # Envía el mensaje a los vecinos filtrados mediante el canal de salida
            self.canal_salida.envia((data, self.reloj, self.id_nodo), vecinos_sin_j)
                    
            yield env.timeout(randint(1, 5))  # Simula un tiempo de espera antes del próximo ciclo de recepción