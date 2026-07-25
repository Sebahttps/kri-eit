"""API del Agente Back-Office (B2B): verificación de stock y órdenes de compra."""
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from ..db import audit, get_pool
from ..graphs.back_office.graph import grafo_oc
from ..schemas import (PurchaseOrderRequest, PurchaseOrderResponse,
                       StockCheckRequest, StockCheckResponse)
from ..tools.proveedores import verificar_stock

router = APIRouter(prefix="/back-office", tags=["Agente Back-Office (B2B)"])


@router.post("/stock/verificar", response_model=StockCheckResponse)
async def verificar(req: StockCheckRequest) -> StockCheckResponse:
    """Verificación de stock en milisegundos contra el proveedor (promesa a)."""
    from datetime import datetime, timezone
    try:
        res = await verificar_stock(req.product_id, req.cantidad)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return StockCheckResponse(
        product_id=req.product_id, en_stock=res.en_stock,
        cantidad_disponible=res.cantidad, latencia_ms=res.latencia_ms,
        fuente=res.fuente, stock_check_id=res.stock_check_id,
        checked_at=datetime.now(timezone.utc))


@router.post("/pedidos/{order_id}/confirmar-stock")
async def confirmar_stock_pedido(order_id: UUID):
    """Verifica stock de TODOS los ítems del pedido y, si están, marca stock_confirmado_at.
    Es el único camino para habilitar el pago (promesa a)."""
    pool = await get_pool()
    items = await pool.fetch(
        "SELECT product_id, cantidad FROM order_items WHERE order_id = $1", order_id)
    if not items:
        raise HTTPException(404, "Pedido sin ítems o inexistente")

    faltantes, ultimo_check = [], None
    for it in items:
        res = await verificar_stock(it["product_id"], it["cantidad"])
        if not res.en_stock:
            faltantes.append(str(it["product_id"]))
        if res.stock_check_id:
            ultimo_check = res.stock_check_id

    if faltantes:
        await pool.execute(
            "UPDATE orders SET status = 'verificando_stock' WHERE id = $1", order_id)
        return {"stock_confirmado": False, "productos_sin_stock": faltantes}

    await pool.execute(
        """UPDATE orders SET status = 'stock_confirmado', stock_confirmado_at = now(),
                             stock_check_id = $2
           WHERE id = $1""", order_id, ultimo_check)
    await audit("back_office", "stock_pedido_confirmado", "orders", str(order_id))
    return {"stock_confirmado": True, "pago_habilitado": True}


@router.post("/ordenes-compra", response_model=PurchaseOrderResponse)
async def emitir_orden_compra(req: PurchaseOrderRequest) -> PurchaseOrderResponse:
    """Corre el grafo B2B. Bajo el umbral emite la OC de inmediato; sobre él,
    pausa (interrupt) y crea una Sugerencia IA para el Supervisor."""
    thread_id = f"oc-{req.order_id}-{uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": thread_id}}
    try:
        resultado = await grafo_oc.ainvoke({"order_id": str(req.order_id)}, config)
    except ValueError as e:
        raise HTTPException(422, str(e))

    interrupts = resultado.get("__interrupt__")
    if interrupts:
        payload = interrupts[0].value
        pool = await get_pool()
        suggestion_id = await pool.fetchval(
            """INSERT INTO ai_suggestions (agente, tipo, titulo, detalle, thread_id)
               VALUES ('back_office', $1, $2, $3::jsonb, $4) RETURNING id""",
            payload["tipo"], payload["titulo"], payload, thread_id)
        await audit("back_office", "sugerencia_creada", "ai_suggestions", str(suggestion_id), payload)
        return PurchaseOrderResponse(
            status="pendiente_aprobacion", suggestion_id=suggestion_id,
            detalle="La OC supera el umbral de autonomía; esperando decisión del Supervisor.")

    return PurchaseOrderResponse(
        status="emitida",
        purchase_order_id=UUID(resultado["purchase_order_id"]),
        detalle="Orden de compra emitida al proveedor de forma autónoma.")
