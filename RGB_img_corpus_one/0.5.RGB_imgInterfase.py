import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox


# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"No se pudo leer la imagen en {image_path}")
    
    image_resized = cv2.resize(image, size)
    _, _, r_channel = cv2.split(image_resized)
    r_vector = r_channel.flatten()
    
    return r_vector, r_channel


def get_image_files(corpus_path, extensions=('.png', '.jpg', '.jpeg')):
    return [f for f in os.listdir(corpus_path) if f.endswith(extensions)]


def save_r_vector_to_excel(r_vector, output_path, image_file, size):
    height, width = size
    df_r = pd.DataFrame(r_vector.reshape((height, width)))
    excel_file = os.path.join(output_path, f'{os.path.splitext(image_file)[0]}_RGB_Vector.xlsx')
    df_r.to_excel(excel_file, index=False, header=False)
    print(f"Archivo guardado en: {excel_file}")


def save_r_channel_image(r_channel, image_file, output_dir):
    g_channel = np.zeros_like(r_channel)
    b_channel = np.zeros_like(r_channel)
    rgb_image = cv2.merge([b_channel, g_channel, r_channel])
    output_image_file = os.path.join(output_dir, f'{os.path.splitext(image_file)[0]}_R_Channel.png')
    cv2.imwrite(output_image_file, rgb_image)
    print(f"Imagen guardada en: {output_image_file}")


def process_and_visualize_images(corpus_path, output_path, size):
    image_files = get_image_files(corpus_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    r_channel_dir = os.path.join(output_path, "R_Channel_Images")
    if not os.path.exists(r_channel_dir):
        os.makedirs(r_channel_dir)

    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)
        r_vector, r_channel = image_to_r_vector(image_path, size)
        save_r_vector_to_excel(r_vector, output_path, image_file, size)
        save_r_channel_image(r_channel, image_file, r_channel_dir)

# Función para calcular estadísticas de un DataFrame
def calculate_statistics(df):

    resultados = {
        'Suma': df.sum(axis=1),
        'Media': df.mean(axis=1),
        'Mediana': df.median(axis=1),
        'Moda': df.mode(axis=1)[0],
        'Varianza': df.var(axis=1),
        'Desviación Estándar': df.std(axis=1),
        'Rango': df.max(axis=1) - df.min(axis=1),
        'Mínimo': df.min(axis=1),
        'Máximo': df.max(axis=1),
        'Cuartil 1': df.quantile(0.25, axis=1),
        'Cuartil 2': df.quantile(0.5, axis=1),
        'Cuartil 3': df.quantile(0.75, axis=1),
    }

    return pd.DataFrame(resultados)

# Función para guardar un DataFrame de estadísticas en un archivo Excel
def save_statistics_to_excel(estadisticas_df, output_file):

    estadisticas_df.to_excel(output_file, index=False)
    print(f"Archivo de estadísticas guardado en: {output_file}")

# =========== Segmento para obtener los valores estadisticos de los vectores ===============

# Función para procesar los archivos Excel de vectores R y calcular sus estadísticas
def process_r_vectors_and_calculate_statistics(input_path, output_path):
    
    excel_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    for excel_file in excel_files:
        excel_path = os.path.join(input_path, excel_file)
        df = pd.read_excel(excel_path, header=None)

        # Calcular estadísticas
        estadisticas_df = calculate_statistics(df)

        # Crear la ruta de salida para el archivo de estadísticas
        output_file = os.path.join(output_path, f"Estadisticas_{excel_file}")

        # Guardar el DataFrame de estadísticas en un archivo Excel
        save_statistics_to_excel(estadisticas_df, output_file)

# ================= Segmento para evaluar los datos estadisticos ===========================

# Función para calcular la regresión lineal
def calcular_regresion(X, Y):
    slope, intercept, r_value, _, _ = stats.linregress(X, Y)
    linea_regresion = [slope * xi + intercept for xi in X]
    return slope, intercept, r_value, linea_regresion

