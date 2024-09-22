import simpy
from Canales.Canal import Canal

#Demora un tiempo para ejemplificar el costo de los pasos que se realizan 
TICK = 1

class CanalBroadcast(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-many.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.
        '''
        for vecino in vecinos:
            
            if hasattr(vecino, 'recibe'):
                vecino.recibe.put(mensaje)
            else:
                #obtiene el canal de salida del vecino  y pone el mensaje
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
