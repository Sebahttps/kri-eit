"""Verificación de webhooks. Solo stdlib: corre sin instalar dependencias."""
import hashlib
import hmac
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.seguridad import firma_valida, respuesta_verificacion  # noqa: E402

SECRETO = "app-secret-de-prueba"
CUERPO = b'{"object":"instagram","entry":[]}'


def _firmar(cuerpo: bytes, secreto: str = SECRETO) -> str:
    return "sha256=" + hmac.new(secreto.encode(), cuerpo, hashlib.sha256).hexdigest()


class TestFirma(unittest.TestCase):

    def test_firma_correcta(self):
        self.assertTrue(firma_valida(CUERPO, _firmar(CUERPO), SECRETO))

    def test_cuerpo_alterado(self):
        firma = _firmar(CUERPO)
        self.assertFalse(firma_valida(CUERPO + b" ", firma, SECRETO))

    def test_secreto_distinto(self):
        self.assertFalse(firma_valida(CUERPO, _firmar(CUERPO, "otro"), SECRETO))

    def test_sin_cabecera(self):
        self.assertFalse(firma_valida(CUERPO, None, SECRETO))

    def test_prefijo_invalido(self):
        digest = hmac.new(SECRETO.encode(), CUERPO, hashlib.sha256).hexdigest()
        self.assertFalse(firma_valida(CUERPO, f"sha1={digest}", SECRETO))
        self.assertFalse(firma_valida(CUERPO, digest, SECRETO))

    def test_sin_app_secret_configurado(self):
        """Sin secreto no se acepta nada: fallar cerrado, no abierto."""
        self.assertFalse(firma_valida(CUERPO, _firmar(CUERPO), ""))

    def test_hex_en_mayusculas(self):
        self.assertTrue(firma_valida(CUERPO, _firmar(CUERPO).upper().replace("SHA256", "sha256"),
                                     SECRETO))


class TestHandshake(unittest.TestCase):

    def test_verificacion_correcta(self):
        self.assertEqual(respuesta_verificacion("subscribe", "tok", "1234", "tok"), "1234")

    def test_token_incorrecto(self):
        self.assertIsNone(respuesta_verificacion("subscribe", "malo", "1234", "tok"))

    def test_modo_incorrecto(self):
        self.assertIsNone(respuesta_verificacion("unsubscribe", "tok", "1234", "tok"))

    def test_verify_token_vacio(self):
        self.assertIsNone(respuesta_verificacion("subscribe", "", "1234", ""))


if __name__ == "__main__":
    unittest.main()