# Función para calcular las distancias entre los puntos y la línea de regresión
def calcular_distancias(Y, linea_regresion):
    distancias = [yi - pred for yi, pred in zip(Y, linea_regresion)]
    return distancias    

# Función para graficar los datos y la línea de regresión
def graficar_regresion(X, Y, linea_regresion, slope, intercept, r_value, output_file):
    plt.scatter(X, Y, color='blue', label='Datos')
    plt.plot(X, linea_regresion, color='red', label=f'Regresión Lineal (R²={r_value**2:.2f})')
    formula = f"Y = {slope:.2f}X + {intercept:.2f}"
    plt.text(0.1 * max(X), max(Y) * 0.9, formula, fontsize=12, color='green')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Regresión Lineal de X e Y')
    plt.legend()
    plt.savefig(output_file)
    plt.close()
    
def process_r_vectors_and_calculate_statistics_result(input_path, output_path, column):
    excel_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Crear un dataframe vacío para almacenar todas las estadísticas
    all_stats = pd.DataFrame()

    for excel_file in excel_files:
        excel_path = os.path.join(input_path, excel_file)
        df = pd.read_excel(excel_path)

        # Verificar si el nombre de la columna es un índice o nombre
        if isinstance(column, int):
            if column >= len(df.columns):
                continue
        elif column not in df.columns:
            continue
        
        # Filtrar los datos para asegurarse de que sean numéricos
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

        # Guardar la gráfica en la carpeta de salida
        output_image = os.path.join(output_path, f"Regresion_{excel_file.replace('.xlsx', '.png')}")
        graficar_regresion(X, Y, linea_regresion, slope, intercept, r_value, output_image)

        # Guardar resultados en el archivo de texto
        output_txt = os.path.join(output_path, f"Resultados_{excel_file.replace('.xlsx', '.txt')}")
        with open(output_txt, 'w') as f:
            f.write(f"Archivo procesado: {excel_file}\n")
            f.write(f"Coeficiente de correlación (R^2): {r_value}\n")
            f.write(f"Ecuación de la recta: Y = {slope:.2f}X + {intercept:.2f}\n")
            f.write(f"Distancias: {distancias}\n")
            f.write(f"Gráfica guardada en: {output_image}\n")

        # Almacenar las estadísticas en el dataframe all_stats
        all_stats = all_stats.append({
            'Archivo': excel_file,
            'Coeficiente de correlación': r_value,
            'Pendiente': slope,
            'Intersección': intercept
        }, ignore_index=True)
    
    # Guardar todas las estadísticas en un archivo Excel
    output_excel = os.path.join(output_path, 'Estadisticas_Resumen.xlsx')
    all_stats.to_excel(output_excel, index=False)

    messagebox.showinfo("Éxito", f"Evaluación estadística procesada y guardada en {output_path}.")

