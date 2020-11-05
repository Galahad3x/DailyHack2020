# BiblioCAT :books:

## Introducción
Los libros nos permiten descubrir mundos de fantasía así como entender mejor el mundo en el que vivimos. Nos permiten aprender todo tipo de cosas, desde "Teo va a la escuela" a "Compilers: Principles, Techniques, and Tools".


Las librerías de Cataluña tienen un sistema de intercanvio de libros, de forma que, cuando alguien se dirige a una biblioteca a buscar un libro para aprender a programar Haskell, y el/la bibliotecario/a le diga "Y eso qué es?!?!?", haya la posibilidad de pedirle a otra biblioteca que tenga el libro que el/la valiente aspirante a aprender Haskell pedía.


## Especificaciones
* Lo que les gustaría a las bibliotecas es maximizar el tiempo en que los libros están generando valor, es decir, el tiempo en que un libro está en manos de algún usuario. **Cada libro genera un valor X. Se tendrá maximizar teniendo en cuenta el tiempo máximo T**
* Hay de tener en cuenta, que mientras un libro está siendo transportado este **NO** genera valor. 
* Dependiendo del lector, y el libro que vaya a leer (en función de si le gusta más o menos), variará el **tiempo  en que se lee el libro**.
* Si hay varias personas que quieren leer un libro, estas se añadirán a una lista de espera, y esperarán a recibir noticias de la biblioteca cuando esté disponible.
* Una persona, como máximo, podrá tener tres libros a la vez. **OJO: NO tres libros por biblioteca, tres libros en TOTAL**. 


## Input File
``` 
tiempo = "T", tiempo_total
biblioteca = "L", id, { % { tiempo transporte id j | j <- [ 0 .. id_max] }  % }
id = % numero unico por tipo %
tiempo transporte id j = % tiempo de tranporte de un libro desde la
              - libreria id hasta j
              %
libro = "B", id, id biblioteca, valor
valor = % numero %
lector = "R", id, id biblioteca, { id libro, tiempo lectura }
tiempo lectura = % numero de tiempo que se
                 - tarda en leer el libro id libro
                 %
```

Por ejemplo:
```
T 6
L 0 0 2 3
L 1 3 0 4
L 2 3 4 0
B 0 0 5
B 1 0 3
B 2 1 10
B 3 2 2
B 4 2 8
R 0 0 0 10 1 2
R 1 0 1 1 2 10 3 3
R 2 1 0 1 1 1 2 1 3 1 4 1
R 3 2 2 5 4 5
```

Vemos que el valor del tiempo T en el que se ha de realizar la optimización es de 6.

En este ejemplo, hay tres bibliotecas (L), donde el coste de llevar un libro
de la biblioteca ''0'' hasta la ''1'' es de 2 y el coste de llevar
un libro de la biblioteca ''1'' hasta la ''0'' es de 3. Además, el coste de
llevar un libro de una biblioteca a sí misma siempre es de 0.


En el caso de los libros (B),  el primer argumento es el id del libro, 
el segundo es el id de la biblioteca donde se encuentra
en el estado inicial, y el tercero es el valor que produce el libro en
ser leído por un lector.


Finalmente, se puede apreciar que el lector con id ''0'', que esta afiliado
a la biblioteca ''0'', quiere leer los libros ''0'' y ''1'', que tardará en
hacerlo ''10'' y ''2'' respectivamente.

## Output File
### Gramática:
```
mover libro = id libro, "m", id biblioteca
leer libro = id libro, "r", id lector
```


El orden de sentencias en el fichero importa.
Por ejemplo, dado el fichero inicial:
```
T 10
L 0 0
B 0 0 5
B 1 0 5
B 2 0 5
B 3 0 5
R 0 0 0 5 1 5 2 5 3 10
```

Con el output:
```
0 r 0
1 r 0
2 r 0
3 r 0
```

Generará un valor de 15 puntos, pues el último
libro se lee fuera del tiempo establecido (10).
Este se leerá a partir del día 5 (empezando en 0),
pues los 5 primeros está ya leyendo 3 libros.


Mientras, este fichero:

```
0 r 0
3 r 0
1 r 0
2 r 0
```

Generará 20 puntos, pues todos los libros son leídos
dentro del terminio.


Sigamos con otro ejemplo:
```
T 10
L 0 0
B 0 0 5
B 1 0 5
B 2 0 5
B 3 0 5
B 4 0 5
R 0 0 0 5 1 5 2 5 3 10 4 3
R 1 0 4 3
```

Entonces, este fichero:
```
0 r 0
1 r 0
2 r 0
4 r 0
4 r 1
```
Generará 15 puntos, ya que:
+ El lector 0 tiene los 5 primeros días ocupados.
+ El libro 4 está hasta el octavo día ocupado, los
   5 primeros sin hacer nada, y del $[5, 8)$ está
   siendo leído por el lector 1
+ El libro 4 se empieza a leer del 8º día hasta el 11º.

Mientras, el siguiente output:
```
0 r 0
1 r 0
2 r 0
4 r 1
4 r 0
```
Generará 20 puntos, pues el libro 4 es leído por dos
lectores.


## Benchmarks
Se pueden descargar las benchmarks en: https://mega.nz/file/DrxQBRKA#9CHHhBS6kiYAswzbK0ZWWgpGNVmJh-RRycRrNDMpzEA


El zip es un poco gordo, al generar las benchmarks generamos una bastante grande (16 GB de benchmark) y después de todo el esfuerzo 
que hizo nuestro pc nos parecía feo no ponerla. A ver qué podéis hacer con ella. :wink:

## Entrega y Evaluación
Para hacer valida vuestra participación nos tendréis que entregar el output de vuestro programa con el formato correcto descrito en el apartado anterior. Para comprobar la score de vuestra solución, podéis descargaros y ejecutar el programa que utilizaremos para determinar vuestra score. 
La suma de las scores que saquéis en cada una de las bencharks será el resultado final y el valor que determinará el ganador.


# Creadores del reto
+ [quimpm](https://github.com/quimpm) :panda_face:
+ [sergisi](https://github.com/sergisi/) :earth_africa:

