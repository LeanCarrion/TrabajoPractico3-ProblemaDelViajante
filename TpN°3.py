import os


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresione ENTER para continuar...")


def mostrar_ciudades():
    limpiar_pantalla()

    print("========================================")
    print("       CAPITALES DE ARGENTINA")
    print("========================================")

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

    for i in range(len(ciudades)):
        print(f"{i + 1}) {ciudades[i]}")

    pausa()


def vecino_mas_cercano():
    limpiar_pantalla()

    print("========================================")
    print("       VECINO MÁS CERCANO")
    print("========================================")

    print("\nSeleccione la ciudad de partida:\n")

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

    for i in range(len(ciudades)):
        print(f"{i + 1}) {ciudades[i]}")

    opcion = input("\nOpción: ")

    if opcion.isdigit() and 1 <= int(opcion) <= len(ciudades):
        ciudad = ciudades[int(opcion) - 1]

        print(f"\nCiudad de partida: {ciudad}")
        print("\nEl algoritmo de vecino más cercano se implementará aquí.")

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