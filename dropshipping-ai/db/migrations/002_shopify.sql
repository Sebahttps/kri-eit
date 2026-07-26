-- Modo híbrido: Shopify como vitrina/checkout, agentes como back-office.
-- Vincula el pedido de Shopify con el pedido interno: deduplica reintentos
-- del webhook orders/create y permite sincronizar el fulfillment de vuelta.
CREATE TABLE IF NOT EXISTS shopify_orders (
  shopify_order_id bigint PRIMARY KEY,
  order_id         uuid NOT NULL REFERENCES orders(id),
  shop_domain      text NOT NULL,
  created_at       timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_shopify_orders_order ON shopify_orders(order_id);
