# Trabajo Práctico: El Problema del Viajante (TSP)

Este proyecto implementa diferentes soluciones para el **Problema del Viajante de Comercio (TSP)** aplicado a las capitales de las provincias de la República Argentina. Se evalúan enfoques exhaustivos, heurísticos (Vecino Más Cercano) y metaheurísticos (Algoritmos Genéticos).

## 👥 Colaboradores
* **Leandro Carrion Lescano**
* **Agustin Gregoret**
* **Marcos Subira**

---

## 📝 Descripción del Problema
El TSP busca encontrar la ruta óptima que, comenzando y terminando en una ciudad específica, visite exactamente una vez un conjunto de $N$ ciudades y minimice la distancia total recorrida.

### 1. Resolución por Método Exhaustivo (Justificación Teórica)
**¿Se puede resolver el problema para Argentina usando un método exhaustivo?**
**No de manera eficiente ni en un tiempo físicamente razonable.** 

Argentina cuenta con **23 capitales provinciales** (sin contar CABA como origen independiente o sumando 23 nodos en total). Para un problema simétrico de 23 ciudades, el número de rutas posibles a evaluar es de:
$$\frac{(N-1)!}{2} = \frac{22!}{2} \approx 5.62 \times 10^{20} \text{ combinaciones}$$

Incluso con una supercomputadora capaz de evaluar **1.000 millones de rutas por segundo**, tardaría más de **17.800 años** en encontrar la solución exacta. Por lo tanto, el enfoque exhaustivo es computacionalmente inviable ($NP\text{-hard}$), lo que justifica el uso de heurísticas y algoritmos genéticos.

---

## 🚀 Características del Programa (Menú)
El software cuenta con una interfaz de menús para ejecutar las siguientes opciones:

* **Opción A (Heurística desde origen):** Permite seleccionar una capital de inicio. Calcula el recorrido usando la heurística: *"Desde cada ciudad ir a la ciudad más cercana no visitada y regresar al origen"*. Muestra el mapa, el recorrido completo y la longitud total.
* **Opción B (Mejor Heurística Global):** Evalúa la heurística del vecino más cercano para todas las capitales como origen y determina cuál de todos los recorridos es el mínimo global.
* **Opción C (Algoritmo Genético):** Encuentra la ruta óptima utilizando evolución biológica simulada.

### 🧬 Parámetros del Algoritmo Genético
* **Tamaño de Población (N):** 50 cromosomas.
* **Cantidad de Ciclos / Generaciones (M):** 200 iteraciones.
* **Estructura del Cromosoma:** Permutaciones de 23 números naturales (1 al 23), donde cada gen representa una capital única.
* **Operador de Cruzamiento:** Crossover Cíclico (CX) para preservar el orden y evitar duplicados de ciudades.

---

## 📌 Aportes Prácticos del TSP en el Mundo Real
Actualmente, el TSP no es solo un problema teórico; se aplica activamente en:

1. **Logística y Distribución de Última Milla:** Empresas de mensajería (como Mercado Libre o Correo Argentino) utilizan variantes del TSP para planificar las rutas diarias de sus camiones de reparto, reduciendo drásticamente el consumo de combustible y los tiempos de entrega.
2. **Fabricación de Circuitos Impresos (PCB):** En la industria electrónica, los brazos robóticos deben perforar miles de agujeros en una placa de circuito. El orden en que el robot visita cada punto se optimiza como un TSP para minimizar el movimiento del cabezal y acelerar la producción en masa.

---

## 🛠️ Instalación y Ejecución
1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias (ej. matplotlib para los mapas):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el programa principal:
   ```bash
   python main.py
   ```
