# calculo_caminos
En este repositorio he subido una serie de scripts que se permiten representar esquemáticamente una red, escoger un origen y destino y calcular cuál será el camino de menor coste. El programa presenta todos estos datos de manera visual y a través de una interfaz amigable con el usuario. Los datos de la red que lee el programa han tenido que ser almacenados previamente en un csv en forma de matriz de costes.
## Funcionamiento y manejo
El programa se inicia desde el script de python ```interfaz_grafica.py```. Un vez ejecutado, aparece una interfaz que permite introducir origen, destino y con 2 botones, uno para seleccionar el archivo donde el programa mirará los datos de la red y otro para calcular el camino más corto en base a la red escogida.

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/interfaz_inicio.png" width="25%" height="25%">

La red que coge el programa está almacenada en un fichero llamado ```red.csv``` en el mismo directorio que el programa con el formato de matriz y separador ```;```

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/archivo_csv.png" width="65%" height="65%">

Esta estructura representa los links o enlaces entre los diferentes nodos de la red, siendo siempre valores positivos o nulos en caso de no estar enlazados. Se considera que las redes son *bidireccionales*, es decir, el coste de ir de un nodo A a B es el mismo que el de ir de B a A. Esto hace que la matriz de pesos del csv deba ser simétrica. De no serlo, el programa lo advierte.

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/warning_csv_seleccionado.png" width="40%" height="40%">

Una vez introducida la matriz adecuada se representará la red con el coste de los enlaces

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/interfaz_red_seleccionada.png" width="50%" height="50%">

Llegados a este punto ya es posible indicar origen y destino y seleccionar ```Calcular``` para conocer cuál es el camino de menor coste. El programa está pensado para que ```origen, destino > N = # nodos red``` y no haya problemas en el resto del código:

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/warning_origen_destino.png" width="50%" height="50%">
<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/warning_origen_destino_iguales.png" width="50%" height="50%">

A continuación el programa muestra en el diagrama de red con el origen, destino y ruta de menor coste destacadas, así como cuánto es el coste:

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/interfaz_camino_calculado.png" width="50%" height="50%">

Es posible volver a repetir la operación con otros origenes y destino o incluso pedir de nuevo la red o cambiarla en caso de modificar ```red.csv``` para continuar trabajando.

## Estructura

El programa está contenido en 3 elementos:
* ```interfaz_grafica.py``` es el script de python encargado de generar la interfaz, coger datos del ```*.csv``` y llamar al programa escrito en C
* ```calculo_camino_interfaz.c``` es un script de C a partir del cual se genera el ```*.exe``` utilizado por ```interfaz_grafica.py```. Se encarga de realizar el cálculo del camino de menor coste teniendo como inputs origen, destino y la red.
* ```red.csv``` es el fichero donde se almacena la información de la red que utilizan los scripts anteriores. Como se comentó previamente, la matriz representa a una red bidireccional (simétrica) donde el elemento ```a(i,j)``` indica el peso o coste del enlace que une el nodo i con el j.

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/red_matriz.png" width="50%" height="50%">

### Programa en C

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/esquema_c.png" width="50%" height="50%">

El programa en C utiliza el *algoritmo de Dijkstra* para obtener la ruta de menor coste. Está estructurado en funciones que o bien realizan una construcción de variables, condiciones iniciales y reserva dinámica de memoria; o implementar el algoritmo. Como resultado se obtiene el coste total de la ruta, los nodos que forman la ruta ordenados desde destino a origen:

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/programa_c.png" width="50%" height="50%">

### Programa en python

<img src="https://github.com/Lba-29/calculo_caminos/blob/main/imagenes_readme/esquema_interfaz.png" width="50%" height="50%">

El script principal esta estructurado como una clase. En ```__init__``` indico todos los elementos que tiene la interfaz (etiquetas, botones, etc) utilizando librería ```tkinter```. Cuando el usuario interacciona con ellos, será cuando se ejecutan algunos métodos de este objeto que harán cambios en la interfaz, tal y como intenta indicarse en el esquema superior.

Para dibujar la red he utilizado la librería ```networkx``` por su facilidad para representar redes y consiguiendo un aspecto agradable. Para insertar los diagramas de red en la interfaz ```tkinter``` es necesaria además la librería ```matplotlib```. Para abrir y tratar los datos de ```red.csv``` lo más cómodo para mi ha sido usar un dataframe de la librería ```pandas```. Finalmente para llamar a un ejecutable de C desde python he usado la librería ```subprocess```.

## Siguientes pasos

Como pasos a mejorar estaría el conseguir una interfaz más lograda, poder manejar el caso de redes no bidireccionales (que el coste del link A->B sea distinto B->A y eso pasa por quitar la restricción de matriz simétrica), la posibilidad de añadir *constraints* (que el usuario pueda bloquear nodos, modificar coste de los links en función de parámetros tales como ocupación o número de saltos, etc)

Adicionalmente, es posible que el código presente algún fallo, o sea posible simplificarlo y hacerlo más legible y/o rápido. En ese caso feel free to change it.

## Referencias

Entorno e IDE utilizados:
* Python 3.7.4
* IPython 7.8.0 -- An enhanced Interactive Python.
* Spyder 3.3.6 
* Code::Blocks 20.03 (20.03-r11983)
* Windows 8.1

Sin toda esta inforamción encontrada en la web, no hubiese sido capaz de realizar este trabajo:
* https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra
* https://stackoverflow.com/questions/7021725/how-to-convert-a-string-to-integer-in-c
* https://realpython.com/python-subprocess/
* https://www.quora.com/How-can-you-create-a-Python-script-that-executes-C-programs-like-an-exe-file
* https://stackoverflow.com/questions/47676319/how-to-create-a-tkinter-error-message-box
* https://stackoverflow.com/questions/8269096/why-is-button-parameter-command-executed-when-declared
* https://towardsdatascience.com/graph-visualisation-basics-with-python-part-ii-directed-graph-with-networkx-5c1cd5564daa
* https://networkx.org/documentation/stable/tutorial.html#examining-elements-of-a-graph
* https://stackoverflow.com/questions/48235215/how-to-create-a-directed-networkx-graph-from-a-pandas-adjacency-matrix-dataframe
* https://datatofish.com/matplotlib-charts-tkinter-gui/
* https://stackoverflow.com/questions/59001195/how-to-update-a-graph-created-by-matplotlib-in-tkinter
