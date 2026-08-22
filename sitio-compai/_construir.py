"""Construye index.html del sitio de CompAI.

Una sola página, un solo archivo, cero dependencias externas: ni webfonts, ni
CDN, ni imágenes sueltas, ni JavaScript. Los dos logotipos van incrustados como
SVG en curvas — el nocturno para pantalla, el diurno para imprimir.

Por qué así y no un sitio: lo único que esta página tiene que lograr es que el
comprador público que lea `compai.cl` al pie de una cotización y escriba la
dirección encuentre lo que esperaba encontrar. Si carga en un segundo desde la
red de un municipio, ya cumplió.

Dirección de arte — "ficha técnica iluminada":
La página se comporta como un documento de ingeniería (retícula, secciones
numeradas, columna de rótulos, datos en monoespaciada) y toda su profundidad
sale de UNA sola fuente de luz: la brasa del logotipo, escalada a la página.
No hay efecto que no tenga una razón física. Sobrio con oficio, no efectista:
el comprador público castiga el humo tanto como la falta de trabajo.

Uso:  python sitio-compai/_construir.py
"""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
MARCA = AQUI.parent / "marca"

RAZON = "COMPAI GLOBAL SOLUTIONS SpA"
RUT = "78.491.451-8"
CORREO = "stapiamena@compai.cl"
# El teléfono SÍ va, decidido el 21-ago-2026. La regla anterior de no
# versionarlo "porque el repo es público" no protegía nada: index.html se
# publica en la web abierta y es igual de público. Y el número ya va impreso en
# la cotización, en la firma de correo y en la ficha de Mercado Público.
TELEFONO = "+56 9 6246 9977"

# Quién responde. Un correo sin persona detrás obliga al comprador a preguntar
# a quién le está escribiendo, y eso es una barrera de conversión.
CONTACTO_NOMBRE = "Sebastián Tapia Mena"
CONTACTO_CARGO = "Gerente General y representante legal"

# Domicilio comercial. Va a nivel de ciudad y región, sin calle: el domicilio
# tributario es particular y publicar la dirección exacta no aporta al
# comprador lo suficiente como para justificarlo.
DOMICILIO = "Santiago, Región Metropolitana"

# Ficha del proveedor en Mercado Público. Con URL, el sello de habilidad deja
# de ser la empresa afirmándolo de sí misma y pasa a ser verificable de un
# clic, que es lo primero que pidió el comprador simulado.
FICHA_PROVEEDOR = "https://proveedor.mercadopublico.cl/ficha/78.491.451-8"

# Hasta cuándo está acreditada, tal como lo declara la ficha. La habilidad es
# un estado que caduca: afirmarla sin fecha deja expuesta a la empresa el día
# que deje de estarlo, justo ante quien rinde cuentas a Contraloría.
ACREDITADO_HASTA = "19 de agosto de 2027"

# Giros vigentes ante el SII, tal como salen en el certificado. El comprador
# público coteja giro contra el rubro de la licitación: es el primer dato que
# copia al expediente.
GIROS = [
    ("465100", "Venta al por mayor de computadores, equipo periférico y programas informáticos"),
    ("469000", "Venta al por mayor no especializada"),
    ("620200", "Consultoría de informática y gestión de instalaciones informáticas"),
    ("620900", "Otras actividades de TI y de servicios informáticos"),
    ("631100", "Procesamiento de datos, hospedaje y actividades conexas"),
]

# Paleta nocturna. El logotipo nació para fondo oscuro y este es el único
# soporte donde puede vivir así: los documentos que se imprimen usan la diurna,
# y esta página también, gracias al bloque @media print.
FONDO = "#080A09"
SUPERFICIE = "#0D100E"
SUPERFICIE_ALTA = "#121714"
CREMA = "#F5F0E4"
AMBAR = "#E0954F"
VERDE = "#4CC48B"
# Texto secundario. #A6AFA8 da 8,81:1 sobre el fondo (antes #8A938D, 6,28:1):
# el cuerpo del texto es la mayor parte de la página y merece el margen.
TEXTO2 = "#A6AFA8"
TENUE = "#8A938D"          # 6,28:1 — solo rótulos cortos en monoespaciada
BORDE = "#1E2320"          # hairline base
BORDE_VIVO = "#2A312C"     # hairline de estado activo

