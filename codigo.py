import random
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del Algoritmo Genético
tamaño_poblacion = 100
tasa_cruce = 0.8
tasa_mutacion = 0.1
generaciones = 500

def generar_grafo(num_nodos):
    """Genera un grafo aleatorio de num_nodos con conexiones aleatorias."""
    grafo = np.zeros((num_nodos, num_nodos))
    for i in range(num_nodos):
        conexiones = random.randint(1, num_nodos - 1)
        nodos_conectados = random.sample(range(num_nodos), conexiones)
        for j in nodos_conectados:
            if i != j:
                peso = random.randint(10, 50)
                grafo[i, j] = peso
                grafo[j, i] = peso  # Conexión bidireccional
    return grafo

def visualizar_grafo(grafo):
    """Visualiza el grafo con todas las conexiones."""
    plt.figure(figsize=(8, 6))
    num_nodos = len(grafo)
    coordenadas = {i: (random.uniform(0, 10), random.uniform(0, 10)) for i in range(num_nodos)}

    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if grafo[i, j] != 0:
                x_values = [coordenadas[i][0], coordenadas[j][0]]
                y_values = [coordenadas[i][1], coordenadas[j][1]]
                plt.plot(x_values, y_values, 'grey', linestyle='--', alpha=0.5)

    for nodo, coord in coordenadas.items():
        plt.plot(coord[0], coord[1], 'o', markersize=10, label=f"Ciudad {nodo}")
        plt.text(coord[0], coord[1], str(nodo), fontsize=12, ha='center')

    plt.title("Grafo Generado Aleatoriamente")
    plt.legend()
    plt.grid()
    plt.show()
    return coordenadas

def distancia_total(ruta, grafo):
    """Calcula la distancia total de una ruta usando la matriz de distancias del grafo."""
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += grafo[ruta[i], ruta[i + 1]]
    distancia += grafo[ruta[-1], ruta[0]]  # Volver a la ciudad inicial
    return distancia

# Crear una ruta inicial aleatoria
def crear_ruta_aleatoria(num_nodos):
    ruta = list(range(num_nodos))
    random.shuffle(ruta)
    return ruta

# Crear una población inicial de rutas
def crear_poblacion(num_nodos):
    return [crear_ruta_aleatoria(num_nodos) for _ in range(tamaño_poblacion)]

# Selección de padres basada en el fitness (distancia de la ruta)
def seleccion(poblacion, grafo):
    puntuaciones = [(ruta, 1 / distancia_total(ruta, grafo)) for ruta in poblacion]
    puntuaciones.sort(key=lambda x: x[1], reverse=True)
    return [puntuaciones[i][0] for i in range(len(puntuaciones) // 2)]

# Cruce entre dos rutas
def crossover(parent1, parent2):
    inicio, fin = sorted(random.sample(range(len(parent1)), 2))
    hijo = [None] * len(parent1)
    hijo[inicio:fin] = parent1[inicio:fin]
    hijo_pos = fin

    for gene in parent2:
        if gene not in hijo:
            if hijo_pos >= len(parent1):
                hijo_pos = 0
            hijo[hijo_pos] = gene
            hijo_pos += 1
    return hijo

# Mutación de una ruta (intercambia dos ciudades)
def mutacion(ruta):
    if random.random() < tasa_mutacion:
        idx1, idx2 = random.sample(range(len(ruta)), 2)
        ruta[idx1], ruta[idx2] = ruta[idx2], ruta[idx1]
    return ruta

# Algoritmo Genético Principal para resolver el TSP
def algoritmo_genetico(grafo):
    num_nodos = len(grafo)
    poblacion = crear_poblacion(num_nodos)
    mejor_ruta = None
    mejor_distancia = float('inf')

    for gen in range(generaciones):
        padres = seleccion(poblacion, grafo)
        nueva_poblacion = []

        while len(nueva_poblacion) < tamaño_poblacion:
            parent1, parent2 = random.sample(padres, 2)
            if random.random() < tasa_cruce:
                hijo = crossover(parent1, parent2)
                hijo = mutacion(hijo)
                nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        # Actualizar la mejor solución en cada generación
        for ruta in poblacion:
            distancia_ruta = distancia_total(ruta, grafo)
            if distancia_ruta < mejor_distancia:
                mejor_distancia = distancia_ruta
                mejor_ruta = ruta

        if gen % 100 == 0 or gen == generaciones - 1:
            print(f"Generación {gen + 1}, Mejor Distancia: {mejor_distancia}")

    return mejor_ruta, mejor_distancia, gen + 1

def visualizar_solucion_final(grafo, ruta, mejor_distancia, coordenadas, generaciones):
    """Visualiza el grafo con la ruta óptima resaltada en rojo."""
    plt.figure(figsize=(8, 6))
    plt.title(f"Mejor Ruta - Distancia Total: {mejor_distancia:.2f} en {generaciones} generaciones")

    # Graficar todas las conexiones
    num_nodos = len(grafo)
    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if grafo[i, j] != 0:
                x_values = [coordenadas[i][0], coordenadas[j][0]]
                y_values = [coordenadas[i][1], coordenadas[j][1]]
                plt.plot(x_values, y_values, 'grey', linestyle='--', alpha=0.5)

    # Graficar la mejor ruta en rojo
    for i in range(len(ruta) - 1):
        ciudad_actual, ciudad_siguiente = ruta[i], ruta[i + 1]
        x_values = [coordenadas[ciudad_actual][0], coordenadas[ciudad_siguiente][0]]
        y_values = [coordenadas[ciudad_actual][1], coordenadas[ciudad_siguiente][1]]
        plt.plot(x_values, y_values, 'r-', linewidth=2.5)

    # Conectar la última ciudad de regreso a la primera
    x_values = [coordenadas[ruta[-1]][0], coordenadas[ruta[0]][0]]
    y_values = [coordenadas[ruta[-1]][1], coordenadas[ruta[0]][1]]
    plt.plot(x_values, y_values, 'r-', linewidth=2.5)

    # Graficar nodos
    for nodo, coord in coordenadas.items():
        plt.plot(coord[0], coord[1], 'o', markersize=10)
        plt.text(coord[0], coord[1], str(nodo), fontsize=12, ha='center')

    plt.grid()
    plt.show()

if __name__ == "__main__":
    num_nodos = int(input("Número de ciudades en el grafo: "))
    while True:
        grafo = generar_grafo(num_nodos)
        coordenadas = visualizar_grafo(grafo)
        respuesta = input("¿Te agrada el grafo? (s para aceptar, cualquier otra tecla para regenerar): ")
        if respuesta.lower() == 's':
            break

    # Ejecutar el algoritmo genético
    mejor_ruta, mejor_distancia, generaciones_usadas = algoritmo_genetico(grafo)
    print(f"\nMejor Ruta: {mejor_ruta}")
    print(f"Distancia Total de la Mejor Ruta: {mejor_distancia}")
    print(f"Generaciones Usadas: {generaciones_usadas}")

    # Visualizar la solución final
    visualizar_solucion_final(grafo, mejor_ruta, mejor_distancia, coordenadas, generaciones_usadas)
