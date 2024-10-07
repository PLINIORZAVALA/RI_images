import numpy as np
import pandas as pd
import os
from scipy import stats

# Función para leer el archivo Excel y calcular las estadísticas
def calculate_statistics_from_excel(excel_path, save_path):
    # Leer el archivo Excel existente
    vector_df = pd.read_excel(excel_path)

    # Calcular las estadísticas para el canal R, G y B
    mode_r = stats.mode(vector_df['R'])
    mode_g = stats.mode(vector_df['G'])
    mode_b = stats.mode(vector_df['B'])
    
    # Imprimir los modos para depuración
    print("Modo R:", mode_r)
    print("Modo G:", mode_g)
    print("Modo B:", mode_b)

    stats_df = pd.DataFrame({
        'Channel': ['R', 'G', 'B'],
        'Moda': [
            mode_r.mode,  # Sin indexar
            mode_g.mode,  # Sin indexar
            mode_b.mode   # Sin indexar
        ],
        'Desviación Estándar': [
            np.std(vector_df['R']), 
            np.std(vector_df['G']), 
            np.std(vector_df['B'])
        ],
        'Promedio': [
            np.mean(vector_df['R']), 
            np.mean(vector_df['G']), 
            np.mean(vector_df['B'])
        ],
        'Valor Máximo': [
            np.max(vector_df['R']), 
            np.max(vector_df['G']), 
            np.max(vector_df['B'])
        ],
        'Valor Mínimo': [
            np.min(vector_df['R']), 
            np.min(vector_df['G']), 
            np.min(vector_df['B'])
        ]
    })

    # Guardar las estadísticas en un nuevo archivo Excel
    save_stats_path = os.path.join(save_path, '0.2.image_imgStatistics.xlsx')
    stats_df.to_excel(save_stats_path, index=False)  # Guardar en Excel

    return stats_df

# Definir la ruta del archivo Excel existente y la carpeta de destino
excel_path = r'E:/BUAP-MEXICO/DECIMO SEMESTRE/0.2.PROJECT/Imagenes/RGB_img/0.1.image_imgVector.xlsx'
save_path = r'E:/BUAP-MEXICO/DECIMO SEMESTRE/0.2.PROJECT/Imagenes/RGB_img'

# Llamar a la función para calcular las estadísticas y guardarlas en un archivo Excel
stats_df = calculate_statistics_from_excel(excel_path, save_path)

# Mostrar las estadísticas en la consola
print("Estadísticas calculadas (R, G, B):")
print(stats_df)
