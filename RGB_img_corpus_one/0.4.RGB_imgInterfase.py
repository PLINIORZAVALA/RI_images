import cv2
import numpy as np
import os
import pandas as pd
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
        try:
            r_vector, r_channel = image_to_r_vector(image_path, size)
            save_r_vector_to_excel(r_vector, output_path, image_file, size)
            save_r_channel_image(r_channel, image_file, r_channel_dir)
        except Exception as e:
            print(f"Error procesando {image_file}: {e}")


# Función para calcular estadísticas de un DataFrame
def calculate_statistics(df):
    """
    Calcula varias estadísticas para cada fila de un DataFrame.
    
    :param df: DataFrame con los datos de entrada.
    :return: Un DataFrame con las estadísticas calculadas.
    """
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
    """
    Guarda un DataFrame en un archivo Excel.
    
    :param estadisticas_df: DataFrame con las estadísticas calculadas.
    :param output_file: Ruta completa del archivo Excel de salida.
    """
    estadisticas_df.to_excel(output_file, index=False)
    print(f"Archivo de estadísticas guardado en: {output_file}")
    
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
        process_button = ttk.Button(self.root, text="Seleccionar carpeta de procesar imágenes", style="TButton", command=self.process_images)
        process_button.pack(pady=10)
        
        # Botón para procesar los datos procesados de la imágenes (Obtención de valores estadísticos)
        process_button_data = ttk.Button(self.root, text="Obtener datos estadísticos", style="TButton", command=self.process_dataImages)
        process_button_data.pack(pady=10)

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
        else:
            messagebox.showwarning("Error", "Debes procesar las imágenes primero antes de calcular estadísticas.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()