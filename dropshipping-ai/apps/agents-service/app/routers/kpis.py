"""KPIs para el Dashboard del Supervisor. Lee las vistas kpi_* del esquema."""
from fastapi import APIRouter

from ..db import get_pool

router = APIRouter(prefix="/kpis", tags=["Dashboard del Supervisor"])


@router.get("/resumen")
async def resumen():
    """Tarjetas superiores del dashboard: el pulso del negocio hoy."""
    pool = await get_pool()
    hoy = await pool.fetchrow(
        """SELECT coalesce(sum(total) FILTER (WHERE payment_status = 'pagado'
                     OR status IN ('contra_entrega_confirmado','oc_emitida','despachado',
                                   'en_transito','entregado','completado')), 0) AS ventas_hoy,
                  count(*) FILTER (WHERE status NOT IN ('carrito','cancelado')) AS pedidos_hoy,
                  round(count(*) FILTER (WHERE status NOT IN ('carrito','cancelado'))::numeric
                        / nullif(count(*), 0) * 100, 1) AS conversion_hoy
           FROM orders WHERE created_at >= date_trunc('day', now())""")
    tickets = await pool.fetchrow("SELECT * FROM kpi_tickets")
    pendientes = await pool.fetchval(
        "SELECT count(*) FROM ai_suggestions WHERE status = 'pendiente'")
    stock = await pool.fetchrow(
        """SELECT round(avg(latencia_ms)) AS latencia_media_ms, count(*) AS checks_24h
           FROM stock_checks WHERE checked_at > now() - interval '24 hours'""")
    return {
        "ventas_hoy": float(hoy["ventas_hoy"]),
        "pedidos_hoy": hoy["pedidos_hoy"],
        "conversion_hoy_pct": float(hoy["conversion_hoy"] or 0),
        "tickets_abiertos": tickets["abiertos"],
        "tickets_resueltos_24h": tickets["resueltos_24h"],
        "horas_promedio_resolucion": float(tickets["horas_promedio_resolucion"] or 0),
        "sugerencias_pendientes": pendientes,
        "stock_latencia_media_ms": int(stock["latencia_media_ms"] or 0),
        "stock_checks_24h": stock["checks_24h"],
    }


@router.get("/ventas")
async def ventas(dias: int = 30):
    """Serie diaria de ventas y conversión para los gráficos de tendencia."""
    dias = max(1, min(dias, 365))
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT d.dia::date::text AS dia, coalesce(v.ventas, 0) AS ventas,
                  coalesce(v.pedidos, 0) AS pedidos,
                  coalesce(c.tasa_conversion_pct, 0) AS conversion_pct
           FROM generate_series(current_date - ($1::int - 1), current_date, '1 day') AS d(dia)
           LEFT JOIN kpi_ventas_diarias v ON v.dia = d.dia::date
           LEFT JOIN kpi_conversion c ON c.dia = d.dia::date
           ORDER BY 1""", dias)
    return [{"dia": r["dia"], "ventas": float(r["ventas"]), "pedidos": r["pedidos"],
             "conversion_pct": float(r["conversion_pct"])} for r in rows]


@router.get("/tendencias")
async def tendencias(limite: int = 8):
    """Productos ordenados por trending_score, con sus ventas recientes y margen."""
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT id, nombre, categoria, trending_score, margen_pct, ventas_7d, ventas_30d
           FROM kpi_tendencias_productos ORDER BY trending_score DESC LIMIT $1""",
        max(1, min(limite, 50)))
    return [dict(r) | {"id": str(r["id"]), "trending_score": float(r["trending_score"]),
                       "margen_pct": float(r["margen_pct"])} for r in rows]


@router.get("/tickets")
async def tickets_recientes(limite: int = 10):
    pool = await get_pool()
    rows = await pool.fetch(
        """SELECT t.numero, t.asunto, t.status::text, t.prioridad, t.created_at,
                  c.nombre AS cliente
           FROM support_tickets t LEFT JOIN customers c ON c.id = t.customer_id
           WHERE t.status IN ('abierto', 'en_progreso', 'esperando_cliente')
           ORDER BY t.prioridad ASC, t.created_at DESC LIMIT $1""",
        max(1, min(limite, 50)))
    return [dict(r) | {"created_at": r["created_at"].isoformat()} for r in rows]
