import os
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import random
import geopandas as gpd

N_POBLACION = 50        
N_CICLOS = 200          
PROB_CROSSOVER = 0.9
PROB_MUTACION = 0.1
TAMANO_TORNEO = 3
ELITES = 2
CORRIDAS_COMPARACION = 10

ARCHIVO_DISTANCIAS = "TablaCapitales_completa.xlsx"
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #significa que se obtiene la ruta del directorio donde se encuentra el archivo Python actual.
ARCHIVO_MAPA = os.path.join(BASE_DIR, "mapa", "ne_10m_admin_0_countries_arg.shp") #significa que se construye la ruta completa al archivo de forma independiente del sistema operativo.

ciudades = [
    "CABA",
    "Córdoba",
    "Corrientes",
    "Formosa",
    "La Plata",
    "La Rioja",
    "Mendoza",
    "Neuquén",
    "Paraná",
    "Posadas",
    "Rawson",
    "Resistencia",
    "Río Gallegos",
    "San Fernando del Valle de Catamarca",
    "San Miguel de Tucumán",
    "San Salvador de Jujuy",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Fe",
    "Santa Rosa",
    "Santiago del Estero",
    "Ushuaia",
    "Viedma",
]

# (latitud, longitud) de cada capital
COORDENADAS = {
    "CABA": (-34.61, -58.38),
    "Córdoba": (-31.42, -64.18),
    "Corrientes": (-27.47, -58.83),
    "Formosa": (-26.18, -58.17),
    "La Plata": (-34.92, -57.95),
    "La Rioja": (-29.41, -66.86),
    "Mendoza": (-32.89, -68.83),
    "Neuquén": (-38.95, -68.06),
    "Paraná": (-31.73, -60.52),
    "Posadas": (-27.37, -55.90),
    "Rawson": (-43.30, -65.10),
    "Resistencia": (-27.46, -58.99),
    "Río Gallegos": (-51.62, -69.22),
    "San Fernando del Valle de Catamarca": (-28.47, -65.78),
    "San Miguel de Tucumán": (-26.82, -65.22),
    "San Salvador de Jujuy": (-24.19, -65.30),
    "Salta": (-24.78, -65.41),
    "San Juan": (-31.54, -68.54),
    "San Luis": (-33.30, -66.34),
    "Santa Fe": (-31.63, -60.70),
    "Santa Rosa": (-36.62, -64.29),
    "Santiago del Estero": (-27.78, -64.26),
    "Ushuaia": (-54.80, -68.30),
    "Viedma": (-40.81, -62.99),
}


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausa():
    input("\nPresione ENTER para continuar...")

def cargar_distancias():
    matriz = pd.read_excel(ARCHIVO_DISTANCIAS, index_col=0)
    matriz = matriz.iloc[:len(ciudades), :len(ciudades)]            

    if list(matriz.columns) != ciudades or list(matriz.index) != ciudades:
        raise ValueError("Los nombres del Excel no coinciden con la lista 'ciudades'.")

    # La diagonal viene vacía en la tabla original: distancia de una ciudad a sí misma = 0
    valores = matriz.to_numpy(dtype=float, copy=True)
    np.fill_diagonal(valores, 0)
    matriz = pd.DataFrame(valores, index=ciudades, columns=ciudades)

    problemas = validar_matriz(matriz)
    if problemas:
        raise ValueError("Matriz inválida:\n" + "\n".join(problemas))
    
    return matriz

def validar_matriz(matriz):
    problemas = []

    # Celdas vacías o no numéricas
    if matriz.isnull().values.any():
        problemas.append("Hay celdas vacías en la matriz.")
    if not all(matriz.dtypes.apply(lambda t: t.kind in "iuf")):
        problemas.append("Hay columnas con valores no numéricos.")

    # Diagonal en cero
    for ciudad in matriz.index:
        if matriz.loc[ciudad, ciudad] != 0:
            problemas.append(f"Diagonal distinta de 0 en {ciudad}: {matriz.loc[ciudad, ciudad]}")

    # Simetría
    for i, a in enumerate(matriz.index):
        for b in matriz.index[i + 1:]:
            if matriz.loc[a, b] != matriz.loc[b, a]:
                problemas.append(
                    f"Asimetría: {a}->{b} = {matriz.loc[a, b]} / {b}->{a} = {matriz.loc[b, a]}"
                )

    return problemas

