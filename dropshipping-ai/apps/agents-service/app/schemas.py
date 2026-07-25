"""Contratos de las APIs de los agentes (Pydantic). FastAPI publica el OpenAPI en /docs."""
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


# --- Front-Office (B2C) -----------------------------------------------------

class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    customer_id: UUID | None = None
    mensaje: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    conversation_id: UUID
    respuesta: str
    acciones: list[str] = []          # ej: ['stock_verificado', 'ticket_creado']


class SeguimientoResponse(BaseModel):
    order_id: UUID
    status: str
    carrier: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    eta: datetime | None = None
    eventos: list[dict[str, Any]] = []


# --- Back-Office (B2B) ------------------------------------------------------

class StockCheckRequest(BaseModel):
    product_id: UUID
    cantidad: int = Field(default=1, ge=1)


class StockCheckResponse(BaseModel):
    product_id: UUID
    en_stock: bool
    cantidad_disponible: int | None = None
    latencia_ms: int
    fuente: Literal["api", "scraping", "cache"]
    stock_check_id: int | None = None   # None si vino de caché
    checked_at: datetime


class PurchaseOrderRequest(BaseModel):
    order_id: UUID


class PurchaseOrderResponse(BaseModel):
    purchase_order_id: UUID | None = None
    status: Literal["emitida", "pendiente_aprobacion"]
    suggestion_id: UUID | None = None   # si quedó esperando al Supervisor
    detalle: str


# --- Sugerencias y aprobaciones (human-in-the-loop) -------------------------

class Suggestion(BaseModel):
    id: UUID
    agente: str
    tipo: str
    titulo: str
    detalle: dict[str, Any]
    status: str
    created_at: datetime


class DecisionRequest(BaseModel):
    decision: Literal["aprobar", "rechazar"]
    supervisor_id: UUID
    comentario: str | None = None


class DecisionResponse(BaseModel):
    suggestion_id: UUID
    status: str
    resultado: str      # qué hizo el agente al reanudarse
