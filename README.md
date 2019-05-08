README

El lenguaje de programación Dist es un lenguaje diseñado para el aprendizaje de funciones estadísticas básicas para alumnos de secundaria y preparatoria. Algunas de las funciones que permite el lenguaje son: 

Para poder utilizar Dist se debe de instalar:

Python 3
    - pandas
    - matplotlib
    - numpy
    - pandas
    - pickle

Antlr4 (Recuerda agregar las variables de ambiente de Antlr)

Para compilar se debe de correr en la terminal dentro de la carpeta del repositorio de Dist:
antlr4 -Dlanguage=Python3 dist.g4

python3 dist.py nombreDelArchivo.dist

python3 run_dist.py nombreDelPrograma.stv ("stv" es la extensión del código intermedio)

```
pow(a:float, val:float): Regresa la potencia ‘a’ del valor ‘val’.

sqrt(a:float, val:float): Regresa la raíz ‘a’ del valor ‘val’.

prob(arr[]:Int, val:int): arr es el arreglo de datos sobre el que se sacará la probabilidad del val.

moment(arr[]:int, num_moment:Int): arr[ ]:int es el arreglo de valores, num_moment es el número de momento que se calculará (desde 0 a 4) para una distribución normal.

var(arr[]:Int): arr es el arreglo de datos sobre el que se sacará la varianza de una distribución normal.

mode(arr[]:Int): arr es el arreglo de datos sobre el que se sacará la moda.

median(arr[]:Int): arr es el arreglo de datos sobre el que se sacará la mediana.

plot_histogram(arr[ ]:int ): arr es el arreglo de valores. Graficar un histograma de los datos proporcionados en arr.

exp_bernoulli(p:float): p = probabilidad. Regresa el valor esperado de un experimiento bernoulli según la probabilidad de éxito.

var_bernoulli(p:float): p = probabilidad. Regresa la varianza de un experimento bernoulli según la probabilidad de éxito.

prob_binomial(p:float, n:int, k:int): p = probabilidad, n = número de intentos, k = valor deseado. Regresa la probabilidad de que haya k éxitos en n experimentos según la probabilidad de éxito p.

exp_binomial(p:float, n:int): n = número de experimentos, p = probabilidad. Regresa el valor esperado de una distribución binomial.

var_binomial(p:float, n:int): n = número de experimentos, p = probabilidad. Regresa la varianza de distribución binomial.

prob_geometric(p:float, n:int): p = probabilidad, n = número de intentos. Regresa la probabilidad de una distribución geométrica.

exp_geometric(p:float): p = probabilidad. Regresa la esperanza de una distribución geométrica.

var_geometric(p:float): p = probabilidad. Regresa la varianza de una distribución geométrica.

```

Los estatutos tienen la siguiente sintaxis:

Declaración de variables (se permiten los tipos int, char, float y bool):

```
var nombre : tipo;

var nombreArreglo[dimension] : tipo;

var nombreMatriz[dimension][dimension] : tipo;

```

Los condicionales deben de escribirse de acorde al siguiente ejemplo:

```
if ( true != false) {
    println("El estatuto fue verdadero. ");
} else {
    println("El estatuto fue falso");
};
```
Los ciclos while deben de escribirse de acorde al siguiente ejemplo:
```
var contador : int;

read(contador);

while (contador < 10 && contador >= 3 ){
    print(contador, " ");
    contador = contador + 1;
}
println();
```

Las funciones tienen la siguiente estructura, de ser una función de tipo void no será posible regresar un valor:

```
fun funcionUno(mat[5][4] : char, i : int, arr[5] : float) : int {
    if (arr[1] == 5 || i < -1000){
        i = 5 + 7 - 4 / 2;
    };
    if (mat[3][2] == 'f'){
        i = - (6 * 4.9);
    } else {
        i = 7;
    };
    return i;
}

```

El siguiente es un pequeño programa integral en dist:

```
program test;
// Solo en esta zona son permitidas las variables globales
var f : float;

fun testFunction(i : float) : float{
    f = 8.0;
    if (i == 5){
        return 9.0*7 * i;
    } else{
        return 9.0/7 * i * f;;
    };
    
}

main{
    /*
        Este es un comentario
        multilínea
    */
    var f : float;
    while (f < 10){
        println(testFunction(f));
        f = f + 1;
    };
}
```

Omar Iván Flores Quijada
Esteban Arocha Ortuño
Enero - Mayo 2019
ITESM
