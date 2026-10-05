from sqlalchemy import create_engine, text
from config import *
import pandas as pd

# Create a database connection
def conecction_db():
    """Crear conexión a la base de datos"""
    # 1. COnstruir la URL de conexión completa
    url_db = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    # 2. Crear el objeto 'motor' (engine) usando la URL
    engine = create_engine(url_db)
    return engine.connect()

def test_conecction():
    """Probar la conexión a la base de datos"""
    connection = conecction_db()
    try:
        with connection:
            print("Conexión exitosa a la base de datos.")
            result = connection.excute(text("SELECT * FROM olist;"))
            print()

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")()

def get_data_list_from_join():
    """Obtener datos de vendedores, productos y ventas"""
    conecction = conecction_db()
    with conecction:
        join_query_sql = """  
            SELECT 
                LOWER(TRIM(s.seller_city)) AS seller_city_clean,
                LOWER(TRIM(s.seller_state)) AS seller_state_clean,
                s.seller_id,
                p.product_id,
                p.product_category_name,
                COUNT(oi.order_item_id) AS unidades_vendidas_producto,
                COUNT(DISTINCT oi.order_id) AS pedidos_distintos_producto,
                ROUND(SUM(oi.price), 2) AS ingreso_total_producto,
                DENSE_RANK() OVER (
                    PARTITION BY s.seller_id 
                    ORDER BY COUNT(oi.order_item_id) DESC, SUM(oi.price) DESC
                ) AS ranking_producto_en_vendedor
            FROM sellers s
            INNER JOIN order_items oi 
                ON s.seller_id = oi.seller_id
            INNER JOIN products p 
                ON oi.product_id = p.product_id
            GROUP BY 
                LOWER(TRIM(s.seller_city)),
                LOWER(TRIM(s.seller_state)),
                s.seller_id,
                p.product_id,
                p.product_category_name
            ORDER BY 
                unidades_vendidas_producto DESC,
                ingreso_total_producto DESC;
        """
    
        result = conecction.execute(text(join_query_sql))
        rows = result.fetchall()
        columns = result.keys()

        # 2. Create the Pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)
            
        # --- 3. EXPORTAR A CSV (Paso Nuevo) ---
        df.to_csv(
            "data/dashboard_vendedores_productos.csv",  # <- Nombre del archivo
            index=False,  # Evita escribir el índice del DataFrame en el archivo
            encoding='utf-8'  # Asegura que caracteres especiales se guarden bien
        )

        print(f"✅ DataFrame successfully created and saved to: {'data/dashboard_vendedores_productos.csv'}")

        return df
        
if __name__ == "__main__":
    test_conecction()
    get_data_list_from_join()
