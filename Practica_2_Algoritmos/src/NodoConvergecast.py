from Nodo import *
from Canales.CanalConvergecast import *

# Demora un tiempo para ejemplificar el costo de los pasos que se realizan 
TICK = 1


class NodoConvergecast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Convergecast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, padre, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.padre = padre
        self.datos_recibidos = ""
        self.propio_mandado = False

    def convergecast(self, env):
        ''' Algoritmo de Convergecast. Comenzando por las hojas, 
        mandamos los mensajes que recibimos y el propio al padre.'''
        # Si el nodo es hoja
        if (len(self.vecinos)==0):
            self.datos_recibidos = "["+ str(self.id_nodo) +", "+ str(self.mensaje) +"]"
            # Mandar mensaje propio al padre
            self.canal_salida.envia('BACK({})'.format(self.datos_recibidos), self.padre)
            self.propio_mandado = True
            yield env.timeout(TICK)
        
        # Si el nodo recibe un mensaje de un hijo
        while True:
            salida = yield self.canal_entrada.get()
            if salida.startswith('BACK'):
                # Extraemos el mensaje para mandarlo al siguiente
                salida = salida[salida.index('(') + 1: salida.index(')')]
                # Agregamos el mensaje propio si no lo mandamos antes
                if not self.propio_mandado:
                    salida += "["+ str(self.id_nodo) +", "+ str(self.mensaje) +"]"
                    self.propio_mandado = True
                # Guardar todos los datos que le han llegado al nodo actual
                self.datos_recibidos += salida
                # Mandar mensaje al padre
                if(self.id_nodo != 0):
                    self.canal_salida.envia('BACK({})'.format(salida), self.padre)
                    yield env.timeout(TICK)
