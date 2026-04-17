import pandas as pd
import simplekml
import os
import re
import numpy as np
from sklearn.cluster import DBSCAN

# =================================================================
# 1. CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# =================================================================
RUTA_MASTER = r"C:\Users\crist\OneDrive\Desktop\Elementos de red\MASTER_BBDD_Consolidada.xlsx"
DIRECTORIO_BASE = r"C:\Users\crist\OneDrive\Desktop\Elementos de red\Gestion_Municipal"

# Parámetros Financieros y Legales
VALOR_UTM_CLP = 66000
VALOR_KILO_COBRE_CLP = 5000
COSTO_RETIRO_SUBSIDIARIO = 45000

# =================================================================
# 2. FUNCIONES DE APOYO Y AUDITORÍA ESPACIAL
# =================================================================
def limpiar_nombre(texto):
    if pd.isna(texto): return "No_Informado"
    return re.sub(r'[\\/*?:"<>|]', "", str(texto).strip().title())

def calcular_infraccion(estado):
    est = str(estado).strip()
    if "Riesgo" in est or "Mal Estado" in est:
        return pd.Series(['Grave (Riesgo Inminente)', 5]) # 5 UTM
    elif "Desuso" in est:
        return pd.Series(['Moderada (Abandono)', 2])      # 2 UTM
    return pd.Series(['Sin Infracción', 0])

def limpiar_outliers_flexibles(df, col_lat='Latitud_WGS84', col_lon='Longitud_WGS84', col_comuna='3. Comuna'):
    """Filtro espacial DBSCAN para eliminar errores de GPS respetando zonas rurales"""
    print("\n[!] Iniciando Escudo Espacial Multipolar (DBSCAN)...")
    df_limpio = pd.DataFrame()
    
    df[col_lat] = pd.to_numeric(df[col_lat], errors='coerce')
    df[col_lon] = pd.to_numeric(df[col_lon], errors='coerce')
    df_validos = df.dropna(subset=[col_lat, col_lon]).copy()
    
    tolerancia_km = 8.0 
    kms_per_radian = 6371.0088
    epsilon = tolerancia_km / kms_per_radian
    
    for comuna, grupo in df_validos.groupby(col_comuna):
        if len(grupo) < 3:
            df_limpio = pd.concat([df_limpio, grupo])
            continue
            
        coords = np.radians(grupo[[col_lat, col_lon]].values)
        db = DBSCAN(eps=epsilon, min_samples=2, algorithm='ball_tree', metric='haversine').fit(coords)
        
        grupo_filtrado = grupo[db.labels_ != -1]
        df_limpio = pd.concat([df_limpio, grupo_filtrado])
        
    puntos_eliminados = len(df_validos) - len(df_limpio)
    print(f"[✓] Auditoría completada. Se neutralizaron {puntos_eliminados} puntos con error grave de georreferenciación.")
    
    return df_limpio

# =================================================================
# 3. GENERADORES DE ARCHIVOS MUNICIPALES
# =================================================================
def generar_excel_comunal(df_c, ruta, nombre):
    p_riesgo = len(df_c[df_c['Estado_Clasificado'] == 'Mal Estado / Riesgo'])
    kg_cobre = df_c[df_c['Material_Principal'] == 'Cobre']['Estimacion_Peso_KG'].sum()
    
    # Tabla 1: Resumen Gerencial
    t_resumen = pd.DataFrame({
        'Indicador': [
            'Puntos Totales', 'Puntos en Riesgo', 'Toneladas Totales',
            'Multas Potenciales (UTM)', 'Recaudación Potencial ($)',
            'Ingreso Potencial Cobre ($)', 'Costo Retiro Subsidiario ($)'
        ],
        'Valor': [
            len(df_c), p_riesgo, round(df_c['Estimacion_Peso_KG'].sum()/1000, 2),
            df_c['Multa_UTM'].sum(), f"$ {df_c['Multa_CLP'].sum():,.0f}",
            f"$ {(kg_cobre * VALOR_KILO_COBRE_CLP):,.0f}",
            f"$ {(p_riesgo * COSTO_RETIRO_SUBSIDIARIO):,.0f}"
        ]
    })

    # Tabla 2: Hoja de Ruta
    t_ruta = df_c[df_c['Estado_Clasificado'] == 'Mal Estado / Riesgo'].copy()
    if not t_ruta.empty:
        t_ruta = t_ruta[['6.Dirección Inicial / Direccion final (deben incluir numeración)', 
                         '7.Tipo del o los elementos a intervenir y su respectivo estado', 
                         'Estimacion_Peso_KG', 'Multa_UTM']].sort_values('Estimacion_Peso_KG', ascending=False).head(30)
        t_ruta.columns = ['DIRECCIÓN', 'TIPO DE ELEMENTO', 'KG EST.', 'MULTA (UTM)']

    # Escritura del Excel con 2 Hojas
    with pd.ExcelWriter(os.path.join(ruta, f"Dashboard_{nombre}.xlsx"), engine='openpyxl') as writer:
        t_resumen.to_excel(writer, sheet_name='Dashboard', index=False)
        if not t_ruta.empty:
            t_ruta.to_excel(writer, sheet_name='Dashboard', startrow=len(t_resumen)+4, index=False)
        df_c.to_excel(writer, sheet_name='Base_Datos_Comunal', index=False)