# Paleta diurna, exclusiva de @media print.
TINTA = "#1A1D1B"
AMBAR_DIA = "#A85F1B"
VERDE_DIA = "#1F7A52"


def _logo(nombre: str, clase: str) -> str:
    """Incrusta un logotipo en curvas, sin width/height y con clase propia."""
    s = (MARCA / "svg" / nombre).read_text(encoding="utf-8")
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    return s.replace("<svg ", f'<svg class="{clase}" ', 1)


def ticks(clase: str = "ticks", ancho: int = 34) -> str:
    """Doble tick suelto, recortado a su propia caja y con stroke heredado.

    El viewBox del kit (216 -18 118 99) deja los ticks ocupando 31 de 118
    unidades: a 34 px de ancho el signo mediría 9 px y se fundiría en un trazo.
    Recortado a 258 24 35 17 el signo ocupa el ancho completo y respeta el
    mínimo de 24 px que fija el manual de marca.
    """
    return (
        f'<svg class="{clase}" viewBox="258 24 35 17" width="{ancho}" '
        'aria-hidden="true" focusable="false">'
        '<g transform="translate(259 20) scale(1.5)" fill="none" '
        'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
        'stroke-linejoin="round">'
        '<path d="M1 8.5 L5 12.5 L12 4"/><path d="M10 8.5 L14 12.5 L21 4"/>'
        "</g></svg>"
    )


def tarjeta(titulo: str, texto: str) -> str:
    return f"""<article class="tarjeta">
        <h3>{titulo}</h3>
        <p>{texto}</p>
      </article>"""


def fila(k: str, v: str) -> str:
    return f'<div class="fila"><dt>{k}</dt><dd>{v}</dd></div>'


def rotulo(num: str, texto: str) -> str:
    return f"""<div class="rotulo">
    <p class="indice">{num}</p>
    <h2>{texto}</h2>
  </div>"""


contacto_pie = f'<a href="mailto:{CORREO}">{CORREO}</a>'
if TELEFONO:
    _tel = TELEFONO.replace(" ", "")
    contacto_pie += f' · <a href="tel:{_tel}">{TELEFONO}</a>'

# Los giros se arman fuera del f-string para no pelear con las llaves.
_giros_html = "".join(
    f'<li><span class="mono">{c}</span> {g}</li>' for c, g in GIROS
)

# Sello de habilidad: enlace verificable si hay ficha, texto si no.
_vigencia = f' · acreditada hasta el {ACREDITADO_HASTA}' if ACREDITADO_HASTA else ''
_sello_habil = f'<span class="habil">{ticks("ticks", 26)}Inscrita y hábil</span>{_vigencia}'
if FICHA_PROVEEDOR:
    _sello_habil = (
        f'<a class="habil verificar" href="{FICHA_PROVEEDOR}" rel="noopener">'
        f'{ticks("ticks", 26)}Inscrita y hábil</a>{_vigencia}'
        f'<span class="verificar-nota">Ver la ficha en Mercado Público</span>'
    )

# Fila de domicilio, solo si está autorizado.
_fila_domicilio = fila("Domicilio", DOMICILIO) if DOMICILIO else ""

# Teléfono en la sección de contacto, no solo en el pie: la pregunta del
# comprador es "si el despacho no llega el viernes, ¿a quién llamo?", y el pie
# está demasiado abajo para contestarla.
_telefono_grande = ""
if TELEFONO:
    _telefono_grande = (
        f'<a class="correo-grande telefono" href="tel:{TELEFONO.replace(" ", "")}">'
        f'{TELEFONO}</a>'
    )

# Persona de contacto sobre el correo.
_persona = ""
if CONTACTO_NOMBRE:
    _persona = (
        f'<p class="contacto-persona"><strong>{CONTACTO_NOMBRE}</strong>'
        f'<span>{CONTACTO_CARGO}</span></p>'
    )

