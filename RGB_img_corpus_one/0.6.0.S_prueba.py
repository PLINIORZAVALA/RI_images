import os
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from scipy import stats

# Función para calcular regresión y obtener desviación estándar de residuos
def calcular_regresion_y_desviacion(X, Y):
    slope, intercept, _, _, _ = stats.linregress(X, Y)
    Y_pred = intercept + slope * X
    residuos = Y - Y_pred
    desviacion_estandar = np.std(residuos)
    return slope, intercept, desviacion_estandar

# Función para procesar y graficar cada columna con sus líneas de confianza
def procesar_y_graficar(input_excel, output_dir):
    df = pd.read_excel(input_excel)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for column in df.columns:
        # Convertir la columna a datos numéricos
        data = pd.to_numeric(df[column], errors='coerce').dropna()
        
        # Evitar procesar si la columna no tiene datos válidos
        if data.empty:
            continue
        
        X = np.arange(len(data))  # Eje X es el índice de los datos
        Y = data.values  # Valores Y de la columna

        # Calcular regresión y desviación estándar
        slope, intercept, sigma_e = calcular_regresion_y_desviacion(X, Y)

        # Calcular las líneas de confianza
        y_reg = intercept + slope * X
        y_upper_68 = (intercept + sigma_e) + slope * X
        y_lower_68 = (intercept - sigma_e) + slope * X
        y_upper_95 = (intercept + 2 * sigma_e) + slope * X
        y_lower_95 = (intercept - 2 * sigma_e) + slope * X
        y_upper_997 = (intercept + 3 * sigma_e) + slope * X
        y_lower_997 = (intercept - 3 * sigma_e) + slope * X

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(X, Y, 'o', label='Datos', markersize=5)
        plt.plot(X, y_reg, 'r-', label=f'Regresión: y = {intercept:.2f} + {slope:.2f}x')
        plt.plot(X, y_upper_68, 'g--', label='68% (+1σ)')
        plt.plot(X, y_lower_68, 'g--', label='68% (-1σ)')
        plt.plot(X, y_upper_95, 'b--', label='95% (+2σ)')
        plt.plot(X, y_lower_95, 'b--', label='95% (-2σ)')
        plt.plot(X, y_upper_997, 'y--', label='99.7% (+3σ)')
        plt.plot(X, y_lower_997, 'y--', label='99.7% (-3σ)')
        
        # Etiquetas y título
        plt.title(f'Columna: {column}')
        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.legend()
        
        # Guardar la gráfica
        output_path = os.path.join(output_dir, f'Grafico_{column}.png')
        plt.savefig(output_path)
        plt.close()

    messagebox.showinfo("Éxito", f"Gráficas generadas y guardadas en {output_dir}.")

# Interfaz gráfica con tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proceso de selección de columnas de Excel")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("arial", 16))
        style.configure("TLabel", font=("arial", 16), background='black', foreground='white')
        
        # Etiqueta de instrucciones
        ttk.Label(self.root, text="Seleccione el archivo Excel y carpeta de salida", style="TLabel").pack(pady=20)

        # Botón para seleccionar archivo de entrada
        self.select_input_button = ttk.Button(self.root, text="Seleccionar archivo Excel", style="TButton", command=self.select_input_file)
        self.select_input_button.pack(pady=10)

        # Botón para seleccionar carpeta de salida
        self.select_output_button = ttk.Button(self.root, text="Seleccionar carpeta de salida", style="TButton", command=self.select_output_folder)
        self.select_output_button.pack(pady=10)

        # Botón para procesar y graficar
        self.process_button = ttk.Button(self.root, text="Procesar y Graficar", style="TButton", command=self.process_files)
        self.process_button.pack(pady=20)

        # Inicializar variables de archivo y carpeta
        self.input_file = None
        self.output_folder = None

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not self.input_file:
            messagebox.showwarning("Advertencia", "No se seleccionó un archivo de entrada.")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if not self.output_folder:
            messagebox.showwarning("Advertencia", "No se seleccionó una carpeta de salida.")

    def process_files(self):
        if not self.input_file:
            messagebox.showwarning("Error", "Selecciona un archivo Excel de entrada.")
            return
        if not self.output_folder:
            messagebox.showwarning("Error", "Selecciona una carpeta de salida.")
            return
        try:
            procesar_y_graficar(self.input_file, self.output_folder)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
