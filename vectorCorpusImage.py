import cv2
import numpy as np
import os

# Función para convertir una imagen en un vector
def image_to_vector(image_path):
    # Leer la imagen en escala de grises
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    # Aplanar la imagen 2D en un vector 1D
    vector = image_resized.flatten()
    return vector

# Función para leer las imágenes de una carpeta y mostrar los vectores de cada una
def load_images_and_show_vectors(directory_path):
    # Verifica si la carpeta existe
    if not os.path.exists(directory_path):
        print(f"La carpeta {directory_path} no existe. Verifica la ruta.")
        return
    
    # Obtener la lista de archivos de imagen en el directorio (png, jpg, jpeg)
    image_files = [f for f in os.listdir(directory_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Verificar si se encontraron imágenes
    if not image_files:
        print(f"No se encontraron imágenes en la carpeta {directory_path}.")
        return
    
    # Iterar sobre cada imagen y mostrar su vector
    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        vector = image_to_vector(image_path)
        print(f"Vector de la imagen {image_file}:")
        print(vector)

# Ruta a la carpeta que contiene las imágenes (ajustada a "curpus")
image_directory = 'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'

# Llamar a la función para cargar y mostrar los vectores
load_images_and_show_vectors(image_directory)
