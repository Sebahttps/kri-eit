-- Eventos en tiempo real vía LISTEN/NOTIFY: el gateway (business-api) escucha
-- el canal 'eventos' y lo retransmite por WebSocket al dashboard.

CREATE OR REPLACE FUNCTION fn_notify_sugerencia() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('eventos', json_build_object(
    'tipo', 'sugerencia', 'id', NEW.id, 'titulo', NEW.titulo,
    'status', NEW.status, 'agente', NEW.agente)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notify_sugerencia
  AFTER INSERT OR UPDATE OF status ON ai_suggestions
  FOR EACH ROW EXECUTE FUNCTION fn_notify_sugerencia();

CREATE OR REPLACE FUNCTION fn_notify_pedido() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('eventos', json_build_object(
    'tipo', 'pedido', 'id', NEW.id, 'numero', NEW.numero,
    'status', NEW.status, 'total', NEW.total)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notify_pedido
  AFTER INSERT OR UPDATE OF status ON orders
  FOR EACH ROW EXECUTE FUNCTION fn_notify_pedido();

CREATE OR REPLACE FUNCTION fn_notify_seguimiento() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('eventos', json_build_object(
    'tipo', 'seguimiento', 'shipment_id', NEW.shipment_id,
    'status', NEW.status, 'descripcion', NEW.descripcion)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notify_seguimiento
  AFTER INSERT ON shipment_events
  FOR EACH ROW EXECUTE FUNCTION fn_notify_seguimiento();

CREATE OR REPLACE FUNCTION fn_notify_ticket() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('eventos', json_build_object(
    'tipo', 'ticket', 'numero', NEW.numero, 'asunto', NEW.asunto,
    'status', NEW.status, 'prioridad', NEW.prioridad)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notify_ticket
  AFTER INSERT OR UPDATE OF status ON support_tickets
  FOR EACH ROW EXECUTE FUNCTION fn_notify_ticket();
