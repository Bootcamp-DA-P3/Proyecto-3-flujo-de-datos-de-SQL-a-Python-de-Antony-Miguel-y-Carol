<img width="11520" height="3456" alt="Banner_notebooks" src="./assets/banner_p3.jpg" />

# Flujo de datos de SQL a Python — Olist Marketplace 🛒

## 📝 Descripción del Proyecto

Este proyecto aborda la extracción, modelado y limpieza de los datos transaccionales del marketplace brasileño **Olist** (2016–2018). El objetivo principal consiste en transformar un modelo de datos relacional y transaccional (OLTP) en un **conjunto de datos analítico (OLAP)** optimizado para responder a preguntas clave de negocio, automatizaciones ETL y la posterior construcción de cuadros de mando analíticos.

El flujo de trabajo se divide en dos grandes bloques:
1. **Modelado y limpieza en SQL:** Creación de dataframes exploratorios y definición de una consulta analítica estandarizada y agregada.
2. **Procesamiento y limpieza final en Python:** Validación de tipos, tratamiento de atípicos, ingeniería de características y exportación optimizada.

---

## 👥 Equipo e Integrantes

* **Integrantes del equipo:**
  * Carol Rueda
  * Anthony Rodriguez
  * Miguel López

---

## 📌 Definición estratégica del Dataframe seleccionado

### Dataframe 3: Vendedores y popularidad

> **Grano declarado:**  
> **«Una fila representa la actividad acumulada de un producto único comercializado por un vendedor específico.»**

* **Clave primaria compuesta:** `(seller_id, product_id)`

---

## 🎯 KPIs y Métricas de Negocio

El dataset preparado permite monitorear y evaluar los siguientes Indicadores Clave de Rendimiento (KPIs):

1. **Unidades vendidas por producto (`unidades_vendidas_producto`):** Frecuencia de movimiento de cada artículo en el catálogo de un vendedor.
2. **Número de pedidos distintos (`pedidos_distintos_producto`):** Penetración del producto en pedidos únicos (evita duplicidades por cantidad).
3. **Facturación por producto (`ingreso_total_producto`):** Volumen monetario total aportado por un producto específico a las ventas de un vendedor.
4. **Ranking de popularidad (`ranking_producto_en_vendedor`):** Posición relativa del producto según la preferencia de compra dentro del catálogo de un vendedor.
5. **Concentración de catálogo:** Proporción del volumen de ventas generado por los productos top en comparación con el resto del inventario.

---

## 🛠️ Extracción y Limpieza en SQL

### Criterios y reglas de negocio aplicadas
* **Estandarización de cadenas:** Aplicación de `LOWER(TRIM())` en `seller_city` y `seller_state` para corregir inconsistencias tipográficas y de formato.
* **Integridad referencial:** Integración mediante `INNER JOIN` entre `sellers`, `order_items` y `products`, garantizando que únicamente se analicen registros activos y válidos.
* **Manejo de duplicidad por ítem:** `order_items` almacena cada unidad vendida como un registro independiente. Se implementó `COUNT(DISTINCT order_id)` para contabilizar la cantidad real de transacciones sin sobreestimar el volumen de pedidos.
* **Productos sin ventas:** Se excluyen los productos del catálogo que no han registrado ventas para centrar el modelo en la actividad económica activa y no distorsionar los cálculos de rendimiento.

### 📄 Consulta SQL Final (`query_vendedores_popularidad.sql`)

```sql
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
```

---

## 🐍 Procesamiento y limpieza en Python (Google Colab)

El procesamiento del dataframe exportado se llevó a cabo dentro del notebook Jupyter en Google Colab siguiendo las siguientes etapas:

1. **Carga e inspección inicial:** Verificación del número de registros, estructura del dataset e identificación del uso de memoria.
2. **Normalización de tipos de datos:** Conversión explícita de campos identificadores a tipo cadena (`string`) y métricas numéricas a enteros/flotantes (`int64`, `float64`).
3. **Tratamiento de valores nulos:** Imputación de categorías desconocidas en `product_category_name` mediante el valor por defecto `'sin_categoria'`.
4. **Validación de inconsistencias y duplicados:** Confirmación de la inexistencia de filas duplicadas en la combinación `(seller_id, product_id)`.
5. **Análisis de outliers:** Identificación de valores atípicos en precios e ingresos agrupados a través de diagramas de caja (boxplots) e histogramas.
6. **Ingeniería de características (Columnas derivadas):**
   * **`precio_promedio_unidad`:** Calculado como `ingreso_total_producto / unidades_vendidas_producto`.
   * **`es_top_vendedor`:** Indicador booleano (`True`/`False`) que identifica si el producto ocupa el puesto número 1 en ventas dentro del catálogo del vendedor.

---

## 🗂️ Estructura del Repositorio

