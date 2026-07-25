"""API de aprobaciones: el human-in-the-loop del Supervisor.

El dashboard lista las sugerencias pendientes y envía la decisión; si la
sugerencia tiene un thread_id de LangGraph, el grafo pausado se reanuda con
Command(resume=<decision>) y continúa exactamente donde quedó.
"""
from uuid import UUID

from fastapi import APIRouter, HTTPException
from langgraph.types import Command

from ..db import audit, get_pool
from ..graphs.back_office.graph import grafo_oc
from ..schemas import DecisionRequest, DecisionResponse, Suggestion

router = APIRouter(prefix="/aprobaciones", tags=["Supervisor (human-in-the-loop)"])


@router.get("/pendientes", response_model=list[Suggestion])
async def pendientes() -> list[Suggestion]:
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT id, agente::text, tipo, titulo, detalle, status::text, created_at
           FROM ai_suggestions WHERE status = 'pendiente' ORDER BY created_at DESC""")
    return [Suggestion(**dict(r)) for r in rows]


@router.post("/{suggestion_id}/decision", response_model=DecisionResponse)
async def decidir(suggestion_id: UUID, req: DecisionRequest) -> DecisionResponse:
    pool = await get_pool()
    sug = await pool.fetchrow(
        "SELECT id, status::text, thread_id FROM ai_suggestions WHERE id = $1", suggestion_id)
    if sug is None:
        raise HTTPException(404, "Sugerencia no encontrada")
    if sug["status"] != "pendiente":
        raise HTTPException(409, f"La sugerencia ya fue decidida ({sug['status']})")

    nuevo_status = "aprobada" if req.decision == "aprobar" else "rechazada"
    await pool.execute(
        """UPDATE ai_suggestions SET status = $2::suggestion_status,
                                     decidido_por = $3, decidido_at = now()
           WHERE id = $1""", suggestion_id, nuevo_status, req.supervisor_id)

    resultado = "registrada"
    if sug["thread_id"]:
        config = {"configurable": {"thread_id": sug["thread_id"]}}
        estado = await grafo_oc.ainvoke(Command(resume=req.decision), config)
        resultado = estado.get("resultado", "reanudado")

    await audit("sistema", f"sugerencia_{nuevo_status}", "ai_suggestions", str(suggestion_id),
                {"supervisor_id": str(req.supervisor_id), "comentario": req.comentario,
                 "resultado_grafo": resultado})
    return DecisionResponse(suggestion_id=suggestion_id, status=nuevo_status, resultado=resultado)
