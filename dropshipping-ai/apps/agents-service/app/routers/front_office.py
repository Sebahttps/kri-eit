"""API del Agente Front-Office (B2C): chat de ventas/soporte y seguimiento."""
from uuid import UUID

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from ..db import get_pool
from ..graphs.front_office.graph import construir_agente
from ..schemas import ChatRequest, ChatResponse, SeguimientoResponse

router = APIRouter(prefix="/front-office", tags=["Agente Front-Office (B2C)"])

_agente = None


def agente():
    global _agente
    if _agente is None:
        _agente = construir_agente()
    return _agente


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    pool = await get_pool()

    conv_id = req.conversation_id
    if conv_id is None:
        conv_id = await pool.fetchval(
            "INSERT INTO conversations (customer_id) VALUES ($1) RETURNING id", req.customer_id)

    await pool.execute(
        "INSERT INTO messages (conversation_id, rol, contenido) VALUES ($1, 'cliente', $2)",
        conv_id, req.mensaje)

    # historial reciente para dar contexto al agente
    historial = await pool.fetch(
        """SELECT rol, contenido FROM messages WHERE conversation_id = $1
           ORDER BY created_at DESC LIMIT 20""", conv_id)
    contexto = "\n".join(f"[{m['rol']}] {m['contenido']}" for m in reversed(historial[1:]))
    entrada = (f"Historial reciente:\n{contexto}\n\nCliente: {req.mensaje}"
               if contexto else req.mensaje)

    resultado = await agente().ainvoke({"messages": [HumanMessage(content=entrada)]})
    mensajes = resultado["messages"]
    respuesta = mensajes[-1].content if mensajes else "Lo siento, no pude procesar tu consulta."
    if isinstance(respuesta, list):  # Claude puede responder en bloques
        respuesta = " ".join(b.get("text", "") for b in respuesta if isinstance(b, dict))

    acciones = sorted({
        tc["name"] for m in mensajes
        for tc in (getattr(m, "tool_calls", None) or [])
    })

    await pool.execute(
        "INSERT INTO messages (conversation_id, rol, contenido) VALUES ($1, 'agente', $2)",
        conv_id, respuesta)

    return ChatResponse(conversation_id=conv_id, respuesta=respuesta, acciones=list(acciones))


@router.get("/pedidos/{order_id}/seguimiento", response_model=SeguimientoResponse)
async def seguimiento(order_id: UUID) -> SeguimientoResponse:
    """Seguimiento en tiempo real (promesa c) — usable por el chat y por la tienda."""
    pool = await get_pool()
    row = await pool.fetchrow(
        """SELECT o.id, o.status, s.id AS shipment_id, s.carrier, s.tracking_number, s.tracking_url, s.eta
           FROM orders o LEFT JOIN shipments s ON s.order_id = o.id WHERE o.id = $1""", order_id)
    if row is None:
        raise HTTPException(404, "Pedido no encontrado")
    eventos = []
    if row["shipment_id"]:
        eventos = [dict(e) for e in await pool.fetch(
            """SELECT status::text, descripcion, ubicacion, ocurrido_at
               FROM shipment_events WHERE shipment_id = $1 ORDER BY ocurrido_at DESC""",
            row["shipment_id"])]
    return SeguimientoResponse(
        order_id=row["id"], status=row["status"], carrier=row["carrier"],
        tracking_number=row["tracking_number"], tracking_url=row["tracking_url"],
        eta=row["eta"], eventos=eventos)
