"""Flujo completo: webhook firmado → clasificación → envío o borrador.

Sustituye el redactor (Anthropic) y el cliente de Instagram por dobles, así que
no toca la red. Requiere las dependencias instaladas.
"""
import hashlib
import hmac
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRETO = "secreto-de-prueba"
MI_ID = "17841400000000000"
_DB = os.path.join(tempfile.mkdtemp(), "test.db")

os.environ.update({
    "IG_APP_SECRET": SECRETO,
    "IG_VERIFY_TOKEN": "verificame",
    "IG_IG_USER_ID": MI_ID,
    "IG_PANEL_TOKEN": "panel-secreto",
    "IG_DB_PATH": _DB,
    "IG_ANTHROPIC_API_KEY": "sk-falsa",
})

try:
    from fastapi.testclient import TestClient
    from app import main, redactor
    from app.politica import Clasificacion
    LISTO = True
except ImportError:                                  # pragma: no cover
    LISTO = False


class InstagramFalso:
    """Registra lo que se habría mandado, en vez de mandarlo."""

    def __init__(self):
        self.dms: list[tuple[str, str]] = []
        self.comentarios: list[tuple[str, str]] = []

    async def enviar_dm(self, destinatario_id, texto):
        self.dms.append((destinatario_id, texto))
        return {"message_id": "enviado"}

    async def responder_comentario(self, comentario_id, texto):
        self.comentarios.append((comentario_id, texto))
        return {"id": "reply"}


def _firmar(cuerpo: bytes) -> str:
    return "sha256=" + hmac.new(SECRETO.encode(), cuerpo, hashlib.sha256).hexdigest()


def _dm(mid: str, texto: str, autor: str = "999") -> bytes:
    return json.dumps({"object": "instagram", "entry": [{
        "id": MI_ID, "time": 1712000000,
        "messaging": [{"sender": {"id": autor}, "recipient": {"id": MI_ID},
                       "timestamp": 1712000000000,
                       "message": {"mid": mid, "text": texto}}],
    }]}).encode()


