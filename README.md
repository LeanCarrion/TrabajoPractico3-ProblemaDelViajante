# Trabajo Práctico: El Problema del Viajante (TSP)

Este proyecto implementa diferentes soluciones para el **Problema del Viajante de Comercio (TSP)** aplicado a las capitales de las provincias de la República Argentina. Se evalúan enfoques exhaustivos (análisis teórico), heurísticos (Vecino Más Cercano) y metaheurísticos (Algoritmos Genéticos).

## 👥 Colaboradores
* **Leandro Carrion Lescano**
* **Agustin Gregoret**
* **Marcos Subira**

---

## 📝 Descripción del Problema
El TSP busca encontrar la ruta óptima que, comenzando y terminando en una ciudad específica, visite exactamente una vez un conjunto de $N$ ciudades y minimice la distancia total recorrida.

Se trabaja con **24 ciudades**: las capitales de las 23 provincias (incluida La Plata) más la Ciudad Autónoma de Buenos Aires. Las distancias provienen de la tabla de capitales de la cátedra y son **distancias en línea recta** entre ciudades.

### 1. Resolución por Método Exhaustivo (Justificación Teórica)
**¿Se puede resolver el problema para Argentina usando un método exhaustivo?**
**No de manera eficiente ni en un tiempo físicamente razonable.**

Para un problema simétrico de $N = 24$ ciudades, con la ciudad de partida fija, el número de rutas posibles a evaluar es:

$$\frac{(N-1)!}{2} = \frac{23!}{2} \approx 1{,}29 \times 10^{22} \text{ combinaciones}$$

Incluso con una supercomputadora capaz de evaluar **1.000 millones de rutas por segundo**, tardaría unos **410.000 años** en encontrar la solución exacta. Agregar una sola ciudad multiplica el número de rutas por $N$, por lo que el problema crece de forma factorial. El enfoque exhaustivo es computacionalmente inviable ($NP\text{-hard}$), lo que justifica el uso de heurísticas y algoritmos genéticos.

---

## 🚀 Características del Programa (Menú)
El programa tiene un menú interactivo con las siguientes opciones:

1. **Mostrar capitales:** lista las 24 ciudades cargadas desde el archivo de distancias.
2. **Vecino más cercano (desde un origen):** permite elegir una capital de inicio. Calcula el recorrido con la heurística *"desde cada ciudad ir a la ciudad más cercana no visitada y regresar al origen"*. Muestra la ciudad de partida, el recorrido completo, la distancia total y un **mapa de la República** con el recorrido.
3. **Mejor recorrido por heurística:** aplica el vecino más cercano desde todas las capitales como origen y determina cuál de todos los recorridos es el de menor distancia.
4. **Algoritmo genético:** busca la ruta de distancia mínima mediante evolución simulada. Muestra el mejor recorrido, su distancia y un gráfico de la mejor distancia por ciclo.
5. **Comparar resultados:** ejecuta la heurística desde todas las ciudades y el algoritmo genético varias veces, y muestra una tabla con el mejor, el promedio y el peor resultado de cada método.

### 🧬 Parámetros del Algoritmo Genético
* **Tamaño de población (N):** 50 cromosomas.
* **Cantidad de ciclos (M):** 200.
* **Cromosoma:** permutación de los números naturales del 1 al 24, donde cada gen representa una capital única.
* **Función de aptitud:** distancia total del circuito cerrado (se busca minimizarla).
* **Selección:** torneo de tamaño 3.
* **Cruzamiento:** crossover cíclico (CX), que preserva las permutaciones y evita ciudades repetidas. Probabilidad de crossover: **0,9**.
* **Mutación:** intercambio de dos genes al azar. Probabilidad de mutación: **0,1**.
* **Elitismo:** los 2 mejores cromosomas pasan sin cambios a la siguiente generación.

---

## 📊 Resultados de Referencia
Resultado de una ejecución de la opción 5 (el algoritmo genético se corrió 10 veces; los valores del genético cambian entre ejecuciones por el azar):

| Método | Mejor (km) | Promedio (km) | Peor (km) |
|---|---|---|---|
| Vecino más cercano | 9335 | 10159 | 11031 |
| Algoritmo genético | 10273 | 11042 | 12034 |

La mejor partida de la heurística es Neuquén.

---

## 📌 Aportes Prácticos del TSP en el Mundo Real
Actualmente, el TSP no es solo un problema teórico; se aplica activamente en:

1. **Logística y Distribución de Última Milla:** las empresas de mensajería y comercio electrónico utilizan variantes del TSP para planificar las rutas diarias de sus vehículos de reparto, reduciendo el consumo de combustible y los tiempos de entrega.
2. **Fabricación de Circuitos Impresos (PCB):** en la industria electrónica, los brazos robóticos deben perforar miles de agujeros en una placa de circuito. El orden en que el robot visita cada punto se optimiza como un TSP para minimizar el movimiento del cabezal y acelerar la producción en masa.

---

## 🗂️ Estructura del Proyecto
```
TrabajoPractico3-ProblemaDelViajante/
├── TpN°3.py                       # Programa principal
├── TablaCapitales_completa.xlsx   # Matriz de distancias entre las 24 ciudades
├── mapa/                          # Shapefile de Natural Earth (límites de Argentina)
├── requirements.txt               # Dependencias
└── README.md
```

El mapa usa los límites de la capa *Admin 0 – Countries (Argentina POV)* de Natural Earth.

---

## 🛠️ Instalación y Ejecución
1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias (pandas, openpyxl, matplotlib y geopandas):
```bash
   python -m pip install -r requirements.txt
```
3. Ejecuta el programa principal (desde la carpeta del proyecto):
```bash
   python "TpN°3.py"
```