def generar_kmz_comunal(df_c, ruta, nombre):
    kml = simplekml.Kml(name=f"Visor {nombre}")
    df_m = df_c[df_c['Estado_Coordenada'] == 'Coordenada Válida']
    
    for _, r in df_m.iterrows():
        lat, lon = r['Latitud_WGS84'], r['Longitud_WGS84']
        dir_inf = str(r.get('6.Dirección Inicial / Direccion final (deben incluir numeración)', 'S/N'))
        
        p = kml.newpoint(name=dir_inf[:25])
        p.coords = [(lon, lat)]
        p.style.iconstyle.color = simplekml.Color.red if "Riesgo" in str(r['Estado_Clasificado']) else simplekml.Color.orange
        
        p.description = f"""
        <table border="1" style="font-family:Arial; border-collapse:collapse; width:300px;">
            <tr style="background:#2c3e50; color:white;"><th colspan="2">DETALLE TÉCNICO</th></tr>
            <tr><td><b>Dirección:</b></td><td>{dir_inf}</td></tr>
            <tr><td><b>Tipo:</b></td><td>{r.get('7.Tipo del o los elementos a intervenir y su respectivo estado', 'N/A')}</td></tr>
            <tr><td><b>Gravedad:</b></td><td style="color:red;"><b>{r['Gravedad_Infraccion']}</b></td></tr>
            <tr><td><b>Multa:</b></td><td>{r['Multa_UTM']} UTM (${r['Multa_CLP']:,.0f})</td></tr>
            <tr><td><b>Peso:</b></td><td>{r['Estimacion_Peso_KG']:.1f} Kg</td></tr>
            <tr><td><b>Origen:</b></td><td>{r.get('GORE, Municipio, Denuncias Ciudadanía o Empresas', 'Autodeclarado')}</td></tr>
        </table>
        """
    kml.savekmz(os.path.join(ruta, f"Visor_360_{nombre}.kmz"))

# =================================================================
# 4. PROCESO PRINCIPAL
# =================================================================
def ejecutar_produccion():
    print(">>> Iniciando Generación desde Base Maestra...")

    if not os.path.exists(RUTA_MASTER):
        print(f"ERROR: No se encontró el archivo en {RUTA_MASTER}")
        return

    print("1. Leyendo datos consolidados...")
    df = pd.read_excel(RUTA_MASTER, engine='openpyxl')

    # Aplicamos el filtro espacial de Outliers
    df = limpiar_outliers_flexibles(df)

    print("2. Aplicando Matriz Infraccional Dinámica...")
    if 'Estado_Clasificado' in df.columns:
        df[['Gravedad_Infraccion', 'Multa_UTM']] = df['Estado_Clasificado'].apply(calcular_infraccion)
        df['Multa_CLP'] = df['Multa_UTM'] * VALOR_UTM_CLP
    else:
        print("ADVERTENCIA: Falta la columna 'Estado_Clasificado'. Multas en 0.")
        df['Gravedad_Infraccion'] = 'Sin Infracción'
        df['Multa_UTM'] = 0
        df['Multa_CLP'] = 0

    print("3. Estructurando Carpetas y Activos Municipales...")
    df['2. Región'] = df['2. Región'].fillna("Region_No_Informada")
    df['Provincia'] = df['Provincia'].fillna("Provincia_No_Informada")
    df['3. Comuna'] = df['3. Comuna'].fillna("Comuna_No_Informada")

    grupos = df.groupby(['2. Región', 'Provincia', '3. Comuna'])
    total = len(grupos)

    for i, ((reg, prov, com), df_com) in enumerate(grupos):
        r_name, p_name, c_name = limpiar_nombre(reg), limpiar_nombre(prov), limpiar_nombre(com)
        ruta_comuna = os.path.join(DIRECTORIO_BASE, r_name, p_name, c_name)
        os.makedirs(ruta_comuna, exist_ok=True)

        generar_excel_comunal(df_com, ruta_comuna, c_name)
        generar_kmz_comunal(df_com, ruta_comuna, c_name)

        if (i+1) % 10 == 0 or (i+1) == total:
            print(f"   -> Procesado: {i+1} / {total} comunas...")

    print("\n4. Actualizando archivo Master con matriz de multas y sin fugitivos espaciales...")
    df.to_excel(RUTA_MASTER, index=False)

    print(f"\n>>> SISTEMA DESPLEGADO CON ÉXITO.")
    print(f"Revisa las carpetas en: {DIRECTORIO_BASE}")

if __name__ == "__main__":
    ejecutar_produccion()