# Interfaz gráfica con tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proceso de determinación de imagen")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.images_processed = False  # Bandera para verificar si las imágenes han sido procesadas
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("arial", 16))
        style.configure("TEntry", font=("arial", 16))

        # Botón para cargar la carpeta de imágenes
        load_button = ttk.Button(self.root, text="Seleccionar carpeta de imágenes", style="TButton", command=self.select_corpus_folder)
        load_button.pack(pady=10)

        # Campos de entrada para ancho y alto de la imagen
        self.width_entry = ttk.Entry(self.root, font=("arial", 16))
        self.width_entry.pack(pady=10)
        self.width_entry.insert(0, "Ancho")

        self.height_entry = ttk.Entry(self.root, font=("arial", 16))
        self.height_entry.pack(pady=10)
        self.height_entry.insert(0, "Altura")

        # Botón para procesar imágenes
        process_button = ttk.Button(self.root, text="Seleccionar carpeta para almacenar vectores", style="TButton", command=self.process_images)
        process_button.pack(pady=10)
        
        # Botón para procesar los datos procesados de la imágenes (Obtención de valores estadísticos)
        process_button_data = ttk.Button(self.root, text="Obtener datos estadísticos", style="TButton", command=self.process_dataImages)
        process_button_data.pack(pady=10)

        # Campos de entrada para colocar el nombre de la columna del excel
        self.colum_entry = ttk.Entry(self.root, font=("arial", 16))
        self.colum_entry.pack(pady=10)
        self.colum_entry.insert(0, "Nombre columna")
        
        # Botón para procesar los datos estadisticos (Obtención de evaluacion de datos estadísticos)
        evaluation_button_stadist = ttk.Button(self.root, text="Obtener Evaluar estadístico", style="TButton", command=self.evalucion_estadistico)
        evaluation_button_stadist.pack(pady=10)
        
        # Canvas para mostrar documentos del corpus
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame = tk.Frame(self.canvas, bg='gray')
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Botón para salir de pantalla completa con la tecla Escape
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def select_corpus_folder(self):
        self.corpus_path = filedialog.askdirectory()
        if not self.corpus_path:
            messagebox.showwarning("Error", "No seleccionaste ninguna carpeta.")
        else:
            self.list_images()

    def list_images(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        image_files = get_image_files(self.corpus_path)

        if image_files:
            for image_file in image_files:
                image_label = tk.Label(self.frame, text=image_file, fg="white", cursor="hand2", bg='gray', font=("arial", 16))
                image_label.pack(anchor='w', pady=2)
        else:
            empty_label = tk.Label(self.frame, text="No se encontraron imágenes en la carpeta.", fg="white", bg='gray', font=("arial", 16))
            empty_label.pack(anchor='w', pady=2)

    def process_images(self):
        if not hasattr(self, 'corpus_path') or not self.corpus_path:
            messagebox.showerror("Error", "No se ha seleccionado una carpeta de imágenes.")
            return
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            image_size = (height, width)
            
            output_path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
            if not output_path:
                messagebox.showwarning("Error", "No seleccionaste ninguna carpeta de salida.")
                return

            process_and_visualize_images(self.corpus_path, output_path, image_size)
            self.images_processed = True  # Marcar que las imágenes han sido procesadas
            messagebox.showinfo("Éxito", "Imágenes procesadas correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ancho y altura deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def process_dataImages(self):
        if self.images_processed:  # Solo permite procesar datos si las imágenes ya fueron procesadas
            input_path = filedialog.askdirectory(title="Seleccionar carpeta de vectores R")
            output_path = filedialog.askdirectory(title="Seleccionar carpeta de salida para estadísticas")
            process_r_vectors_and_calculate_statistics(input_path, output_path)
            messagebox.showinfo("Éxito", "Estadísticas procesadas correctamente.")
            self.stadit_processed = True
        else:
            messagebox.showwarning("Error", "Debes procesar las imágenes primero antes de calcular estadísticas.")

    def evalucion_estadistico(self):
        try:
            colum_input = self.colum_entry.get()  # Obtiene la entrada (puede ser nombre o índice)
            if colum_input.isdigit():
                colum = int(colum_input)  # Si es un número, conviértelo a entero
            else:
                colum = colum_input  # Si no es un número, se asume que es un nombre de columna
                
            input_path = filedialog.askdirectory(title="Seleccionar carpeta donde se encuentra los valores estadisticos")
            output_path = filedialog.askdirectory(title="Seleccionar carpeta de salida para evaluación de datos estadísticos")
            if not output_path:
                messagebox.showwarning("Error", "No seleccionaste ninguna carpeta de salida.")
                return

            process_r_vectors_and_calculate_statistics_result(input_path, output_path, colum)
            messagebox.showinfo("Éxito", "Evaluación estadística procesada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "La columna ingresada tiene que coincidir con el Excel.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