```
.
├── sql/                               ← las TRES consultas, en SQL Workbench
│   ├── df1_actividad_clientes.sql
│   ├── df2_catalogo_productos.sql
│   └── df3_vendedores_popularidad.sql
│
├── src/                               ← el código, en VS Code
│   ├── config.py                        lee las credenciales del .env
│   └── main.py                          conecta, consulta y exporta el CSV
│
├── notebooks/
│   └── limpieza.ipynb                 ← la limpieza final, en Colab o VS Code
│
├── data/                              ← el CSV exportado. NO se sube
│   └── .gitkeep
│
├── .env                               ← vuestras credenciales. NO se sube
├── .env_example                         plantilla del anterior, SÍ se sube
├── .gitignore
├── requirements.txt
└── README.md                          ← documentad aquí vuestras decisiones
```

---

## 🚀 Instrucciones de Ejecución

1. **Configuración de la Base de Datos (MySQL)
   * **Descargar e importar el archivo olist.sql en tu gestor de base de datos MySQL local:

   Descarga el volcado y cárgalo en tu MySQL local:

   📥 **[olist.sql.gz](https://drive.google.com/drive/folders/1apSXjn6eQ5o9RdutbD4skSjvH6ytvR06?usp=sharing)** · 46 MB comprimido, 145 MB al descomprimir

   ```bash
   # Windows (PowerShell), tras descomprimir con 7-Zip:
   mysql -u root -p < olist.sql
   ```

   Tarda unos minutos: son **1.550.922 filas**. Al terminar tendrás la base `olist` con 9 tablas.

   ### ✅ Comprueba que cargó bien

   Antes de empezar, ejecuta esto. Las nueve tablas deben coincidir:

   ```sql
   USE olist;

   SELECT 'categoria_traduccion' t, COUNT(*) filas, 71      esperado FROM categoria_traduccion
   UNION ALL SELECT 'products',       COUNT(*),      32951   FROM products
   UNION ALL SELECT 'sellers',        COUNT(*),      3095    FROM sellers
   UNION ALL SELECT 'customers',      COUNT(*),      99441   FROM customers
   UNION ALL SELECT 'geolocation',    COUNT(*),      1000163 FROM geolocation
   UNION ALL SELECT 'orders',         COUNT(*),      99441   FROM orders
   UNION ALL SELECT 'order_items',    COUNT(*),      112650  FROM order_items
   UNION ALL SELECT 'order_payments', COUNT(*),      103886  FROM order_payments
   UNION ALL SELECT 'order_reviews',  COUNT(*),      99224   FROM order_reviews;
   ```

   Y comprueba que los acentos portugueses se cargaron bien:

   ```sql
   SELECT DISTINCT product_category_name FROM products
   WHERE product_category_name LIKE '%m_veis%' LIMIT 3;   -- debe salir 'moveis_...'
   ```

   Si algún número no cuadra, vuelve a cargar el volcado antes de seguir.
   
   > [!NOTE]
   > Son datos **reales** de 99.441 pedidos realizados en Brasil entre 2016 y 2018.
   > Fuente: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) · licencia CC BY-NC-SA 4.0.


2.  **Entorno y ejecución en Visual Studio Code
    * **Abrir un terminal en la carpeta que se quiera descargar el proyecto.

    ```bash
    git clone https://github.com/Bootcamp-DA-P3/Proyecto-3-flujo-de-datos-de-SQL-a-Python-de-Antony-Miguel-y-Carol.git
    cd Proyecto-3-flujo-de-datos-de-SQL-a-Python-de-Antony-Miguel-y-Carol
    code .
    ```

    * **Instalación de librerias necesarias.

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

    * **Crear copia de `.env_example` llamada `.env` y rellenar los datos de vuestro entorno.

    ```bash
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    DB_NAME=
    ```

     * **Generar fichero .csv

    ```bash
    python src/main.py
    ```

    3.  **Entorno y ejecución en Google Colab
    * **Abrir Google Colab y subir el notebook TERMINAR
    * **Cargar el archivo CSV exportado desde SQL en el entorno de trabajo del notebook.
    * **Ejecutar de forma secuencial todas las celdas del notebook para generar los análisis, visualizaciones y la versión final del dataset procesado.

---

## 📋 Checklist de Limpieza (Python)

- [ ] Verificación de tipos de datos y conversión adecuada.
- [ ] Detección y tratamiento de valores duplicados.
- [ ] Tratamiento de datos faltantes (nulos).
- [ ] Estandarización de texto (cadenas sin espacios y en minúsculas).
- [ ] Detección e inspección visual de outliers.
- [ ] Creación de columnas derivadas útiles para negocio.
- [ ] Generación de visualizaciones explicativas y de validación.
- [ ] Exportación del dataset procesado en formato final.