import simpy
from Canales.Canal import Canal

class CanalBroadcast(Canal):
    '''
    Clase que modela un canal de comunicación tipo "broadcast".
    Permite enviar mensajes a múltiples destinos (one-to-many).
    
    Atributos:
        env: El entorno de SimPy donde se ejecutan los procesos.
        capacidad: La capacidad del canal (por defecto es infinita).
        canales: Lista que almacena los canales de entrada.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        '''
        Inicializa un canal broadcast.

        Args:
            env: El entorno de SimPy.
            capacidad: La capacidad del canal (opcional, por defecto es infinita).
        '''
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos): 
        '''
        Envía un mensaje a los canales de salida de los vecinos.

        Este método verifica los canales disponibles para los vecinos y
        envía el mensaje a cada uno de ellos.

        Args:
            mensaje: El mensaje que se enviará a los vecinos.
            vecinos: Una lista de índices que representan los vecinos
                      a los que se enviará el mensaje.

        Returns:
            SimPy event: Un evento que se completa cuando todos los
                         mensajes han sido enviados.
        '''
        # Lista con todos los canales de los vecinos que sí tenemos
        canales_disponibles = [self.canales[i] for i in range(len(self.canales)) if i in vecinos]

        eventos_msj = []

        # Envía un mensaje al canal de los vecinos
        for canal in canales_disponibles:
            eventos_msj.append(canal.put(mensaje))

        # El método termina en el momento en que todos los mensajes fueron enviados 
        return self.env.all_of(eventos_msj)

    def crea_canal_de_entrada(self):
        '''
        Crea un canal de entrada.

        Este método inicializa un nuevo canal de entrada y lo agrega a la lista
        de canales.

        Returns:
            simpy.Store: El canal de entrada creado.
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
