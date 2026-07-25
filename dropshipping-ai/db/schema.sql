-- ============================================================================
-- KRI-EIT · Sistema de Dropshipping Autónomo con Agentes IA
-- Esquema PostgreSQL 16
--
-- Las 5 promesas de venta están codificadas como reglas duras de la base:
--   (a) Stock confirmado antes de procesar el pago  -> trigger trg_pago_requiere_stock
--   (b) Pago contra entrega habilitado              -> enum payment_method ('contra_entrega')
--   (c) Despacho con seguimiento en tiempo real     -> tabla shipments + shipment_events
--   (d) Garantía legal de 6 meses automatizada      -> trigger trg_entrega_activa_garantia
--   (e) Retracto de 10 días sin fricción            -> trigger trg_retracto_dentro_de_plazo
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;      -- gen_random_uuid()
-- CREATE EXTENSION IF NOT EXISTS vector;     -- descomentar para memoria RAG del agente B2C

-- ----------------------------------------------------------------------------
-- Enums
-- ----------------------------------------------------------------------------

CREATE TYPE order_status AS ENUM (
  'carrito',                    -- cliente armando el pedido
  'verificando_stock',          -- Agente B2B consultando proveedor
  'stock_confirmado',           -- promesa (a): stock verificado, se habilita el pago
  'pago_pendiente',
  'pagado',
  'contra_entrega_confirmado',  -- promesa (b): pedido válido sin pago anticipado
  'oc_emitida',                 -- orden de compra enviada al proveedor
  'despachado',
  'en_transito',
  'entregado',
  'completado',                 -- ventana de retracto vencida sin reclamos
  'cancelado',
  'retractado'                  -- promesa (e) ejercida
);

CREATE TYPE payment_method  AS ENUM ('online', 'contra_entrega');
CREATE TYPE payment_status  AS ENUM ('pendiente', 'autorizado', 'pagado', 'reembolsado', 'fallido', 'no_aplica');
CREATE TYPE supplier_mode   AS ENUM ('api', 'scraping');
CREATE TYPE po_status       AS ENUM ('borrador', 'emitida', 'aceptada', 'rechazada', 'completada');
CREATE TYPE shipment_status AS ENUM ('preparando', 'despachado', 'en_transito', 'en_reparto', 'entregado', 'devuelto', 'extraviado');
CREATE TYPE warranty_status AS ENUM ('activa', 'vencida', 'en_reclamo', 'consumida');
CREATE TYPE claim_status    AS ENUM ('abierto', 'en_gestion', 'aprobado', 'rechazado', 'resuelto');
CREATE TYPE withdrawal_status AS ENUM ('solicitado', 'aprobado_auto', 'recoleccion_agendada', 'reembolsado', 'cerrado');
CREATE TYPE ticket_status   AS ENUM ('abierto', 'en_progreso', 'esperando_cliente', 'resuelto', 'cerrado');
CREATE TYPE suggestion_status AS ENUM ('pendiente', 'aprobada', 'rechazada', 'expirada');
CREATE TYPE agent_kind      AS ENUM ('front_office', 'back_office', 'sistema');

-- ----------------------------------------------------------------------------
-- Núcleo: usuarios, proveedores, productos
-- ----------------------------------------------------------------------------