def mostrar_ciudades():
    limpiar_pantalla()

    print("========================================")
    print("       CAPITALES DE ARGENTINA")
    print("========================================")

    matriz = cargar_distancias()


    print("\nCiudades encontradas en el archivo:\n")

    for i, ciudad in enumerate(matriz.columns):
        print(f"{i + 1}) {ciudad}")

    pausa()

   

def calcular_vecino_mas_cercano(ciudad_inicial, matriz):
    ciudades = list(matriz.columns)

    ciudad_actual = ciudad_inicial
    visitadas = [ciudad_inicial]
    distancia_total = 0

    while len(visitadas) < len(ciudades):

        menor_distancia = float("inf")
        siguiente_ciudad = None

        for ciudad in ciudades:

            if ciudad not in visitadas:
                distancia = matriz.loc[ciudad_actual, ciudad]

                if distancia < menor_distancia:
                    menor_distancia = distancia
                    siguiente_ciudad = ciudad

        visitadas.append(siguiente_ciudad)
        distancia_total += menor_distancia
        ciudad_actual = siguiente_ciudad

    # Regreso a la ciudad inicial
    distancia_regreso = matriz.loc[ciudad_actual, ciudad_inicial]
    distancia_total += distancia_regreso
    visitadas.append(ciudad_inicial)

    return visitadas, distancia_total


def cargar_pais():
    mundo = gpd.read_file(ARCHIVO_MAPA)
    return mundo[mundo["ADMIN"] == "Argentina"]


def dibujar_mapa(recorrido, titulo):
    # recorrido: lista de nombres de ciudades; la última es igual a la primera
    fig, ax = plt.subplots(figsize=(7, 10))

    # Contorno real del país (punto de vista argentino)
    cargar_pais().plot(ax=ax, color="#eef2e6", edgecolor="gray", linewidth=0.8, zorder=0)
    ax.set_xlim(-74, -52)
    ax.set_ylim(-56, -21)

    # Todas las capitales
    for nombre, (lat, lon) in COORDENADAS.items():
        ax.scatter(lon, lat, color="steelblue", s=25, zorder=3)
        ax.annotate(nombre, (lon, lat), fontsize=6, xytext=(3, 3),
                    textcoords="offset points", zorder=4)

    # Recorrido con flechas, en orden
    for i in range(len(recorrido) - 1):
        lat1, lon1 = COORDENADAS[recorrido[i]]
        lat2, lon2 = COORDENADAS[recorrido[i + 1]]
        ax.annotate("", xy=(lon2, lat2), xytext=(lon1, lat1),
                    arrowprops=dict(arrowstyle="->", color="crimson", lw=1), zorder=2)

    # Ciudad de partida resaltada
    lat0, lon0 = COORDENADAS[recorrido[0]]
    ax.scatter(lon0, lat0, color="green", s=90, marker="*", zorder=5, label="Partida / llegada")

    ax.set_title(titulo)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect(1 / np.cos(np.radians(40)))   # corrige la deformación de lon/lat
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    plt.show()

def vecino_mas_cercano():
    limpiar_pantalla()

    print("========================================")
    print("       VECINO MÁS CERCANO")
    print("========================================")

    matriz = cargar_distancias()
    ciudades = list(matriz.columns)

    print("\nSeleccione la ciudad de partida:\n")

    for i in range(len(ciudades)):
        print(f"{i + 1}) {ciudades[i]}")

    opcion = input("\nOpción: ")

    if opcion.isdigit() and 1 <= int(opcion) <= len(ciudades):

        ciudad_inicial = ciudades[int(opcion) - 1]

        recorrido, distancia_total = calcular_vecino_mas_cercano(
            ciudad_inicial,
            matriz
        )

        print(f"\nCiudad de partida: {ciudad_inicial}")

        print("\nRecorrido encontrado:\n")
        print(" -> ".join(recorrido))

        print(f"\nDistancia total: {distancia_total} km")

        dibujar_mapa(recorrido, f"Vecino más cercano desde {ciudad_inicial} ({distancia_total:.0f} km)")
    else:
        print("\nOpción inválida.")

    pausa()

#--------------------------- Algoritmo genético ---------------------------------------#
def crear_cromosoma(n_ciudades):
    # Permutación aleatoria de los números 1..n_ciudades
    cromosoma = list(range(1, n_ciudades + 1))
    random.shuffle(cromosoma)
    return cromosoma


def crear_poblacion(tamano, n_ciudades):
    return [crear_cromosoma(n_ciudades) for _ in range(tamano)]


