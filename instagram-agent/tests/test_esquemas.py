"""Normalización de payloads de webhook. Requiere pydantic instalado."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.esquemas import normalizar
    HAY_PYDANTIC = True
except ImportError:                                  # pragma: no cover
    HAY_PYDANTIC = False

MI_ID = "17841400000000000"


def _payload_messaging(item: dict) -> dict:
    return {"object": "instagram", "entry": [{"id": MI_ID, "time": 1712000000,
                                              "messaging": [item]}]}


@unittest.skipUnless(HAY_PYDANTIC, "requiere pip install -r requirements.txt")
class TestNormalizar(unittest.TestCase):

    def test_dm_de_texto(self):
        eventos = normalizar(_payload_messaging({
            "sender": {"id": "999"}, "recipient": {"id": MI_ID},
            "timestamp": 1712000000000,
            "message": {"mid": "m1", "text": "cómo estái"},
        }), MI_ID)
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0].tipo, "mensaje")
        self.assertEqual(eventos[0].texto, "cómo estái")
        self.assertEqual(eventos[0].id, "msg:m1")

    def test_eco_propio_se_descarta(self):
        """Sin esto el agente se responde a sí mismo en bucle."""
        eventos = normalizar(_payload_messaging({
            "sender": {"id": MI_ID}, "recipient": {"id": "999"},
            "message": {"mid": "m2", "text": "hola", "is_echo": True},
        }), MI_ID)
        self.assertEqual(eventos, [])

    def test_reaccion(self):
        eventos = normalizar(_payload_messaging({
            "sender": {"id": "999"}, "timestamp": 1712000000000,
            "reaction": {"mid": "m3", "action": "react", "reaction": "love",
                         "emoji": "❤️"},
        }), MI_ID)
        self.assertEqual(eventos[0].tipo, "reaccion")
        self.assertEqual(eventos[0].texto, "❤️")

    def test_quitar_reaccion_no_genera_evento(self):
        eventos = normalizar(_payload_messaging({
            "sender": {"id": "999"},
            "reaction": {"mid": "m3", "action": "unreact"},
        }), MI_ID)
        self.assertEqual(eventos, [])

    def test_respuesta_a_historia(self):
        eventos = normalizar(_payload_messaging({
            "sender": {"id": "999"}, "timestamp": 1712000000000,
            "message": {"mid": "m4", "text": "🔥",
                        "reply_to": {"story": {"id": "s1", "url": "http://x"}}},
        }), MI_ID)
        self.assertEqual(eventos[0].tipo, "respuesta_historia")

    def test_adjunto_sin_texto(self):
        eventos = normalizar(_payload_messaging({
            "sender": {"id": "999"},
            "message": {"mid": "m5", "attachments": [{"type": "image"}]},
        }), MI_ID)
        self.assertEqual(eventos[0].tipo, "reaccion")
        self.assertIn("image", eventos[0].contexto)

    def test_comentario(self):
        eventos = normalizar({"object": "instagram", "entry": [{
            "id": MI_ID, "time": 1712000000,
            "changes": [{"field": "comments", "value": {
                "id": "c1", "text": "quedó buenísima",
                "from": {"id": "999", "username": "juan"},
                "media": {"id": "media1"}}}],
        }]}, MI_ID)
        self.assertEqual(eventos[0].tipo, "comentario")
        self.assertEqual(eventos[0].comentario_id, "c1")
        self.assertEqual(eventos[0].autor_usuario, "juan")

    def test_otros_campos_de_cambio_se_ignoran(self):
        eventos = normalizar({"object": "instagram", "entry": [{
            "id": MI_ID, "time": 1712000000,
            "changes": [{"field": "mentions", "value": {"comment_id": "c9"}}],
        }]}, MI_ID)
        self.assertEqual(eventos, [])

    def test_varios_eventos_en_un_payload(self):
        payload = {"object": "instagram", "entry": [{
            "id": MI_ID, "time": 1712000000,
            "messaging": [
                {"sender": {"id": "1"}, "message": {"mid": "a", "text": "hola"}},
                {"sender": {"id": "2"}, "message": {"mid": "b", "text": "buenas"}},
            ],
        }]}
        self.assertEqual(len(normalizar(payload, MI_ID)), 2)


if __name__ == "__main__":
    unittest.main()
