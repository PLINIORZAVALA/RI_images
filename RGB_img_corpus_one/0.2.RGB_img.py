import cv2
import numpy as np
import os
import pandas as pd

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 4x4 píxeles
    image_resized = cv2.resize(image, (4, 4))
    
    # Separar la imagen en los tres canales B, G, R (OpenCV usa BGR por defecto)
    _, _, r_channel = cv2.split(image_resized)
    
    # Aplanar el canal R en un vector 1D
    r_vector = r_channel.flatten()
    
    return r_vector

# Ruta del corpus de imágenes
corpus_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\curpus'

# Obtener todos los archivos de imagen en el directorio
image_files = [f for f in os.listdir(corpus_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Ruta donde se guardará el archivo Excel
output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.2.dataImages'

# Verificar si la carpeta de destino existe, si no, crearla
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Iterar a través de cada archivo de imagen
for image_file in image_files:
    image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
    r_vector = image_to_r_vector(image_path)  # Convertir la imagen a vector R

    # Crear un DataFrame de 4x4 para el vector R
    r_matrix = r_vector.reshape((4, 4))
    df_r = pd.DataFrame(r_matrix)

    # Guardar cada DataFrame en un archivo Excel diferente
    excel_file = os.path.join(output_path, f'{os.path.splitext(image_file)[0]}_RGB_Vector.xlsx')
    df_r.to_excel(excel_file, index=False, header=False)  # Guardar sin índice y sin encabezados

    # Mostrar la ruta donde se ha guardado el archivo Excel
    print(f"Archivo guardado en: {excel_file}")
