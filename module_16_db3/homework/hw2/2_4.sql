SELECT c.full_name, o.order_no
FROM 'order' AS o
JOIN customer AS c ON o.customer_id = c.customer_id
WHERE o.manager_id IS NULL;