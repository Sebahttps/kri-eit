"""Qué se responde solo y qué espera tu visto bueno.

Este módulo es la parte del sistema que decide, y por eso es deliberadamente
aburrido: sin red, sin base de datos, sin modelo. Solo stdlib, para poder
testearlo entero y cambiar la política sin tocar nada más.
"""
from dataclasses import dataclass, field

# Categorías que el clasificador puede asignar. El orden no importa; los
# nombres sí: `config.auto_categorias` los usa tal cual.
CATEGORIAS = (
    "reaccion_trivial",   # "🔥", "jajaja", reacción a historia, sticker
    "cumplido",           # elogio corto sin pregunta
    "saludo_conocido",    # "tanto tiempo", "cómo estái"
    "pregunta_personal",  # pregunta real sobre ti, tus planes, tu vida
    "peticion_favor",     # te piden algo: contacto, dato, ayuda, juntarse
    "comercial",          # colaboración, marca, propuesta de trabajo
    "sensible",           # conflicto, coqueteo, mala noticia, tema delicado
    "spam",               # bots, estafas, promos masivas
)

# Nunca se responden solas, aunque estén en la lista de auto-categorías.
# Es una barrera, no una preferencia: acá es donde un bot queda mal de verdad.
CATEGORIAS_BLOQUEADAS = frozenset({"sensible", "comercial", "spam"})


@dataclass(frozen=True)
class Clasificacion:
    """Lo que devuelve el redactor para un mensaje entrante."""
    categoria: str
    confianza: float
    respuesta: str
    requiere_contexto_personal: bool = False   # necesita algo que solo tú sabes
    motivo: str = ""


@dataclass(frozen=True)
class Contexto:
    """Estado del hilo en el momento de decidir."""
    autorespuestas_hoy: int = 0        # cuántas van con este contacto hoy
    ultimo_turno_fue_mio: bool = False  # ya respondí y no me han contestado
    dentro_de_ventana: bool = True      # ventana de 24 h de mensajería de Meta
    es_primer_contacto: bool = False    # nunca hemos hablado por DM


@dataclass(frozen=True)
class Decision:
    accion: str                        # "enviar" | "borrador" | "ignorar"
    razon: str
    respuesta: str = ""
    prioridad: str = "normal"          # "normal" | "alta"
    avisos: tuple[str, ...] = field(default_factory=tuple)

    @property
    def envia(self) -> bool:
        return self.accion == "enviar"


def decidir(clas: Clasificacion, ctx: Contexto, *,
            auto_categorias: set[str],
            confianza_minima: float,
            max_por_contacto_dia: int,
            max_caracteres: int,
            solo_borradores: bool) -> Decision:
    """Decide qué hacer con un mensaje ya clasificado.

    Regla de fondo: ante la duda, borrador. Que respondas tarde se perdona;
    que te pillen contestando con un bot a un amigo, no.
    """
    # Spam: ni respuesta ni ruido en tu bandeja de revisión.
    if clas.categoria == "spam" and clas.confianza >= confianza_minima:
        return Decision("ignorar", "spam detectado")

    # Lo delicado sube de prioridad y va derecho a ti.
    if clas.categoria == "sensible":
        return Decision("borrador", "tema sensible: lo contestas tú",
                        clas.respuesta, prioridad="alta",
                        avisos=("Revisar antes de responder.",))

    if solo_borradores:
        return Decision("borrador", "modo solo-borradores activo", clas.respuesta)

    if not ctx.dentro_de_ventana:
        return Decision("borrador", "fuera de la ventana de 24 h de Meta", clas.respuesta,
                        avisos=("Meta bloquea el envío automático pasadas 24 h "
                                "desde el último mensaje de la persona.",))

    if clas.categoria in CATEGORIAS_BLOQUEADAS or clas.categoria not in auto_categorias:
        return Decision("borrador", f"categoría '{clas.categoria}' no es automática",
                        clas.respuesta)

    if clas.confianza < confianza_minima:
        return Decision("borrador", f"confianza {clas.confianza:.2f} bajo el mínimo",
                        clas.respuesta)

    if clas.requiere_contexto_personal:
        return Decision("borrador", "necesita información que el agente no tiene",
                        clas.respuesta)

    # Nunca abrir conversación con un desconocido de forma automática.
    if ctx.es_primer_contacto:
        return Decision("borrador", "primer contacto por DM", clas.respuesta)

    # No insistir: si ya respondí y no me han contestado, callarse.
    if ctx.ultimo_turno_fue_mio:
        return Decision("ignorar", "ya respondí y no hay turno nuevo de la persona")

    if ctx.autorespuestas_hoy >= max_por_contacto_dia:
        return Decision("borrador", "tope diario de respuestas automáticas con este contacto",
                        clas.respuesta)

    # Una respuesta trivial que salió larga dejó de ser trivial.
    if len(clas.respuesta) > max_caracteres:
        return Decision("borrador", f"respuesta de {len(clas.respuesta)} caracteres: demasiado larga "
                                    "para enviarla sin leerla", clas.respuesta)

    if not clas.respuesta.strip():
        return Decision("ignorar", "el agente decidió no responder")

    return Decision("enviar", f"{clas.categoria} con confianza {clas.confianza:.2f}",
                    clas.respuesta)
