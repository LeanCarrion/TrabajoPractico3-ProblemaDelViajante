import os
import pandas as pd


ARCHIVO_DISTANCIAS = "TablaCapitales.xlsx"

ciudades = [
    "Buenos Aires",
    "Catamarca",
    "Córdoba",
    "Corrientes",
    "Resistencia",
    "Formosa",
    "San Salvador de Jujuy",
    "Santa Rosa",
    "La Rioja",
    "Mendoza",
    "Posadas",
    "Neuquén",
    "Paraná",
    "Salta",
    "San Juan",
    "San Luis",
    "Río Gallegos",
    "Santa Fe",
    "Santiago del Estero",
    "Rawson",
    "San Miguel de Tucumán",
    "Ushuaia",
    "Viedma"
]

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresione ENTER para continuar...")


# Agregó funcion para leer el xlsx

def cargar_distancias():
    matriz = pd.read_excel(ARCHIVO_DISTANCIAS, index_col=0)

    # Nos quedamos solamente con las filas correspondientes a ciudades
    matriz = matriz.iloc[:24]

    # Unificamos los nombres de las filas con los nombres de las columnas
    matriz.index = matriz.columns

    return matriz


# Esto sirve para ver si lee las ciudades y distancias correctamente

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

    else:
        print("\nOpción inválida.")

    pausa()

def mejor_recorrido_heuristico():
    limpiar_pantalla()

    print("========================================")
    print("     MEJOR RECORRIDO - HEURÍSTICA")
    print("========================================")

    print("\nAquí se ejecutará el vecino más cercano")
    print("comenzando desde las 23 ciudades.")

    pausa()


def algoritmo_genetico():
    limpiar_pantalla()

    print("========================================")
    print("         ALGORITMO GENÉTICO")
    print("========================================")

    print("\nParámetros del problema:")
    print("Cantidad de cromosomas: 50")
    print("Cantidad de ciclos: 200")
    print("Cantidad de ciudades: 23")
    print("Crossover: Cíclico")

    print("\nEl algoritmo genético se implementará aquí.")

    pausa()


def comparar():
    limpiar_pantalla()

    print("========================================")
    print("          COMPARACIÓN DE MÉTODOS")
    print("========================================")

    print("\nAquí se mostrarán los resultados de:")
    print("- Vecino más cercano")
    print("- Algoritmo genético")

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