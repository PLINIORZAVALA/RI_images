import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size=(4, 4)):
    """
    Convierte una imagen en un vector 1D del canal R.
    
    :param image_path: La ruta completa de la imagen.
    :param size: Tamaño al que se redimensionará la imagen, por defecto 4x4.
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
def save_r_vector_to_excel(r_vector, output_path, image_file, size=(4, 4)):
    """
    Guarda un vector R en un archivo Excel como una matriz.
    
    :param r_vector: Vector del canal R.
    :param output_path: Ruta donde se guardará el archivo Excel.
    :param image_file: Nombre del archivo de imagen (se usará para nombrar el archivo Excel).
    :param size: Tamaño al que se redimensionó la imagen (por defecto 4x4).
    """
    # Crear un DataFrame de 4x4 para el vector R
    r_matrix = r_vector.reshape(size)
    df_r = pd.DataFrame(r_matrix)

    # Crear el nombre del archivo Excel
    excel_file = os.path.join(output_path, f'{os.path.splitext(image_file)[0]}_RGB_Vector.xlsx')
    
    # Guardar el DataFrame en un archivo Excel
    df_r.to_excel(excel_file, index=False, header=False)
    
    # Mostrar la ruta donde se ha guardado el archivo Excel
    print(f"Archivo guardado en: {excel_file}")

# Función para visualizar el canal R en tonos de rojo
def visualize_r_channel(r_channel, image_file):
    """
    Visualiza el canal R de una imagen en tonos de rojo.
    
    :param r_channel: El canal R de la imagen en formato 2D.
    :param image_file: Nombre del archivo de imagen para el título de la visualización.
    """
    # Crear canales G y B vacíos
    g_channel = np.zeros_like(r_channel)  # Canal G vacío
    b_channel = np.zeros_like(r_channel)  # Canal B vacío

    # Combinar los canales para formar una imagen RGB
    rgb_image = cv2.merge([b_channel, g_channel, r_channel])

    # Mostrar la imagen con tonos de rojo
    plt.imshow(rgb_image)
    plt.title(f"Canal R Visualizado en Rojo: {image_file}")
    plt.axis('off')
    plt.show()

# Función principal para procesar todas las imágenes, guardar sus vectores R y visualizarlas
def process_and_visualize_images(corpus_path, output_path, size=(4, 4)):
    """
    Procesa todas las imágenes en un directorio, convierte su canal R en un vector,
    guarda el resultado en archivos Excel y visualiza el canal R en tonos de rojo.
    
    :param corpus_path: Ruta del directorio donde están las imágenes.
    :param output_path: Ruta donde se guardarán los archivos Excel.
    :param size: Tamaño al que se redimensionarán las imágenes (por defecto 4x4).
    """
    # Obtener todos los archivos de imagen en el directorio
    image_files = get_image_files(corpus_path)
    
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Iterar a través de cada archivo de imagen
    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
        r_vector, r_channel = image_to_r_vector(image_path, size)  # Convertir la imagen a vector R

        # Guardar el vector R en un archivo Excel
        save_r_vector_to_excel(r_vector, output_path, image_file, size)

        # Visualizar el canal R en tonos de rojo
        visualize_r_channel(r_channel, image_file)

# Función principal que orquesta todo- el flujo
def main():
    corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'
    output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.2.dataImages'
    image_size = (4, 4)  # Tamaño de las imágenes a procesar
    
    # Procesar todas las imágenes, guardar sus vectores R y visualizarlas
    process_and_visualize_images(corpus_path, output_path, image_size)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
