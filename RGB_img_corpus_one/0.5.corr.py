import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Función para generar los datos X e Y
def generar_datos():
    Y = [
        255, 255, 255, 255, 254.97, 254.62, 253.28, 250.08, 242.76, 232.59,
        222.22, 214.68, 213.47, 212.78, 212, 212.58, 212.68, 211.92, 212.06,
        212.77, 212.85, 213.08, 213.46, 214.62, 211.31, 184.9, 182.34, 198.37,
        201.77, 203.64, 208.11, 216.1, 224.25, 224.1, 227.06, 230.3, 231.09,
        230.77, 229.15, 237.27, 240.22, 240.57, 241.1, 241.5, 241.67, 241.81,
        241.84, 241.81, 241.79, 241.84, 242, 241.88, 241.66, 240.92, 240.58,
        240.93, 241.16, 241.25, 241.16, 240.96, 240.86, 240.88, 240.96, 241.04,
        241.1, 241.06, 241.18, 241.3, 241.3, 241.15, 241.14, 241.06, 241.23,
        241.52, 241.35, 241.56, 241.34, 241.12, 241.4, 241.53, 241.54, 241.45,
        241.58, 241.44, 241.58, 241.18, 241.05, 241.06, 240.82, 240.27, 238.5,
        230.32, 221.56, 230.95, 242.11, 253.36, 255, 255, 255, 255
    ]
    X = list(range(1, len(Y) + 1))
    return X, Y

# Función para calcular la regresión lineal
def calcular_regresion(X, Y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    linea_regresion = [slope * xi + intercept for xi in X]
    return slope, intercept, r_value, linea_regresion

# Función para calcular las distancias entre los puntos y la línea de regresión
def calcular_distancias(Y, linea_regresion):
    distancias = [yi - pred for yi, pred in zip(Y, linea_regresion)]
    return distancias

# Función para graficar los datos y la línea de regresión
def graficar_regresion(X, Y, linea_regresion, slope, intercept, r_value):
    plt.scatter(X, Y, color='blue', label='Datos')
    plt.plot(X, linea_regresion, color='red', label=f'Regresión Lineal (R²={r_value**2:.2f})')

    # Añadir la fórmula de la línea de regresión en la gráfica
    formula = f"Y = {slope:.2f}X + {intercept:.2f}"
    plt.text(10, max(Y) - 10, formula, fontsize=12, color='green')

    # Etiquetas y título
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Regresión Lineal de X e Y')
    plt.legend()

    # Mostrar la gráfica
    plt.show()

# Función principal para ejecutar todo el proceso
def main():
    # Generar datos
    X, Y = generar_datos()
    
    # Calcular la regresión lineal
    slope, intercept, r_value, linea_regresion = calcular_regresion(X, Y)
    
    # Calcular las distancias entre los puntos y la línea de regresión
    distancias = calcular_distancias(Y, linea_regresion)

    # Graficar los resultados
    graficar_regresion(X, Y, linea_regresion, slope, intercept, r_value)
    
    # Imprimir resultados
    print(f"Coeficiente de correlación: {r_value}")
    print(f"Ecuación de la recta: Y = {slope:.2f}X + {intercept:.2f}")
    print("Distancias entre los puntos y la línea de regresión:")
    print(distancias)

# Ejecutar el programa
main()
