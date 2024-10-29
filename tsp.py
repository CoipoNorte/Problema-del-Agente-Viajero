import random
import numpy as np
import matplotlib.pyplot as plt

# Matriz de adyacencia: Distancias definidas manualmente entre cada par de ciudades
# Ejemplo de 6 ciudades
distancias = np.array([
    [0, 10, 15, 20, 0, 0],   # Ciudad 0 conectada a 1, 2, 3
    [10, 0, 35, 25, 30, 0],  # Ciudad 1 conectada a 0, 2, 3, 4
    [15, 35, 0, 30, 0, 20],  # Ciudad 2 conectada a 0, 1, 3, 5
    [20, 25, 30, 0, 15, 10], # Ciudad 3 conectada a 0, 1, 2, 4, 5
    [0, 30, 0, 15, 0, 25],   # Ciudad 4 conectada a 1, 3, 5
    [0, 0, 20, 10, 25, 0]    # Ciudad 5 conectada a 2, 3, 4
])

# Parámetros del Algoritmo Genético
tamaño_poblacion = 100
tasa_cruce = 0.8
tasa_mutacion = 0.1
generaciones = 500

# Calcular la distancia total de una ruta usando la matriz de distancias
def distancia_total(ruta):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += distancias[ruta[i], ruta[i + 1]]
    distancia += distancias[ruta[-1], ruta[0]]  # Volver a la ciudad inicial
    return distancia

# Crear una ruta inicial aleatoria
def crear_ruta_aleatoria():
    ruta = list(range(len(distancias)))
    random.shuffle(ruta)
    return ruta

# Crear una población inicial de rutas
def crear_poblacion():
    return [crear_ruta_aleatoria() for _ in range(tamaño_poblacion)]

# Selección de padres basada en el fitness (distancia de la ruta)
def seleccion(poblacion):
    puntuaciones = [(ruta, 1 / distancia_total(ruta)) for ruta in poblacion]
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
def algoritmo_genetico():
    poblacion = crear_poblacion()
    mejor_ruta = None
    mejor_distancia = float('inf')

    for gen in range(generaciones):
        padres = seleccion(poblacion)
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
            distancia_ruta = distancia_total(ruta)
            if distancia_ruta < mejor_distancia:
                mejor_distancia = distancia_ruta
                mejor_ruta = ruta

        if gen % 100 == 0 or gen == generaciones - 1:
            print(f"Generación {gen + 1}, Mejor Distancia: {mejor_distancia}")

    return mejor_ruta, mejor_distancia

# Visualizar el grafo de ciudades y la ruta final
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

# Ejecutar el algoritmo genético y mostrar la mejor ruta encontrada
mejor_ruta, mejor_distancia = algoritmo_genetico()
print("\nMejor Ruta:", mejor_ruta)
print("Distancia Total de la Mejor Ruta:", mejor_distancia)

# Visualizar el grafo y la mejor ruta
visualizar_grafo(distancias, mejor_ruta, mejor_distancia)
