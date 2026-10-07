import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import *

RAIZ = Path(__file__).resolve().parent.parent
SQL = RAIZ / "sql"
DATA = RAIZ / "data"

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DEL EQUIPO
# ---------------------------------------------------------------------------

# CSV elegido
CONSULTA = "df3_vendedores_popularidad.sql"

# El grano, en lenguaje de negocio.
GRANO = "Actividad acumulada de un producto único comercializado por un vendedor específico"

# Columna que identifica una fila según ese grano.
CLAVE_DE_GRANO = "seller_id, product_id"

# ---------------------------------------------------------------------------

def crear_engine():
    print("Entro - Crear engine")
    """Crea el motor de conexión a MySQL con las credenciales del .env."""
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

    except SQLAlchemyError as e:
        print(f"❌ Error al conectar a la base de datos o ejecutar el SQL: {e}")
        return None

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
    DATA.mkdir(exist_ok=True)  # por si la carpeta no existe todavía
    # Definir la ruta completa del archivo
    ruta_salida = DATA / nombre_csv
    # Exportar con index=False y encoding='utf-8-sig'
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
    print(f"Archivo exportado correctamente en: {ruta_salida.resolve()}")

def main():
    print(f"Consulta ....... {CONSULTA}")
    print(f"Grano .......... una fila = {GRANO}")

    engine = crear_engine()
    consulta_sql = leer_consulta(CONSULTA)
    df = ejecutar(engine, consulta_sql)

    print(df)

    print(f"Filas .......... {len(df):,}")
    print(f"Columnas ....... {df.shape[1]}")

    comprobar_grano(df)
    exportar(df, CONSULTA.replace(".sql", ".csv"))


if __name__ == "__main__":
    main()