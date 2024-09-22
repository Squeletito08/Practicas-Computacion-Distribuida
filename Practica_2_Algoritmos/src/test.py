from Canales.CanalBroadcast import *
from NodoBroadcast import *
# from NodoGenerador import *
from NodoVecinos import *
from NodoConvergecast import *

# Las unidades de tiempo que les daremos a las pruebas
TIEMPO_DE_EJECUCION = 50


class TestPractica1:
    ''' Clase para las pruebas unitarias de la práctica 1. '''
    # Las aristas de adyacencias de la gráfica.
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]

    # Aristas de adyacencias del árbol
    adyacencias_arbol = [[1, 2], [3], [5], [4], [], []]

    # Prueba para el algoritmo de conocer a los vecinos de vecinos.
    def test_ejercicio_uno(self):
        ''' Método que prueba el algoritmo de conocer a los vecinos de vecinos. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoVecinos(i, self.adyacencias[i],
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.conoceVecinos(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Ahora si, probamos
        identifiers_esperados = [[0, 3, 5], [1, 2, 4],
                                 [1, 2, 4], [0, 3, 5], [1, 2, 4], [0, 3, 5]]
        # Para cada nodo verificamos que su lista de identifiers sea la esperada.
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            assert set(identifiers_esperados[i]) == set(
                nodo.identifiers), ('El nodo %d está mal' % nodo.id_nodo)

    # # Prueba para el algoritmo que construye un árbol generador.
    # def test_ejercicio_dos(self):
    #     ''' Prueba para el algoritmo que construye un árbol generador. '''
    #     # Creamos el ambiente y el objeto Canal
    #     env = simpy.Environment()
    #     bc_pipe = CanalBroadcast(env)

    #     # La lista que representa la gráfica
    #     grafica = []

    #     # Creamos los nodos
    #     for i in range(0, len(self.adyacencias)):
    #         grafica.append(NodoGenerador(i, self.adyacencias[i],
    #                                      bc_pipe.crea_canal_de_entrada(), bc_pipe))

    #     # Le decimos al ambiente lo que va a procesar ...
    #     for nodo in grafica:
    #         env.process(nodo.genera_arbol(env))
    #     # ...y lo corremos
    #     env.run(until=TIEMPO_DE_EJECUCION)

    #     # Y probamos que los padres y los hijos sean los correctos.
    #     padres = [0, 0, 0, 1, 3, 2]
    #     hijos = [[1, 2], [3], [5], [4], [], []]
    #     for i in range(0, len(grafica)):
    #         nodo = grafica[i]
    #         assert nodo.padre == padres[i], (
    #             'El nodo %d tiene un padre erróneo' % nodo.id_nodo)
    #         assert set(nodo.hijos) == set(hijos[i]), ('El nodo %d no tiene a los hijos correctos'
    #                                                   % nodo.id_nodo)

    # Prueba para el algoritmo de Broadcast.
    def test_ejercicio_tres(self):
        ''' Prueba para el algoritmo de Broadcast. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)
        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
       
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoBroadcast(i, self.adyacencias_arbol[i],
                                         bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.broadcast(env))
        # ...y lo corremos
    
        env.run(until=TIEMPO_DE_EJECUCION)

        # Probamos que todos los nodos tengan ya el mensaje
        mensaje_enviado = grafica[0].mensaje
        for nodo in grafica:
           
            assert mensaje_enviado == nodo.mensaje, (  
                'El nodo %d no tiene el mensaje correcto' % nodo.id_nodo) 

    # Prueba para el algoritmo de Convergecast en la raíz.
    def test1_ejercicio_cuatro(self):
        ''' Prueba para el algoritmo de Convergecast en la raíz. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalConvergecast(env)
        # La lista que representa la gráfica
        grafica = []
        
        # Padres de cada nodo
        padres_arbol = [0, 0, 0, 1, 3, 2]

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoConvergecast(i, self.adyacencias_arbol[i],
                                         bc_pipe.crea_canal_de_entrada(), bc_pipe, padres_arbol[i]))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.convergecast(env))
        # ...y lo corremos
    
        env.run(until=TIEMPO_DE_EJECUCION)

        # Probamos que la raíz tenga todos los mensajes        
        mensaje_enviado = grafica[0].datos_recibidos

        for nodo in grafica:
            assert "["+ str(nodo.id_nodo) +", "+ str(nodo.mensaje) +"]" in mensaje_enviado, (  
                'El nodo 0 no tiene el mensaje del nodo %d' % nodo.id_nodo)

    # Prueba para el algoritmo de Convergecast en cada nodo.
    def test2_ejercicio_cuatro(self):
        ''' Prueba para el algoritmo de Convergecast en cada nodo. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalConvergecast(env)
        # La lista que representa la gráfica
        grafica = []
        
        # Nuevo árbol
        adyacencias_arbol = [[1, 2], [3], [5], [4, 6], [], [], []]
        padres_arbol = [0, 0, 0, 1, 3, 2, 3]

        # Creamos los nodos
        for i in range(0, len(adyacencias_arbol)):
            grafica.append(NodoConvergecast(i, adyacencias_arbol[i],
                                         bc_pipe.crea_canal_de_entrada(), bc_pipe, padres_arbol[i]))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.convergecast(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Probamos que todos los nodos tengan bien convergecast. 
        resultado = [
            "[5, None][2, None][0, None][4, None][3, None][1, None][6, None]",
            "[4, None][3, None][1, None][6, None]",
            "[5, None][2, None]",
            "[4, None][3, None][6, None]",
            "[4, None]",
            "[5, None]",
            "[6, None]"
        ]

        for i in range(0, len(adyacencias_arbol)):
            assert grafica[i].datos_recibidos == resultado[i], (  
                'El nodo %d no tiene todos los mensajes' % i)