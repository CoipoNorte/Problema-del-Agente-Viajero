import csv
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# Parámetros del Algoritmo Genético
tamaño_poblacion = 100
tasa_cruce = 0.8
tasa_mutacion = 0.1
generaciones = 500

# Función para leer las coordenadas desde el CSV
def leer_ciudades_desde_csv(nombre_archivo):
    ciudades = []
    with open(nombre_archivo, newline='') as csvfile:
        lector = csv.reader(csvfile)
        for fila in lector:
            x, y = map(float, fila)
            ciudades.append((x, y))
    return ciudades

# Función para calcular la distancia entre dos ciudades
def distancia(ciudad1, ciudad2):
    return np.sqrt((ciudad1[0] - ciudad2[0]) ** 2 + (ciudad1[1] - ciudad2[1]) ** 2)

# Crear una matriz de distancias completa entre todas las ciudades
def calcular_matriz_distancias(ciudades):
    num_ciudades = len(ciudades)
    matriz = np.zeros((num_ciudades, num_ciudades))
    for i in range(num_ciudades):
        for j in range(i + 1, num_ciudades):
            dist = distancia(ciudades[i], ciudades[j])
            matriz[i, j] = dist
            matriz[j, i] = dist  # La distancia es bidireccional
    return matriz

# Calcular la distancia total de una ruta
def distancia_total(ruta, matriz_distancias):
    return sum(matriz_distancias[ruta[i], ruta[i + 1]] for i in range(len(ruta) - 1)) + matriz_distancias[ruta[-1], ruta[0]]

# Crear una ruta inicial aleatoria
def crear_ruta_aleatoria(num_ciudades):
    ruta = list(range(num_ciudades))
    random.shuffle(ruta)
    return ruta

# Crear una población inicial de rutas
def crear_poblacion(num_ciudades):
    return [crear_ruta_aleatoria(num_ciudades) for _ in range(tamaño_poblacion)]

# Selección de padres basada en el fitness (distancia de la ruta)
def seleccion(poblacion, matriz_distancias):
    puntuaciones = [(ruta, 1 / distancia_total(ruta, matriz_distancias)) for ruta in poblacion]
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
def algoritmo_genetico(matriz_distancias):
    num_ciudades = len(matriz_distancias)
    poblacion = crear_poblacion(num_ciudades)
    mejor_ruta = None
    mejor_distancia = float('inf')

    for gen in range(generaciones):
        padres = seleccion(poblacion, matriz_distancias)
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
            distancia_ruta = distancia_total(ruta, matriz_distancias)
            if distancia_ruta < mejor_distancia:
                mejor_distancia = distancia_ruta
                mejor_ruta = ruta

        if gen % 100 == 0 or gen == generaciones - 1:
            print(f"Generación {gen + 1}, Mejor Distancia: {mejor_distancia}")

    return mejor_ruta, mejor_distancia, gen + 1

# Visualizar el grafo con todas las conexiones y la ruta óptima
def visualizar_grafo(ciudades, matriz_distancias, ruta=None, mejor_distancia=None, generaciones=None):
    plt.figure(figsize=(10, 8))
    plt.title("Grafo de Ciudades" if ruta is None else f"Mejor Ruta - Distancia: {mejor_distancia:.2f} en {generaciones} generaciones")

    # Graficar todas las conexiones en gris
    for i in range(len(ciudades)):
        for j in range(i + 1, len(ciudades)):
            x_values = [ciudades[i][0], ciudades[j][0]]
            y_values = [ciudades[i][1], ciudades[j][1]]
            plt.plot(x_values, y_values, 'grey', linestyle='--', alpha=0.5)

    # Graficar los nodos (ciudades)
    for i, (x, y) in enumerate(ciudades):
        plt.plot(x, y, 'o', markersize=10, label=f"Ciudad {i}")
        plt.text(x, y, f"{i}", fontsize=12, ha='right')

    # Si se proporciona una ruta, graficar la mejor ruta en rojo
    if ruta is not None:
        for i in range(len(ruta) - 1):
            x_values = [ciudades[ruta[i]][0], ciudades[ruta[i + 1]][0]]
            y_values = [ciudades[ruta[i]][1], ciudades[ruta[i + 1]][1]]
            plt.plot(x_values, y_values, 'r-', linewidth=2.5)
        # Conectar la última ciudad de regreso a la primera
        x_values = [ciudades[ruta[-1]][0], ciudades[ruta[0]][0]]
        y_values = [ciudades[ruta[-1]][1], ciudades[ruta[0]][1]]
        plt.plot(x_values, y_values, 'r-', linewidth=2.5)

    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Leer las ciudades desde el archivo CSV
    nombre_archivo = os.path.join(os.path.dirname(__file__), "Viajero15Ciudades_X_Y.csv")
    ciudades = leer_ciudades_desde_csv(nombre_archivo)

    # Calcular la matriz de distancias
    matriz_distancias = calcular_matriz_distancias(ciudades)

    # Visualizar el grafo inicial con todas las conexiones
    visualizar_grafo(ciudades, matriz_distancias)

    # Ejecutar el algoritmo genético
    mejor_ruta, mejor_distancia, generaciones_usadas = algoritmo_genetico(matriz_distancias)
    print(f"\nMejor Ruta: {mejor_ruta}")
    print(f"Distancia Total de la Mejor Ruta: {mejor_distancia}")
    print(f"Generaciones Usadas: {generaciones_usadas}")

    # Visualizar la solución final con la mejor ruta resaltada
    visualizar_grafo(ciudades, matriz_distancias, mejor_ruta, mejor_distancia, generaciones_usadas)
