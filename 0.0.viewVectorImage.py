import cv2
import numpy as np
import matplotlib.pyplot as plt

# Función para convertir una imagen en un vector
def image_to_vector(image_path):
    # Leer la imagen
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Redimensionar la imagen a un tamaño fijo, por ejemplo 100x100 píxeles
    image_resized = cv2.resize(image, (100, 100))
    # Aplanar la imagen 2D en un vector 1D
    vector = image_resized.flatten()
    return vector, image_resized

# Cargar la imagen y convertirla a vector
image_path = 'manzana.png'  # Cambia esto por la ruta de tu imagen
vector, image_resized = image_to_vector(image_path)

# Visualizar el vector
print("Vector de la imagen:")
print(vector)  # Esto te muestra los valores del vector en consola

# Opcional: Visualiza la imagen original y redimensionada
plt.subplot(1, 2, 1)
plt.title("Imagen Original")
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
plt.imshow(original_image, cmap='gray')

plt.subplot(1, 2, 2)
plt.title("Imagen Redimensionada (100x100)")
plt.imshow(image_resized, cmap='gray')

plt.show()
