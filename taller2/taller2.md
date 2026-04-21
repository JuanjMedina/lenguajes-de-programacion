Práctica 2
Analizador Sintáctico - Lenguaje EsJS

Profesor: Felipe Restrepo Calle (ferestrepoca@unal.edu.co)
Monitor: Reinaldo Toledo Leguizamón (rtoledol@unal.edu.co)

Dado un programa en el lenguaje de programación EsJS, su tarea consiste en realizar el análisis sintáctico. Para realizar la implementación se podrán utilizar únicamente los siguientes lenguajes de programación: Python 3.9, C/C++ y Java.
Entrada
La entrada consiste en el código fuente de un programa en EsJS, el cual puede estar correcto sintácticamente o no. Su programa debe recibir por la entrada estándar (consola) el código fuente de un programa escrito en el lenguaje de programación EsJS. La entrada dada no contiene errores léxicos. 

Para evaluar el analizador sintáctico de forma automática, su programa debe realizar el análisis sintáctico de la entrada dada y generar la salida adecuada de acuerdo con las especificaciones dadas. A continuación se muestra la manera correcta de generar las salidas correspondientes.
Salida
Las salidas se deben generar por la salida estándar (consola). Nos vamos a enfocar en los errores sintácticos generados. Note que en este punto no interesa si el programa tiene errores semánticos porque, por el momento, nos enfocaremos solamente en el análisis sintáctico.

En caso de que el programa esté bien formado de acuerdo a las reglas de la gramática del lenguaje EsJS, se debe mostrar el mensaje: 

El analisis sintactico ha finalizado exitosamente.

Note que no se permiten tildes. 

En caso contrario, es decir, si se encontró algún error sintáctico, se debe abortar el análisis y reportar únicamente el primer error sintáctico detectado.
Consideraciones gramaticales
Se deben considerar todas las construcciones sintácticas definidas en el manual de referencia así como el alcance definido para las prácticas. Puede apoyarse del entorno de desarrollo en línea de EsJS para identificar algunas de las reglas gramaticales que no pueden ser explícitas en el manual de referencia.


A continuación se detallan algunos puntos importantes:

Vamos a suponer que en el archivo de entrada se le intenta asignar una cadena a una variable la siguiente secuencia de operaciones 
por ejemplo: 		x = "n"+a-verdadero*(vari[3] % 70) 


Dado que en el lenguaje EsJS todos los tipos de variables son correctos; podemos decir que el ejemplo mostrado anteriormente refiere a un error dado que no se pueden operar esos tipos de datos entre sí (y aún desconociendo los tipos de variables a y el contenido del arreglo vari). Por ende, el ejemplo hace referencia a un error semántico dado que no se presentan errores de sintaxis al ser capaces de operar todos los tipos de datos si fueran almacenados en variables. Por ende, en estos casos en particular, podemos permitir en expresiones aritméticas y relacionales, todos los tipos de datos presentes en el lenguaje dado que pueden ser definidos como variables. De esta manera, le corresponderá al analizador semántico verificar si las operaciones presentes en la expresión se pueden realizar con los tipos de datos ahí presentes.

El analizador sintáctico tan solo se encarga de validar que el programa ingresado satisfaga las reglas gramaticales del lenguaje.

Tenga en cuenta que en EsJS es posible acceder a un índice de un arreglo por medio de una operación aritmética mientras satisfaga el hecho de que el resultado sea un número entero (responsabilidad del analizador semántico), por lo que expresiones mostradas anteriormente son válidas sintácticamente para referir al índice de un arreglo. 

A diferencia del analizador léxico, para el desarrollo del analizador sintáctico no se debe contemplar el uso del operador de coalescencia nula (??) ni del operador de propagación (...), así como el uso de los tokens correspondientes a expresiones regulares.

Aunque en la mayoría de lenguajes de programación se considera el fin de línea para manejar reglas sintácticas (ej. Python), o en su defecto, la definición de un token que representa el fin de sentencias (ej “;” en C++ y Java). En nuestro caso, EsJS es un lenguaje que no es sensible a saltos de línea ni terminación explícita de sentencias. Por ende, los siguientes códigos tendrían el mismo resultado en nuestro analizador sintáctico; y también son correctos semánticamente.

var a = 4; 
var b = 5;
var a = 4; var b=5; 


Errores sintácticos
En el caso de cualquier error sintáctico, se debe informar al programador usando el siguiente formato:

<linea:col> Error sintactico: se encontro: <lexema del token encontrado>; se esperaba: <lista de simbolos/tokens esperados separados por comas>.

