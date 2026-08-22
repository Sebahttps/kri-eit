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
# El teléfono ya es público por decisión del 21-ago-2026: va impreso en
# compai.cl, en la firma de correo y en la ficha de Mercado Público. La regla
# anterior de dejarlo vacío "porque el repo es público" no protegía nada.
# Los datos que SÍ siguen fuera del repo —RUN y domicilio particular— se leen
# de `_datos_privados.py`, que está en el .gitignore de esta carpeta.
RAZON = "COMPAI GLOBAL SOLUTIONS SpA"
FANTASIA = "CompAI SpA"
RUT = "78.491.451-8"
CORREO = "stapiamena@compai.cl"
SITIO = "compai.cl"
TELEFONO = "+56 9 6246 9977"

# Datos que no se versionan. Si el archivo no está, el documento se genera
# igual y deja los marcadores a la vista: una degradación honesta, se nota
# que falta algo en vez de salir un dato en blanco sin avisar.
PRIVADOS = {}
try:
    import _datos_privados
    PRIVADOS = getattr(_datos_privados, "DATOS", {})
except ImportError:
    pass

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


# =============================================================================
# 3. Descripción del negocio para el SII
# =============================================================================
# Se arma desde el markdown de `asistente-administrativo/gestion/compai-spa/`
# para que exista UNA sola fuente: si el texto cambia allá, el documento con
# papelería se regenera y no quedan dos versiones divergentes.
#
# Diferencia con los otros dos: este no cabe en una hoja. Los documentos de una
# página dibujan la carta con `@page { margin: 0 }` y el padding adentro de
# `.hoja`; acá eso dejaría las páginas de continuación con el texto pegado al
# borde, porque el padding solo aplica a la primera. Por eso este lleva
# márgenes reales en `@page` y suelta el padding al imprimir.

import re as _re

FUENTE_SII = (AQUI.parent.parent / "asistente-administrativo" / "gestion" /
              "compai-spa" / "sii-descripcion-del-negocio.md")


def _md(t):
    """Markdown acotado: lo que este documento usa y nada más.

    Los párrafos se acumulan: el markdown viene con saltos de línea duros a
    ~85 caracteres, y un <p> por línea partiría cada párrafo en pedazos.
    """
    salida, en_tabla, en_lista, parrafo = [], False, False, []

    def cerrar_parrafo():
        if parrafo:
            salida.append("<p>" + " ".join(parrafo) + "</p>")
            parrafo.clear()

    def cerrar_lista():
        nonlocal en_lista
        if en_lista:
            salida.append("</ul>")
            en_lista = False

    def cerrar_tabla():
        nonlocal en_tabla
        if en_tabla:
            salida.append("</table>")
            en_tabla = False

    for linea in t.split("\n"):
        l = linea.rstrip()

        if l.startswith("|"):
            cerrar_parrafo()
            cerrar_lista()
            celdas = [c.strip() for c in l.strip("|").split("|")]
            if all(_re.fullmatch(r":?-{2,}:?", c or "-") for c in celdas):
                continue
            if not en_tabla:
                salida.append('<table class="datos">')
                en_tabla = True
                salida.append("<tr>" + "".join("<th>" + c + "</th>" for c in celdas) + "</tr>")
            else:
                salida.append("<tr>" + "".join("<td>" + c + "</td>" for c in celdas) + "</tr>")
            continue
        cerrar_tabla()

        if not l.strip():
            cerrar_parrafo()
            cerrar_lista()
            continue

        if l.strip() == "---":
            cerrar_parrafo()
            cerrar_lista()
            continue

        if l.startswith("#"):
            cerrar_parrafo()
            cerrar_lista()
            nivel = len(l) - len(l.lstrip("#"))
            texto = l[nivel:].strip()
            if nivel == 1:
                salida.append("<h1>" + texto + "</h1>")
            elif nivel == 2:
                salida.append("<h2>" + texto + "</h2>")
            else:
                salida.append("<h3>" + texto + "</h3>")
            continue

        if l.startswith("> "):
            cerrar_parrafo()
            cerrar_lista()
            salida.append("<blockquote>" + l[2:] + "</blockquote>")
            continue

        if l.startswith("- ") or _re.match(r"^\d+\. ", l):
            cerrar_parrafo()
            if not en_lista:
                salida.append("<ul>")
                en_lista = True
            salida.append("<li>" + _re.sub(r"^(- |\d+\. )", "", l) + "</li>")
            continue

        # Continuación de un item de lista: se pega al anterior.
        if en_lista and l.startswith("  "):
            if salida and salida[-1].endswith("</li>"):
                salida[-1] = salida[-1][:-5] + " " + l.strip() + "</li>"
            continue

        parrafo.append(l.strip())

    cerrar_parrafo()
    cerrar_lista()
    cerrar_tabla()

    h = "\n".join(salida)
    h = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
    h = _re.sub(r"`([^`]+?)`", r"<code>\1</code>", h)
    return h


