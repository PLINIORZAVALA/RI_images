import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# Función para convertir una imagen en un vector
def image_to_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    # Aplanar la imagen 3D (100x100x3) en un vector 1D
    vector = image_resized.flatten()
    return vector, image_resized

# Ruta del corpus de imágenes
corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'

# Obtener todos los archivos de imagen en el directorio
image_files = [f for f in os.listdir(corpus_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Crear un DataFrame para almacenar nombres de imágenes y vectores
data = {
    'Nombre de Imagen': [],
    'Vector': []
}

# Crear una figura para mostrar las imágenes
num_images = len(image_files)
plt.figure(figsize=(15, 5 * (num_images // 3 + 1)))  # Ajustar el tamaño de la figura según la cantidad de imágenes

# Iterar a través de cada archivo de imagen
for idx, image_file in enumerate(image_files):
    image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
    vector, image_resized = image_to_vector(image_path)  # Convertir la imagen a vector

    # Almacenar el nombre de la imagen y su vector en el DataFrame
    data['Nombre de Imagen'].append(image_file)
    data['Vector'].append(vector)

    # Mostrar la imagen redimensionada
    plt.subplot((num_images // 3 + 1), 3, idx + 1)
    image_resized_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
    plt.imshow(image_resized_rgb)
    plt.title(f"Imagen: {image_file}")  # Muestra solo el nombre del archivo
    plt.axis('off')

# Mostrar la figura con todas las imágenes
plt.tight_layout()
plt.show()

# Crear un DataFrame de Pandas
df = pd.DataFrame(data)


# Mostrar el DataFrame en consola
print("DataFrame de Imágenes y Vectores:")
print(df)