CREATE TABLE supervisors (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email         text NOT NULL UNIQUE,
  nombre        text NOT NULL,
  password_hash text NOT NULL,
  activo        boolean NOT NULL DEFAULT true,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE suppliers (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre             text NOT NULL,
  modo               supplier_mode NOT NULL,          -- api | scraping
  base_url           text NOT NULL,
  api_key_ref        text,                            -- referencia al secreto (nunca la clave en claro)
  selector_stock     text,                            -- selector CSS/XPath si modo = scraping
  latencia_media_ms  integer NOT NULL DEFAULT 0,
  confiabilidad      numeric(4,3) NOT NULL DEFAULT 1.000 CHECK (confiabilidad BETWEEN 0 AND 1),
  activo             boolean NOT NULL DEFAULT true,
  created_at         timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE products (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  supplier_id     uuid NOT NULL REFERENCES suppliers(id),
  sku             text NOT NULL,
  nombre          text NOT NULL,
  descripcion     text,
  categoria       text NOT NULL,
  costo           numeric(12,2) NOT NULL CHECK (costo >= 0),
  precio_venta    numeric(12,2) NOT NULL CHECK (precio_venta >= 0),
  margen_pct      numeric(5,2) GENERATED ALWAYS AS
                    (CASE WHEN costo > 0 THEN round((precio_venta - costo) / costo * 100, 2) ELSE 0 END) STORED,
  url_proveedor   text,                               -- página del producto para verificación de stock
  trending_score  numeric(6,2) NOT NULL DEFAULT 0,    -- calculado por el Agente B2B
  activo          boolean NOT NULL DEFAULT true,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (supplier_id, sku)
);

-- Historial de verificaciones de stock (promesa a): cada consulta queda registrada
CREATE TABLE stock_checks (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_id   uuid NOT NULL REFERENCES products(id),
  supplier_id  uuid NOT NULL REFERENCES suppliers(id),
  en_stock     boolean NOT NULL,
  cantidad     integer,
  latencia_ms  integer NOT NULL,
  fuente       supplier_mode NOT NULL,
  checked_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_stock_checks_product ON stock_checks (product_id, checked_at DESC);

-- ----------------------------------------------------------------------------
-- Clientes y pedidos
-- ----------------------------------------------------------------------------

CREATE TABLE customers (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre     text NOT NULL,
  email      text UNIQUE,
  telefono   text,
  direccion  text,
  comuna     text,
  region     text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  numero                bigint GENERATED ALWAYS AS IDENTITY,   -- número humano correlativo
  customer_id           uuid NOT NULL REFERENCES customers(id),
  status                order_status NOT NULL DEFAULT 'carrito',
  payment_method        payment_method,
  payment_status        payment_status NOT NULL DEFAULT 'pendiente',
  total                 numeric(12,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
  -- promesa (a): el trigger exige este campo antes de aceptar un pago
  stock_confirmado_at   timestamptz,
  stock_check_id        bigint REFERENCES stock_checks(id),
  pagado_at             timestamptz,
  entregado_at          timestamptz,
  -- promesa (e): límite calculado al momento de la entrega (entregado_at + 10 días)
  limite_retracto_at    timestamptz,
  cancelado_motivo      text,
  created_at            timestamptz NOT NULL DEFAULT now(),
  updated_at            timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_created ON orders (created_at DESC);

CREATE TABLE order_items (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id        uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id      uuid NOT NULL REFERENCES products(id),
  cantidad        integer NOT NULL CHECK (cantidad > 0),
  precio_unitario numeric(12,2) NOT NULL CHECK (precio_unitario >= 0),
  costo_unitario  numeric(12,2) NOT NULL CHECK (costo_unitario >= 0)
);
CREATE INDEX idx_order_items_order ON order_items (order_id);

-- ----------------------------------------------------------------------------
-- B2B: órdenes de compra al proveedor y despachos
-- ----------------------------------------------------------------------------

CREATE TABLE purchase_orders (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id      uuid NOT NULL REFERENCES orders(id),
  supplier_id   uuid NOT NULL REFERENCES suppliers(id),
  status        po_status NOT NULL DEFAULT 'borrador',
  costo_total   numeric(12,2) NOT NULL DEFAULT 0,
  emitida_por   agent_kind NOT NULL DEFAULT 'back_office',
  ref_proveedor text,                                  -- id/nro que devuelve el proveedor
  emitida_at    timestamptz,
  created_at    timestamptz NOT NULL DEFAULT now()
);

-- Promesa (c): seguimiento en tiempo real
CREATE TABLE shipments (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id        uuid NOT NULL REFERENCES orders(id),
  carrier         text NOT NULL,
  tracking_number text NOT NULL,
  tracking_url    text,
  status          shipment_status NOT NULL DEFAULT 'preparando',
  eta             timestamptz,
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (carrier, tracking_number)
);

CREATE TABLE shipment_events (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  shipment_id uuid NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
  status      shipment_status NOT NULL,
  descripcion text NOT NULL,
  ubicacion   text,
  ocurrido_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_shipment_events ON shipment_events (shipment_id, ocurrido_at DESC);

-- ----------------------------------------------------------------------------
-- Post-venta: garantías (d) y retracto (e)
-- ----------------------------------------------------------------------------

CREATE TABLE warranties (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_item_id uuid NOT NULL UNIQUE REFERENCES order_items(id),
  status        warranty_status NOT NULL DEFAULT 'activa',
  inicia_at     timestamptz NOT NULL,
  vence_at      timestamptz NOT NULL,     -- inicia_at + 6 meses (lo fija el trigger)
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE warranty_claims (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  warranty_id  uuid NOT NULL REFERENCES warranties(id),
  status       claim_status NOT NULL DEFAULT 'abierto',
  descripcion  text NOT NULL,
  resolucion   text,
  gestionado_por agent_kind NOT NULL DEFAULT 'front_office',
  created_at   timestamptz NOT NULL DEFAULT now(),
  resuelto_at  timestamptz
);

CREATE TABLE withdrawals (      -- retracto, promesa (e)
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id     uuid NOT NULL UNIQUE REFERENCES orders(id),
  status       withdrawal_status NOT NULL DEFAULT 'solicitado',
  motivo       text,
  solicitado_at timestamptz NOT NULL DEFAULT now(),
  reembolsado_at timestamptz
);

-- ----------------------------------------------------------------------------
-- Front-Office: conversaciones y tickets
-- ----------------------------------------------------------------------------

CREATE TABLE conversations (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid REFERENCES customers(id),
  canal       text NOT NULL DEFAULT 'web',
  abierta     boolean NOT NULL DEFAULT true,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE messages (
  id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  conversation_id uuid NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  rol             text NOT NULL CHECK (rol IN ('cliente', 'agente', 'sistema')),
  contenido       text NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_messages_conv ON messages (conversation_id, created_at);

CREATE TABLE support_tickets (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  numero          bigint GENERATED ALWAYS AS IDENTITY,
  customer_id     uuid REFERENCES customers(id),
  order_id        uuid REFERENCES orders(id),
  conversation_id uuid REFERENCES conversations(id),
  status          ticket_status NOT NULL DEFAULT 'abierto',
  asunto          text NOT NULL,
  prioridad       smallint NOT NULL DEFAULT 3 CHECK (prioridad BETWEEN 1 AND 5),
  created_at      timestamptz NOT NULL DEFAULT now(),
  resuelto_at     timestamptz
);
CREATE INDEX idx_tickets_status ON support_tickets (status, created_at DESC);

-- ----------------------------------------------------------------------------
-- Supervisión: sugerencias de la IA y auditoría
-- ----------------------------------------------------------------------------

-- Módulo "Sugerencias de la IA" del dashboard: toda decisión crítica pasa por aquí.
-- Guarda el thread_id del checkpoint de LangGraph para reanudar el grafo al decidir.
CREATE TABLE ai_suggestions (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  agente        agent_kind NOT NULL,
  tipo          text NOT NULL,               -- ej: 'ajuste_margen', 'nuevo_producto', 'cambio_proveedor'
  titulo        text NOT NULL,               -- ej: 'Producto X en tendencia: ¿subir margen a 40%?'
  detalle       jsonb NOT NULL DEFAULT '{}', -- payload estructurado (producto, valores propuestos, evidencia)
  status        suggestion_status NOT NULL DEFAULT 'pendiente',
  thread_id     text,                        -- checkpoint LangGraph a reanudar tras la decisión
  decidido_por  uuid REFERENCES supervisors(id),
  decidido_at   timestamptz,
  expira_at     timestamptz,
  created_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_suggestions_pending ON ai_suggestions (status, created_at DESC);

-- Auditoría total: cada acción de agente queda registrada (clave para garantías legales)
CREATE TABLE agent_actions (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  agente      agent_kind NOT NULL,
  accion      text NOT NULL,                 -- ej: 'stock_verificado', 'oc_emitida', 'garantia_activada'
  entidad     text,                          -- tabla afectada
  entidad_id  text,
  detalle     jsonb NOT NULL DEFAULT '{}',
  created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_agent_actions ON agent_actions (agente, created_at DESC);

-- ----------------------------------------------------------------------------
-- Triggers: las promesas como reglas inquebrantables
-- ----------------------------------------------------------------------------

-- (a) Ningún pago se procesa sin stock confirmado por el proveedor
CREATE OR REPLACE FUNCTION fn_pago_requiere_stock() RETURNS trigger AS $$
BEGIN
  IF NEW.payment_status IN ('autorizado', 'pagado') AND NEW.stock_confirmado_at IS NULL THEN
    RAISE EXCEPTION 'PROMESA_A_VIOLADA: no se puede procesar el pago del pedido % sin stock confirmado', NEW.id;
  END IF;
  IF NEW.status = 'contra_entrega_confirmado' AND NEW.stock_confirmado_at IS NULL THEN
    RAISE EXCEPTION 'PROMESA_A_VIOLADA: no se puede confirmar contra entrega del pedido % sin stock confirmado', NEW.id;
  END IF;
  NEW.updated_at := now();
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pago_requiere_stock
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION fn_pago_requiere_stock();

-- (d) + (e) Al marcar entregado: activa garantías de 6 meses por ítem
--           y fija la ventana de retracto de 10 días
CREATE OR REPLACE FUNCTION fn_entrega_activa_garantia() RETURNS trigger AS $$
BEGIN
  IF NEW.status = 'entregado' AND (OLD.status IS DISTINCT FROM 'entregado') THEN
    NEW.entregado_at      := COALESCE(NEW.entregado_at, now());
    NEW.limite_retracto_at := NEW.entregado_at + interval '10 days';

    INSERT INTO warranties (order_item_id, inicia_at, vence_at)
    SELECT oi.id, NEW.entregado_at, NEW.entregado_at + interval '6 months'
    FROM order_items oi
    WHERE oi.order_id = NEW.id
    ON CONFLICT (order_item_id) DO NOTHING;

    INSERT INTO agent_actions (agente, accion, entidad, entidad_id, detalle)
    VALUES ('sistema', 'garantia_activada', 'orders', NEW.id::text,
            jsonb_build_object('vence_garantia', NEW.entregado_at + interval '6 months',
                               'limite_retracto', NEW.limite_retracto_at));
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_entrega_activa_garantia
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION fn_entrega_activa_garantia();

-- (e) Retracto sin fricción: dentro del plazo se aprueba automáticamente;
--     fuera del plazo, la base lo rechaza de plano
CREATE OR REPLACE FUNCTION fn_retracto_dentro_de_plazo() RETURNS trigger AS $$
DECLARE v_limite timestamptz;
BEGIN
  SELECT limite_retracto_at INTO v_limite FROM orders WHERE id = NEW.order_id;
  IF v_limite IS NULL THEN
    RAISE EXCEPTION 'RETRACTO_INVALIDO: el pedido % aún no ha sido entregado', NEW.order_id;
  END IF;
  IF now() > v_limite THEN
    RAISE EXCEPTION 'RETRACTO_FUERA_DE_PLAZO: el plazo de 10 días del pedido % venció el %', NEW.order_id, v_limite;
  END IF;
  NEW.status := 'aprobado_auto';   -- sin fricción: aprobación inmediata
  UPDATE orders SET status = 'retractado' WHERE id = NEW.order_id;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_retracto_dentro_de_plazo
  BEFORE INSERT ON withdrawals
  FOR EACH ROW EXECUTE FUNCTION fn_retracto_dentro_de_plazo();

-- ----------------------------------------------------------------------------
-- Vistas de KPIs para el dashboard
-- ----------------------------------------------------------------------------

CREATE VIEW kpi_ventas_diarias AS
SELECT date_trunc('day', created_at)::date AS dia,
       count(*) FILTER (WHERE status NOT IN ('carrito', 'cancelado')) AS pedidos,
       coalesce(sum(total) FILTER (WHERE payment_status = 'pagado'
                                      OR status IN ('contra_entrega_confirmado','oc_emitida','despachado',
                                                    'en_transito','entregado','completado')), 0) AS ventas
FROM orders
GROUP BY 1;

CREATE VIEW kpi_conversion AS
SELECT date_trunc('day', created_at)::date AS dia,
       count(*) AS total_pedidos,
       count(*) FILTER (WHERE status NOT IN ('carrito','cancelado')) AS convertidos,
       round(count(*) FILTER (WHERE status NOT IN ('carrito','cancelado'))::numeric
             / nullif(count(*), 0) * 100, 2) AS tasa_conversion_pct
FROM orders
GROUP BY 1;

CREATE VIEW kpi_tickets AS
SELECT count(*) FILTER (WHERE status IN ('abierto','en_progreso')) AS abiertos,
       count(*) FILTER (WHERE status = 'resuelto' AND resuelto_at > now() - interval '24 hours') AS resueltos_24h,
       round(avg(extract(epoch FROM (resuelto_at - created_at)) / 3600)
             FILTER (WHERE resuelto_at IS NOT NULL), 1) AS horas_promedio_resolucion
FROM support_tickets;

CREATE VIEW kpi_tendencias_productos AS
SELECT p.id, p.nombre, p.categoria, p.trending_score, p.margen_pct,
       count(oi.id) FILTER (WHERE o.created_at > now() - interval '7 days') AS ventas_7d,
       count(oi.id) FILTER (WHERE o.created_at > now() - interval '30 days') AS ventas_30d
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
LEFT JOIN orders o ON o.id = oi.order_id AND o.status NOT IN ('carrito','cancelado')
GROUP BY p.id;