if FUENTE_SII.exists():
    _texto = FUENTE_SII.read_text(encoding="utf-8")

    # Fuera los dos bloques internos del borrador.
    if "> **AVISO INTERNO" in _texto:
        _a = _texto.index("> **AVISO INTERNO")
        _texto = _texto[:_a] + _texto[_texto.index("---", _a):]
    if "## Marcadores a completar" in _texto:
        _b = _texto.index("## Marcadores a completar")
        _texto = _texto[:_texto.rindex("---", 0, _b)].rstrip()

    for _marcador, _valor in PRIVADOS.items():
        _texto = _texto.replace(_marcador, _valor)

    _faltan = sorted(set(_re.findall(r"\[[^\]\n]{3,45}\]", _texto)))

    # El título ya lo pone el encabezado; se saca del cuerpo para no repetirlo.
    _texto = _re.sub(r"^# .+?\n", "", _texto, count=1)
    # El encabezado ya dice a quién va dirigido; repetirlo en el cuerpo sobra.
    _texto = _texto.replace(
        "**Documento preparado para el Servicio de Impuestos Internos**\n", "", 1)

    _ESTILO = (
        "<style>\n"
        "  @page { size: letter; margin: 18mm 20mm; }\n"
        "  .hoja { min-height: 0; }\n"
        "  h2 { font-size: 12pt; margin: 18px 0 7px; padding-bottom: 3px;\n"
        "       border-bottom: .75pt solid " + LINEA + "; page-break-after: avoid; }\n"
        "  h3 { font-size: 10.5pt; margin: 13px 0 5px; color: " + GRIS + ";\n"
        "       page-break-after: avoid; }\n"
        "  p { margin: 0 0 7px; text-align: justify; }\n"
        "  ul { margin: 4px 0 9px 16px; padding: 0; }\n"
        "  li { margin: 3px 0; }\n"
        "  table.datos { margin: 7px 0 12px; font-size: 9.5pt; page-break-inside: avoid; }\n"
        "  table.datos th, table.datos td { border: .75pt solid " + LINEA + ";\n"
        "       padding: 4px 7px; text-align: left; vertical-align: top; }\n"
        "  table.datos th { background: #F4F3EF; font-weight: bold; }\n"
        "  blockquote { margin: 9px 0; padding: 7px 12px;\n"
        "       border-left: 2.5pt solid " + AMBAR + "; background: #FBF7EC; font-size: 10pt; }\n"
        "  code { font-family: " + MONO + "; font-size: 9.5pt; }\n"
        "  @media print { .hoja { padding: 0; width: auto; } }\n"
        "</style>"
    )

    _cab = (
        '<div class="kicker">Servicio de Impuestos Internos</div>'
        '<div style="font-size:12.5pt; font-weight:bold; margin-top:3px;">'
        'Descripción del negocio</div>'
        '<div style="font-family:' + MONO + '; font-size:8.5pt; color:' + GRIS +
        '; margin-top:3px;">' + RAZON + '<br>RUT ' + RUT + '</div>'
    )

    if _faltan:
        _aviso = nota("<strong>Faltan datos por completar:</strong> " + ", ".join(_faltan) +
                      ". Se rellenan en <code>marca/comercial/_datos_privados.py</code>, "
                      "que no se versiona.")
    else:
        _aviso = nota("Documento con papelería CompAI. Se genera desde "
                      "<code>sii-descripcion-del-negocio.md</code>: si el texto cambia allá, "
                      "hay que volver a correr este script. Ctrl+P para guardar como PDF.")

    _cuerpo = (_aviso + '\n<div class="hoja">\n  <div class="cuerpo">\n    ' +
               encabezado(_cab) + "\n" + _md(_texto) + "\n  </div>\n  " +
               pie(RAZON + " · RUT " + RUT, contacto()) + "\n</div>")

    _html = (BASE.replace("__TITULO__", "Descripción del negocio para el SII — " + FANTASIA)
                 .replace("__CUERPO__", _cuerpo)
                 .replace("</style></head>", "</style>" + _ESTILO + "</head>"))
    (AQUI / "sii-descripcion-del-negocio.html").write_text(_html, encoding="utf-8")
    print("Escrito: sii-descripcion-del-negocio.html" +
          ("" if not _faltan else "  — faltan por completar: " + ", ".join(_faltan)))
else:
    print("No se encontró el markdown del SII; ese documento no se generó.")