def calcular_distancia_ruta(cromosoma, distancias):

    # distancias: matriz numpy. Los genes van de 1 a N, los índices de 0 a N-1
    total = 0
    for i in range(len(cromosoma)):
        origen = cromosoma[i] - 1
        destino = cromosoma[(i + 1) % len(cromosoma)] - 1   # el último vuelve al primero
        total += distancias[origen][destino]
    return total

def seleccionar_padre(poblacion, distancias_pob):
    # Torneo: se sortean k índices al azar y gana el de menor distancia
    candidatos = random.sample(range(len(poblacion)), TAMANO_TORNEO)
    ganador = min(candidatos, key=lambda i: distancias_pob[i])
    return poblacion[ganador]

def crossover_ciclico(padre1, padre2):
    # Devuelve dos hijos. Con probabilidad PROB_CROSSOVER se cruzan; si no, pasan copias.
    if random.random() > PROB_CROSSOVER:
        return padre1[:], padre2[:]

    return _cx(padre1, padre2), _cx(padre2, padre1)

def ejecutar_genetico(distancias, n_ciudades):
    poblacion = crear_poblacion(N_POBLACION, n_ciudades)

    mejor_cromosoma = None
    mejor_distancia = float("inf")
    historial = []   # mejor distancia de cada ciclo

    for ciclo in range(N_CICLOS):
        distancias_pob = [calcular_distancia_ruta(c, distancias) for c in poblacion]

        # Orden de menor a mayor distancia (el primero es el mejor)
        orden = sorted(range(len(poblacion)), key=lambda i: distancias_pob[i])

        if distancias_pob[orden[0]] < mejor_distancia:
            mejor_distancia = distancias_pob[orden[0]]
            mejor_cromosoma = poblacion[orden[0]][:]
        historial.append(mejor_distancia)

        # Elitismo: los mejores pasan sin cambios
        nueva_poblacion = [poblacion[i][:] for i in orden[:ELITES]]

        # El resto se genera por selección, crossover cíclico y mutación
        while len(nueva_poblacion) < N_POBLACION:
            padre1 = seleccionar_padre(poblacion, distancias_pob)
            padre2 = seleccionar_padre(poblacion, distancias_pob)
            hijo1, hijo2 = crossover_ciclico(padre1, padre2)
            nueva_poblacion.append(mutar(hijo1))
            if len(nueva_poblacion) < N_POBLACION:
                nueva_poblacion.append(mutar(hijo2))

        poblacion = nueva_poblacion

    return mejor_cromosoma, mejor_distancia, historial

def _cx(base, otro):
    n = len(base)
    hijo = [None] * n

    # Ciclo que arranca en la posición 0: esos genes vienen de 'base'
    pos = 0
    while hijo[pos] is None:
        hijo[pos] = base[pos]
        pos = base.index(otro[pos])

    # El resto de las posiciones se completan con los genes de 'otro'
    for i in range(n):
        if hijo[i] is None:
            hijo[i] = otro[i]

    return hijo

def mutar(cromosoma):
    # Con probabilidad PROB_MUTACION intercambia dos genes al azar
    resultado = cromosoma[:]
    if random.random() < PROB_MUTACION:
        i, j = random.sample(range(len(resultado)), 2)
        resultado[i], resultado[j] = resultado[j], resultado[i]
    return resultado
#----------------------------------------------------------------------------------------#



def mejor_recorrido_heuristico():
    limpiar_pantalla()

    print("========================================")
    print("     MEJOR RECORRIDO - HEURÍSTICA")
    print("========================================")

    matriz = cargar_distancias()
    ciudades = list(matriz.columns)

    mejor_recorrido = None
    mejor_distancia = float("inf")
    mejor_ciudad_inicial = None

    for ciudad in ciudades:

        recorrido, distancia = calcular_vecino_mas_cercano(
            ciudad,
            matriz
        )
        
        print(f"{ciudad}: {distancia} km")

        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_recorrido = recorrido
            mejor_ciudad_inicial = ciudad

    print(f"\nMejor ciudad de partida: {mejor_ciudad_inicial}")

    print("\nMejor recorrido encontrado:\n")
    print(" -> ".join(mejor_recorrido))

    print(f"\nDistancia total: {mejor_distancia} km")

    pausa()

