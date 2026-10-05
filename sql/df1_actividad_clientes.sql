-- DATAFRAME 1 · Actividad de clientes
-- Tablas: customers, orders, order_payments, order_reviews, geolocation
--
-- GRANO DECLARADO: una fila = ...............................
-- (rellenad esta linea ANTES de escribir el primer JOIN)

SELECT COUNT(DISTINCT customer_unique_id) AS total_clientes
FROM customers;
SELECT c.customer_state, 
    AVG(r.review_score) AS nota_media,
    COUNT(DISTINCT c.customer_unique_id) AS clientes
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_reviews r ON o.order_id = r.order_id
GROUP BY c.customer_state
ORDER BY clientes DESC;
SELECT c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    COUNT(o.order_id) AS total_pedidos
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id, c.customer_city, c.customer_state
ORDER BY total_pedidos DESC
LIMIT 10;
SELECT review_score, COUNT(*) AS cantidad
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;