@unittest.skipUnless(LISTO, "requiere pip install -r requirements.txt")
class TestFlujo(unittest.TestCase):

    def setUp(self):
        self.instagram = InstagramFalso()
        main.procesador.instagram = self.instagram
        self.respuesta_falsa = Clasificacion("cumplido", 0.95, "gracias!")

        async def redactor_falso(evento, historial=None):
            return self.respuesta_falsa

        self._original = redactor.clasificar_y_redactar
        redactor.clasificar_y_redactar = redactor_falso
        # `procesador` importó la función por nombre, hay que parchear ahí también.
        from app import procesador
        procesador.clasificar_y_redactar = redactor_falso

        # Como contexto: así corre el `lifespan` y se crean las tablas.
        self._ctx = TestClient(main.app)
        self.cliente = self._ctx.__enter__()

    def tearDown(self):
        self._ctx.__exit__(None, None, None)
        redactor.clasificar_y_redactar = self._original
        from app import procesador
        procesador.clasificar_y_redactar = self._original

    # --- webhook ---------------------------------------------------------

    def test_verificacion_del_webhook(self):
        r = self.cliente.get("/webhook", params={
            "hub.mode": "subscribe", "hub.verify_token": "verificame",
            "hub.challenge": "abc123"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "abc123")

    def test_verificacion_con_token_malo(self):
        r = self.cliente.get("/webhook", params={
            "hub.mode": "subscribe", "hub.verify_token": "malo",
            "hub.challenge": "abc123"})
        self.assertEqual(r.status_code, 403)

    def test_payload_sin_firma_se_rechaza(self):
        r = self.cliente.post("/webhook", content=_dm("m0", "hola"))
        self.assertEqual(r.status_code, 403)
        self.assertEqual(self.instagram.dms, [])

    def _entrante(self, mid: str, texto: str, autor: str):
        cuerpo = _dm(mid, texto, autor)
        return self.cliente.post("/webhook", content=cuerpo,
                                 headers={"x-hub-signature-256": _firmar(cuerpo)})

    def test_primer_dm_de_un_contacto_nunca_sale_solo(self):
        """Arranque en frío: sin historial, ni un cumplido se responde solo."""
        r = self._entrante("m1a", "quedó increíble la foto", "111")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.instagram.dms, [])

        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        self.assertTrue(any(b["autor_id"] == "111" for b in pendientes))

    def test_cumplido_se_responde_solo_cuando_ya_hay_historial(self):
        self._entrante("m1b", "hola!", "222")
        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        bid = next(b for b in pendientes if b["autor_id"] == "222")["id"]
        self.cliente.post(f"/borradores/{bid}/enviar",
                          params={"token": "panel-secreto"}, json={"texto": "hola!"})

        self._entrante("m1c", "quedó increíble la foto", "222")
        self.assertEqual(self.instagram.dms[-1], ("222", "gracias!"))

    def test_evento_duplicado_no_se_procesa_dos_veces(self):
        """Meta reintenta los webhooks; el mismo mid no genera dos respuestas."""
        self.respuesta_falsa = Clasificacion("comercial", 0.9, "lo veo")
        cuerpo = _dm("m-dup", "propuesta", autor="666")
        cabeceras = {"x-hub-signature-256": _firmar(cuerpo)}
        self.cliente.post("/webhook", content=cuerpo, headers=cabeceras)
        self.cliente.post("/webhook", content=cuerpo, headers=cabeceras)

        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        self.assertEqual(len([b for b in pendientes if b["autor_id"] == "666"]), 1)

    def test_pregunta_personal_queda_en_borrador(self):
        self.respuesta_falsa = Clasificacion(
            "pregunta_personal", 0.93, "sí, ahí estaré", True)
        cuerpo = _dm("m2", "vai el sábado?", autor="777")
        self.cliente.post("/webhook", content=cuerpo,
                          headers={"x-hub-signature-256": _firmar(cuerpo)})

        self.assertEqual(self.instagram.dms, [])
        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        self.assertTrue(any(b["texto_entrante"] == "vai el sábado?" for b in pendientes))

    # --- panel -----------------------------------------------------------

    def test_panel_exige_token(self):
        self.assertEqual(self.cliente.get("/borradores").status_code, 401)
        self.assertEqual(self.cliente.get("/panel", params={"token": "x"}).status_code, 401)

    def test_aprobar_borrador_con_edicion(self):
        self.respuesta_falsa = Clasificacion("comercial", 0.9, "hola, cuéntame más")
        cuerpo = _dm("m3", "te escribo de una marca", autor="555")
        self.cliente.post("/webhook", content=cuerpo,
                          headers={"x-hub-signature-256": _firmar(cuerpo)})

        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        borrador = next(b for b in pendientes if b["autor_id"] == "555")

        r = self.cliente.post(f"/borradores/{borrador['id']}/enviar",
                              params={"token": "panel-secreto"},
                              json={"texto": "gracias, lo veo y te digo"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.instagram.dms, [("555", "gracias, lo veo y te digo")])

    def test_no_se_envia_dos_veces_el_mismo_borrador(self):
        self.respuesta_falsa = Clasificacion("comercial", 0.9, "dale")
        cuerpo = _dm("m4", "propuesta", autor="444")
        self.cliente.post("/webhook", content=cuerpo,
                          headers={"x-hub-signature-256": _firmar(cuerpo)})
        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        bid = next(b for b in pendientes if b["autor_id"] == "444")["id"]

        p = {"token": "panel-secreto"}
        self.assertEqual(self.cliente.post(f"/borradores/{bid}/enviar", params=p,
                                           json={}).status_code, 200)
        self.assertEqual(self.cliente.post(f"/borradores/{bid}/enviar", params=p,
                                           json={}).status_code, 400)
        self.assertEqual(len(self.instagram.dms), 1)

    def test_panel_escapa_html_del_contacto(self):
        """El texto de un DM es contenido de terceros: no se inyecta crudo."""
        self.respuesta_falsa = Clasificacion("comercial", 0.9, "ok")
        cuerpo = _dm("m5", "<script>alert(1)</script>", autor="333")
        self.cliente.post("/webhook", content=cuerpo,
                          headers={"x-hub-signature-256": _firmar(cuerpo)})

        html = self.cliente.get("/panel", params={"token": "panel-secreto"}).text
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)


if __name__ == "__main__":
    unittest.main()
