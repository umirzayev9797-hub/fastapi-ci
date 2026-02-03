SELECT
    o.order_no,
    m.full_name,
    c.full_name
FROM 'order' AS o
JOIN manager AS m ON o.manager_id = m.manager_id
JOIN customer AS c ON o.customer_id = c.customer_id
WHERE m.city <> c.city;