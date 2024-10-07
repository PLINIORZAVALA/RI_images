import pandas as pd
import os

# Ruta donde se guardaron los archivos Excel de los vectores de imágenes
input_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.2.dataImages'

# Ruta donde se guardarán los resultados estadísticos de cada archivo
output_path = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus_one\0.3.dataStadictist'

# Obtener todos los archivos Excel en el directorio
excel_files = [f for f in os.listdir(input_path) if f.endswith('.xlsx')]

# Iterar a través de cada archivo Excel
for excel_file in excel_files:
    excel_path = os.path.join(input_path, excel_file)  # Ruta completa del archivo Excel
    df = pd.read_excel(excel_path, header=None)  # Leer el archivo Excel sin encabezados

    # Calcular estadísticas
    resultados = {
        'Suma': df.sum(axis=1),
        'Media': df.mean(axis=1),
        'Mediana': df.median(axis=1),
        'Moda': df.mode(axis=1)[0],  # Tomando solo el primer modo
        'Varianza': df.var(axis=1),
        'Desviación Estándar': df.std(axis=1),
        'Rango': df.max(axis=1) - df.min(axis=1),
        'Mínimo': df.min(axis=1),
        'Máximo': df.max(axis=1),
        'Cuartil 1': df.quantile(0.25, axis=1),
        'Cuartil 2': df.quantile(0.5, axis=1),
        'Cuartil 3': df.quantile(0.75, axis=1),
    }

    # Crear un DataFrame para las estadísticas
    estadisticas_df = pd.DataFrame(resultados)

    # Crear la ruta de salida para el archivo de estadísticas
    output_file = os.path.join(output_path, f"Estadisticas_{excel_file}")

    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Guardar el DataFrame de estadísticas en un archivo Excel
    estadisticas_df.to_excel(output_file, index=False)

    # Mostrar la ruta donde se ha guardado el archivo Excel
    print(f"Archivo de estadísticas guardado en: {output_file}")
