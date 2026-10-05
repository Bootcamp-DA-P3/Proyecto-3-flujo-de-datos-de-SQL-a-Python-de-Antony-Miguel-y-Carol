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
    print("URL: ", url)
    return create_engine(url)

def leer_consulta(nombre):
    print("Entro - Leer consulta")
    """Devuelve el contenido del fichero .sql que contiene la consulta."""
    ruta = SQL / nombre
    print(ruta)
    contenido = ruta.read_text(encoding="utf-8")
    print(contenido)
    return contenido

def ejecutar(engine, consulta_sql):
    print("Entro - Ejecutar")
    """Ejecuta la consulta y devuelve un DataFrame de pandas."""
    print("Empeiza la fiesta")

    try:
        with engine.connect() as conexion:
            print("hola vecinito")
            df = pd.read_sql_query(sql=text(consulta_sql), con=conexion)
            print("hola holita")
            print(df.head(5))
            return df

    except SQLAlchemyError as e:
        print(f"❌ Error al conectar a la base de datos o ejecutar el SQL: {e}")
        return None

    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        return None

def comprobar_grano(df):
    print("Entro - Compruebo grano")
    """Avisa si el número de filas no cuadra con el grano declarado.

    Si el grano es 'un pedido', entonces debe cumplirse que
    len(df) == número de order_id distintos. Si no cuadra, el JOIN
    está duplicando filas y todas vuestras sumas serán mayores de lo real.
    """
    # TODO: comparar el total de filas con el de valores únicos de
    #       CLAVE_DE_GRANO, e imprimir un aviso claro si no coinciden
    #raise NotImplementedError("comprobar_grano")

def exportar(df, nombre_csv):
    print("Entro - Exportar")
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

    #print(f"Filas .......... {len(df):,}")
    #print(f"Columnas ....... {df.shape[1]}")

    #comprobar_grano(df)
    exportar(df, CONSULTA.replace(".sql", ".csv"))


if __name__ == "__main__":
    main()