# Resolución del Problema del Agente Viajero (TSP) en un Grafo Complejo usando Algoritmos Genéticos

Este proyecto utiliza un **Algoritmo Genético** para resolver el **Problema del Agente Viajero (TSP)** en un grafo complejo. En lugar de un plano simple, el TSP se representa aquí como un grafo en el cual cada ciudad tiene conexiones específicas con otras ciudades, representadas en una matriz de adyacencia. 

## Descripción del Problema

El **Problema del Agente Viajero (TSP)** consiste en encontrar la ruta más corta que permita visitar todas las ciudades exactamente una vez y regresar al punto de partida. En este caso, hemos definido un grafo en el que no todas las ciudades están conectadas directamente, haciendo que el problema sea más realista y complicado.

## Representación del Grafo

El grafo se representa mediante una **matriz de adyacencia**, donde cada entrada `(i, j)` indica la distancia entre las ciudades `i` y `j`. Si la entrada `(i, j)` es `0`, significa que no existe conexión directa entre esas dos ciudades.

Ejemplo de matriz de adyacencia para 6 ciudades:
```python
distancias = np.array([
    [0, 10, 15, 20, 0, 0],   # Ciudad 0 conectada a 1, 2, 3
    [10, 0, 35, 25, 30, 0],  # Ciudad 1 conectada a 0, 2, 3, 4
    [15, 35, 0, 30, 0, 20],  # Ciudad 2 conectada a 0, 1, 3, 5
    [20, 25, 30, 0, 15, 10], # Ciudad 3 conectada a 0, 1, 2, 4, 5
    [0, 30, 0, 15, 0, 25],   # Ciudad 4 conectada a 1, 3, 5
    [0, 0, 20, 10, 25, 0]    # Ciudad 5 conectada a 2, 3, 4
])
```

## Algoritmo Genético para Resolver el TSP

Los pasos del **Algoritmo Genético (AG)** en este proyecto son:
1. **Inicialización**: Crear una población inicial de rutas aleatorias.
2. **Evaluación (Fitness)**: Calcular la distancia de cada ruta usando la matriz de adyacencia.
3. **Selección**: Seleccionar las rutas más cortas (mejor fitness) para la próxima generación.
4. **Cruce (Crossover)**: Crear nuevas rutas combinando segmentos de las rutas seleccionadas.
5. **Mutación**: Introducir cambios aleatorios en las rutas para mantener la diversidad.
6. **Repetición**: Repetir los pasos de evaluación, selección, cruce y mutación por el número de generaciones definido.

### Código de Distancia Total de la Ruta

La función `distancia_total` calcula la distancia total de una ruta utilizando la matriz de adyacencia:

```python
def distancia_total(ruta):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += distancias[ruta[i], ruta[i + 1]]
    distancia += distancias[ruta[-1], ruta[0]]  # Volver a la ciudad inicial
    return distancia
```

## Visualización del Grafo y la Mejor Ruta

Para visualizar el grafo, utilizamos **matplotlib**:
1. **Grafo Completo**: La función `visualizar_grafo` dibuja todas las conexiones entre ciudades definidas en la matriz de adyacencia. Estas conexiones se muestran con líneas grises para dar la apariencia de una red completa.
2. **Ruta Óptima**: La mejor ruta encontrada se resalta en **rojo** sobre el grafo, indicando la secuencia óptima de ciudades.

### Código para Visualización del Grafo

```python
def visualizar_grafo(distancias, ruta, mejor_distancia):
    plt.figure(figsize=(8, 6))
    plt.title(f"Mejor Ruta Encontrada - Distancia Total: {mejor_distancia:.2f}")
    
    # Coordenadas de ejemplo para las ciudades en el gráfico
    coordenadas = {
        0: (0, 0), 1: (1, 2), 2: (3, 1), 3: (4, 4), 4: (2, 3), 5: (3, 6)
    }

    # Graficar las conexiones del grafo completo basado en la matriz de adyacencia
    for i in range(len(distancias)):
        for j in range(i + 1, len(distancias)):
            if distancias[i, j] != 0:  # Solo graficar si existe una conexión
                x_values = [coordenadas[i][0], coordenadas[j][0]]
                y_values = [coordenadas[i][1], coordenadas[j][1]]
                plt.plot(x_values, y_values, 'grey', linestyle='--', alpha=0.5)  # Línea de conexión en gris claro

    # Graficar los nodos (ciudades)
    for ciudad, coord in coordenadas.items():
        plt.plot(coord[0], coord[1], 'o', markersize=10, label=f"Ciudad {ciudad}")
        plt.text(coord[0], coord[1], f"{ciudad}", fontsize=12, ha='center')

    # Graficar las conexiones de la ruta final resaltada
    for i in range(len(ruta) - 1):
        ciudad_actual, ciudad_siguiente = ruta[i], ruta[i + 1]
        x_values = [coordenadas[ciudad_actual][0], coordenadas[ciudad_siguiente][0]]
        y_values = [coordenadas[ciudad_actual][1], coordenadas[ciudad_siguiente][1]]
        plt.plot(x_values, y_values, 'r-', linewidth=2)  # Ruta resaltada en rojo

    # Conectar la última ciudad de regreso a la primera
    x_values = [coordenadas[ruta[-1]][0], coordenadas[ruta[0]][0]]
    y_values = [coordenadas[ruta[-1]][1], coordenadas[ruta[0]][1]]
    plt.plot(x_values, y_values, 'r-', linewidth=2)  # Ruta resaltada en rojo

    plt.grid()
    plt.legend()
    plt.show()
```

## Ejecución del Proyecto

### Requisitos

OJO piojo, tener **Python 3** y la librería **matplotlib** instalada. Puedes instalar matplotlib con:
```bash
pip install matplotlib
```

### Ejecutar el Código

Para ejecutar el código y ver el resultado:
```bash
python tsp.py
```

El script imprimirá en consola la mejor ruta y la distancia total. Al finalizar, mostrará una gráfica:
- Las conexiones del grafo completo se dibujarán en **gris**.
- La mejor ruta encontrada se destacará en **rojo**.

## CoipoNota

El uso de un **Algoritmo Genético** en este grafo complejo de ciudades proporciona una solución aproximada para el TSP. La visualización ayuda a comprender la estructura de las conexiones y el camino óptimo entre las ciudades. Esto permite resolver problemas similares de optimización en redes y grafos en situaciones reales.
