-- Datos de demostración (solo desarrollo): pedidos de los últimos 30 días,
-- tickets y una sugerencia pendiente, para ver el dashboard con vida.
-- Aplicar DESPUÉS de schema.sql y seed.sql.

INSERT INTO customers (id, nombre, email, comuna) VALUES
  ('cccccccc-0000-0000-0000-000000000001', 'María González', 'maria@example.cl', 'Providencia'),
  ('cccccccc-0000-0000-0000-000000000002', 'Jorge Díaz', 'jorge@example.cl', 'Maipú'),
  ('cccccccc-0000-0000-0000-000000000003', 'Camila Rojas', 'camila@example.cl', 'Concepción');

-- 30 días de pedidos con volumen variable (una fila por pedido)
DO $$
DECLARE
  d integer;
  n integer;
  i integer;
  v_customer uuid;
  v_order uuid;
  v_product record;
  v_estado order_status;
BEGIN
  FOR d IN 0..29 LOOP
    n := 2 + (d * 7 % 5) + CASE WHEN d % 7 IN (5, 6) THEN 3 ELSE 0 END;
    FOR i IN 1..n LOOP
      SELECT id INTO v_customer FROM customers ORDER BY random() LIMIT 1;
      SELECT id, precio_venta, costo INTO v_product FROM products ORDER BY random() LIMIT 1;
      -- ~1 de cada 4 se queda en carrito (alimenta la tasa de conversión)
      v_estado := CASE WHEN i % 4 = 0 THEN 'carrito' ELSE 'completado' END;

      INSERT INTO orders (customer_id, status, payment_method, payment_status,
                          total, stock_confirmado_at, created_at)
      VALUES (v_customer, 'carrito',
              (CASE WHEN i % 3 = 0 THEN 'contra_entrega' ELSE 'online' END)::payment_method,
              'pendiente', v_product.precio_venta,
              CASE WHEN v_estado <> 'carrito' THEN now() - (d || ' days')::interval END,
              now() - (d || ' days')::interval - (i || ' hours')::interval)
      RETURNING id INTO v_order;

      INSERT INTO order_items (order_id, product_id, cantidad, precio_unitario, costo_unitario)
      VALUES (v_order, v_product.id, 1, v_product.precio_venta, v_product.costo);

      IF v_estado <> 'carrito' THEN
        UPDATE orders SET status = 'stock_confirmado' WHERE id = v_order;
        UPDATE orders SET status = 'pagado', payment_status = 'pagado',
                          pagado_at = created_at + interval '1 hour'
        WHERE id = v_order;
        UPDATE orders SET status = 'completado' WHERE id = v_order;
      END IF;
    END LOOP;
  END LOOP;
END $$;

-- Verificaciones de stock recientes (para el KPI de latencia)
INSERT INTO stock_checks (product_id, supplier_id, en_stock, cantidad, latencia_ms, fuente)
SELECT p.id, p.supplier_id, true, 20 + (row_number() OVER ()) * 3,
       CASE s.modo WHEN 'api' THEN 90 + (row_number() OVER ()) * 7 ELSE 700 + (row_number() OVER ()) * 40 END,
       s.modo
FROM products p JOIN suppliers s ON s.id = p.supplier_id, generate_series(1, 5);

-- Tickets de soporte
INSERT INTO support_tickets (customer_id, asunto, status, prioridad) VALUES
  ('cccccccc-0000-0000-0000-000000000001', 'Mi pedido llegó con la caja dañada', 'abierto', 2),
  ('cccccccc-0000-0000-0000-000000000002', 'Consulta sobre garantía de la freidora', 'en_progreso', 3),
  ('cccccccc-0000-0000-0000-000000000003', '¿Puedo cambiar la dirección de entrega?', 'abierto', 4);
INSERT INTO support_tickets (asunto, status, prioridad, created_at, resuelto_at) VALUES
  ('Seguimiento no cargaba', 'resuelto', 3, now() - interval '20 hours', now() - interval '18 hours'),
  ('Duda sobre pago contra entrega', 'resuelto', 4, now() - interval '10 hours', now() - interval '9 hours');

-- Una sugerencia pendiente del Agente B2B (sin thread_id: decisión solo-registro)
INSERT INTO ai_suggestions (agente, tipo, titulo, detalle) VALUES
  ('back_office', 'ajuste_margen',
   '"Audífonos inalámbricos Pro" está en tendencia (score 91): ¿autorizas subir el precio a $24.990?',
   '{"producto_sku": "IS-101", "precio_actual": 21990, "precio_propuesto": 24990, "evidencia": "ventas 7d al alza y stock estable del proveedor"}');
