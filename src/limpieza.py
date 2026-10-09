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