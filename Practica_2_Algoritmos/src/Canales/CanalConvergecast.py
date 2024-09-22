import simpy
from Canales.Canal import Canal


class CanalConvergecast(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-one.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecino):
        '''
        Envia un mensaje al canal de salida de un vecino.
        '''
        if hasattr(vecino, 'recibe'):
            vecino.recibe.put(mensaje)
        else:
            # Obtiene el canal de salida del vecino  y pone el mensaje
            canal_salida = self.canales[vecino]
            if canal_salida:
                canal_salida.put(mensaje)
        
    def crea_canal_de_entrada(self):
        '''
        Creamos un canal de entrada
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
