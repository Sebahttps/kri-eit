"""Servicio de Agentes IA — KRI-EIT Dropshipping.

Levanta las APIs de los dos agentes y el módulo de aprobaciones:
  /front-office/*   Agente B2C (chat de ventas/soporte, seguimiento)
  /back-office/*    Agente B2B (stock, órdenes de compra)
  /aprobaciones/*   Human-in-the-loop del Supervisor

OpenAPI interactivo en /docs.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import close_pool, get_pool
from .routers import aprobaciones, back_office, front_office


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    yield
    await close_pool()


app = FastAPI(
    title="KRI-EIT · Agentes IA de Dropshipping",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(front_office.router)
app.include_router(back_office.router)
app.include_router(aprobaciones.router)


@app.get("/health", tags=["infra"])
async def health():
    pool = await get_pool()
    await pool.fetchval("SELECT 1")
    return {"status": "ok"}
