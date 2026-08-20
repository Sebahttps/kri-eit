"""Verificación de webhooks de Meta. Solo stdlib: se puede testear sin instalar nada."""
import hashlib
import hmac


def firma_valida(cuerpo_crudo: bytes, cabecera: str | None, app_secret: str) -> bool:
    """Valida la cabecera `X-Hub-Signature-256` de Meta.

    Meta firma el cuerpo EXACTO de la petición con HMAC-SHA256 usando el App
    Secret. Hay que validar los bytes crudos: si el framework reserializa el
    JSON, la firma deja de coincidir.
    """
    if not app_secret or not cabecera:
        return False

    prefijo, _, recibida = cabecera.partition("=")
    if prefijo != "sha256" or not recibida:
        return False

    esperada = hmac.new(app_secret.encode(), cuerpo_crudo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperada, recibida.lower())


def respuesta_verificacion(mode: str | None, token: str | None,
                           challenge: str | None, verify_token: str) -> str | None:
    """Handshake inicial del webhook (GET). Devuelve el challenge si todo cuadra."""
    if mode == "subscribe" and token and verify_token and hmac.compare_digest(token, verify_token):
        return challenge
    return None
