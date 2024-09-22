Cervantes Duarte Jose Fernando   422100827
Rivera Lara Sandra Valeria   320039823


FUNCIONAMIENTO DE CONVERGECAST

Al NodoConvergecast se le agregaron los atributos de "padre" para saber a quien mandarle el mensaje, "datos_recibidos" para almacenar el la información del nodo y los datos mandados por sus hijos, "propio_mandado" para saber si el nodo ya mandó al padre su propio dato y así no repetir información.

En el algoritmo convergecast se van a mandar mensajes entre nodos dentro de BACK() y a través de CanalConvergecast. Primero las hojas guardan su propio mensaje asociado a su id en una cadena de la forma [id, mensaje], para después enviar eso a su padre. Ahora, cuando un nodo que no es hoja reciba datos de sus hijos, este los guarda y los manda a su padre. Asimismo, guarda una vez su propio mensaje asociado a su id y lo manda una sola vez a su padre. De esta forma, cada nodo realiza convergecast correctamente, guardándose las duplas que debería de tener cada uno en la cadena "datos_recibidos".

EJECUCIÓN DE CONVERGECAST

Además de los datos que se piden en NodoBroadcast, vamos a solicitar el padre de cada nodo en el método constructor. Nótese que para el nodo distinguido, su padre es él mismo.

Tras ejecutar convergecast en los nodos, se guardarán los datos que debería tener un nodo en su atributo "datos_recibidos". Se agregaron dos pruebas, la primera verifica que la raíz recibió la dupla [id, mensaje] de todos los nodos del árbol propuesto para los tests anteriores. El segundo test verifica con un árbol diferente que cada nodo guardó correctamente todas las duplas que debería de tener al ejecutar convergecast.

