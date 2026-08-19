"""Flujo completo: webhook firmado → clasificación → envío o borrador.

Sustituye el redactor (Anthropic) y el cliente de Instagram por dobles, así que
no toca la red. Requiere las dependencias instaladas.
"""
import hashlib
import hmac
import json
import time
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


def _ahora_ms() -> int:
    """El fixture tenía la fecha clavada en abril de 2024.

    Daba igual mientras `dentro_de_ventana` era siempre `True`; ahora que la
    ventana de 24 h se mide contra el reloj, un mensaje de hace dos años entra
    fuera de plazo y todo termina en borrador sin que el test lo diga.
    """
    return int(time.time() * 1000)


def _dm(mid: str, texto: str, autor: str = "999", ts: int | None = None) -> bytes:
    marca = _ahora_ms() if ts is None else ts
    return json.dumps({"object": "instagram", "entry": [{
        "id": MI_ID, "time": marca // 1000,
        "messaging": [{"sender": {"id": autor}, "recipient": {"id": MI_ID},
                       "timestamp": marca,
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

    # --- barreras, ejercidas por el flujo real y no con un Contexto a mano ----
    #
    # Los tests de `test_politica.py` prueban que la función pura decide bien
    # cuando le entregan el estado correcto. Estos prueban lo otro, que es donde
    # estaba el bug: que el estado que el almacén construye de verdad llegue a
    # tomar esos valores alguna vez.

    def test_desconocido_que_escribe_dos_veces_sigue_sin_respuesta_sola(self):
        """Dos mensajes seguidos no son una conversación.

        Contando mensajes, el segundo DM de un desconocido ya dejaba de ser
        "primer contacto" y se respondía solo. Lo que abre la puerta es que él
        haya contestado, no que el otro insista.
        """
        self._entrante("m-desc1", "hola", "888")
        self._entrante("m-desc2", "quedó increíble la foto", "888")

        self.assertEqual([d for d in self.instagram.dms if d[0] == "888"], [])

    def test_tope_diario_cruzado_de_verdad(self):
        """El cuarto cumplido del día ya no sale solo.

        El tope es 3 y se cuenta contra la base, no contra un número puesto a
        mano. Hace falta un turno suyo previo para salir de "primer contacto".
        """
        self._entrante("m-tope0", "hola", "901")
        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        bid = next(b for b in pendientes if b["autor_id"] == "901")["id"]
        self.cliente.post(f"/borradores/{bid}/enviar",
                          params={"token": "panel-secreto"}, json={"texto": "hola!"})

        for i in range(3):
            self._entrante(f"m-tope{i + 1}", "quedó increíble", "901")
        automaticos = [d for d in self.instagram.dms if d == ("901", "gracias!")]
        self.assertEqual(len(automaticos), 3)

        self._entrante("m-tope4", "en serio, increíble", "901")
        self.assertEqual(
            len([d for d in self.instagram.dms if d == ("901", "gracias!")]), 3)
        pendientes = self.cliente.get("/borradores",
                                      params={"token": "panel-secreto"}).json()
        self.assertTrue(any(b["autor_id"] == "901" and "tope diario" in b["razon"]
                            for b in pendientes))

    def test_mensaje_viejo_no_se_responde_solo(self):
        """Un webhook rezagado cae fuera de la ventana de 24 h de Meta.

        Antes esto no podía fallar: la ventana se medía contra el turno que el
        propio procesador acababa de escribir, así que siempre daba "recién
        llegado".
        """
        viejo = _ahora_ms() - 48 * 60 * 60 * 1000
        cuerpo = _dm("m-viejo", "quedó increíble la foto", "555", ts=viejo)
        self.cliente.post("/webhook", content=cuerpo,
                          headers={"x-hub-signature-256": _firmar(cuerpo)})

        self.assertEqual([d for d in self.instagram.dms if d[0] == "555"], [])

    # --- el token del panel --------------------------------------------------

    def test_token_por_url_queda_en_cookie_y_no_se_repite(self):
        """Entrar por la URL deja la sesión en una cookie `HttpOnly`.

        La credencial abre sus DMs: en el query string quedaría escrita en el
        log de accesos de Caddy y en el historial del navegador.
        """
        cliente = TestClient(main.app)
        r = cliente.get("/panel", params={"token": "panel-secreto"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(cliente.cookies.get("ig_panel"), "panel-secreto")
        self.assertIn("httponly", r.headers["set-cookie"].lower())
        self.assertNotIn("panel-secreto", r.text)

        # Y de ahí en adelante entra sin token en la URL.
        self.assertEqual(cliente.get("/borradores").status_code, 200)

    def test_cookie_falsa_no_abre_el_panel(self):
        cliente = TestClient(main.app)
        cliente.cookies.set("ig_panel", "panel-secretp")   # una letra distinta
        self.assertEqual(cliente.get("/borradores").status_code, 401)


if __name__ == "__main__":
    unittest.main()
