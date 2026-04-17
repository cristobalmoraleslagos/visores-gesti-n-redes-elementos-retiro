import pandas as pd
import glob
import os

# Configuración
path = r"C:\Users\crist\OneDrive\Desktop\MUNI PLANTAS\Ñuñoa\PLANTA\Remuneración"
output_file = os.path.join(path, "Consolidado_Remuneraciones_2025_2026.csv")

# Obtener todos los archivos .csv
all_files = glob.glob(os.path.join(path, "*.csv"))

data_frames = []
column_reference = None

print("Iniciando consolidación...")

for file in all_files:
    if file == output_file:
        continue
    
    # Probamos encoding 'latin-1' o 'utf-8' que son los comunes en Chile
    # El separador suele ser ';' en CSVs exportados de Excel en español
    try:
        df = pd.read_csv(file, sep=None, engine='python', encoding='latin-1')
        
        # Validación de formato (Columnas)
        current_columns = list(df.columns)
        if column_reference is None:
            column_reference = current_columns
        elif current_columns != column_reference:
            print(f"⚠️ Alerta: {os.path.basename(file)} tiene columnas distintas.")
        
        # Añadimos mes/año desde el nombre del archivo para no perder el contexto
        df['Archivo_Origen'] = os.path.basename(file)
        data_frames.append(df)
        print(f"✅ Procesado: {os.path.basename(file)}")
        
    except Exception as e:
        print(f"❌ Error en {os.path.basename(file)}: {e}")

# Unión final
if data_frames:
    df_final = pd.concat(data_frames, ignore_index=True)
    # Guardamos en UTF-8 con BOM para que Excel lo abra perfecto
    df_final.to_csv(output_file, index=False, sep=';', encoding='utf-8-sig')
    print(f"\n--- Proceso Finalizado ---")
    print(f"Archivo consolidado creado con {len(df_final)} registros.")
else:
    print("No se cargó ningún dato.")
    # Agregar una columna con el nombre del archivo original (útil para auditoría)
    df['Origen_Archivo'] = os.path.basename(file)
    
    data_frames.append(df)
    print(f"Cargado: {os.path.basename(file)} - Filas: {len(df)}")

# Consolidar todo
if data_frames:
    consolidated_df = pd.concat(data_frames, ignore_index=True)
    
    # Guardar el resultado
    consolidated_df.to_excel(output_file, index=False)
    print(f"\n--- Éxito ---")
    print(f"Total de archivos procesados: {len(data_frames)}")
    print(f"Total de registros: {len(consolidated_df)}")
    print(f"Archivo guardado en: {output_file}")
else:
    print("No se encontraron archivos para consolidar.")