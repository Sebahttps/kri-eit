-- Datos de ejemplo para desarrollo local
-- UUID fijo (identidad por defecto del dashboard). La contraseña no está en el
-- repo, solo su hash bcrypt; para usar la tuya, genera un hash y reemplázalo
-- (ver docs/deploy-production.md, sección "Cambiar la contraseña del Supervisor").
INSERT INTO supervisors (id, email, nombre, password_hash)
VALUES ('00000000-0000-0000-0000-000000000001', 'sebastianmenat@gmail.com', 'Supervisor',
        '$2a$10$f3aWjjLDOEgCcYxKXougg.zeoKkO4f/vjx.H4FhZmNrppJWqyjp.i');

INSERT INTO suppliers (id, nombre, modo, base_url, latencia_media_ms, confiabilidad) VALUES
  ('11111111-1111-1111-1111-111111111111', 'MayoristaExpress', 'api',      'https://api.mayoristaexpress.example', 120, 0.98),
  ('22222222-2222-2222-2222-222222222222', 'ImportadoraSur',  'scraping',  'https://importadorasur.example',       850, 0.91);

INSERT INTO products (supplier_id, sku, nombre, categoria, costo, precio_venta, url_proveedor, trending_score) VALUES
  ('11111111-1111-1111-1111-111111111111', 'ME-001', 'Freidora de aire 5L',        'hogar',       28000, 42000, 'https://api.mayoristaexpress.example/products/ME-001', 87.5),
  ('11111111-1111-1111-1111-111111111111', 'ME-002', 'Aspiradora robot compacta',  'hogar',       55000, 79900, 'https://api.mayoristaexpress.example/products/ME-002', 74.2),
  ('22222222-2222-2222-2222-222222222222', 'IS-101', 'Audífonos inalámbricos Pro', 'tecnología',  12000, 21990, 'https://importadorasur.example/p/IS-101',              91.0),
  ('22222222-2222-2222-2222-222222222222', 'IS-205', 'Lámpara de escritorio LED',  'iluminación',  6500, 12990, 'https://importadorasur.example/p/IS-205',              45.8);
