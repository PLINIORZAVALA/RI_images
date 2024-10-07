import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Función para convertir una imagen en un vector y almacenar la imagen RGB y su vector separado por canales
def image_to_vector_and_save(image_path, save_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    
    # Separar la imagen en los tres canales (B, G, R)
    B, G, R = cv2.split(image_resized)

    # Aplanar cada canal 2D en un vector 1D
    R_vector = R.flatten()
    G_vector = G.flatten()
    B_vector = B.flatten()

    # Crear un DataFrame con columnas separadas para R, G y B
    vector_df = pd.DataFrame({
        'R': R_vector,
        'G': G_vector,
        'B': B_vector
    })

    # Guardar la imagen redimensionada en la ruta especificada
    save_image_path = os.path.join(save_path, '0.1.image_imgVector.png')
    cv2.imwrite(save_image_path, image_resized)

    # Guardar el vector de la imagen en un archivo Excel con los canales separados
    save_vector_path = os.path.join(save_path, '0.1.image_imgVector.xlsx')
    vector_df.to_excel(save_vector_path, index=False)  # Guardar en Excel

    return vector_df, image_resized

# Definir la ruta de la imagen original y la carpeta de destino
image_path = 'manzana.png'  # Cambia esto por la ruta de tu imagen
save_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img'

# Crear la carpeta si no existe
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Llamar a la función para convertir la imagen y almacenar los resultados
vector_df, image_resized = image_to_vector_and_save(image_path, save_path)

# Visualizar el vector en la consola
print("Vector de la imagen (canales R, G, B separados):")
print(vector_df)

# Opcional: Visualiza la imagen original y redimensionada
plt.subplot(1, 2, 1)
plt.title("Imagen Original")
original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
# Convertir de BGR a RGB, ya que OpenCV carga la imagen en BGR por defecto
original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
plt.imshow(original_image_rgb)

plt.subplot(1, 2, 2)
plt.title("Imagen Redimensionada (100x100)")
# Convertir la imagen redimensionada de BGR a RGB para mostrarla correctamente
image_resized_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
plt.imshow(image_resized_rgb)

plt.show()
