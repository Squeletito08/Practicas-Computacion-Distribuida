import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

 #Funcion auxiliar buscar el menor 
def menor_numero(lista):
        if len(lista) == 0:
            return None  # Si la lista está vacía, no hay un menor número
        
        menor = lista[0]  # Inicializamos el menor con el primer número de la lista
        for numero in lista:
            if numero < menor:
                menor = numero  # Actualizamos el menor si encontramos un número más pequeño
            return menor


#Funcion auxiliar para eliminar una lista de otro lista
def eliminar_elementos(lista_principal, elementos_a_eliminar):
    for elemento in elementos_a_eliminar:
        while elemento in lista_principal:
            lista_principal.remove(elemento)  # Elimina todas las apariciones del elemento
    return lista_principal



class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra:
        self.hijos = []
        self.padre = -1
        self.distancia = -1
        self.visitados=[]
        

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        yield env.timeout(TICK)

        if self.id_nodo == 0:
            #Avisa a todos los vecinos que el ya fue visitado (mandando VISITED()) 
            self.canal_salida.envia([self.id_nodo,'VISITED'],self.vecinos)
            self.padre=self.id_nodo
                
            #Tomar el menor de sus vecinos 
            vecino_menor= menor_numero(self.vecinos)
            #Agregarlo como hijo 
            self.hijos.append(vecino_menor)
            self.canal_salida.envia([self.id_nodo,'GO()'], [vecino_menor])

        while True: 
            mensaje=yield self.canal_entrada.get()
            mensajero=mensaje[0]
            tipo_mensaje=mensaje[1]

            if 'GO' in tipo_mensaje:
        
                self.padre=mensajero
                self.hijos=[]
                #convierto las listas en conjuntos ,porque si el orden es diferente , ya no la misma lista
                conjunto1=set(self.vecinos)
                conjunto2=set(self.visitados)
                if (conjunto1==conjunto2):
                 
                    self.canal_salida.envia([self.id_nodo,'VISITED'],self.vecinos)
                    # yield env.timeout(TICK*2)
                    self.canal_salida.envia([self.id_nodo,'BACK'], [mensajero])

                else : 
                    #Busca al menor en los no visitados
                    aux = self.vecinos.copy()
                    aux1=eliminar_elementos(aux,self.visitados)
                    vecino_menor=menor_numero(aux1)
        
                    self.hijos.append(vecino_menor)
                    self.canal_salida.envia([self.id_nodo,'VISITED'],self.vecinos)
                    # yield env.timeout(TICK)
                    self.canal_salida.envia([self.id_nodo,'GO()'], [vecino_menor])

            if 'BACK' in tipo_mensaje:
              
                conjunto1=set(self.vecinos)
                conjunto2=set(self.visitados)
                if (conjunto1==conjunto2):
    
                    if self.padre==self.id_nodo:
                        print("Ha terminado el proceso ")
                        break
                    else : 
                        #si no es la raiz entonces regresar a nodo padre
                        self.canal_salida.envia([self.id_nodo,'BACK()'], [self.padre])
                else :
                  
                    aux = self.vecinos.copy()
                    aux1=eliminar_elementos(aux,self.visitados)
                    vecino_menor=menor_numero(aux1)
                  
                    self.hijos.append(vecino_menor)
                    self.canal_salida.envia([self.id_nodo,'VISITED'],self.vecinos)
                    # yield env.timeout(TICK)

                    self.canal_salida.envia([self.id_nodo,'GO()'], [vecino_menor])

            # si entra en este caso  en mensajero es guardado como visitado en la lista local
            # del nodo , para tener un control de a que nodo , seguir mandando mensajes
            if 'VISITED' in tipo_mensaje:
                if mensajero not in self.visitados:
                    self.visitados.append (mensajero)
        






            


    
