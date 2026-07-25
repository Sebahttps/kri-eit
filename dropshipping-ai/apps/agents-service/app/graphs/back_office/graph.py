"""Agente Back-Office (B2B): flujo de emisión de órdenes de compra.

Grafo LangGraph con human-in-the-loop:

    verificar_pedido -> evaluar_autonomia -+-> emitir_oc            (bajo umbral: autónomo)
                                           +-> esperar_supervisor   (interrupt: Sugerencia IA)
                                                    |
                                          [Supervisor aprueba/rechaza en el dashboard]
                                                    |
                                           emitir_oc | rechazado

El interrupt persiste en el checkpointer Postgres; el grafo se reanuda con
Command(resume=...) cuando llega la decisión vía POST /aprobaciones/{id}/decision.
"""
import json
from typing import Literal, TypedDict
from uuid import UUID

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from ...config import settings
from ...db import audit, get_pool


class EstadoOC(TypedDict, total=False):
    order_id: str
    supplier_id: str
    costo_total: float
    stock_ok: bool
    requiere_aprobacion: bool
    decision: str            # 'aprobar' | 'rechazar'
    purchase_order_id: str
    resultado: str


async def verificar_pedido(state: EstadoOC) -> EstadoOC:
    """Valida que el pedido tenga stock confirmado y pago resuelto, y calcula el costo."""
    pool = await get_pool()
    row = await pool.fetchrow(
        """SELECT o.id, o.status, o.stock_confirmado_at,
                  sum(oi.costo_unitario * oi.cantidad) AS costo_total,
                  min(p.supplier_id::text) AS supplier_id
           FROM orders o
           JOIN order_items oi ON oi.order_id = o.id
           JOIN products p ON p.id = oi.product_id
           WHERE o.id = $1
           GROUP BY o.id""",
        UUID(state["order_id"]),
    )
    if row is None:
        raise ValueError(f"Pedido {state['order_id']} no existe")
    if row["stock_confirmado_at"] is None:
        raise ValueError("PROMESA_A: el pedido no tiene stock confirmado; no se emite OC")
    if row["status"] not in ("pagado", "contra_entrega_confirmado"):
        raise ValueError(f"El pedido está en estado '{row['status']}'; se requiere pago o contra entrega confirmada")
    return {
        "stock_ok": True,
        "costo_total": float(row["costo_total"]),
        "supplier_id": row["supplier_id"],
    }


async def evaluar_autonomia(state: EstadoOC) -> Command[Literal["emitir_oc", "esperar_supervisor"]]:
    """Bajo el umbral el agente actúa solo; sobre él, escala al Supervisor."""
    if state["costo_total"] <= settings.umbral_costo_oc:
        return Command(goto="emitir_oc", update={"requiere_aprobacion": False})
    return Command(goto="esperar_supervisor", update={"requiere_aprobacion": True})


async def esperar_supervisor(state: EstadoOC) -> EstadoOC:
    """Pausa el grafo y registra una Sugerencia IA. Se reanuda con la decisión del dashboard."""
    decision = interrupt({
        "tipo": "aprobar_oc",
        "titulo": f"OC de ${state['costo_total']:,.0f} supera el umbral de autonomía "
                  f"(${settings.umbral_costo_oc:,.0f}). ¿Autorizas la compra?",
        "order_id": state["order_id"],
        "costo_total": state["costo_total"],
    })
    return {"decision": decision}


async def emitir_oc(state: EstadoOC) -> EstadoOC:
    if state.get("requiere_aprobacion") and state.get("decision") != "aprobar":
        return {"resultado": "rechazada_por_supervisor"}
    pool = await get_pool()
    po_id = await pool.fetchval(
        """INSERT INTO purchase_orders (order_id, supplier_id, status, costo_total, emitida_at)
           VALUES ($1, $2, 'emitida', $3, now()) RETURNING id""",
        UUID(state["order_id"]), UUID(state["supplier_id"]), state["costo_total"],
    )
    await pool.execute("UPDATE orders SET status = 'oc_emitida' WHERE id = $1", UUID(state["order_id"]))
    await audit("back_office", "oc_emitida", "purchase_orders", str(po_id),
                {"order_id": state["order_id"], "costo_total": state["costo_total"],
                 "aprobada_por_supervisor": bool(state.get("requiere_aprobacion"))})
    return {"purchase_order_id": str(po_id), "resultado": "emitida"}


def construir_grafo(checkpointer=None):
    g = StateGraph(EstadoOC)
    g.add_node("verificar_pedido", verificar_pedido)
    g.add_node("evaluar_autonomia", evaluar_autonomia)
    g.add_node("esperar_supervisor", esperar_supervisor)
    g.add_node("emitir_oc", emitir_oc)
    g.add_edge(START, "verificar_pedido")
    g.add_edge("verificar_pedido", "evaluar_autonomia")
    g.add_edge("esperar_supervisor", "emitir_oc")
    g.add_edge("emitir_oc", END)
    return g.compile(checkpointer=checkpointer or MemorySaver())


# Instancia por defecto (en producción se inyecta PostgresSaver desde main.py)
grafo_oc = construir_grafo()
