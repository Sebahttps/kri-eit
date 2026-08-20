"""Genera la carátula de oferta técnica y la ficha de empresa.

Por qué un generador y no dos HTML escritos a mano: los dos documentos
incrustan el logotipo en base64 —para que el archivo viaje solo, sin carpeta de
imágenes al lado— y eso son 39 KB de texto ilegible pegados en medio del
código. Con el generador, lo que se edita son los datos y la maqueta; el logo se
pega solo al construir.

Uso:  python marca/comercial/_generar-documentos.py
Salida: caratula-oferta-tecnica.html y ficha-empresa.html, en esta carpeta.

**La hoja está dibujada, no supuesta.** Los dos documentos pintan una carta de
216 × 279 mm con sus márgenes reales, así que lo que se ve en el navegador es lo
que sale impreso. La primera versión de esto maquetaba solo con `@page`, que no
existe en pantalla: el contenido quedaba pegado al borde y el pie se montaba
encima del texto sin que se notara hasta imprimir.

Para el PDF: Ctrl+P → Guardar como PDF, **márgenes «Ninguno»**. El margen lo
pone la hoja; si además lo pone el navegador, se suman y el documento encoge.
"""
import base64
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
MARCA = AQUI.parent

# --- Datos de la empresa -----------------------------------------------------
# El teléfono NO va acá: este archivo se versiona en un repo público. Quien
# genere el documento completa la variable antes de correrlo y la deja en blanco
# al guardar. Si queda vacía, el bloque de contacto simplemente la omite.
RAZON = "COMPAI GLOBAL SOLUTIONS SpA"
FANTASIA = "CompAI SpA"
RUT = "78.491.451-8"
CORREO = "stapiamena@compai.cl"
SITIO = "compai.cl"
TELEFONO = ""   # ej. "+56 9 0000 0000"

# --- Marca -------------------------------------------------------------------
TINTA = "#1A1D1B"
AMBAR = "#A85F1B"     # acento y reglas. 4,86:1 sobre blanco: no sirve para texto corrido
VERDE = "#1F7A52"
GRIS = "#4A524E"
GRIS_TENUE = "#6B7370"
LINEA = "#E2E5E3"

# Arial y Courier New, no webfonts: estos documentos los abre e imprime un
# tercero en su equipo, y una fuente que no carga cambia la maqueta completa.
SANS = "Arial, Helvetica, sans-serif"
MONO = "'Courier New', Courier, monospace"


def logo(nombre: str) -> str:
    datos = base64.b64encode((MARCA / "png" / f"{nombre}.png").read_bytes()).decode()
    return f"data:image/png;base64,{datos}"


def contacto(sep=" · ") -> str:
    partes = [CORREO] + ([TELEFONO] if TELEFONO else []) + [SITIO]
    return sep.join(partes)


