import pandas as pd
from ast import literal_eval

# Definir la ruta de entrada y salida
INPUT_EXCEL_PATH = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus\0.1.all_image_vectors.xlsx'
OUTPUT_EXCEL_PATH = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus\0.2.resultado_R.xlsx'

try:
    # Leer el archivo Excel
    df = pd.read_excel(INPUT_EXCEL_PATH)

    # Verificar que la columna 'R' está presente
    if 'R' not in df.columns:
        raise ValueError("La columna 'R' no se encuentra en el DataFrame.")

    # Crear una lista para almacenar los resultados
    results = []

    # Procesar la columna 'R'
    for index, row in df.iterrows():
        # Convertir el vector de la columna R de cadena a lista
        vector_r = literal_eval(row['R']) if isinstance(row['R'], str) else row['R']
        
        # Crear un diccionario con la imagen y los valores R
        image_data = {'Imagen': row['Imagen']}
        for i in range(len(vector_r)):
            image_data[f'R_{i}'] = vector_r[i]
        
        # Agregar el diccionario a la lista de resultados
        results.append(image_data)

    # Convertir los resultados a un DataFrame
    df_results = pd.DataFrame(results).T

    # Guardar el resultado en un nuevo archivo Excel
    df_results.to_excel(OUTPUT_EXCEL_PATH, index=False)
    print(f'Archivo guardado en: {OUTPUT_EXCEL_PATH}')

except FileNotFoundError:
    print(f"Error: El archivo '{INPUT_EXCEL_PATH}' no fue encontrado.")
except ValueError as e:
    print(f"Error de valor: {e}")
except Exception as e:
    print(f'Ocurrió un error inesperado: {e}')
