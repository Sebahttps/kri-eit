"""Clasifica el mensaje entrante y redacta la respuesta, en una sola llamada.

Separarlo en dos llamadas duplicaría latencia y costo sin ganar nada: la
categoría y el texto se deciden con la misma información.
"""
import json
import logging
from functools import lru_cache
from pathlib import Path

from anthropic import AsyncAnthropic

from .config import settings
from .esquemas import EventoEntrante
from .politica import CATEGORIAS, Clasificacion

log = logging.getLogger(__name__)

ESQUEMA_SALIDA = {
    "type": "object",
    "properties": {
        "categoria": {"type": "string", "enum": list(CATEGORIAS)},
        "confianza": {"type": "number"},
        "respuesta": {
            "type": "string",
            "description": "La respuesta lista para enviar, en el tono de la persona. "
                           "Cadena vacía si lo correcto es no responder nada.",
        },
        "requiere_contexto_personal": {
            "type": "boolean",
            "description": "true si responder bien exige información que solo el dueño "
                           "de la cuenta tiene (planes, opiniones, precios, disponibilidad).",
        },
        "motivo": {
            "type": "string",
            "description": "Una frase corta explicando la clasificación, para el panel.",
        },
    },
    "required": ["categoria", "confianza", "respuesta",
                 "requiere_contexto_personal", "motivo"],
    "additionalProperties": False,
}

INSTRUCCIONES = """Eres el asistente de mensajes de una cuenta PERSONAL de Instagram \
con ~10.000 seguidores. No es una cuenta de marca ni de soporte: del otro lado hay \
amigos, conocidos y seguidores de años.

Tu trabajo tiene dos partes:

1. **Clasificar** el mensaje entrante en una de las categorías disponibles.
2. **Redactar** la respuesta como la escribiría el dueño de la cuenta, siguiendo al \
pie de la letra el archivo de tono que viene más abajo.

Sobre la confianza: es qué tan seguro estás de la categoría Y de que la respuesta se \
puede mandar sin que nadie la lea antes. Si dudas, baja la confianza — el sistema la \
usa para mandar a revisión, y una respuesta revisada tarde es mejor que una \
automática equivocada.

Marca `requiere_contexto_personal` en true ante cualquier pregunta cuya respuesta \
honesta dependa de la vida, agenda, opiniones o decisiones del dueño de la cuenta. \
Nunca inventes un dato para rellenar: si no lo sabes, no lo escribas.

Deja `respuesta` vacía cuando lo correcto sea el silencio (spam, un "jaja" que ya \
cierra la conversación, una reacción que no pide nada).

Escribe la respuesta directamente, sin comillas, sin prefijos y sin explicar nada \
dentro de ella."""


@lru_cache(maxsize=1)
def _persona() -> str:
    ruta = Path(settings.persona_path)
    return ruta.read_text(encoding="utf-8") if ruta.exists() else ""


@lru_cache(maxsize=1)
def _cliente() -> AsyncAnthropic:
    return AsyncAnthropic(api_key=settings.anthropic_api_key or None)


def _contexto_evento(evento: EventoEntrante, historial: list[dict]) -> str:
    partes = [f"Tipo de evento: {evento.tipo}"]
    if evento.contexto:
        partes.append(f"Contexto: {evento.contexto}")
    if evento.autor_usuario:
        partes.append(f"De: @{evento.autor_usuario}")

    if historial:
        lineas = [f"[{'yo' if t['rol'] == 'yo' else 'contacto'}] {t['texto']}"
                  for t in historial]
        partes.append("Conversación previa con esta persona:\n" + "\n".join(lineas))
    else:
        partes.append("No hay conversación previa registrada con esta persona.")

    partes.append(f"Mensaje entrante:\n{evento.texto or '(sin texto)'}")
    return "\n\n".join(partes)


async def clasificar_y_redactar(evento: EventoEntrante,
                                historial: list[dict] | None = None) -> Clasificacion:
    """Devuelve categoría + respuesta. Ante cualquier fallo, cae a borrador."""
    sistema = [
        {"type": "text", "text": INSTRUCCIONES},
        {"type": "text", "text": f"# Archivo de tono\n\n{_persona()}",
         "cache_control": {"type": "ephemeral"}},
    ]

    try:
        respuesta = await _cliente().messages.create(
            model=settings.model,
            max_tokens=2000,
            system=sistema,
            output_config={
                "effort": settings.effort,
                "format": {"type": "json_schema", "schema": ESQUEMA_SALIDA},
            },
            messages=[{"role": "user",
                       "content": _contexto_evento(evento, historial or [])}],
        )
    except Exception as exc:                       # red, cuota, modelo caído
        log.exception("Falló la redacción del evento %s", evento.id)
        return Clasificacion("pregunta_personal", 0.0, "", True,
                             f"error del redactor: {exc}")

    if respuesta.stop_reason == "refusal":
        return Clasificacion("sensible", 1.0, "", True,
                             "el modelo declinó redactar esta respuesta")

    texto = next((b.text for b in respuesta.content if b.type == "text"), "")
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError:
        log.error("Respuesta no parseable para %s: %r", evento.id, texto[:200])
        return Clasificacion("pregunta_personal", 0.0, "", True,
                             "salida del modelo no parseable")

    return Clasificacion(
        categoria=datos.get("categoria", "pregunta_personal"),
        confianza=float(datos.get("confianza", 0.0)),
        respuesta=(datos.get("respuesta") or "").strip(),
        requiere_contexto_personal=bool(datos.get("requiere_contexto_personal", True)),
        motivo=datos.get("motivo", ""),
    )
