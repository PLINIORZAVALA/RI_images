import pandas as pd

# Definir la ruta del archivo de entrada y salida
OUTPUT_EXCEL_PATH = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus\0.2.resultado_R.xlsx'
OUTPUT_EXCEL_STATS_PATH = r'E:\BUAP-MEXICO\DECIMO SEMESTRE\0.2.PROJECT\Imagenes\RGB_img_corpus\0.3.resultado_Estadisticas.xlsx'

try:
    # Leer el archivo Excel
    df = pd.read_excel(OUTPUT_EXCEL_PATH)

    # Crear una lista para almacenar las estadísticas
    estadisticas = []

    # Iterar sobre cada columna
    for columna in df.columns:
        # Obtener los valores de la columna
        valores_columna = df[columna]

        # Filtrar solo los valores numéricos
        valores_numericos = pd.to_numeric(valores_columna, errors='coerce')

        # OBTENCIÓN DE VALORES ESTADÍSTICOS
        suma = valores_numericos.sum()
        media = valores_numericos.mean()
        mediana = valores_numericos.median()
        varianza = valores_numericos.var()
        desviacion_estandar = valores_numericos.std()
        minimo = valores_numericos.min()
        maximo = valores_numericos.max()

        # Almacenar los resultados en la lista
        estadisticas.append({
            "Columna": columna,
            "Suma": suma,
            "Media": media,
            "Mediana": mediana,
            "Varianza": varianza,
            "Desviación estándar": desviacion_estandar,
            "Mínimo": minimo,
            "Máximo": maximo
        })

    # Crear un DataFrame a partir de la lista de estadísticas
    estadisticas_df = pd.DataFrame(estadisticas)

    # Imprimir las estadísticas de cada columna
    print("Estadísticas de valores numéricos por columna:")
    print(estadisticas_df)

    # Guardar los resultados en un nuevo archivo Excel
    estadisticas_df.to_excel(OUTPUT_EXCEL_STATS_PATH, index=False)
    print(f'Archivo de estadísticas guardado en: {OUTPUT_EXCEL_STATS_PATH}')

except FileNotFoundError:
    print(f"Error: El archivo '{OUTPUT_EXCEL_PATH}' no fue encontrado.")
except ValueError as e:
    print(f"Error de valor: {e}")
except Exception as e:
    print(f'Ocurrió un error inesperado: {e}')
