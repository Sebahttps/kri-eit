"""Normalización de los payloads de webhook de Instagram.

Meta manda cuatro formas distintas de "alguien te habló" (mensaje, reacción,
respuesta a historia, comentario). Acá se aplanan todas a `EventoEntrante`
para que el resto del servicio no tenga que saber de qué forma vino.
"""
from typing import Any, Literal

from pydantic import BaseModel

TipoEvento = Literal["mensaje", "reaccion", "respuesta_historia", "comentario"]


class EventoEntrante(BaseModel):
    id: str                       # id único del evento (para deduplicar reintentos)
    tipo: TipoEvento
    autor_id: str                 # IGSID de quien escribe (o id del comentarista)
    autor_usuario: str | None = None
    texto: str = ""
    timestamp_ms: int = 0
    media_id: str | None = None   # solo comentarios
    comentario_id: str | None = None
    contexto: str = ""            # de qué historia/publicación cuelga


class Borrador(BaseModel):
    id: int
    evento_id: str
    autor_id: str
    autor_usuario: str | None
    tipo: TipoEvento
    texto_entrante: str
    respuesta: str
    categoria: str
    confianza: float
    razon: str
    prioridad: str
    estado: str                   # "pendiente" | "enviado" | "descartado"
    creado_en: str
    comentario_id: str | None = None


def _evento_de_messaging(item: dict[str, Any]) -> EventoEntrante | None:
    """Traduce una entrada de `entry[].messaging[]` (DMs, reacciones, historias)."""
    autor = (item.get("sender") or {}).get("id", "")
    ts = int(item.get("timestamp") or 0)

    reaccion = item.get("reaction")
    if reaccion:
        if reaccion.get("action") == "unreact":
            return None
        emoji = reaccion.get("emoji") or reaccion.get("reaction") or "❤️"
        return EventoEntrante(
            id=f"react:{reaccion.get('mid', '')}:{ts}",
            tipo="reaccion", autor_id=autor, texto=emoji, timestamp_ms=ts,
            contexto="reaccionó a un mensaje tuyo",
        )

    mensaje = item.get("message")
    if not mensaje:
        return None

    # Ecos: mensajes que enviaste tú. Si se procesan, el agente se responde solo.
    if mensaje.get("is_echo"):
        return None

    mid = mensaje.get("mid", "")
    texto = mensaje.get("text") or ""
    respuesta_a = mensaje.get("reply_to") or {}

    if "story" in respuesta_a:
        return EventoEntrante(
            id=f"msg:{mid}", tipo="respuesta_historia", autor_id=autor,
            texto=texto, timestamp_ms=ts, contexto="respondió a tu historia",
        )

    if not texto:
        # Adjunto sin texto (sticker, gif, foto suelta): se trata como reacción.
        adjuntos = mensaje.get("attachments") or []
        tipo_adjunto = adjuntos[0].get("type", "adjunto") if adjuntos else "adjunto"
        return EventoEntrante(
            id=f"msg:{mid}", tipo="reaccion", autor_id=autor, texto="",
            timestamp_ms=ts, contexto=f"te mandó un {tipo_adjunto} sin texto",
        )

    return EventoEntrante(
        id=f"msg:{mid}", tipo="mensaje", autor_id=autor, texto=texto, timestamp_ms=ts,
    )


def _evento_de_comentario(valor: dict[str, Any], ts: int) -> EventoEntrante | None:
    autor = valor.get("from") or {}
    texto = valor.get("text") or ""
    comentario_id = valor.get("id") or ""
    if not comentario_id or not texto:
        return None
    return EventoEntrante(
        id=f"cmt:{comentario_id}", tipo="comentario",
        autor_id=autor.get("id", ""), autor_usuario=autor.get("username"),
        texto=texto, timestamp_ms=ts,
        media_id=(valor.get("media") or {}).get("id"),
        comentario_id=comentario_id,
        contexto="comentó en una publicación tuya",
    )


def normalizar(payload: dict[str, Any], ig_user_id: str = "") -> list[EventoEntrante]:
    """Aplana un payload completo de webhook a una lista de eventos entrantes."""
    eventos: list[EventoEntrante] = []

    for entry in payload.get("entry") or []:
        ts_entry = int(entry.get("time") or 0) * 1000

        for item in entry.get("messaging") or []:
            evento = _evento_de_messaging(item)
            if evento:
                eventos.append(evento)

        for change in entry.get("changes") or []:
            if change.get("field") != "comments":
                continue
            evento = _evento_de_comentario(change.get("value") or {}, ts_entry)
            if evento:
                eventos.append(evento)

    # Tus propios mensajes y comentarios nunca se procesan.
    return [e for e in eventos if e.autor_id and e.autor_id != ig_user_id]
