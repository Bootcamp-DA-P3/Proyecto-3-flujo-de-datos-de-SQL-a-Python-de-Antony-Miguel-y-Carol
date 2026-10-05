-- DATAFRAME 2 · Catalogo de productos
-- Tablas: products, categoria_traduccion, order_items, sellers
--
-- GRANO DECLARADO: una fila = ...............................

SELECT 
    o.order_id AS 'ID de Pedido',
    o.order_status AS 'Estado',
    o.order_purchase_timestamp AS 'Fecha de Compra',
    c.customer_unique_id AS 'ID Único Cliente',
    c.customer_city AS 'Ciudad Cliente',
    c.customer_state AS 'Estado Cliente'
FROM `orders` o
INNER JOIN `customers` c ON o.customer_id = c.customer_id
ORDER BY o.order_purchase_timestamp DESC;