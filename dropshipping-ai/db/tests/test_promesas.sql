-- Prueba de las promesas codificadas en la base
\set ON_ERROR_STOP off

-- setup: cliente + pedido + ítem
INSERT INTO customers (id, nombre, email) VALUES ('aaaaaaaa-0000-0000-0000-000000000001', 'Cliente Test', 'test@test.cl');
INSERT INTO orders (id, customer_id, total, payment_method)
  VALUES ('bbbbbbbb-0000-0000-0000-000000000001', 'aaaaaaaa-0000-0000-0000-000000000001', 42000, 'online');
INSERT INTO order_items (order_id, product_id, cantidad, precio_unitario, costo_unitario)
  SELECT 'bbbbbbbb-0000-0000-0000-000000000001', id, 1, 42000, 28000 FROM products WHERE sku = 'ME-001';

\echo '--- TEST (a): pagar SIN stock confirmado debe FALLAR ---'
UPDATE orders SET payment_status = 'pagado' WHERE id = 'bbbbbbbb-0000-0000-0000-000000000001';

\echo '--- TEST (a): con stock confirmado el pago debe PASAR ---'
UPDATE orders SET status = 'stock_confirmado', stock_confirmado_at = now()
  WHERE id = 'bbbbbbbb-0000-0000-0000-000000000001';
UPDATE orders SET payment_status = 'pagado', status = 'pagado', pagado_at = now()
  WHERE id = 'bbbbbbbb-0000-0000-0000-000000000001';
SELECT status, payment_status FROM orders WHERE id = 'bbbbbbbb-0000-0000-0000-000000000001';

\echo '--- TEST (d)+(e): entregar debe activar garantia 6m y ventana retracto 10d ---'
UPDATE orders SET status = 'entregado' WHERE id = 'bbbbbbbb-0000-0000-0000-000000000001';
SELECT w.status, (w.vence_at - w.inicia_at) AS duracion_garantia,
       (o.limite_retracto_at - o.entregado_at) AS ventana_retracto
FROM warranties w JOIN order_items oi ON oi.id = w.order_item_id
JOIN orders o ON o.id = oi.order_id
WHERE o.id = 'bbbbbbbb-0000-0000-0000-000000000001';

\echo '--- TEST (e): retracto dentro de plazo debe auto-aprobarse ---'
INSERT INTO withdrawals (order_id, motivo) VALUES ('bbbbbbbb-0000-0000-0000-000000000001', 'no me gusto');
SELECT w.status AS retracto, o.status AS pedido
FROM withdrawals w JOIN orders o ON o.id = w.order_id
WHERE w.order_id = 'bbbbbbbb-0000-0000-0000-000000000001';

\echo '--- TEST (e): retracto de pedido NO entregado debe FALLAR ---'
INSERT INTO orders (id, customer_id, total) VALUES ('bbbbbbbb-0000-0000-0000-000000000002', 'aaaaaaaa-0000-0000-0000-000000000001', 100);
INSERT INTO withdrawals (order_id) VALUES ('bbbbbbbb-0000-0000-0000-000000000002');

\echo '--- Auditoria registrada automaticamente ---'
SELECT agente, accion, entidad FROM agent_actions ORDER BY id;
