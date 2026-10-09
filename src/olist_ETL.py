"""ETL de Olist: extrae con SQL, comprueba el grano y deja un CSV por consulta.

Las tres fases del proceso estan separadas:
    extraer   -> lee el .sql y lo ejecuta contra MySQL
    comprobar -> valida que el resultado tiene el grano declarado
    limpiar   -> aplica las reglas de src/limpieza.py
    exportar  -> escribe el CSV
    Las comprobaciones de grano son las que diferencian un ETL de un script que
escribe ficheros.
"""

from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text

from src.limpieza import limpiar
from src.config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    CARPETA_SQL,
    CARPETA_DATA,
)
# Cada consulta con la columna que define su grano.
CONSULTAS = {
    # Mx TABLA DE HECHOS. Mide, y es el centro del modelo.
    # DIMENSIONES. Describen, y se unen al hecho por su clave.
    # Segundo hecho
    # Un modelo puede tener varios hechos mientras cada uno declare su grano.
}
def crear_engine():
    print("Entro - Crear engine")
    """Crea el motor de conexión a MySQL con las credenciales del .env."""
    if not DB_USER or not DB_PASSWORD:
        raise RuntimeError(
            "Faltan DB_USER o DB_PASSWORD en el fichero .env. "
            "Copiad .env.example como .env y rellenadlo."
        )
    #url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)
def leer_consulta(nombre):
    """Devuelve el contenido del fichero .sql que contiene la consulta."""
    ruta = SQL / nombre
    return ruta.read_text(encoding="utf-8")

def ejecutar(engine, consulta_sql):
    """Ejecuta la consulta y devuelve un DataFrame de pandas."""
    try:
        with engine.connect() as conexion:
            df = pd.read_sql_query(consulta_sql, con=conexion)
            return df

    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        return None
def comprobar_grano(df):
    """Avisa si el número de filas no cuadra con el grano declarado."""
    filas = len(df)
    vendedores = df['seller_id'].nunique()
    #productos = df[product_id].nunique()

    if filas != vendedores:
        filas_dupli = filas - vendedores
        print(
            f"El DataFrame no cumple el grano de un vendedor'.\n"
            f"El JOIN está duplicando filas."
        )
        return False
    print("El grano es correcto.")
    return True    
def exportar(df, nombre_csv):
    """Guarda el DataFrame en data/ como CSV."""
    CARPETA_DATA.mkdir(exist_ok=True)  # por si la carpeta no existe todavía
    # Definir la ruta completa del archivo
    ruta_salida = CARPETA_DATA / nombre_csv
    # Exportar con index=False y encoding='utf-8-sig'
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
    print(f"Archivo exportado correctamente en: {ruta_salida.resolve()}")

def ejecutar_etl():
    """Recorre todas las consultas. Devuelve {nombre: (filas, ruta del csv)}."""
    engine = crear_engine()
    resultados = {}
    """"Mx"""

    return resultados