# JSON-LD: que el dominio se lea como entidad y no como enlace pelado cuando
# circula pegado en un correo entre compradores. Se arma con concatenación
# para no doblar llaves dentro del f-string.
_jsonld = (
    '{"@context":"https://schema.org","@type":"Organization",'
    '"name":"CompAI","legalName":"' + RAZON + '",'
    '"taxID":"' + RUT + '",'
    '"url":"https://compai.cl/",'
    '"email":"' + CORREO + '",'
    '"areaServed":"CL",'
    '"address":{"@type":"PostalAddress","addressLocality":"Santiago",'
    '"addressRegion":"Región Metropolitana","addressCountry":"CL"}'
    + (',"telephone":"' + TELEFONO + '"' if TELEFONO else '')
    + '}'
)

DESCRIPCION = (
    f"{RAZON} provee hardware, insumos y servicios de tecnología a organismos "
    f"del Estado a través de Mercado Público. RUT {RUT}, inscrita y hábil en el "
    f"Registro de Proveedores."
)

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CompAI · Equipamiento tecnológico y servicios informáticos para el sector público</title>
<meta name="description" content="{DESCRIPCION}">
<link rel="canonical" href="https://compai.cl/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CompAI">
<meta property="og:title" content="CompAI · Equipamiento tecnológico y servicios informáticos para el sector público">
<meta property="og:description" content="{DESCRIPCION}">
<meta property="og:url" content="https://compai.cl/">
<meta property="og:locale" content="es_CL">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{_jsonld}</script>
<meta name="theme-color" content="{FONDO}">
<meta name="color-scheme" content="dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%23080A09'/><path d='M14 34l7 7 13-15M30 34l7 7 13-15' fill='none' stroke='%234CC48B' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/></svg>">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}

  :root {{
    --fondo: {FONDO};
    --superficie: {SUPERFICIE};
    --superficie-alta: {SUPERFICIE_ALTA};
    --crema: {CREMA};
    --ambar: {AMBAR};
    --verde: {VERDE};
    --texto2: {TEXTO2};
    --tenue: {TENUE};
    --borde: {BORDE};
    --borde-vivo: {BORDE_VIVO};
    /* Retícula técnica: paso menor 34 px, paso mayor 170 px (5×). */
    --paso: 34px;
    --paso-mayor: 170px;
    --canal: 52px;        /* aire entre columna de rótulos y cuerpo */
    --col-rotulo: 168px;
  }}

  html {{
    background: var(--fondo);
    -webkit-text-size-adjust: 100%;
    scrollbar-color: var(--borde-vivo) var(--fondo);
    scrollbar-width: thin;
  }}

  body {{
    margin: 0;
    background: transparent;
    color: var(--crema);
    position: relative;
    isolation: isolate;
    overflow-x: hidden;
    /* Pila del sistema: la página no descarga ni una fuente. Abre igual de
       rápido en la red de un municipio que en fibra. */
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                 Helvetica, Arial, sans-serif;
    font-size: 17px;
    line-height: 1.66;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }}

  /* ── Sustrato: retícula de plano + una sola fuente de luz ───────────────
     La retícula da textura sin ruido y cuesta cero bytes de red. El halo es
     la brasa del logotipo escalada a la página: la luz entra por arriba a la
     izquierda, que es donde está el logotipo, y todos los reflejos internos
     de las tarjetas apuntan en esa misma dirección. */
  body::before {{
    content: "";
    position: absolute;
    inset: 0;
    z-index: -2;
    pointer-events: none;
    background-image:
      repeating-linear-gradient(90deg, rgba(245,240,228,.085) 0 1px, transparent 1px var(--paso-mayor)),
      repeating-linear-gradient(180deg, rgba(245,240,228,.085) 0 1px, transparent 1px var(--paso-mayor)),
      repeating-linear-gradient(90deg, rgba(245,240,228,.042) 0 1px, transparent 1px var(--paso)),
      repeating-linear-gradient(180deg, rgba(245,240,228,.042) 0 1px, transparent 1px var(--paso));
    -webkit-mask-image: linear-gradient(180deg, #000 0, rgba(0,0,0,.55) 620px, rgba(0,0,0,.28) 1400px, rgba(0,0,0,.28) 100%);
    mask-image: linear-gradient(180deg, #000 0, rgba(0,0,0,.55) 620px, rgba(0,0,0,.28) 1400px, rgba(0,0,0,.28) 100%);
  }}

  body::after {{
    content: "";
    position: absolute;
    /* Ancho atado al del body: una capa decorativa nunca puede generar
       barra horizontal en un teléfono. */
    top: -300px; left: 0; right: 0;
    height: 1200px;
    z-index: -1;
    pointer-events: none;
    /* Solo luz ambiente, neutra y centrada: el único foco de color es la
       brasa del logotipo, que sí queda en registro a cualquier ancho. Un
       resplandor ámbar suelto se despega del lockup en pantallas anchas. */
    background:
      radial-gradient(64% 44% at 50% 30%, rgba(206,214,208,.05), rgba(206,214,208,0) 74%);
  }}

  /* Cinta superior: el filo de color que separa "página publicada" de
     "documento suelto". 2 px, se apaga hacia la derecha, no parpadea. */
  .cinta {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    z-index: 10;
    background: linear-gradient(90deg,
      var(--ambar) 0%, var(--verde) 38%, rgba(76,196,139,.28) 68%, rgba(76,196,139,0) 96%);
  }}

  .marco {{ width: min(100% - 44px, 1040px); margin-inline: auto; }}

  a {{ color: var(--verde); text-underline-offset: 3px; text-decoration-thickness: 1px; }}
  a:hover {{ color: var(--crema); }}
  :focus-visible {{ outline: 2px solid var(--ambar); outline-offset: 3px; border-radius: 2px; }}
  ::selection {{ background: var(--ambar); color: var(--fondo); }}

  .mono {{
    font-family: 'Courier New', Courier, monospace;
    font-variant-numeric: tabular-nums;
  }}

  /* ── Encabezado ─────────────────────────────────────────────────────────
     No es el logotipo suelto: es una barra con el dato que este comprador
     viene a buscar (habilidad en el Registro) resuelto en el primer segundo. */
  .encabezado {{
    display: flex; align-items: center; justify-content: space-between;
    gap: 24px; flex-wrap: wrap;
    padding: 30px 0 24px;
    border-bottom: 1px solid var(--borde);
  }}
  /* El logotipo trae el filtro `brasa` en el SVG. Aquí se le extiende ese
     mismo gesto a la página: una brasa mayor, en registro exacto detrás del
     lockup, que es la única fuente de luz de todo el documento. */
  .marca {{ position: relative; line-height: 0; }}
  .marca::before {{
    content: "";
    position: absolute; z-index: -1; pointer-events: none;
    left: 4%; top: 6%; width: 96%; height: 88%;
    background:
      radial-gradient(closest-side, rgba(224,149,79,.30), rgba(224,149,79,0) 100%),
      radial-gradient(closest-side at 76% 50%, rgba(76,196,139,.20), rgba(76,196,139,0) 100%);
    filter: blur(26px);
    transform: scale(1.9);
  }}
  .logo {{ width: 212px; height: auto; display: block; overflow: visible; }}
  .logo-dia {{ display: none; }}

  .sello {{
    display: flex; align-items: center; gap: 13px;
    padding: 9px 15px 9px 13px;
    border: 1px solid var(--borde-vivo);
    border-radius: 999px;
    background: rgba(76,196,139,.05);
  }}
  .sello .ticks {{ color: var(--verde); height: auto; flex: none; display: block; }}
  .sello-txt {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px; line-height: 1.45; letter-spacing: .1em;
    text-transform: uppercase; color: var(--tenue); margin: 0;
  }}
  .sello-txt b {{ display: block; color: var(--verde); font-weight: 700; letter-spacing: .06em; }}

  /* ── Portada ────────────────────────────────────────────────────────────*/
  .hero {{ padding: 76px 0 84px; }}
  .kicker {{
    display: inline-flex; align-items: center; gap: 12px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 12px; letter-spacing: .17em; text-transform: uppercase;
    color: var(--verde); margin: 0 0 26px;
  }}
  .kicker::before {{
    content: ""; width: 28px; height: 1px; background: var(--verde); opacity: .8;
  }}
  h1 {{
    font-size: clamp(31px, 5.6vw, 54px);
    line-height: 1.06; margin: 0; max-width: 21ch;
    letter-spacing: -.026em; font-weight: 700;
  }}
  .bajada {{
    margin: 26px 0 0; max-width: 60ch; color: var(--texto2);
    font-size: clamp(17px, 2vw, 19.5px);
  }}
  .bajada strong {{ color: var(--crema); font-weight: 600; }}

  .pildora {{
    display: inline-flex; align-items: center; gap: 11px;
    margin-top: 38px; padding: 13px 22px;
    border: 1px solid var(--borde-vivo); border-radius: 999px;
    font-family: 'Courier New', Courier, monospace; font-size: 15.5px;
    color: var(--verde); text-decoration: none;
    background: var(--superficie);
    transition: border-color .16s ease, background-color .16s ease, color .16s ease;
  }}
  .pildora .ticks {{ height: auto; flex: none; display: block; }}
  .pildora:hover {{ border-color: var(--verde); background: var(--superficie-alta); color: var(--crema); }}

  /* ── Secciones: rótulo a la izquierda, cuerpo a la derecha ──────────────
     La regla vertical continua entre ambas columnas es lo que convierte una
     lista de bloques en un documento con estructura. */
  .seccion {{
    position: relative;
    display: grid;
    grid-template-columns: var(--col-rotulo) minmax(0, 1fr);
    gap: 0 var(--canal);
    padding: 66px 0;
    border-top: 1px solid var(--borde);
  }}
  .rotulo {{ padding-top: 2px; }}
  .indice {{
    margin: 0; font-family: 'Courier New', Courier, monospace;
    font-size: 12px; font-weight: 700; letter-spacing: .16em; color: var(--ambar);
  }}
  h2 {{
    margin: 8px 0 0; font-family: 'Courier New', Courier, monospace;
    font-size: 13px; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: var(--crema);
  }}
  /* La espina: en vez de un borde por bloque, una línea que no se interrumpe
     entre secciones. Es lo que convierte cuatro bloques en un documento. */
  .seccion::before {{
    content: "";
    position: absolute; top: 0; bottom: 0;
    left: calc(var(--col-rotulo) + var(--canal));
    width: 1px; background: var(--borde);
  }}
  /* Marca de cota: une el rótulo con la espina, como una acotación de plano. */
  .rotulo::after {{
    content: "";
    display: block; height: 1px; margin-top: 14px;
    background: linear-gradient(90deg, var(--borde-vivo), var(--borde));
    width: calc(100% + var(--canal));
  }}
  .cuerpo {{ padding-left: var(--canal); }}

  /* ── Tarjetas: un solo instrumento de tres cuerpos, no tres fichas ──────
     El gap de 1 px sobre fondo de borde las une en una sola pieza; el
     reflejo superior interno viene del mismo lado que el halo de la portada. */
  .grilla {{
    display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1px; background: var(--borde);
    border: 1px solid var(--borde); border-radius: 14px; overflow: hidden;
  }}
  .tarjeta {{
    background:
      linear-gradient(180deg, rgba(245,240,228,.038), rgba(245,240,228,0) 110px),
      var(--superficie);
    padding: 26px 24px 30px;
    transition: background-color .16s ease;
  }}
  .tarjeta:hover {{ background-color: var(--superficie-alta); }}
  .tarjeta::before {{
    content: ""; display: block; width: 22px; height: 2px;
    background: var(--ambar); border-radius: 2px; margin-bottom: 18px;
  }}
  .tarjeta h3 {{ font-size: 18.5px; margin: 0 0 9px; letter-spacing: -.012em; font-weight: 600; }}
  .tarjeta p {{ margin: 0; color: var(--texto2); font-size: 15.5px; line-height: 1.6; }}

  /* ── Texto corrido ─────────────────────────────────────────────────────*/
  .parrafos p {{ max-width: 62ch; margin: 0 0 18px; color: var(--texto2); font-size: 17.5px; }}
  .parrafos p:last-child {{ margin-bottom: 0; }}
  .parrafos strong {{ color: var(--crema); font-weight: 600; }}

  /* ── Ficha de empresa: se lee como un extracto de registro ─────────────*/
  .ficha {{
    margin: 0; border: 1px solid var(--borde); border-radius: 14px;
    overflow: hidden; background: var(--superficie);
  }}
  .fila {{
    display: grid; grid-template-columns: 232px minmax(0, 1fr);
    gap: 6px 22px; align-items: baseline;
    padding: 16px 22px; border-top: 1px solid var(--borde);
  }}
  .fila:first-child {{ border-top: 0; }}
  dt {{
    font-family: 'Courier New', Courier, monospace; font-size: 11.5px;
    letter-spacing: .11em; text-transform: uppercase; color: var(--tenue);
  }}
  dd {{ margin: 0; font-size: 17px; color: var(--crema); }}
  .habil {{ display: inline-flex; align-items: center; gap: 10px; color: var(--verde); font-weight: 600; }}
  .habil .ticks {{ height: auto; flex: none; }}

  /* La única pieza con énfasis tipográfico real de la página: es la frase
     que sostiene la credibilidad de una empresa sin historial. */
  .declaracion {{
    margin: 26px 0 0; padding: 4px 0 4px 22px;
    border-left: 2px solid var(--ambar);
    max-width: 62ch; color: var(--texto2); font-size: 17.5px;
  }}
  .declaracion strong {{ color: var(--crema); font-weight: 600; }}

  /* ── Contacto y pie ────────────────────────────────────────────────────*/
  .correo-grande {{
    display: inline-block; margin: 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: clamp(19px, 3.2vw, 26px); letter-spacing: -.01em;
    color: var(--verde); text-decoration: none;
    border-bottom: 1px solid rgba(76,196,139,.4); padding-bottom: 3px;
    transition: color .16s ease, border-color .16s ease;
  }}
  .correo-grande:hover {{ color: var(--crema); border-color: var(--crema); }}
  .contacto-nota {{ margin: 16px 0 0; color: var(--tenue); font-size: 15px; max-width: 52ch; }}
  .vias {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 26px; }}
  .correo-grande.telefono {{ color: var(--crema); border-color: rgba(245,240,228,.35); }}
  .correo-grande.telefono:hover {{ color: var(--verde); border-color: var(--verde); }}
  .contacto-persona {{ margin: 0 0 14px; line-height: 1.45; }}
  .contacto-persona strong {{ display: block; color: var(--crema); font-size: 18.5px; font-weight: 600; }}
  .contacto-persona span {{
    display: block; margin-top: 2px; color: var(--texto2); font-size: 15px;
  }}

  /* Giros: lista de datos duros dentro de la ficha, no prosa. */
  .giros {{ margin: 0; padding: 0; list-style: none; }}
  .giros li {{
    display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 12px;
    align-items: baseline; padding: 3px 0; font-size: 15.5px; color: var(--texto2);
  }}
  .giros li + li {{ border-top: 1px solid var(--borde); margin-top: 3px; padding-top: 6px; }}
  .giros .mono {{ color: var(--crema); }}
  a.verificar {{ text-decoration: none; border-bottom: 1px solid rgba(76,196,139,.4); }}
  a.verificar:hover {{ color: var(--crema); border-color: var(--crema); }}
  .verificar-nota {{
    display: block; margin-top: 6px;
    font-family: 'Courier New', Courier, monospace; font-size: 12px;
    letter-spacing: .06em; text-transform: uppercase; color: var(--tenue);
  }}
  @media print {{ .verificar-nota {{ color: #46504A; }} }}

  footer {{
    border-top: 1px solid var(--borde);
    padding: 30px 0 70px;
    display: flex; align-items: center; gap: 14px 20px; flex-wrap: wrap;
    color: var(--tenue); font-size: 13px;
  }}
  footer .ticks {{ color: var(--borde-vivo); height: auto; flex: none; }}
  footer p {{ margin: 0; }}
  .pie-contacto {{ margin-left: auto; }}
  footer .legal {{
    font-family: 'Courier New', Courier, monospace; font-size: 12.5px;
    letter-spacing: .04em;
  }}

  /* ── Móvil ─────────────────────────────────────────────────────────────*/
  @media (max-width: 880px) {{
    body {{ font-size: 16.5px; }}
    .marco {{ width: min(100% - 32px, 1040px); }}
    .encabezado {{ padding: 22px 0 18px; gap: 16px; }}
    .logo {{ width: 156px; }}
    .sello {{ padding: 8px 13px 8px 11px; }}
    .hero {{ padding: 46px 0 52px; }}
    h1 {{ max-width: none; }}
    .seccion {{ grid-template-columns: 1fr; padding: 44px 0; }}
    .rotulo {{
      display: flex; align-items: baseline; gap: 12px; margin-bottom: 22px;
      padding-bottom: 12px; border-bottom: 1px solid var(--borde);
    }}
    h2 {{ margin: 0; }}
    .seccion::before {{ display: none; }}
    .rotulo::after {{ display: none; }}
    .cuerpo {{ padding-left: 0; }}
    .tarjeta {{ padding: 22px 20px 24px; }}
    .fila {{ grid-template-columns: 1fr; padding: 14px 18px; }}
    .parrafos p, .declaracion {{ font-size: 16.5px; }}
    footer {{ padding: 24px 0 54px; }}
  }}

  @media (max-width: 620px) {{
    .grilla {{ grid-template-columns: 1fr; }}
    footer p:last-child {{ margin-left: 0; }}
  }}

  /* Nada se mueve solo en esta página; solo hay transiciones de estado.
     Aun así, se respetan las preferencias del sistema. */
  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
      transition-duration: .01ms !important;
      animation-duration: .01ms !important;
      animation-iteration-count: 1 !important;
      scroll-behavior: auto !important;
    }}
  }}

  /* ── Impresión ─────────────────────────────────────────────────────────
     El comprador público imprime, y a menudo en blanco y negro. La página se
     da vuelta a la paleta diurna del manual de marca y cambia el logotipo
     nocturno por el de tinta plana: sale una ficha, no una captura oscura. */
  @media print {{
    html, body {{ background: #fff; color: {TINTA}; font-size: 11.5pt; }}
    body::before, body::after, .cinta, .marca::before {{ display: none !important; }}
    .seccion::before {{ background: #CFCABC; }}
    .logo-noche {{ display: none; }}
    .logo-dia {{ display: block; width: 52mm; }}
    a {{ color: {VERDE_DIA}; }}
    .kicker, .habil, .sello-txt b, .correo-grande {{ color: {VERDE_DIA} !important; }}
    .indice, .tarjeta::before, .declaracion {{ color: {AMBAR_DIA}; }}
    .tarjeta::before {{ background: {AMBAR_DIA}; }}
    .declaracion {{ border-left-color: {AMBAR_DIA}; }}
    h1, h2, h3, dd, strong {{ color: {TINTA} !important; }}
    .bajada, .parrafos p, .tarjeta p, .declaracion, .contacto-nota,
    dt, footer, .sello-txt {{ color: #46504A !important; }}
    .encabezado, .seccion, .ficha, .fila, .cuerpo, footer,
    .grilla, .sello, .pildora {{ border-color: #CFCABC !important; }}
    .tarjeta, .ficha, .sello, .pildora {{ background: #fff !important; }}
    .seccion, .tarjeta, .ficha {{ break-inside: avoid; }}
    .correo-grande {{ border-bottom-color: {VERDE_DIA}; }}
    footer .ticks {{ color: #CFCABC; }}
    .sello .ticks, .habil .ticks {{ color: {VERDE_DIA}; }}
    @page {{ margin: 14mm; }}
  }}
</style>
</head>
<body>

<div class="cinta" aria-hidden="true"></div>

<header class="marco encabezado">
  <div class="marca">
    {_logo("compai-logotipo-curvas.svg", "logo logo-noche")}
    {_logo("compai-logotipo-dia-curvas.svg", "logo logo-dia")}
  </div>
  <div class="sello">
    {ticks("ticks", 30)}
    <p class="sello-txt">Registro de Proveedores<b>Inscrita y hábil</b></p>
  </div>
</header>

<div class="marco hero">
  <p class="kicker">Proveedor del Estado · Mercado Público</p>
  <h1>Equipamiento tecnológico y servicios informáticos para el sector público</h1>
  <p class="bajada">CompAI provee hardware, insumos y servicios de tecnología a
    organismos del Estado, con <strong>entrega directa del distribuidor al
    comprador</strong> y sin intermediación de bodega.</p>
  <a class="pildora" href="mailto:{CORREO}" aria-label="Escribir a {CORREO}">
    {ticks("ticks", 26)}<span>{CORREO}</span>
  </a>
</div>

<section class="marco seccion">
  {rotulo("01", "Qué hacemos")}
  <div class="cuerpo">
    <div class="grilla">
      {tarjeta("Equipamiento",
               "Computadores, servidores, periféricos, equipos de red y "
               "telecomunicaciones, e insumos tecnológicos.")}
      {tarjeta("Servicios informáticos",
               "Consultoría en TI, integración de sistemas, procesamiento de "
               "datos y soporte técnico.")}
      {tarjeta("Datos e inteligencia artificial",
               "Depuración de bases de datos, tableros de gestión y "
               "automatización de procesos administrativos.")}
    </div>
  </div>
</section>

<section class="marco seccion">
  {rotulo("02", "Cómo trabajamos")}
  <div class="cuerpo parrafos">
    <p>La mercadería va <strong>del distribuidor al organismo</strong>, sin pasar
      por una bodega intermedia. Eso acorta el plazo de entrega y elimina un costo
      que otros proveedores trasladan al precio.</p>
    <p>Antes de ofertar se confirma stock y plazo con el distribuidor por escrito.
      <strong>No se compromete una fecha que no esté respaldada</strong>: una
      entrega tardía le cuesta al comprador más que la diferencia de precio que lo
      hizo elegirnos.</p>
  </div>
</section>

<section class="marco seccion">
  {rotulo("03", "La empresa")}
  <div class="cuerpo">
    <dl class="ficha">
      {fila("Razón social", RAZON)}
      {fila("RUT", f'<span class="mono">{RUT}</span>')}
      {fila("Constitución", '<span class="mono">15 de agosto de 2026</span>')}
      {fila("Registro de Proveedores", _sello_habil)}
      {fila("Giros ante el SII", f'<ul class="giros">{_giros_html}</ul>')}
      {fila("Facturación", "Electrónica, con inicio de actividades vigente")}
      {_fila_domicilio}
    </dl>
    <p class="declaracion">CompAI es una empresa nueva y opera con inicio de
      actividades vigente, facturación electrónica y habilidad al día.
      <strong>No declaramos experiencia que no tengamos</strong>: lo que
      ofrecemos es precio competitivo, plazo cumplido y un expediente sin
      observaciones.</p>
  </div>
</section>

<section class="marco seccion">
  {rotulo("04", "Contacto")}
  <div class="cuerpo">
    {_persona}
    <div class="vias">
      <a class="correo-grande" href="mailto:{CORREO}">{CORREO}</a>
      {_telefono_grande}
    </div>
    <p class="contacto-nota">Consultas de cotización, disponibilidad y plazos de
      entrega.</p>
  </div>
</section>

<footer class="marco">
  {ticks("ticks", 26)}
  <p class="legal">{RAZON} · RUT {RUT} · Santiago, Chile</p>
  <p class="pie-contacto">{contacto_pie}</p>
</footer>

</body>
</html>
"""

(AQUI / "index.html").write_text(HTML, encoding="utf-8")
destino = AQUI / "index.html"
print("Escrito:", destino, f"({destino.stat().st_size / 1024:.1f} KB)")

# La 404 de GitHub Pages muestra el octocat y descubre el andamio. Esta usa la
# misma cabecera y el mismo pie, así que un enlace mal copiado desde un PDF
# sigue aterrizando en CompAI.
# Corta justo después del encabezado: el aviso tiene que ser lo primero que se
# vea, no ir debajo del hero de portada.
_corte_cabeza = HTML.index("</header>") + len("</header>")
_corte_pie = HTML.index('<footer class="marco">')
HTML_404 = (
    HTML[:_corte_cabeza]
    + '''

<div class="marco hero">
  <p class="kicker">Error 404</p>
  <h1>Esa dirección no existe</h1>
  <p class="bajada">La página de <strong>''' + RAZON + '''</strong> es una sola.
    Si llegaste desde una cotización, el enlace correcto es compai.cl sin nada
    después.</p>
  <p style="margin:26px 0 0">
    <a class="correo-grande" href="/">compai.cl</a>
  </p>
</div>

'''
    + HTML[_corte_pie:]
).replace(
    "<title>CompAI · Equipamiento tecnológico y servicios informáticos para el sector público</title>",
    "<title>Página no encontrada · CompAI</title>",
    1,
).replace(
    '<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1
)
(AQUI / "404.html").write_text(HTML_404, encoding="utf-8")
print("Escrito:", AQUI / "404.html", f"({(AQUI / '404.html').stat().st_size / 1024:.1f} KB)")
if not TELEFONO:
    print("TELEFONO vacío: el pie sale solo con el correo.")
