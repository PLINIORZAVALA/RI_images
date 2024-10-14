import cv2
import numpy as np
import os
import pandas as pd

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size=(4, 4)):
    """
    Convierte una imagen en el vector del canal rojo (R).
    :param image_path: Ruta de la imagen.
    :param size: Tamaño para redimensionar la imagen (ancho, alto).
    :return: Vector 1D del canal R.
    """
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"No se pudo leer la imagen en {image_path}")
    
    # Redimensionar la imagen al tamaño especificado
    image_resized = cv2.resize(image, size)
    
    # Separar la imagen en los tres canales B, G, R
    _, _, r_channel = cv2.split(image_resized)
    
    # Aplanar el canal R en un vector 1D
    r_vector = r_channel.flatten()
    
    return r_vector

# Función para obtener los archivos de imagen en un directorio dado
def get_image_files(directory, extensions=('.png', '.jpg', '.jpeg')):
    """
    Obtiene todos los archivos de imagen en un directorio que coincidan con las extensiones dadas.
    :param directory: Directorio donde buscar imágenes.
    :param extensions: Extensiones de imagen permitidas.
    :return: Lista de archivos de imagen.
    """
    return [f for f in os.listdir(directory) if f.endswith(extensions)]

# Función para procesar un corpus de imágenes y convertirlas a vectores R
def process_image_corpus(corpus_path):
    """
    Procesa todas las imágenes en un directorio y las convierte a vectores R.
    :param corpus_path: Directorio del corpus de imágenes.
    :return: Diccionario con los vectores R de las imágenes.
    """
    image_files = get_image_files(corpus_path)
    data_r = {}
    
    # Iterar a través de cada archivo de imagen
    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
        r_vector = image_to_r_vector(image_path)  # Convertir la imagen a vector R
        data_r[image_file] = r_vector
    
    return data_r

# Función para guardar los vectores R en un archivo Excel
def save_vectors_to_excel(vectors, output_dir, filename='0.0.RGB_Vectors.xlsx'):
    """
    Guarda un diccionario de vectores en un archivo Excel.
    :param vectors: Diccionario con los vectores a guardar.
    :param output_dir: Directorio de salida.
    :param filename: Nombre del archivo Excel.
    """
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Crear un DataFrame a partir del diccionario
    df_r = pd.DataFrame(vectors)
    
    # Guardar el DataFrame en un archivo Excel
    excel_file = os.path.join(output_dir, filename)
    df_r.to_excel(excel_file, index=False)

    print(f"Archivo guardado en: {excel_file}")
    return excel_file

# Función principal que coordina todo el proceso
def main():
    corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'
    output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one'
    
    # Procesar el corpus de imágenes para obtener los vectores R
    image_vectors_r = process_image_corpus(corpus_path)
    
    # Guardar los vectores R en un archivo Excel
    save_vectors_to_excel(image_vectors_r, output_path)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
