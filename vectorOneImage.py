    import cv2
    import numpy as np

    # Función para convertir una imagen en un vector
    def image_to_vector(image_path):
        # Leer la imagen en escala de grises
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Redimensionar la imagen a un tamaño fijo, por ejemplo 100x100 píxeles
        image_resized = cv2.resize(image, (100, 100))
        # Aplanar la imagen 2D en un vector 1D
        vector = image_resized.flatten()
        return vector

    # Cargar la imagen y convertirla a vector
    image_path = 'manzana.png'  # Cambia esto por la ruta de tu imagen
    vector = image_to_vector(image_path)

    # Para mostrar todo el vector sin truncamiento
    np.set_printoptions(threshold=np.inf)

    # Visualizar el vector en consola
    print("Vector de la imagen:")
    print(vector)
