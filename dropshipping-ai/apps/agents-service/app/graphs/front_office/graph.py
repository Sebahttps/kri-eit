"""Agente Front-Office (B2C): chatbot de ventas y post-venta.

Agente ReAct (LangGraph) con Claude y herramientas contra la base de datos.
Las 5 promesas de venta están hard-coded en el system prompt Y en las
herramientas: el agente no puede prometer un pago sin verificar stock porque
la herramienta `verificar_disponibilidad` es el único camino para confirmarlo,
y el retracto/garantía los valida la propia base de datos (triggers).
"""
from uuid import UUID

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from ...config import settings
from ...db import get_pool
from ...tools.proveedores import verificar_stock

PROMESAS = """Eres el agente de ventas y post-venta de la tienda. Hablas español chileno cercano y profesional.

PROMESAS INQUEBRANTABLES (nunca las contradigas, siempre ofrécelas cuando aplique):
a) El pago SOLO se procesa después de confirmar stock con el proveedor. Verifica SIEMPRE con la herramienta antes de ofrecer el pago.
b) Ofrecemos reserva con abono: el cliente abona para reservar y paga el saldo al recibir. NUNCA ofrezcas pago 100% contra entrega.
c) Todo despacho incluye seguimiento en tiempo real; entrega el link/estado cuando te lo pidan.
d) Todos los productos tienen garantía legal de 6 meses; los reclamos se gestionan al instante con la herramienta de garantía.
e) El cliente tiene 10 días desde la entrega para retractarse sin dar explicaciones; si lo pide y está en plazo, ejecútalo de inmediato.

Persuade con honestidad: destaca beneficios reales, urgencia solo si el stock es realmente bajo. Si no sabes algo, crea un ticket de soporte en vez de inventar."""


@tool
async def buscar_productos(consulta: str) -> str:
    """Busca productos activos del catálogo por nombre o categoría."""
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT id, nombre, categoria, precio_venta, trending_score
           FROM products WHERE activo AND (nombre ILIKE '%' || $1 || '%' OR categoria ILIKE '%' || $1 || '%')
           ORDER BY trending_score DESC LIMIT 5""",
        consulta,
    )
    if not rows:
        return "Sin resultados para esa búsqueda."
    return "\n".join(f"- {r['nombre']} ({r['categoria']}) ${r['precio_venta']:,.0f} [id={r['id']}]" for r in rows)


@tool
async def verificar_disponibilidad(product_id: str, cantidad: int = 1) -> str:
    """Verifica stock real con el proveedor ANTES de ofrecer el pago (promesa a). Único camino válido para confirmar disponibilidad."""
    res = await verificar_stock(UUID(product_id), cantidad)
    if res.en_stock:
        return (f"STOCK CONFIRMADO con el proveedor en {res.latencia_ms} ms "
                f"(disponibles: {res.cantidad or 'suficientes'}). Puedes ofrecer pago online completo o reserva con abono.")
    return "SIN STOCK con el proveedor. NO ofrezcas el pago; sugiere alternativas del catálogo."


@tool
async def estado_pedido(order_id: str) -> str:
    """Consulta estado y seguimiento en tiempo real de un pedido (promesa c)."""
    pool = await get_pool()
    row = await pool.fetchrow(
        """SELECT o.status, s.carrier, s.tracking_number, s.tracking_url, s.status AS envio,
                  (SELECT descripcion FROM shipment_events se WHERE se.shipment_id = s.id
                   ORDER BY ocurrido_at DESC LIMIT 1) AS ultimo_evento
           FROM orders o LEFT JOIN shipments s ON s.order_id = o.id
           WHERE o.id = $1""",
        UUID(order_id),
    )
    if row is None:
        return "Pedido no encontrado."
    if row["tracking_number"] is None:
        return f"Estado del pedido: {row['status']}. Aún sin número de seguimiento."
    return (f"Estado: {row['status']} · Envío: {row['envio']} vía {row['carrier']} "
            f"({row['tracking_number']}) · Último evento: {row['ultimo_evento'] or 'sin eventos'} "
            f"· Link: {row['tracking_url'] or 'disponible pronto'}")


@tool
async def iniciar_reclamo_garantia(order_item_id: str, descripcion: str) -> str:
    """Abre un reclamo de garantía legal de 6 meses (promesa d). La base valida la vigencia."""
    pool = await get_pool()
    warranty = await pool.fetchrow(
        "SELECT id, status, vence_at FROM warranties WHERE order_item_id = $1", UUID(order_item_id))
    if warranty is None:
        return "Ese ítem aún no tiene garantía activa (se activa al momento de la entrega)."
    if warranty["status"] not in ("activa", "en_reclamo"):
        return f"La garantía está en estado '{warranty['status']}' (vencía el {warranty['vence_at']:%d-%m-%Y})."
    claim_id = await pool.fetchval(
        """INSERT INTO warranty_claims (warranty_id, descripcion) VALUES ($1, $2) RETURNING id""",
        warranty["id"], descripcion)
    await pool.execute("UPDATE warranties SET status = 'en_reclamo' WHERE id = $1", warranty["id"])
    return f"Reclamo de garantía abierto (folio {claim_id}). Vigente hasta {warranty['vence_at']:%d-%m-%Y}."


@tool
async def ejercer_retracto(order_id: str, motivo: str = "") -> str:
    """Ejecuta el derecho a retracto de 10 días (promesa e). El trigger de la base aprueba o rechaza según el plazo."""
    pool = await get_pool()
    try:
        await pool.execute(
            "INSERT INTO withdrawals (order_id, motivo) VALUES ($1, $2)", UUID(order_id), motivo or None)
        return "Retracto APROBADO automáticamente. Coordinaremos la recolección y el reembolso."
    except Exception as e:  # el trigger levanta RETRACTO_FUERA_DE_PLAZO / RETRACTO_INVALIDO
        msg = str(e)
        if "FUERA_DE_PLAZO" in msg:
            return "El plazo de 10 días desde la entrega ya venció, por lo que el retracto no aplica. Ofrece revisar la garantía de 6 meses si hay una falla."
        if "RETRACTO_INVALIDO" in msg:
            return "El pedido aún no ha sido entregado; puede cancelarse en vez de retractarse."
        raise


@tool
async def crear_ticket(asunto: str, order_id: str = "", prioridad: int = 3) -> str:
    """Crea un ticket de soporte para casos que el agente no puede resolver solo."""
    pool = await get_pool()
    numero = await pool.fetchval(
        """INSERT INTO support_tickets (asunto, order_id, prioridad)
           VALUES ($1, $2, $3) RETURNING numero""",
        asunto, UUID(order_id) if order_id else None, max(1, min(5, prioridad)))
    return f"Ticket #{numero} creado. Un humano lo revisará si el agente no logra resolverlo."


HERRAMIENTAS = [buscar_productos, verificar_disponibilidad, estado_pedido,
                iniciar_reclamo_garantia, ejercer_retracto, crear_ticket]


def construir_agente():
    modelo = ChatAnthropic(model=settings.model, api_key=settings.anthropic_api_key,
                           max_tokens=1024, temperature=0.3)
    return create_react_agent(modelo, HERRAMIENTAS, prompt=PROMESAS)
