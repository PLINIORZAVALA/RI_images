import cv2
import numpy as np
import matplotlib.pyplot as plt

# Función para convertir una imagen en un vector
def image_to_vector(image_path):
    # Leer la imagen en formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo, 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    # Aplanar la imagen 3D (100x100x3) en un vector 1D
    vector = image_resized.flatten()
    return vector, image_resized

# Cargar la imagen y convertirla a vector
image_path = 'E:/BUAP-MEXICO/DECIMO SEMESTRE/0.2.PROJECT/Imagenes/manzana.png'  # Cambia esto por la ruta de tu imagen
vector, image_resized = image_to_vector(image_path)

# Visualizar el vector
print("Vector de la imagen:")
print(vector)  # Esto te muestra los valores del vector en consola

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