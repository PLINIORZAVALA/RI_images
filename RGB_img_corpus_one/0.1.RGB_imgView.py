import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    
    # Separar la imagen en los tres canales B, G, R (OpenCV usa BGR por defecto)
    _, _, r_channel = cv2.split(image_resized)
    
    # Aplanar el canal R en un vector 1D
    r_vector = r_channel.flatten()
    
    return r_vector, r_channel

# Ruta del corpus de imágenes
corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'

# Obtener todos los archivos de imagen en el directorio
image_files = [f for f in os.listdir(corpus_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Crear un diccionario para almacenar los vectores R de cada imagen
data_r = {}
image_original_size = (100, 100)  # Tamaño fijo de las imágenes

# Iterar a través de cada archivo de imagen
for image_file in image_files:
    image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
    r_vector, _ = image_to_r_vector(image_path)  # Convertir la imagen a vector R

    # Almacenar el vector R en el diccionario usando el nombre de la imagen como clave
    data_r[image_file] = r_vector

# Crear un DataFrame para los vectores R, con los nombres de las imágenes como columnas
df_r = pd.DataFrame(data_r)

# Seleccionar uno de los vectores (ejemplo: la primera imagen)
image_name = image_files[0]  # Seleccionar la primera imagen
r_vector = df_r[image_name]  # Obtener el vector R de la imagen seleccionada

# Reconstruir el canal R en una imagen 2D
r_image = np.reshape(r_vector.values, image_original_size)

# Crear una imagen en RGB con el canal R lleno y los canales G y B en cero
r_channel = r_image  # Canal R (ya reconstruido)
g_channel = np.zeros_like(r_channel)  # Canal G (todo cero)
b_channel = np.zeros_like(r_channel)  # Canal B (todo cero)

# Combinar los canales para formar una imagen RGB
rgb_image = cv2.merge([b_channel, g_channel, r_channel])

# Mostrar la imagen con tonos de rojo
plt.imshow(rgb_image)
plt.title(f"Canal R Visualizado en Rojo: {image_name}")
plt.axis('off')
plt.show()
