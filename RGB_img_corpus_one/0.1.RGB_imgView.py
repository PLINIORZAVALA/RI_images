import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Funciones del código anterior ------------------

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path, size=(100, 100)):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"No se pudo leer la imagen en {image_path}")
    
    # Redimensionar la imagen
    image_resized = cv2.resize(image, size)
    
    # Separar la imagen en los canales B, G, R
    _, _, r_channel = cv2.split(image_resized)
    
    # Aplanar el canal R
    r_vector = r_channel.flatten()
    
    return r_vector, r_channel

# Función para obtener archivos de imagen en un directorio
def get_image_files(directory, extensions=('.png', '.jpg', '.jpeg')):
    return [f for f in os.listdir(directory) if f.endswith(extensions)]

# Función para procesar un corpus de imágenes y convertirlas a vectores R
def process_image_corpus(corpus_path, size=(100, 100)):
    image_files = get_image_files(corpus_path)
    data_r = {}
    
    # Procesar cada imagen en el corpus
    for image_file in image_files:
        image_path = os.path.join(corpus_path, image_file)
        r_vector, _ = image_to_r_vector(image_path, size)
        data_r[image_file] = r_vector
    
    return data_r, image_files

# Función para reconstruir la imagen del canal R a partir de su vector
def reconstruct_r_image(r_vector, size=(100, 100)):
    return np.reshape(r_vector, size)

# Función para crear una imagen RGB donde solo el canal R esté lleno
def create_rgb_image_from_r(r_channel):
    g_channel = np.zeros_like(r_channel)
    b_channel = np.zeros_like(r_channel)
    
    rgb_image = cv2.merge([b_channel, g_channel, r_channel])
    return rgb_image

# Función para mostrar la imagen en tonos rojos utilizando matplotlib
def show_image_in_red(rgb_image, image_name):
    plt.imshow(rgb_image)
    plt.title(f"Canal R Visualizado en Rojo: {image_name}")
    plt.axis('off')
    plt.show()

# ------------------ Nuevas funcionalidades a integrar ------------------

# Función para mostrar el histograma del canal R
def plot_r_histogram(r_channel):
    """
    Muestra el histograma del canal R de una imagen.
    :param r_channel: El canal R en 2D.
    """
    plt.hist(r_channel.ravel(), bins=256, color='red', alpha=0.75)
    plt.title('Histograma del Canal R')
    plt.xlabel('Intensidad de Rojo')
    plt.ylabel('Frecuencia')
    plt.show()

# Función para guardar los datos R de las imágenes en un archivo Excel
def save_r_vectors_to_excel(df_r, output_path):
    """
    Guarda los vectores R en un archivo Excel.
    :param df_r: DataFrame que contiene los vectores R.
    :param output_path: Ruta del archivo Excel.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    excel_file = os.path.join(output_path, '0.1.RGB_Vectors.xlsx')
    df_r.to_excel(excel_file, index=False)
    print(f"Archivo guardado en: {excel_file}")

# Función principal que coordina el proceso
def main():
    corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'
    output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one'
    image_original_size = (100, 100)

    # Procesar el corpus de imágenes y obtener los vectores R
    data_r, image_files = process_image_corpus(corpus_path, image_original_size)
    
    # Crear un DataFrame para los vectores R
    df_r = pd.DataFrame(data_r)

    # Guardar los vectores R en un archivo Excel
    save_r_vectors_to_excel(df_r, output_path)
    
    # Seleccionar el vector R de la primera imagen
    image_name = image_files[0]
    r_vector = df_r[image_name]
    
    # Reconstruir el canal R en una imagen 2D
    r_image = reconstruct_r_image(r_vector.values, image_original_size)
    
    # Crear una imagen RGB con solo el canal R activo
    rgb_image = create_rgb_image_from_r(r_image)
    
    # Mostrar la imagen con tonos de rojo
    show_image_in_red(rgb_image, image_name)
    
    # Mostrar el histograma del canal R
    plot_r_histogram(r_image)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
