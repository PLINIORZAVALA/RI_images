import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ Funciones de procesamiento de imágenes ------------------------

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size=(4, 4)):
    """
    Convierte una imagen en un vector 1D del canal R.
    
    :param image_path: La ruta completa de la imagen.
    :param size: Tamaño al que se redimensionará la imagen, por defecto 4x4.
    :return: Un vector 1D del canal R y el canal R en 2D.
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"No se pudo leer la imagen en {image_path}")
    
    image_resized = cv2.resize(image, size)
    _, _, r_channel = cv2.split(image_resized)
    r_vector = r_channel.flatten()
    
    return r_vector, r_channel

# Función para obtener todos los archivos de imagen en un directorio
def get_image_files(corpus_path, extensions=('.png', '.jpg', '.jpeg')):
    """
    Obtiene todos los archivos de imagen en el directorio especificado.
    
    :param corpus_path: Ruta del directorio donde están las imágenes.
    :param extensions: Extensiones de archivo permitidas.
    :return: Lista de nombres de archivos de imagen.
    """
    return [f for f in os.listdir(corpus_path) if f.endswith(extensions)]

# Función para guardar el DataFrame de una matriz R en un archivo Excel
def save_r_vector_to_excel(r_vector, output_path, image_file, size=(4, 4)):
    """
    Guarda un vector R en un archivo Excel como una matriz.
    
    :param r_vector: Vector del canal R.
    :param output_path: Ruta donde se guardará el archivo Excel.
    :param image_file: Nombre del archivo de imagen (se usará para nombrar el archivo Excel).
    :param size: Tamaño al que se redimensionó la imagen.
    """
    r_matrix = r_vector.reshape(size)
    df_r = pd.DataFrame(r_matrix)
    excel_file = os.path.join(output_path, f'{os.path.splitext(image_file)[0]}_RGB_Vector.xlsx')
    df_r.to_excel(excel_file, index=False, header=False)
    print(f"Archivo guardado en: {excel_file}")

# Función para visualizar el canal R en tonos de rojo
def visualize_r_channel(r_channel, image_file):
    """
    Visualiza el canal R de una imagen en tonos de rojo.
    
    :param r_channel: El canal R de la imagen en formato 2D.
    :param image_file: Nombre del archivo de imagen para el título de la visualización.
    """
    g_channel = np.zeros_like(r_channel)
    b_channel = np.zeros_like(r_channel)
    rgb_image = cv2.merge([b_channel, g_channel, r_channel])
    plt.imshow(rgb_image)
    plt.title(f"Canal R Visualizado en Rojo: {image_file}")
    plt.axis('off')
    plt.show()

# Función principal para procesar imágenes
def process_and_visualize_images(corpus_path, output_path, size=(4, 4)):
    """
    Procesa todas las imágenes en un directorio, convierte su canal R en un vector,
    guarda el resultado en archivos Excel y visualiza el canal R en tonos de rojo.
    
    :param corpus_path: Ruta del directorio donde están las imágenes.
    :param output_path: Ruta donde se guardarán los archivos Excel.
    :param size: Tamaño al que se redimensionarán las imágenes.
    """
    image_files = get_image_files(corpus_path)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)
        r_vector, r_channel = image_to_r_vector(image_path, size)
        save_r_vector_to_excel(r_vector, output_path, image_file, size)
        visualize_r_channel(r_channel, image_file)

# ------------------------ Funciones de cálculo de estadísticas ------------------------

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
    """
    Procesa todos los archivos Excel de vectores R, calcula sus estadísticas y guarda los resultados.
    
    :param input_path: Ruta donde se guardaron los archivos Excel de los vectores de imágenes.
    :param output_path: Ruta donde se guardarán los resultados estadísticos de cada archivo.
    """
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

# ------------------------ Función principal que orquesta todo el flujo ------------------------

def main():
    corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'
    output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.2.dataImages'
    image_size = (4, 4)
    
    # Procesar todas las imágenes, guardar sus vectores R y visualizarlas
    process_and_visualize_images(corpus_path, output_path, image_size)
    
    # Procesar los archivos Excel de vectores R y calcular sus estadísticas
    stats_output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.3.dataStadictist'
    process_r_vectors_and_calculate_statistics(output_path, stats_output_path)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
