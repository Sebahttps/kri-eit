-- Datos de ejemplo para desarrollo local
-- UUID fijo (identidad por defecto del dashboard).
--
-- El Supervisor nace BLOQUEADO a propósito. Este repositorio es público, y
-- publicar un hash bcrypt real —aunque la contraseña no esté— permite
-- descifrarlo sin conexión: sin límite de intentos, sin bloqueo y sin dejar
-- rastro. Con el correo también público y la URL del panel documentada, eso
-- basta para entrar al back-office.
--
-- El marcador de abajo no tiene la longitud de un hash bcrypt, así que
-- bcryptjs.compare() devuelve false para cualquier contraseña sin lanzar: el
-- login responde 401 limpio. Verificado.
--
--   Producción: `dropship-setup` pide correo y contraseña y los aplica.
--   Desarrollo local: generar un hash y hacer el UPDATE a mano —
--     node -e "console.log(require('bcryptjs').hashSync('tu-clave',10))"
--     UPDATE supervisors SET email='tu@correo', password_hash='<hash>'
--       WHERE id='00000000-0000-0000-0000-000000000001';
INSERT INTO supervisors (id, email, nombre, password_hash)
VALUES ('00000000-0000-0000-0000-000000000001', 'supervisor@example.invalid', 'Supervisor',
        'BLOQUEADO-sin-contrasena-ver-docs-deploy-production');

INSERT INTO suppliers (id, nombre, modo, base_url, latencia_media_ms, confiabilidad) VALUES
  ('11111111-1111-1111-1111-111111111111', 'MayoristaExpress', 'api',      'https://api.mayoristaexpress.example', 120, 0.98),
  ('22222222-2222-2222-2222-222222222222', 'ImportadoraSur',  'scraping',  'https://importadorasur.example',       850, 0.91);

INSERT INTO products (supplier_id, sku, nombre, categoria, costo, precio_venta, url_proveedor, trending_score) VALUES
  ('11111111-1111-1111-1111-111111111111', 'ME-001', 'Freidora de aire 5L',        'hogar',       28000, 42000, 'https://api.mayoristaexpress.example/products/ME-001', 87.5),
  ('11111111-1111-1111-1111-111111111111', 'ME-002', 'Aspiradora robot compacta',  'hogar',       55000, 79900, 'https://api.mayoristaexpress.example/products/ME-002', 74.2),
  ('22222222-2222-2222-2222-222222222222', 'IS-101', 'Audífonos inalámbricos Pro', 'tecnología',  12000, 21990, 'https://importadorasur.example/p/IS-101',              91.0),
  ('22222222-2222-2222-2222-222222222222', 'IS-205', 'Lámpara de escritorio LED',  'iluminación',  6500, 12990, 'https://importadorasur.example/p/IS-205',              45.8);
