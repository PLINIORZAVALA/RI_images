import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size):
    """
    Convierte una imagen en un vector 1D del canal R.
    
    :param image_path: La ruta completa de la imagen.
    :param size: Tamaño al que se redimensionará la imagen.
    :return: Un vector 1D del canal R y el canal R en 2D.
    """
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"No se pudo leer la imagen en {image_path}")
    
    # Redimensionar la imagen a un tamaño fijo
    image_resized = cv2.resize(image, size)
    
    # Separar la imagen en los tres canales B, G, R (OpenCV usa BGR por defecto)
    _, _, r_channel = cv2.split(image_resized)
    
    # Aplanar el canal R en un vector 1D
    r_vector = r_channel.flatten()
    
    return r_vector, r_channel

# Función para obtener todos los archivos de imagen en un directorio
def get_image_files(corpus_path, extensions=('.png', '.jpg', '.jpeg')):
    """
    Obtiene todos los archivos de imagen en el directorio especificado.
    
    :param corpus_path: Ruta del directorio donde están las imágenes.
    :param extensions: Extensiones de archivo permitidas (por defecto: .png, .jpg, .jpeg).
    :return: Lista de nombres de archivos de imagen.
    """
    return [f for f in os.listdir(corpus_path) if f.endswith(extensions)]

# Función para guardar el DataFrame de una matriz R en un archivo Excel
def save_r_vector_to_excel(r_vector, output_path, image_file, size):
    """
    Guarda un vector R en un archivo Excel como una matriz.
    
    :param r_vector: Vector del canal R.
    :param output_path: Ruta donde se guardará el archivo Excel.
    :param image_file: Nombre del archivo de imagen (se usará para nombrar el archivo Excel).
    :param size: Tamaño de la imagen (ancho y alto).
    """
    # Calcular el número de filas y columnas según el tamaño de la imagen
    height, width = size
    df_r = pd.DataFrame(r_vector.reshape((height, width)))  # Cambiar el tamaño según la imagen

    # Crear el nombre del archivo Excel
    excel_file = os.path.join(output_path, f'{os.path.splitext(image_file)[0]}_RGB_Vector.xlsx')
    
    # Guardar el DataFrame en un archivo Excel
    df_r.to_excel(excel_file, index=False, header=False)
    
    # Mostrar la ruta donde se ha guardado el archivo Excel
    print(f"Archivo guardado en: {excel_file}")

# Función para guardar el canal R en tonos de rojo como imagen
def save_r_channel_image(r_channel, image_file, output_dir):
    """
    Guarda el canal R de una imagen en tonos de rojo en un archivo.
    
    :param r_channel: El canal R de la imagen en formato 2D.
    :param image_file: Nombre del archivo de imagen para el título de la visualización.
    :param output_dir: Ruta del directorio donde se guardará la imagen.
    """
    # Crear canales G y B vacíos
    g_channel = np.zeros_like(r_channel)  # Canal G vacío
    b_channel = np.zeros_like(r_channel)  # Canal B vacío

    # Combinar los canales para formar una imagen RGB
    rgb_image = cv2.merge([b_channel, g_channel, r_channel])

    # Crear el nombre del archivo de salida
    output_image_file = os.path.join(output_dir, f'{os.path.splitext(image_file)[0]}_R_Channel.png')

    # Guardar la imagen
    cv2.imwrite(output_image_file, rgb_image)

    # Mostrar la ruta donde se ha guardado la imagen
    print(f"Imagen guardada en: {output_image_file}")

# Función principal para procesar todas las imágenes, guardar sus vectores R y visualizarlas
def process_and_visualize_images(corpus_path, output_path, size):
    """
    Procesa todas las imágenes en un directorio, convierte su canal R en un vector,
    guarda el resultado en archivos Excel y guarda el canal R como imágenes.
    
    :param corpus_path: Ruta del directorio donde están las imágenes.
    :param output_path: Ruta donde se guardarán los archivos Excel.
    :param size: Tamaño al que se redimensionarán las imágenes.
    """
    # Obtener todos los archivos de imagen en el directorio
    image_files = get_image_files(corpus_path)
    
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Crear un subdirectorio para almacenar las imágenes del canal R
    r_channel_dir = os.path.join(output_path, "R_Channel_Images")
    if not os.path.exists(r_channel_dir):
        os.makedirs(r_channel_dir)

    # Iterar a través de cada archivo de imagen
    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
        r_vector, r_channel = image_to_r_vector(image_path, size)  # Convertir la imagen a vector R

        # Guardar el vector R en un archivo Excel
        save_r_vector_to_excel(r_vector, output_path, image_file, size)

        # Guardar el canal R como imagen
        save_r_channel_image(r_channel, image_file, r_channel_dir)

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
# Función principal que orquesta todo el flujo
def main():
    corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'
    output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.2.dataImages'
    
    # Solicitar al usuario las dimensiones de la imagen
    while True:
        try:
            width = int(input("Ingrese el ancho de la imagen (ejemplo: 10): "))
            height = int(input("Ingrese la altura de la imagen (ejemplo: 10): "))
            image_size = (height, width)  # Notar que el orden es (alto, ancho)
            break
        except ValueError:
            print("Por favor, ingrese números válidos para el ancho y la altura.")

    # Procesar todas las imágenes, guardar sus vectores R y visualizarlas
    process_and_visualize_images(corpus_path, output_path, image_size)
    
        
    # Procesar los archivos Excel de vectores R y calcular sus estadísticas
    stats_output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.3.dataStadictist'
    
    #Almacena todos los valores estadisticos el archivo
    process_r_vectors_and_calculate_statistics(output_path, stats_output_path)


# Ejecutar la función principal
if __name__ == "__main__":
    main()
