"""Construye index.html del sitio de CompAI.

Una sola página, un solo archivo, cero dependencias externas: ni webfonts, ni
CDN, ni imágenes sueltas. El logotipo va incrustado como SVG en curvas.

Por qué así y no un sitio: lo único que esta página tiene que lograr es que el
comprador público que lea `compai.cl` al pie de una cotización y escriba la
dirección encuentre lo que esperaba encontrar. Si carga en un segundo desde la
red de un municipio, ya cumplió.

Uso:  python sitio-compai/_construir.py
"""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
MARCA = AQUI.parent / "marca"

RAZON = "COMPAI GLOBAL SOLUTIONS SpA"
RUT = "78.491.451-8"
CORREO = "stapiamena@compai.cl"
# El teléfono no se versiona: el repo es público. Completar antes de construir.
TELEFONO = ""

# Paleta nocturna. El logotipo nació para fondo oscuro y este es el único
# soporte donde puede vivir así: los documentos que se imprimen usan la diurna.
FONDO = "#080A09"
SUPERFICIE = "#0D100E"
CREMA = "#F5F0E4"
AMBAR = "#E0954F"
VERDE = "#4CC48B"
TENUE = "#8A938D"
BORDE = "#1E2320"


def logo_svg() -> str:
    s = (MARCA / "svg" / "compai-logotipo-curvas.svg").read_text(encoding="utf-8")
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    return s.replace("<svg ", '<svg class="logo" ', 1)


def servicio(titulo: str, texto: str) -> str:
    return f"""<div class="tarjeta">
      <h3>{titulo}</h3>
      <p>{texto}</p>
    </div>"""


def dato(k: str, v: str) -> str:
    return f'<div class="dato"><dt>{k}</dt><dd>{v}</dd></div>'