def algoritmo_genetico():
    limpiar_pantalla()

    print("========================================")
    print("         ALGORITMO GENÉTICO")
    print("========================================")

    matriz = cargar_distancias()
    distancias = matriz.to_numpy()
    n = len(ciudades)

    print("\nParámetros:")
    print(f"Cantidad de cromosomas: {N_POBLACION}")
    print(f"Cantidad de ciclos: {N_CICLOS}")
    print(f"Cantidad de ciudades: {n}")
    print(f"Probabilidad de crossover: {PROB_CROSSOVER}")
    print(f"Probabilidad de mutación: {PROB_MUTACION}")
    print("Crossover: Cíclico")

    print("\nEjecutando...")
    cromosoma, distancia, historial = ejecutar_genetico(distancias, n)

    # Rotamos el circuito para que arranque en CABA (gen 1): es el mismo circuito, más legible
    idx = cromosoma.index(1)
    cromosoma = cromosoma[idx:] + cromosoma[:idx]
    recorrido = [ciudades[g - 1] for g in cromosoma] + [ciudades[0]]

    print("\nMejor recorrido encontrado:\n")
    print(" -> ".join(recorrido))
    print(f"\nDistancia total: {distancia:.0f} km")

    # Evolución de la mejor distancia por ciclo
    plt.plot(range(1, len(historial) + 1), historial)
    plt.title("Algoritmo genético: mejor distancia por ciclo")
    plt.xlabel("Ciclo")
    plt.ylabel("Distancia (km)")
    plt.grid(True)
    plt.show()

    pausa()

def comparar():
    limpiar_pantalla()

    print("========================================")
    print("        COMPARACIÓN DE MÉTODOS")
    print("========================================")

    matriz = cargar_distancias()
    distancias = matriz.to_numpy()
    n = len(ciudades)

    # Heurística: vecino más cercano desde cada ciudad de partida
    resultados_nn = {c: calcular_vecino_mas_cercano(c, matriz)[1] for c in ciudades}
    mejor_ciudad = min(resultados_nn, key=resultados_nn.get)
    mejor_nn = resultados_nn[mejor_ciudad]
    peor_nn = max(resultados_nn.values())
    promedio_nn = sum(resultados_nn.values()) / len(resultados_nn)

    # Algoritmo genético: varias corridas, porque depende del azar
    print(f"\nEjecutando el algoritmo genético {CORRIDAS_COMPARACION} veces...")
    resultados_ga = []

    for _ in range(CORRIDAS_COMPARACION):
        cromosoma, distancia, historial = ejecutar_genetico(distancias, n)
        resultados_ga.append(distancia)

    mejor_ga = min(resultados_ga)
    peor_ga = max(resultados_ga)
    promedio_ga = sum(resultados_ga) / len(resultados_ga)

    print("\n" + "-" * 55)
    print(f"{'Método':<28}{'Mejor':>8}{'Promedio':>10}{'Peor':>8}")
    print("-" * 55)
    print(f"{'Vecino más cercano':<28}{mejor_nn:>8.0f}{promedio_nn:>10.0f}{peor_nn:>8.0f}")
    print(f"{'Algoritmo genético':<28}{mejor_ga:>8.0f}{promedio_ga:>10.0f}{peor_ga:>8.0f}")
    print("-" * 55)

    print("(distancias en km)")
    print(f"\nMejor partida de la heurística: {mejor_ciudad}")

    diferencia = (mejor_ga - mejor_nn) / mejor_nn * 100

    if diferencia > 0:
        print(f"El mejor del genético es {diferencia:.1f}% más largo que el mejor de la heurística.")
    else:
        print(f"El mejor del genético es {abs(diferencia):.1f}% más corto que el mejor de la heurística.")

    pausa()


def menu():

    while True:

        limpiar_pantalla()

        print("=" * 45)
        print("      TRABAJO PRÁCTICO")
        print("      PROBLEMA DEL VIAJANTE")
        print("=" * 45)

        print("\n1) Mostrar capitales")
        print("2) Vecino más cercano")
        print("3) Mejor recorrido por heurística")
        print("4) Algoritmo genético")
        print("5) Comparar resultados")
        print("0) Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            mostrar_ciudades()

        elif opcion == "2":
            vecino_mas_cercano()

        elif opcion == "3":
            mejor_recorrido_heuristico()

        elif opcion == "4":
            algoritmo_genetico()

        elif opcion == "5":
            comparar()

        elif opcion == "0":
            print("\nHasta luego.")
            break

        else:
            print("\nOpción inválida.")
            pausa()



menu()