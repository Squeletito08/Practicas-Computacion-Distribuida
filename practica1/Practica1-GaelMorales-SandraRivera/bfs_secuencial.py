import queue

class GraficaIncorrecta(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class Grafica:
    """
    Clase que implementa la estructura de datos gŕafica
    Una gráfica tiene nodos, número de nodos, aristas y número de aristas
    """

    def __init__(self, grafica=None):
        """
        Constructor de la clase gráfica
        
        Parametros:
        - una gráfica o None
        """

        if grafica is None: 

            try: 
                self.numNodos = int(input("Introduce el número de nodos: "))
                if self.numNodos <= 0:
                    raise GraficaIncorrecta("Número de nodos incorrectos")
            except ValueError as e: 
                raise ValueError("Número de nodos incorrectos")

            max_aristas = (self.numNodos * (self.numNodos - 1)) // 2
            
            try: 
                self.numAristas = int(input("Introduce el número de aristas: "))
                if self.numAristas < 0 or self.numAristas > max_aristas:
                    raise GraficaIncorrecta("Número de aristas incorrectas")
            except ValueError as e:
                raise ValueError("Número de aristas incorrectas")

            self.nodos = self._pedir_nodos()
            self.adyacencias = self._pedir_aristas()
        else:
            self.nodos = {nodo: False for nodo in grafica.keys()}
            self.adyacencias = grafica

    def _pedir_nodos(self):
        """
        Pide al usuario por entrada estandar los nodos que tendrá la gráfica 
        """
        print("Introduce los nodos separados por espacios: ")
        nodos = input().split()  
        if len(nodos) != self.numNodos:
            raise GraficaIncorrecta(f"Se esperaban {self.numNodos} nodos")
        nodos_dict = {nodo: False for nodo in nodos}  
        return nodos_dict

    def _pedir_aristas(self):
        """
        Pide al usuario por entrada estandar las aristas entre los nodos
        """
        print("Introduce las aristas en formato 'x y': ")
        adyacencias = {nodo: [] for nodo in self.nodos}

        for i in range(self.numAristas):
            arista = input().split()
            if len(arista) != 2:
                raise GraficaIncorrecta("El formato de la arista debe ser 'x y'")
            v, u = arista
            
            if v not in self.nodos:
                raise GraficaIncorrecta(f"El nodo {v} no está en la gráfica")

            if u not in self.nodos:
                raise GraficaIncorrecta(f"El nodo {u} no está en la gráfica")

            if (v == u):
                raise GraficaIncorrecta("No se permiten lazos en la gŕafica")

            if u not in adyacencias[v]:
                adyacencias[v].append(u)
            if v not in adyacencias[u]:
                adyacencias[u].append(v)

        return adyacencias

    def bfs(self, v):
        """
        Implementación de BFS para gráficas 

        Parametros:
        - un nodo cualquiera de la gráfica

        Regresa:
        - una lista con el recorrido de BFS
        """

        if v not in self.nodos:
            raise GraficaIncorrecta(f"El nodo {v} no está en la gráfica")

        recorrido = []  

        cola = queue.Queue()  
        self.nodos[v] = True  

        cola.put(v) 

        while not cola.empty():
            v = cola.get() 
            recorrido.append(v)

            for vecino in self.adyacencias[v]:
                if not self.nodos[vecino]:
                    cola.put(vecino)  
                    self.nodos[vecino] = True 

        for u in self.nodos:
            self.nodos[u] = False

        return recorrido

    def es_conexa(self):
        """
        Indica si la gráfica es conexa

        Regresa:
        - True si la gráfica es conexa y False en otro caso
        """

        nodo_inicio = next(iter(self.nodos)) 
        recorrido = self.bfs(nodo_inicio)
        return len(recorrido) == len(self.nodos)


def mostrar_menu():
    print("\nMenú:")
    print("1. Ejecutar con la gráfica predeterminada")
    print("2. Introducir tu propia gráfica")
    print("3. Ejecutar BFS sobre la gráfica")
    print("4. Salir")

def ejecutar_opcion(opcion, grafica=None):
    g = grafica
    inicio = None

    if opcion == '1':
        grafica_predeterminada = {
            'A': ['B', 'C', 'D', 'E'],
            'B': ['A', 'C', 'G'],
            'C': ['A', 'B', 'D'],
            'D': ['H', 'E', 'A', 'C'],
            'E': ['A', 'D', 'F'],
            'F': ['G', 'E', 'H', 'I'],
            'G': ['F', 'B'],
            'H': ['F', 'D'],
            'I': ['F']
        }
        try:
            g = Grafica(grafica_predeterminada)
            inicio = 'A'
            if not g.es_conexa():
                raise GraficaIncorrecta("La gráfica dada no es conexa")
        except GraficaIncorrecta as e:
            print("Error: ", e)
            return None

    elif opcion == '2':
        try: 
            g = Grafica()
            if not g.es_conexa():
                raise GraficaIncorrecta("La gráfica dada no es conexa")
            inicio = input("Introduce el nodo inicial para BFS: ")
        except GraficaIncorrecta as e:
            print("Error: ", e)
            return None

    elif opcion == '3':
        try:
            if g is None:
                raise GraficaIncorrecta("Aún no se ha introducido ninguna gráfica")
            inicio = input("Introduce el nodo inicial para BFS: ")
        except GraficaIncorrecta as e:
            print("Error:", e)
            return None

    else:
        print("Opción no válida")
        raise ValueError("La opción seleccionada no es válida. Debe ser 1, 2, 3 o 4.")
        return None
    
    try:
        recorrido_bfs = g.bfs(inicio)
        print(f"Recorrido BFS empezando desde el nodo {inicio}:", recorrido_bfs)
        return g
    except GraficaIncorrecta as e:
        print("Error:", e)

def main():
    g = None
    while True:
        mostrar_menu()
        try:
            opcion = input("Selecciona una opción: ")
            if opcion == '4':
                break
            g = ejecutar_opcion(opcion, g)
        except ValueError as e:
            print(e)  
        except GraficaIncorrecta as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
