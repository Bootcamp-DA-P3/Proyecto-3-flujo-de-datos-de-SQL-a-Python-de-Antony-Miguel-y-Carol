-- DATAFRAME 3 · Vendedores y popularidad
-- Tablas: sellers, order_items, products
--
-- GRANO DECLARADO: Una fila representa la actividad acumulada de un producto único comercializado por un vendedor específico

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