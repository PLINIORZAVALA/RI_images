import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from scipy import stats

# Función para calcular la regresión lineal
def calcular_regresion(X, Y):
    slope, intercept, r_value, _, _ = stats.linregress(X, Y)
    linea_regresion = [slope * xi + intercept for xi in X]
    return slope, intercept, r_value, linea_regresion

# Función para calcular las distancias entre los puntos y la línea de regresión
def calcular_distancias(Y, linea_regresion):
    distancias = [yi - pred for yi, pred in zip(Y, linea_regresion)]
    return distancias  

# Función para procesar los archivos Excel y obtener los datos
def process_excel_files(input_path, output_path, column):
    excel_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Crear un dataframe vacío para almacenar todas las estadísticas y distancias
    all_data = pd.DataFrame()

    for excel_file in excel_files:
        excel_path = os.path.join(input_path, excel_file)
        df = pd.read_excel(excel_path)

        # Verificar si la columna es válida
        if isinstance(column, int):
            if column >= len(df.columns):
                continue
        elif column not in df.columns:
            continue

        # Extraer la columna seleccionada y asegurarse de que los datos sean numéricos
        if isinstance(column, int):
            data = pd.to_numeric(df.iloc[:, column], errors='coerce').dropna()
        else:
            data = pd.to_numeric(df[column], errors='coerce').dropna()

        # Evitar procesar si no hay datos válidos
        if data.empty:
            continue

        X = list(range(1, len(data) + 1))
        Y = data.tolist()

        # Calcular la regresión lineal
        slope, intercept, r_value, linea_regresion = calcular_regresion(X, Y)

        # Calcular las distancias entre los puntos y la línea de regresión
        distancias = calcular_distancias(Y, linea_regresion)

        # Guardar los datos en el dataframe all_data
        all_data[f"{excel_file}_Y"] = Y  # Los valores originales
        all_data[f"{excel_file}_Distancias"] = distancias  # Las distancias

        # Almacenar las estadísticas (pendiente, intersección, R^2)
        all_data[f"{excel_file}_Pendiente"] = [slope] * len(Y)
        all_data[f"{excel_file}_Intersección"] = [intercept] * len(Y)
        all_data[f"{excel_file}_Coeficiente_R2"] = [r_value**2] * len(Y)

    # Guardar los resultados en un archivo Excel
    output_excel = os.path.join(output_path, 'Resultados_Columnas_y_Distancias.xlsx')
    all_data.to_excel(output_excel, index=False)

    messagebox.showinfo("Éxito", f"Datos procesados y guardados en {output_path}.")

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
        style.configure("TEntry", font=("arial", 16))

        # Campo de entrada para el nombre o índice de la columna
        self.colum_entry = ttk.Entry(self.root, font=("arial", 16))
        self.colum_entry.pack(pady=10)
        self.colum_entry.insert(0, "Nombre o índice de columna")

        # Botón para procesar los archivos Excel
        process_button = ttk.Button(self.root, text="Procesar archivos Excel", style="TButton", command=self.process_files)
        process_button.pack(pady=10)

        # Botón para salir de pantalla completa con la tecla Escape
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def process_files(self):
        try:
            column_input = self.colum_entry.get()  # Obtener el valor de la columna ingresada
            if column_input.isdigit():
                column = int(column_input)  # Convertir a entero si es un número
            else:
                column = column_input  # Usar el nombre de la columna

            input_path = filedialog.askdirectory(title="Seleccionar carpeta de entrada")
            output_path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
            if not output_path:
                messagebox.showwarning("Error", "No seleccionaste ninguna carpeta de salida.")
                return

            process_excel_files(input_path, output_path, column)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