Donde:
linea y col son los números de línea y columna donde se detectó el error.
<lexema del token encontrado>: corresponde al lexema encontrado que no se esperaba encerrado entre comillas dobles (OJO: el lexema, no el token).
<lista de simbolos/tokens esperados separados por comas>: corresponde a lista de tokens esperados separados por comas y encerrados entre comillas dobles. Por ejemplo: "repetir", "si", "/", "-", "+", "^", "*", …
El mensaje no debe contener tildes.

Nótese que debe manejar un lenguaje que sea fácilmente comprensible para el programador de lenguaje EsJS. Los símbolos ")", ",", ":" pueden haber tenido otros nombres internamente, por ejemplo: tkn_closing_par, tkn_comma, tkn_colon. No obstante, estos detalles no deberían ser conocidos por el programador de EsJS. Es por ello que en la lista de símbolos/tokens:

Para las palabras reservadas se muestra el lexema correspondiente, pues sabemos que el tipo de token y el lexema son iguales en ese caso. (Por ejemplo: "escribir")
Para los identificadores se muestra "id".
Para los tokens de tipo tkn_num se muestra "valor_numérico".
Para los tokens de tipo tkn_str se muestra "cadena_de_caracteres".
Para los operadores y símbolos se muestra el operador o símbolo correspondiente (Por ejemplo, "+", en reemplazo a tkn_plus).
Si se esperaba el final del archivo, se muestra "final de archivo".

IMPORTANTE: En casos como el anterior, cuando se debe imprimir una lista de varios símbolos/tokens esperados, éstos deben estar entre comillas dobles, separados por un espacio en blanco, y el orden en que debe aparecer la lista está determinado por el orden lexicográfico ascendente de los mismos, es decir, simplemente se debe ordenar el arreglo de strings. 

En caso que se encuentre el fin de archivo (el token “EOF”) de manera inesperada, el analizador debe mostrar el siguiente error:	

<linea:col> Error sintactico: se encontro: “final de archivo”; se esperaba: <lista de simbolos/tokens esperados separados por comas>.

Ejemplos
Así debería reportarse un programa sin errores sintácticos:

Entrada
Salida
//Ejemplo Fecha
funcion iniciar() {
 const fecha = crear Fecha()
 consola.escribir(fecha)
}

iniciar()


El analisis sintactico ha finalizado exitosamente.


Y así los programas con errores sintácticos:

Entrada
Salida
var 1;
<1:5> Error sintactico: se encontro: "1"; se esperaba: "id".



Entrada
Salida
consola.escribir(45"this")
<1:20> Error sintactico: se encontro: "this"; se esperaba: "&&", ")", ",", "/", "==", ">=", ">", "<=", "<", "-", "%", "!=", "||", "+", "**", "===", "!==", "?", "*".


Nótese que el token “)” podría estar en las siguientes líneas o posiciones (después del número 45), siempre y cuando sea el siguiente token leído. 

Veamos más ejemplos.

Entrada
Salida
mut entrada;

si (entrada === indefinido) {
  consola.error('Valor indefinido');
} sino {
  consola.escribir('Valor definido');
}


El analisis sintactico ha finalizado exitosamente.




Entrada
Salida
mut i = 0;

mientras (i < 5) {
    consola escribir(i);
    i = i + 1;
}
<4:13> Error sintactico: se encontro: "escribir"; se esperaba: ".".

Nota: Tenga en cuenta que tal y como se mencionó anteriormente, la salida del analizador sintáctico debe imprimirse en una sola línea, no confundirse con el cambio de formato y alteración de los ejemplos presentes en este enunciado.
Recomendaciones
Es posible implementar el analizador sintáctico calculando los conjuntos de predicción e implementando el analizador “a mano”. Sin embargo, esto puede significar tener que escribir muchas líneas de código repetitivas, lo cual puede ser susceptible de errores.

Se recomienda lo siguiente:

Nivel 1. Hacer un programa que halle los conjuntos de predicción (siguientes y primeros) dada una gramática LL(1). Esto evitará que pierda tiempo haciendo cosas muy repetitivas.

Nivel 2. Hacer un programa que genere automáticamente el analizador dada la gramática, usando el paso anterior: esto le ahorrará también mucho trabajo tedioso, reemplazándolo por trabajo interesante. En este caso, deberá enviar todos los archivos de su proyecto (incluida la gramática) junto con la entrega del programa resultante. No olvide consultar la documentación de UNCode respecto al envío de múltiples archivos.
