# Convertir el número a texto y concatenar con la ciudad
df['nueva_columna'] = df['seller_city_clean'].astype(str) + ' - ' + df['ranking_producto_en_vendedor'].astype(str)

# Visualizar el resultado
df[['seller_city_clean', 'ranking_producto_en_vendedor', 'nueva_columna']].head()
df['product_category_name'] = df['product_category_name'].fillna('unknown')
df['product_category_name']
df[df['product_category_name'] == 'unknown']
import numpy as np

# 1. Cargar el archivo CSV ignorando líneas corruptas o incompletas con el nombre correcto
df = pd.read_csv('df3_vendedores_popularidad.csv', on_bad_lines='skip')

# 2. Estandarizar nombres de columnas (eliminar espacios y convertir a minúsculas)
df.columns = df.columns.str.strip().str.lower()

# 3. Limpiar espacios en blanco innecesarios en todas las columnas de texto
string_columns = df.select_dtypes(include=['object']).columns
for col in string_columns:
    df[col] = df[col].astype(str).str.strip()

# 4. Estandarizar el código de estado a mayúsculas (ej: 'sp' -> 'SP')
df['seller_state_clean'] = df['seller_state_clean'].str.upper()

# 6. Convertir tipos de datos numéricos
numeric_integers = [
    'unidades_vendidas_producto',
    'pedidos_distintos_producto',
    'ranking_producto_en_vendedor'
]

for col in numeric_integers:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

df['ingreso_total_producto'] = pd.to_numeric(df['ingreso_total_producto'], errors='coerce')

# 7. Eliminar filas con datos cuantitativos incompletos (como la última fila truncada)
df = df.dropna(subset=['ingreso_total_producto', 'unidades_vendidas_producto'])

# 8. Eliminar registros duplicados si existieran
df = df.drop_duplicates().reset_index(drop=True)

print(f"--- Limpieza finalizada ---")
print(f"Registros válidos procesados: {len(df)}")
print(f"Columnas procesadas: {list(df.columns)}")



# --- 1. INSPECCIÓN INICIAL ---
print("--- Dimensiones originales ---")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}\n")

# --- 2. ELIMINACIÓN DE DUPLICADOS ---
# Eliminamos registros idénticos si es que existen
duplicados = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"-> Se eliminaron {duplicados} filas completamente duplicadas.")

# --- 3. LIMPIEZA DE TEXTO (Estandarización) ---
# Quitar comillas residuales y espacios en blanco al inicio/final de los textos
columnas_texto = ['Ciudad Cliente', 'Estado Cliente', 'Estado']
for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()

# Convertir ciudades a formato Título (ej. "sao paulo" -> "Sao Paulo")
if 'Ciudad Cliente' in df.columns:
    df['Ciudad Cliente'] = df['Ciudad Cliente'].str.title()

# Convertir estados a mayúsculas rígidas (ej. "sp" -> "SP")
if 'Estado Cliente' in df.columns:
    df['Estado Cliente'] = df['Estado Cliente'].str.upper()

# --- 4. CORRECCIÓN DE FORMATOS DE FECHA ---
# Convertir la fecha de compra a un formato datetime real de Python
if 'Fecha de Compra' in df.columns:
    df['Fecha de Compra'] = pd.to_datetime(df['Fecha de Compra'], errors='coerce')

# --- 5. MANEJO DE VALORES VACÍOS (NaN) ---
# Visualizar si quedan campos nulos tras las conversiones
print("\n--- Valores nulos por columna ---")
print(df.isnull().sum())

# Opcional: Reemplazar textos "nan" que se hayan generado al convertir strings
df.replace('nan', None, inplace=True)

print("\n¡Limpieza de datos completada con éxito!")
df.head(10)


import pandas as pd
import io

# 1. Copia de los nuevos datos proporcionados (Reseñas y cantidades)
raw_reviews = """review_score,cantidad
1,11424
2,3151
3,8179
4,19142
5,57328"""

# Inicializar el DataFrame
df_reviews = pd.read_csv(io.StringIO(raw_reviews))

# --- PROCESO DE LIMPIEZA Y VALIDACIÓN ---

# 1. Normalizar encabezados (quitar espacios en blanco invisibles si los hubiera)
df_reviews.columns = df_reviews.columns.str.strip()

# 2. Asegurar tipos de datos correctos (Puntuaciones y cantidades como enteros)
df_reviews['review_score'] = df_reviews['review_score'].astype(int)
df_reviews['cantidad'] = df_reviews['cantidad'].astype(int)

# 3. Validar consistencia de los datos (Las puntuaciones de satisfacción deben estar entre 1 y 5)
df_reviews = df_reviews[(df_reviews['review_score'] >= 1) & (df_reviews['review_score'] <= 5)]

# 4. Crear una columna calculada de porcentaje (%) para enriquecer el análisis
total_reviews = df_reviews['cantidad'].sum()
df_reviews['porcentaje'] = ((df_reviews['cantidad'] / total_reviews) * 100).round(2)

# Visualizar la tabla limpia y formateada en Colab
print(f"Total de reseñas procesadas de forma limpia: {total_reviews:,}\n")
df_reviews
