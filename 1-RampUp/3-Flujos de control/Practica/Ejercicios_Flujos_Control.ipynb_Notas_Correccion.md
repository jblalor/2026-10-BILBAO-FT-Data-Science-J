# Informe: Revisión de Jupyter Notebook de Julioo Blanco Lorenzo

**Nombre de archivo:** Ejercicios_Flujos_de_control.ipynb

---

## Calificación Global: **Bien**

### Resumen de Desempeño en Factores Principales

1. **Comprensión de las Tareas** – Julioo demuestra una excelente comprensión de las estructuras de control en Python (bucles `for`, `while` y condicionales `if-elif-else`). Ha captado la lógica detrás de cada problema, aunque ha tenido pequeños descuidos al trasladar las especificaciones exactas de los enunciados al código.
2. **Corrección de las Respuestas** – La mayoría de las soluciones son funcionales y se ejecutan sin errores de sintaxis. No obstante, se han detectado fallos de precisión en los ejercicios 2, 6, 8 y 9 (errores en operadores lógicos, valores asignados, formato de salida y número de intentos).
3. **Ejercicios No Resueltos** – Todos los ejercicios (9 en total) cuentan con su respectiva celda de código ejecutada. No hay ejercicios sin resolver.

### Resumen de Desempeño en Factores Secundarios

1. **Legibilidad del Código** – El código es limpio, directo y fácil de seguir. Las variables utilizadas son adecuadas y la estructura general del notebook es ordenada.
2. **Comentarios en el Código** – No se han incluido comentarios explicativos en ninguna de las celdas. Aunque los ejercicios son sencillos, es una buena práctica habituarse a comentar el código para explicar la lógica aplicada, especialmente en bloques condicionales o bucles.

---

## Lista de Ejercicios con Problemas

| Nº de Ejercicio | Ejercicio | Problema Detectado | Recomendación |
| :--- | :--- | :--- | :--- |
| **2** | **Calculador de precios de casas** | 1. En la condición de "Salamanca", se evalúa `superficie < 150` cuando el enunciado pide "al menos 150 metros" (`>= 150`).<br>2. En la tercera condición, se asigna un precio de `60` en lugar de `600`. | Corregir los operadores y valores numéricos en el código:<br>```python\nelif distrito == "Salamanca" and superficie >= 150:\n    precio = 1500.\nelif distrito != "Retiro" and 60 <= superficie <= 80:\n    precio = 600.\n``` |
| **6** | **Divisibles por 5 y parada > 150** | El bucle imprime el número `180` antes de detenerse. Al ser `180 > 150`, el bucle debería haberse detenido antes de imprimirlo para cumplir estrictamente con "detener el bucle si nos encontramos con alguno mayor que 150". | Colocar la condición de parada al inicio del bucle para evitar que se procese e imprima el elemento que supera el límite:<br>```python\nfor i in list1:\n    if i > 150:\n        break\n    if i % 5 == 0:\n        print(i)\n``` |
| **8** | **Imprimir patrón numérico** | Se imprimen listas de Python (ej. `[5, 4, 3, 2, 1]`) en lugar de los números limpios y formateados separados por espacios (ej. `5 4 3 2 1`) como solicita el patrón. | Desempaquetar el rango al imprimir utilizando el operador `*` para obtener el formato correcto:<br>```python\nfor i in range(5):\n    print(*range(5-i, 0, -1))\n``` |
| **9** | **Juego de adivinar el número** | Se inicializa la variable `vidas = 3`, pero el enunciado especifica claramente que "tenemos dos intentos para acertar" (`vidas = 2`). | Cambiar el valor inicial de la variable a `vidas = 2`. |

---

## Comentarios Finales

Julioo ha completado con éxito la totalidad del notebook, demostrando que domina la sintaxis y la lógica de los flujos de control en Python. Los errores identificados no son de comprensión de la programación en sí, sino de atención a los detalles de los enunciados (requisitos de negocio). 

Para futuros trabajos, se recomienda:
* **Prestar máxima atención a los detalles del enunciado:** Verificar que los límites numéricos (`>`, `>=`, `<`, `<=`), los valores de salida y las restricciones se implementen exactamente como se solicitan.
* **Validar el formato de salida:** Asegurarse de que la presentación de los resultados (como en el Ejercicio 8) coincida con el patrón requerido.
* **Documentar el código:** Incorporar comentarios breves que expliquen el porqué de ciertas decisiones en el código, lo cual es un estándar fundamental en la Ciencia de Datos.