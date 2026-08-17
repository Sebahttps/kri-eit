"""La política de autonomía: qué sale solo y qué espera aprobación."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.politica import Clasificacion, Contexto, decidir  # noqa: E402

AUTO = {"reaccion_trivial", "cumplido", "saludo_conocido"}

REGLAS = dict(auto_categorias=AUTO, confianza_minima=0.80,
              max_por_contacto_dia=3, max_caracteres=140, solo_borradores=False)


def _decidir(clas: Clasificacion, ctx: Contexto | None = None, **cambios):
    return decidir(clas, ctx or Contexto(), **{**REGLAS, **cambios})


class TestCaminoFeliz(unittest.TestCase):

    def test_reaccion_trivial_se_envia_sola(self):
        d = _decidir(Clasificacion("reaccion_trivial", 0.95, "jaja gracias"))
        self.assertEqual(d.accion, "enviar")
        self.assertEqual(d.respuesta, "jaja gracias")

    def test_cumplido_se_envia_solo(self):
        self.assertTrue(_decidir(Clasificacion("cumplido", 0.91, "gracias!")).envia)


class TestBarreras(unittest.TestCase):

    def test_sensible_nunca_se_envia(self):
        d = _decidir(Clasificacion("sensible", 0.99, "hablemos"))
        self.assertEqual(d.accion, "borrador")
        self.assertEqual(d.prioridad, "alta")

    def test_sensible_ignora_la_lista_de_auto_categorias(self):
        """Ni configurándolo a mano: 'sensible' está bloqueado por diseño."""
        d = _decidir(Clasificacion("sensible", 0.99, "ok"),
                     auto_categorias=AUTO | {"sensible"})
        self.assertEqual(d.accion, "borrador")

    def test_comercial_va_a_borrador(self):
        self.assertEqual(_decidir(Clasificacion("comercial", 0.97, "hola")).accion,
                         "borrador")

    def test_pregunta_personal_va_a_borrador(self):
        self.assertEqual(_decidir(Clasificacion("pregunta_personal", 0.99, "sí")).accion,
                         "borrador")

    def test_spam_se_ignora(self):
        self.assertEqual(_decidir(Clasificacion("spam", 0.96, "")).accion, "ignorar")

    def test_spam_con_poca_confianza_no_se_descarta(self):
        d = _decidir(Clasificacion("spam", 0.40, "hola"))
        self.assertEqual(d.accion, "borrador")


class TestLimites(unittest.TestCase):

    def test_confianza_baja(self):
        d = _decidir(Clasificacion("cumplido", 0.62, "gracias"))
        self.assertEqual(d.accion, "borrador")
        self.assertIn("confianza", d.razon)

    def test_necesita_contexto_personal(self):
        d = _decidir(Clasificacion("saludo_conocido", 0.99, "el sábado", True))
        self.assertEqual(d.accion, "borrador")

    def test_primer_contacto(self):
        d = _decidir(Clasificacion("cumplido", 0.99, "gracias"),
                     Contexto(es_primer_contacto=True))
        self.assertEqual(d.accion, "borrador")

    def test_no_insiste_si_ya_respondi(self):
        d = _decidir(Clasificacion("cumplido", 0.99, "gracias"),
                     Contexto(ultimo_turno_fue_mio=True))
        self.assertEqual(d.accion, "ignorar")

    def test_tope_diario_por_contacto(self):
        d = _decidir(Clasificacion("cumplido", 0.99, "gracias"),
                     Contexto(autorespuestas_hoy=3))
        self.assertEqual(d.accion, "borrador")
        self.assertIn("tope diario", d.razon)

    def test_fuera_de_ventana_de_24h(self):
        d = _decidir(Clasificacion("cumplido", 0.99, "gracias"),
                     Contexto(dentro_de_ventana=False))
        self.assertEqual(d.accion, "borrador")

    def test_respuesta_larga_no_es_trivial(self):
        d = _decidir(Clasificacion("cumplido", 0.99, "g" * 200))
        self.assertEqual(d.accion, "borrador")
        self.assertIn("larga", d.razon)

    def test_respuesta_vacia_es_silencio(self):
        self.assertEqual(_decidir(Clasificacion("reaccion_trivial", 0.99, "   ")).accion,
                         "ignorar")

    def test_modo_solo_borradores_apaga_todo(self):
        d = _decidir(Clasificacion("reaccion_trivial", 0.99, "jaja"),
                     solo_borradores=True)
        self.assertEqual(d.accion, "borrador")

    def test_solo_borradores_no_bloquea_el_descarte_de_spam(self):
        """El interruptor de pánico no debe llenarte la bandeja de spam."""
        d = _decidir(Clasificacion("spam", 0.99, ""), solo_borradores=True)
        self.assertEqual(d.accion, "ignorar")


if __name__ == "__main__":
    unittest.main()
