"""Cliente de la Graph API de Instagram: enviar DMs y responder comentarios."""
import logging

import httpx

from .config import settings

log = logging.getLogger(__name__)


class ErrorInstagram(RuntimeError):
    def __init__(self, mensaje: str, codigo: int | None = None, detalle: dict | None = None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.detalle = detalle or {}


class ClienteInstagram:
    def __init__(self, token: str | None = None, base: str | None = None):
        self.token = token or settings.access_token
        self.base = base or settings.graph_url

    async def _post(self, ruta: str, payload: dict) -> dict:
        url = f"{self.base}/{ruta.lstrip('/')}"
        async with httpx.AsyncClient(timeout=20) as cliente:
            resp = await cliente.post(url, json=payload,
                                      params={"access_token": self.token})
        if resp.status_code >= 400:
            detalle = _cuerpo(resp)
            error = (detalle.get("error") or {})
            log.warning("Graph API %s → %s: %s", ruta, resp.status_code, error.get("message"))
            raise ErrorInstagram(error.get("message", resp.text),
                                 error.get("code"), detalle)
        return _cuerpo(resp)

    async def enviar_dm(self, destinatario_id: str, texto: str) -> dict:
        """Manda un DM. Sujeto a la ventana de 24 h de mensajería de Meta."""
        return await self._post("me/messages", {
            "recipient": {"id": destinatario_id},
            "message": {"text": texto},
        })

    async def reaccionar(self, destinatario_id: str, mensaje_id: str,
                         emoji: str = "❤️") -> dict:
        """Reacciona a un mensaje en vez de escribir. Lo más barato socialmente."""
        return await self._post("me/messages", {
            "recipient": {"id": destinatario_id},
            "sender_action": "react",
            "payload": {"message_id": mensaje_id, "reaction": "love", "emoji": emoji},
        })

    async def responder_comentario(self, comentario_id: str, texto: str) -> dict:
        """Responde en público, colgando del comentario original."""
        return await self._post(f"{comentario_id}/replies", {"message": texto})

    async def responder_en_privado(self, comentario_id: str, texto: str) -> dict:
        """Private reply: convierte un comentario público en un DM.

        Meta solo permite uno por comentario y dentro de los 7 días.
        """
        return await self._post("me/messages", {
            "recipient": {"comment_id": comentario_id},
            "message": {"text": texto},
        })

    async def perfil(self, usuario_id: str) -> dict:
        """Nombre y @ de un contacto, para dar contexto al redactor."""
        url = f"{self.base}/{usuario_id}"
        async with httpx.AsyncClient(timeout=15) as cliente:
            resp = await cliente.get(url, params={"fields": "name,username",
                                                  "access_token": self.token})
        return _cuerpo(resp) if resp.status_code < 400 else {}


def _cuerpo(resp: httpx.Response) -> dict:
    try:
        return resp.json()
    except ValueError:
        return {"raw": resp.text}
