import cv2
import numpy as np
import os
import pandas as pd

# Función para convertir una imagen en un vector y almacenar el vector separado por canales
def image_to_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (8, 8))
    
    # Separar la imagen en los tres canales (B, G, R)
    B, G, R = cv2.split(image_resized)

    # Aplanar cada canal 2D en un vector 1D
    R_vector = R.flatten()
    G_vector = G.flatten()
    B_vector = B.flatten()

    return R_vector, G_vector, B_vector

# Ruta del corpus de imágenes
corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'

# Obtener todos los archivos de imagen en el directorio
image_files = [f for f in os.listdir(corpus_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# DataFrame para almacenar los datos de las imágenes
all_vectors_df = pd.DataFrame()

# Iterar a través de cada archivo de imagen
for image_file in image_files:
    image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
    R_vector, G_vector, B_vector = image_to_vector(image_path)  # Convertir la imagen a vector

    # Crear un DataFrame temporal para la imagen actual
    vector_df = pd.DataFrame({
        'Imagen': image_file,
        'R': [R_vector.tolist()],  # Convertir a lista para guardar en Excel
        'G': [G_vector.tolist()],
        'B': [B_vector.tolist()]
    })

    # Concatenar los datos al DataFrame general
    all_vectors_df = pd.concat([all_vectors_df, vector_df], ignore_index=True)

# Guardar el DataFrame de todos los vectores en un archivo Excel
output_excel_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus\0.1.all_image_vectors.xlsx'
all_vectors_df.to_excel(output_excel_path, index=False)  # Guardar en Excel

# Mostrar el DataFrame en consola
print("DataFrame de Vectores de Imágenes (R, G, B separados):")
print(all_vectors_df)
