import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint


# El tiempo de retardo puede variar entre esos 2 valores 
A= 1
B=1000


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


#Funcion auxiliar para escoger la lista con los valores mas grandes // la ocupo para los relojes 
def escoger_lista_mayor(lista1, lista2):
    # Limitar la comparación a la longitud mínima de ambas listas
    longitud_minima = min(len(lista1), len(lista2))
    sublista1 = lista1[:longitud_minima]
    sublista2 = lista2[:longitud_minima]
    
    # Comprobar si todos los elementos de sublista1 son mayores que los de sublista2
    if all(x > y for x, y in zip(sublista1, sublista2)):
        return lista1
    # Comprobar si todos los elementos de sublista2 son mayores que los de sublista1
    elif all(y > x for x, y in zip(sublista1, sublista2)):
        return lista2
    # En caso de empate (ninguna lista es completamente mayor), elige la que tenga el máximo más alto
    else:
        if max(lista1) > max(lista2):
            return lista1
        elif max(lista2) > max(lista1):
            return lista2
        else:
            # Si ambas tienen el mismo valor máximo, devuelve cualquiera de las dos (en este caso, lista1)
            return lista1




class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, num_nodos):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = self.id_nodo
        self.hijos = []
        self.eventos = []
        self.reloj = [0] * num_nodos
        self.visitados=[]
    

    def dfs(self, env):
     
        ''' Algoritmo DFS. '''

        if self.id_nodo == 0:

         
            self.padre=self.id_nodo
            self.visitados.append(self.id_nodo)
            #Tomar el menor de sus vecinos 
            vecino_menor= menor_numero(self.vecinos)
            #Agregarlo como hijo 
            self.hijos.append(vecino_menor)
            self.reloj[self.id_nodo] +=1
            #Se manda un copy porque si no se pasa la referencia y todos los relojes valdrian lo mismo
            #En la entrada 2 de eventos mando string por problemas en el test porque listas no pueden ser llave en un diccionario
            self.eventos.append([self.reloj.copy(),'E','[0]',self.id_nodo,vecino_menor])
            self.canal_salida.envia([self.id_nodo,'GO()',self.visitados,self.reloj], [vecino_menor])
         


        while True: 
            #Recibe el mensaje y espera un momento
            mensaje=yield self.canal_entrada.get()
            valor=randint(A,B )
            yield env.timeout(valor)

            #Desglosa el mensaje
            mensajero=mensaje[0]
            tipo_mensaje=mensaje[1]
            conjunto_visitados=mensaje[2]
            reloj=mensaje[3]

            #Sincronizar relojes e incrementar 
            self.reloj=escoger_lista_mayor(reloj,self.reloj)
            self.reloj[self.id_nodo] +=1
            #Cuando recibe , en los eventos hay que poner el nodo que mando es decir el mensajero , para poder comparar los eventos despues 
            self.eventos.append([self.reloj.copy(),'R',str(conjunto_visitados),mensajero,self.id_nodo])


        

            if 'GO' in tipo_mensaje:


                 #Para actualizar la lista de visitados
                for elemento in conjunto_visitados:
                    if elemento not in self.visitados:
                        self.visitados.append(elemento)
                if self.id_nodo not in self.visitados:
                    self.visitados.append(self.id_nodo)


        
                self.padre=mensajero
                self.hijos=[]
               
                conjunto1=set(self.vecinos)
                conjunto2=set(self.visitados)
                #verifico que id_nodo no este en visitados ya , para no tener problemas despues
                if self.id_nodo not in self.visitados:
                    self.visitados.append(self.id_nodo)

                #<=  Verifica que todos los vecinos esten en visitados 
                if (conjunto1 <= conjunto2):
                   
                    self.reloj[self.id_nodo] +=1

                    self.eventos.append([self.reloj.copy(),'E',str(self.visitados),self.id_nodo,mensajero])
                    self.canal_salida.envia([self.id_nodo,'BACK',self.visitados,self.reloj], [mensajero])

                else : 
                    #Busca al menor en los no visitados
                    aux = self.vecinos.copy()
                    aux1=eliminar_elementos(aux,self.visitados)
                    vecino_menor=menor_numero(aux1)
                    self.hijos.append(vecino_menor)
                
                    self.reloj[self.id_nodo] +=1

        
                    self.eventos.append([self.reloj.copy(),'E',str(self.visitados),self.id_nodo,vecino_menor])
                    self.canal_salida.envia([self.id_nodo,'GO()',self.visitados,self.reloj], [vecino_menor])

            if 'BACK' in tipo_mensaje:
              
                #Para actualizar la lista de visitados , aqui ya no le agrego el id_nodo 
                for elemento in conjunto_visitados:
                    if elemento not in self.visitados:
                        self.visitados.append(elemento)

                conjunto1=set(self.vecinos)
                conjunto2=set(self.visitados)
                if (conjunto1 <= conjunto2):
    
                    if self.padre==self.id_nodo:
                        print("Ha terminado el proceso ")
                        break
                    else : 
                        #si no es la raiz entonces regresar a nodo padre
                        self.reloj[self.id_nodo] +=1
                        self.eventos.append([self.reloj.copy(),'E',str(self.visitados),self.id_nodo,self.padre])
                        self.canal_salida.envia([self.id_nodo,'BACK()',self.visitados,self.reloj], [self.padre])
                else :
                    #Escoge al menor de sus vecinos no visitados y manda GO
                    aux = self.vecinos.copy()
                    aux1=eliminar_elementos(aux,self.visitados)
                    vecino_menor=menor_numero(aux1)
                    self.hijos.append(vecino_menor)
                    
                    self.reloj[self.id_nodo] +=1
                
                    self.eventos.append([self.reloj.copy(),'E',str(self.visitados),self.id_nodo,vecino_menor])
                    self.canal_salida.envia([self.id_nodo,'GO()',self.visitados,self.reloj], [vecino_menor])

        
