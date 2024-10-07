import cv2
import numpy as np
import os
import pandas as pd

# Función para convertir una imagen en el vector del canal R (Rojo)
def image_to_r_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
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

# Crear un diccionario para almacenar los vectores R de cada imagen
data_r = {}

# Iterar a través de cada archivo de imagen
for image_file in image_files:
    image_path = os.path.join(corpus_path, image_file)  # Ruta completa de la imagen
    r_vector = image_to_r_vector(image_path)  # Convertir la imagen a vector R

    # Almacenar el vector R en el diccionario usando el nombre de la imagen como clave
    data_r[image_file] = r_vector

# Crear un DataFrame para los vectores R, con los nombres de las imágenes como columnas
df_r = pd.DataFrame(data_r)

# Ruta donde se guardará el archivo Excel(Se obtiene unicamente los vectore R de las imagenes del "corpus")
output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one'

# Verificar si la carpeta de destino existe, si no, crearla
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Guardar el DataFrame en un archivo Excel
excel_file = os.path.join(output_path, '0.0.RGB_Vectors.xlsx')
df_r.to_excel(excel_file, index=False)

# Mostrar la ruta donde se ha guardado el archivo Excel
print(f"Archivo guardado en: {excel_file}")
