"""Servicio del agente de Instagram.

    GET  /webhook      handshake de verificación de Meta
    POST /webhook      eventos entrantes (DMs, reacciones, historias, comentarios)
    GET  /panel        bandeja de borradores pendientes
    POST /borradores/{id}/enviar
    POST /borradores/{id}/descartar
    GET  /health
"""
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from .almacen import Almacen
from .config import settings
from .esquemas import normalizar
from .procesador import Procesador
from .seguridad import firma_valida, respuesta_verificacion

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("instagram-agent")

almacen = Almacen(settings.db_path)
procesador = Procesador(almacen)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await almacen.iniciar()
    yield


app = FastAPI(title="KRI-EIT · Agente de Instagram", version="0.1.0", lifespan=lifespan)


def _autorizar(token: str | None = Query(default=None)) -> None:
    """El panel expone tus DMs: sin token configurado, no se abre."""
    if not settings.panel_token:
        raise HTTPException(503, "IG_PANEL_TOKEN no está configurado")
    if token != settings.panel_token:
        raise HTTPException(401, "token inválido")


@app.get("/health", tags=["infra"])
async def health():
    return {"status": "ok", "modo": "solo_borradores" if settings.modo_solo_borradores
            else "auto", "auto_categorias": sorted(settings.auto_categorias_set)}


@app.get("/webhook", response_class=PlainTextResponse, tags=["meta"])
async def verificar(request: Request):
    p = request.query_params
    challenge = respuesta_verificacion(p.get("hub.mode"), p.get("hub.verify_token"),
                                       p.get("hub.challenge"), settings.verify_token)
    if challenge is None:
        raise HTTPException(403, "verificación fallida")
    return challenge


@app.post("/webhook", tags=["meta"])
async def recibir(request: Request, tareas: BackgroundTasks):
    crudo = await request.body()

    if not firma_valida(crudo, request.headers.get("x-hub-signature-256"),
                        settings.app_secret):
        log.warning("Webhook con firma inválida, descartado")
        raise HTTPException(403, "firma inválida")

    payload = await request.json()
    eventos = normalizar(payload, settings.ig_user_id)

    # Meta reintenta si no contestamos rápido; el trabajo real va en segundo plano.
    for evento in eventos:
        tareas.add_task(_procesar_seguro, evento)

    return {"recibidos": len(eventos)}


async def _procesar_seguro(evento) -> None:
    try:
        decision = await procesador.procesar(evento)
        log.info("Evento %s → %s (%s)", evento.id, decision.accion, decision.razon)
    except Exception:
        log.exception("Error procesando %s", evento.id)


class EnvioBorrador(BaseModel):
    texto: str | None = None


@app.get("/borradores", tags=["panel"], dependencies=[Depends(_autorizar)])
async def listar_borradores():
    return await almacen.pendientes()


@app.post("/borradores/{borrador_id}/enviar", tags=["panel"],
          dependencies=[Depends(_autorizar)])
async def enviar_borrador(borrador_id: int, cuerpo: EnvioBorrador):
    try:
        return await procesador.enviar_borrador(borrador_id, cuerpo.texto)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@app.post("/borradores/{borrador_id}/descartar", tags=["panel"],
          dependencies=[Depends(_autorizar)])
async def descartar_borrador(borrador_id: int):
    await almacen.marcar_borrador(borrador_id, "descartado")
    return {"id": borrador_id, "estado": "descartado"}


@app.get("/panel", response_class=HTMLResponse, tags=["panel"],
         dependencies=[Depends(_autorizar)])
async def panel(token: str = Query()):
    from .panel import render
    return render(await almacen.pendientes(), token)
