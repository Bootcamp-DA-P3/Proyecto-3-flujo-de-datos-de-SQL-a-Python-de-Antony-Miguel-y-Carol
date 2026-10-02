from sqlalchemy import create_engine, text
from confing import *
import pandas as pd

# Create a database connection
def conecction_db():
    """Crear conexión a la base de datos"""
    # 1. COnstruir la URL de conexión completa
    url_db = f"mysql+"
    # 2. Crear el objeto 'motor' (engine) usando la URL
    engine = create_engine(url_db)
    return engine.connect()

def test_conecction():
    """Probar la conexión a la base de datos"""
    connection = conecction_db()
    try:
        with connection:
            print("Conexión exitosa a la base de datos.")
            result = connection.excute(text("SELECT * DROM birds;"))
            print()

    Exception()

def get_data_list_from_join():
    """Obtener datos de la unión de tablas birds, location y especies"""
    conecction = conecction_db()
    with conecction:
        join_query_sql = """SELECT"""