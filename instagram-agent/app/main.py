"""Servicio del agente de Instagram.

    GET  /webhook      handshake de verificación de Meta
    POST /webhook      eventos entrantes (DMs, reacciones, historias, comentarios)
    GET  /panel        bandeja de borradores pendientes
    POST /borradores/{id}/enviar
    POST /borradores/{id}/descartar
    GET  /health
"""
import hmac
import logging
from contextlib import asynccontextmanager

from fastapi import (BackgroundTasks, Cookie, Depends, FastAPI, HTTPException,
                     Query, Request)
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
    # Sin `IG_IG_USER_ID` el filtro de `esquemas.normalizar` compara contra ""
    # y no excluye nada: un comentario propio —que no trae `is_echo`— entraría
    # como si fuera de otra persona y el agente se contestaría a sí mismo. Es la
    # mitad de la defensa contra el bucle y era opcional por descuido, así que
    # el servicio no arranca sin ella.
    if not settings.ig_user_id:
        raise RuntimeError(
            "Falta IG_IG_USER_ID (el IGSID de tu propia cuenta). Sin eso el "
            "agente no distingue tus propios comentarios y puede responderse "
            "a sí mismo en bucle.")
    await almacen.iniciar()
    yield


app = FastAPI(title="KRI-EIT · Agente de Instagram", version="0.1.0", lifespan=lifespan)


COOKIE_PANEL = "ig_panel"


def _autorizar(token: str | None = Query(default=None),
               cookie: str | None = Cookie(default=None, alias=COOKIE_PANEL)) -> None:
    """El panel expone tus DMs: sin token configurado, no se abre.

    El token se acepta por query **solo para entrar**; de ahí en adelante viaja
    en una cookie `HttpOnly`. Una credencial en la URL queda escrita en el log
    de accesos de Caddy y en el historial del navegador, y esta abre los
    mensajes privados de Sebastián: no puede vivir ahí.

    `compare_digest` en vez de `==` porque comparar credenciales carácter a
    carácter filtra por tiempo cuánto prefijo acertaste.
    """
    if not settings.panel_token:
        raise HTTPException(503, "IG_PANEL_TOKEN no está configurado")
    presentado = cookie or token or ""
    if not hmac.compare_digest(presentado, settings.panel_token):
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
async def panel(request: Request, token: str | None = Query(default=None)):
    from .panel import render

    respuesta = HTMLResponse(render(await almacen.pendientes()))
    if token:
        # Llegó por la URL: se guarda en cookie y no se vuelve a pedir. `samesite
        # strict` es lo que evita que otra página dispare los POST de enviar o
        # descartar en nombre de Sebastián.
        #
        # `secure` sigue al esquema en vez de ir fijo en `True`: en producción
        # Caddy sirve todo por HTTPS y la cookie va marcada, pero clavarlo hace
        # que en HTTP el navegador guarde una cookie que después no manda —
        # sesión que no arranca y nada que lo explique.
        respuesta.set_cookie(
            COOKIE_PANEL, token, httponly=True, samesite="strict",
            secure=request.url.scheme == "https", max_age=30 * 24 * 60 * 60)
    return respuesta