BASE = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>__TITULO__</title>
<style>
  @page {{ size: letter; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: {SANS}; color: {TINTA}; font-size: 10.5pt;
          line-height: 1.55; margin: 0; background: #EDECE8; }}

  /* La hoja carta, con sus márgenes adentro. Es lo que hace que la pantalla
     y el papel coincidan. */
  .hoja {{ width: 216mm; min-height: 279mm; padding: 18mm 20mm;
           margin: 0 auto; background: #fff;
           display: flex; flex-direction: column; }}
  /* El pie empujado abajo por el flujo, no por `position:fixed`. Fijo se monta
     encima del contenido en cuanto el texto crece, y no se nota hasta imprimir. */
  .cuerpo {{ flex: 1; }}
  .pie {{ margin-top: auto; padding-top: 10px; }}

  .kicker {{ font-family: {MONO}; font-size: 7.5pt; letter-spacing: .14em;
             text-transform: uppercase; color: {GRIS_TENUE}; }}
  .regla {{ border: 0; border-top: 1pt solid {AMBAR}; margin: 0; }}
  h1, h2 {{ margin: 0; font-weight: bold; letter-spacing: -.01em; }}
  table {{ width: 100%; border-collapse: collapse; }}
  .campo {{ border-bottom: .75pt solid {LINEA}; padding: 7px 0 5px;
            font-size: 11.5pt; min-height: 26px; }}

  @media screen {{
    body {{ padding: 26px 0; }}
    .hoja {{ box-shadow: 0 2px 22px rgba(26,38,32,.16); }}
  }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .hoja {{ box-shadow: none; min-height: 279mm; }}
    .nota-pantalla {{ display: none !important; }}
  }}
  .nota-pantalla {{ width: 216mm; margin: 0 auto 14px; background: #FBF7EC;
                    border-left: 2.5pt solid {AMBAR}; padding: 11px 16px;
                    font-size: 9pt; color: {GRIS}; }}
</style></head>
<body>
__CUERPO__
</body></html>
"""


def encabezado(derecha: str) -> str:
    """Logotipo diurno a la izquierda, datos a la derecha, regla ámbar debajo."""
    return f"""<table><tr>
  <td style="vertical-align:top;"><img src="{logo('compai-logotipo-dia')}"
      alt="CompAI" style="width:48mm; height:auto; display:block;"></td>
  <td style="vertical-align:top; text-align:right; padding-top:3px;">{derecha}</td>
</tr></table>
<hr class="regla" style="margin-top:14px;">"""


def pie(izq: str, der: str) -> str:
    return f"""<div class="pie">
  <hr class="regla" style="border-top-width:.75pt;">
  <table style="margin-top:7px;"><tr>
    <td style="font-family:{MONO}; font-size:8pt; color:{GRIS};">{izq}</td>
    <td style="text-align:right; font-family:{MONO}; font-size:7.5pt;
               color:{GRIS_TENUE};">{der}</td>
  </tr></table>
</div>"""


def nota(texto: str) -> str:
    return f'<div class="nota-pantalla">{texto}</div>'


def escribir(archivo: str, titulo: str, cuerpo: str) -> None:
    html = BASE.replace("__TITULO__", titulo).replace("__CUERPO__", cuerpo)
    (AQUI / archivo).write_text(html, encoding="utf-8")


# =============================================================================
# 1. Carátula de oferta técnica
# =============================================================================
# Es lo primero que abre el evaluador y el único documento que puede dejar una
# oferta inadmisible antes de que alguien lea la propuesta. Por eso los campos
# van en el orden en que él los busca —ID del proceso primero, oferente
# después— y no en el orden en que a uno le gustaría presentarse.

def campo(etiqueta: str) -> str:
    return f"""<div class="kicker">{etiqueta}</div>
      <div class="campo">&nbsp;</div>"""


escribir("caratula-oferta-tecnica.html", "Carátula de oferta técnica — CompAI", f"""
{nota("<strong>Esta nota no se imprime.</strong> Completar los campos en pantalla "
      "o a mano. Al guardar como PDF, elegir márgenes «Ninguno»: el margen lo pone "
      "la hoja, y si además lo pone el navegador el documento sale encogido.")}

<div class="hoja">
<div class="cuerpo">

{encabezado(f'''<div style="font-size:8.5pt; color:{GRIS}; line-height:1.65;">
    {RAZON}<br>RUT {RUT}<br>{contacto("<br>")}</div>''')}

<div style="margin-top:52mm;">
  <div class="kicker" style="color:{VERDE};">Oferta técnica</div>
  <h1 style="font-size:26pt; line-height:1.15; margin-top:10px;">
    Propuesta técnica y económica</h1>
  <p style="margin:14px 0 0; color:{GRIS}; font-size:11pt;">
    Presentada a través del Sistema de Información de Compras y Contratación
    Pública, mercadopublico.cl</p>
</div>

<div style="margin-top:24mm;">
  <table>
    <tr>
      <td style="width:50%; padding:0 16px 20px 0; vertical-align:top;">
        {campo("ID de la adquisición")}</td>
      <td style="width:50%; padding:0 0 20px; vertical-align:top;">
        {campo("Fecha de presentación")}</td>
    </tr>
  </table>
  <div style="padding-bottom:20px;">{campo("Organismo comprador")}</div>
  <div style="padding-bottom:20px;">{campo("Nombre del proceso")}</div>
</div>

<div style="margin-top:10mm; border-top:.75pt solid {LINEA}; padding-top:15px;">
  <div class="kicker" style="color:{VERDE};">Oferente</div>
  <table style="margin-top:11px;"><tr>
    <td style="width:60%; padding-right:14px; vertical-align:top;">
      <div style="font-size:13pt; font-weight:bold;">{RAZON}</div>
      <div style="color:{GRIS}; font-size:9.5pt; margin-top:4px;">
        Nombre de fantasía: {FANTASIA}</div>
    </td>
    <td style="vertical-align:top; font-family:{MONO}; font-size:9.5pt;">
      RUT {RUT}<br><span style="color:{GRIS};">{CORREO}</span>
    </td>
  </tr></table>
</div>

</div>
{pie(f"{RAZON} · RUT {RUT}", SITIO)}
</div>
""")


# =============================================================================
# 2. Ficha de empresa
# =============================================================================
# Una hoja. Sostiene el criterio de "experiencia del oferente" y sirve de
# adjunto en cualquier correo comercial.
#
# Está escrita sin inventar trayectoria, y no por pudor: en compras públicas los
# antecedentes van bajo declaración jurada, y un dato inflado deja de ser
# marketing para ser el art. 210 del Código Penal. Lo que sí se puede afirmar
# —constitución, giros, habilidad vigente, modelo de entrega— es verificable, y
# ante un comprador que le teme al riesgo eso pesa más que un adjetivo.

def bloque(kicker: str, titulo: str, cuerpo: str) -> str:
    return f"""<div style="margin-top:22px;">
  <div class="kicker" style="color:{VERDE};">{kicker}</div>
  <h2 style="font-size:12.5pt; margin-top:6px;">{titulo}</h2>
  <div style="margin-top:6px; color:{GRIS};">{cuerpo}</div>
</div>"""


def fila(k: str, v: str) -> str:
    return f"""<tr>
  <td style="padding:5px 16px 5px 0; color:{GRIS_TENUE}; font-family:{MONO};
             font-size:8pt; white-space:nowrap; vertical-align:top;
             width:34%;">{k}</td>
  <td style="padding:5px 0; vertical-align:top;">{v}</td></tr>"""


escribir("ficha-empresa.html", "Ficha de empresa — CompAI", f"""
{nota("<strong>Esta nota no se imprime.</strong> Guardar como PDF con márgenes "
      "«Ninguno». Este es el adjunto de cualquier correo comercial y el respaldo "
      "del criterio de experiencia del oferente.")}

<div class="hoja">
<div class="cuerpo">

{encabezado('<div class="kicker">Ficha de empresa</div>')}

<div style="margin-top:20px;">
  <h1 style="font-size:18pt; line-height:1.25;">
    Equipamiento tecnológico y servicios informáticos<br>
    para el sector público</h1>
  <p style="margin:11px 0 0; color:{GRIS}; font-size:10.5pt; line-height:1.6;">
    CompAI provee hardware, insumos y servicios de tecnología a organismos del
    Estado a través de Mercado Público, con entrega directa del distribuidor al
    comprador y sin intermediación de bodega.</p>
</div>

<div style="margin-top:20px; border:.75pt solid {LINEA}; padding:14px 16px;">
  <table>
    {fila("Razón social", f"<strong>{RAZON}</strong>")}
    {fila("Nombre de fantasía", FANTASIA)}
    {fila("RUT", f'<span style="font-family:{MONO};">{RUT}</span>')}
    {fila("Constitución", "15 de agosto de 2026 · Registro de Empresas y Sociedades")}
    {fila("Tipo", "Sociedad por Acciones · segmento micro empresa")}
    {fila("Registro de Proveedores",
          f'<span style="color:{VERDE}; font-weight:bold;">Inscrita y hábil</span>')}
  </table>
</div>

{bloque("Qué hacemos", "Tres líneas de servicio", f"""
<table style="margin-top:2px;"><tr>
  <td style="width:33.33%; padding-right:16px; vertical-align:top;">
    <strong style="color:{TINTA};">Equipamiento</strong><br>
    Computadores, servidores, periféricos, equipos de red y telecomunicaciones,
    e insumos tecnológicos.</td>
  <td style="width:33.33%; padding-right:16px; vertical-align:top;">
    <strong style="color:{TINTA};">Servicios informáticos</strong><br>
    Consultoría en TI, integración de sistemas, procesamiento de datos y soporte
    técnico.</td>
  <td style="vertical-align:top;">
    <strong style="color:{TINTA};">Datos e inteligencia artificial</strong><br>
    Depuración de bases de datos, tableros de gestión y automatización de
    procesos administrativos.</td>
</tr></table>""")}

{bloque("Cómo trabajamos",
        "Sin bodega, sin intermediarios y con la fecha comprometida por escrito", f"""
<p style="margin:0 0 7px;">La mercadería va <strong style="color:{TINTA};">del
distribuidor al organismo</strong>, sin pasar por una bodega intermedia. Eso
acorta el plazo de entrega y elimina un costo que otros proveedores trasladan al
precio.</p>
<p style="margin:0;">Antes de ofertar se confirma stock y plazo con el
distribuidor por escrito. <strong style="color:{TINTA};">No se compromete una
fecha que no esté respaldada</strong>: una entrega tardía le cuesta al comprador
más que la diferencia de precio que lo hizo elegirnos.</p>""")}

{bloque("Antecedentes", "Empresa nueva, con la documentación al día", f"""
<p style="margin:0;">CompAI se constituyó en agosto de 2026 y opera con inicio de
actividades vigente, facturación electrónica y habilidad al día en el Registro de
Proveedores. <strong style="color:{TINTA};">No declaramos experiencia que no
tengamos.</strong> Lo que ofrecemos es lo verificable: precio competitivo, plazo
cumplido y un expediente sin observaciones.</p>""")}

</div>
{pie(contacto(), f"RUT {RUT} · Santiago, Chile")}
</div>
""")


print("Generados en", AQUI)
for f in ("caratula-oferta-tecnica.html", "ficha-empresa.html"):
    print(" ", f)
if not TELEFONO:
    print("\nTELEFONO está vacío: el bloque de contacto sale sin él.")
    print("Completarlo antes de generar, y dejarlo en blanco al versionar.")