contacto = f'<a href="mailto:{CORREO}">{CORREO}</a>'
if TELEFONO:
    tel = TELEFONO.replace(" ", "")
    contacto += f' · <a href="tel:{tel}">{TELEFONO}</a>'

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CompAI · Equipamiento tecnológico y servicios informáticos para el sector público</title>
<meta name="description" content="{RAZON} provee hardware, insumos y servicios de tecnología a organismos del Estado a través de Mercado Público. RUT {RUT}, inscrita y hábil en el Registro de Proveedores.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%23080A09'/><path d='M14 34l7 7 13-15M30 34l7 7 13-15' fill='none' stroke='%234CC48B' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/></svg>">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  :root {{
    --fondo: {FONDO}; --superficie: {SUPERFICIE}; --crema: {CREMA};
    --ambar: {AMBAR}; --verde: {VERDE}; --tenue: {TENUE}; --borde: {BORDE};
  }}
  html {{ -webkit-text-size-adjust: 100%; }}
  body {{
    margin: 0; background: var(--fondo); color: var(--crema);
    /* Pila del sistema: la página no descarga ni una fuente. Abre igual de
       rápido en la red de un municipio que en fibra. */
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                 Helvetica, Arial, sans-serif;
    font-size: 17px; line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }}
  .marco {{ width: min(100% - 40px, 880px); margin-inline: auto; }}
  .logo {{ width: 200px; height: auto; display: block; }}
  a {{ color: var(--verde); text-underline-offset: 3px; }}
  a:hover {{ color: var(--crema); }}

  header {{ padding: 44px 0 0; }}

  .hero {{ padding: 56px 0 64px; border-bottom: 1px solid var(--borde); }}
  .kicker {{
    font-family: 'Courier New', Courier, monospace; font-size: 12px;
    letter-spacing: .16em; text-transform: uppercase; color: var(--verde);
    margin: 0 0 18px;
  }}
  h1 {{
    font-size: clamp(30px, 5.2vw, 46px); line-height: 1.12; margin: 0;
    letter-spacing: -.02em; font-weight: 700;
  }}
  .bajada {{
    margin: 22px 0 0; max-width: 60ch; color: var(--tenue);
    font-size: clamp(17px, 2.1vw, 19px);
  }}
  .bajada strong {{ color: var(--crema); font-weight: 600; }}

  section {{ padding: 56px 0; border-bottom: 1px solid var(--borde); }}
  h2 {{ font-size: 13px; letter-spacing: .16em; text-transform: uppercase;
        color: var(--tenue); margin: 0 0 28px; font-weight: 600;
        font-family: 'Courier New', Courier, monospace; }}
  h3 {{ font-size: 19px; margin: 0 0 10px; letter-spacing: -.01em; }}

  .grilla {{ display: grid; gap: 20px; grid-template-columns: repeat(3, 1fr); }}
  .tarjeta {{
    background: var(--superficie); border: 1px solid var(--borde);
    border-radius: 12px; padding: 24px 22px;
  }}
  .tarjeta p {{ margin: 0; color: var(--tenue); font-size: 16px; }}

  .parrafos p {{ max-width: 68ch; margin: 0 0 16px; color: var(--tenue); }}
  .parrafos p:last-child {{ margin-bottom: 0; }}
  .parrafos strong {{ color: var(--crema); font-weight: 600; }}

  dl {{ margin: 0; display: grid; gap: 0;
        grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .dato {{ padding: 15px 0; border-top: 1px solid var(--borde); }}
  .dato:nth-child(-n+2) {{ border-top: 0; }}
  dt {{ font-family: 'Courier New', Courier, monospace; font-size: 12px;
        letter-spacing: .08em; text-transform: uppercase; color: var(--tenue); }}
  dd {{ margin: 5px 0 0; font-size: 17px; }}
  .habil {{ color: var(--verde); font-weight: 600; }}
  .mono {{ font-family: 'Courier New', Courier, monospace; }}

  footer {{ padding: 40px 0 64px; color: var(--tenue); font-size: 14px; }}
  footer .mono {{ font-size: 13px; }}

  @media (max-width: 720px) {{
    .grilla {{ grid-template-columns: 1fr; }}
    dl {{ grid-template-columns: 1fr; }}
    .dato:nth-child(2) {{ border-top: 1px solid var(--borde); }}
    section, .hero {{ padding: 40px 0; }}
  }}
</style>
</head>
<body>

<header class="marco">
  {logo_svg()}
</header>

<div class="marco hero">
  <p class="kicker">Proveedor del Estado · Mercado Público</p>
  <h1>Equipamiento tecnológico y servicios informáticos para el sector público</h1>
  <p class="bajada">CompAI provee hardware, insumos y servicios de tecnología a
    organismos del Estado, con <strong>entrega directa del distribuidor al
    comprador</strong> y sin intermediación de bodega.</p>
</div>

<section class="marco">
  <h2>Qué hacemos</h2>
  <div class="grilla">
    {servicio("Equipamiento",
              "Computadores, servidores, periféricos, equipos de red y "
              "telecomunicaciones, e insumos tecnológicos.")}
    {servicio("Servicios informáticos",
              "Consultoría en TI, integración de sistemas, procesamiento de "
              "datos y soporte técnico.")}
    {servicio("Datos e inteligencia artificial",
              "Depuración de bases de datos, tableros de gestión y "
              "automatización de procesos administrativos.")}
  </div>
</section>

<section class="marco parrafos">
  <h2>Cómo trabajamos</h2>
  <p>La mercadería va <strong>del distribuidor al organismo</strong>, sin pasar
    por una bodega intermedia. Eso acorta el plazo de entrega y elimina un costo
    que otros proveedores trasladan al precio.</p>
  <p>Antes de ofertar se confirma stock y plazo con el distribuidor por escrito.
    <strong>No se compromete una fecha que no esté respaldada</strong>: una
    entrega tardía le cuesta al comprador más que la diferencia de precio que lo
    hizo elegirnos.</p>
</section>

<section class="marco">
  <h2>La empresa</h2>
  <dl>
    {dato("Razón social", RAZON)}
    {dato("RUT", f'<span class="mono">{RUT}</span>')}
    {dato("Constitución", "15 de agosto de 2026")}
    {dato("Registro de Proveedores", '<span class="habil">Inscrita y hábil</span>')}
  </dl>
  <p class="bajada" style="margin-top:26px; font-size:16px;">CompAI es una
    empresa nueva y opera con inicio de actividades vigente, facturación
    electrónica y habilidad al día. <strong>No declaramos experiencia que no
    tengamos</strong>: lo que ofrecemos es precio competitivo, plazo cumplido y
    un expediente sin observaciones.</p>
</section>

<footer class="marco">
  <p style="margin:0 0 6px;">{contacto}</p>
  <p class="mono" style="margin:0;">{RAZON} · RUT {RUT} · Santiago, Chile</p>
</footer>

</body>
</html>
"""

(AQUI / "index.html").write_text(HTML, encoding="utf-8")
print("Escrito:", AQUI / "index.html")
if not TELEFONO:
    print("TELEFONO vacío: el pie sale solo con el correo.")
