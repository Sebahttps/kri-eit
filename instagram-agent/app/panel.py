"""Bandeja de revisión: los borradores pendientes, con un botón para enviarlos.

HTML plano y sin dependencias. Todo lo que viene de Instagram se escapa: el
texto de un DM es contenido de un tercero y no se inyecta crudo en la página.
"""
import json
from html import escape

ESTILOS = """
:root { color-scheme: light dark; --borde:#8883; --fondo:#fff; --texto:#111; --tenue:#666; }
@media (prefers-color-scheme: dark) { :root { --fondo:#14161a; --texto:#eceff4; --tenue:#9aa4b2; } }
* { box-sizing:border-box }
body { font:15px/1.55 ui-sans-serif,system-ui,-apple-system,sans-serif;
       background:var(--fondo); color:var(--texto); margin:0; padding:24px 16px; }
main { max-width:720px; margin:0 auto }
h1 { font-size:20px; margin:0 0 4px }
.sub { color:var(--tenue); margin:0 0 24px }
.item { border:1px solid var(--borde); border-radius:12px; padding:16px; margin-bottom:14px }
.item.alta { border-color:#e0564a; border-width:2px }
.meta { display:flex; gap:8px; flex-wrap:wrap; align-items:center;
        color:var(--tenue); font-size:13px; margin-bottom:10px }
.tag { border:1px solid var(--borde); border-radius:999px; padding:1px 9px }
.tag.alta { border-color:#e0564a; color:#e0564a }
blockquote { margin:0 0 12px; padding:9px 12px; border-left:3px solid var(--borde);
             background:#8881; border-radius:0 8px 8px 0; white-space:pre-wrap }
textarea { width:100%; min-height:64px; padding:10px; border-radius:8px;
           border:1px solid var(--borde); background:transparent; color:inherit;
           font:inherit; resize:vertical }
.acciones { display:flex; gap:8px; margin-top:10px; align-items:center }
button { font:inherit; padding:7px 14px; border-radius:8px; border:1px solid var(--borde);
         background:transparent; color:inherit; cursor:pointer }
button.enviar { background:#2f6df6; border-color:#2f6df6; color:#fff }
.estado { color:var(--tenue); font-size:13px }
.vacio { color:var(--tenue); text-align:center; padding:48px 0 }
"""

SCRIPT = """
async function accion(id, ruta, texto) {
  const estado = document.getElementById('estado-' + id);
  estado.textContent = 'enviando…';
  const r = await fetch(`/borradores/${id}/${ruta}?token=${TOKEN}`, {
    method: 'POST', headers: {'content-type': 'application/json'},
    body: JSON.stringify(texto === undefined ? {} : {texto}),
  });
  if (r.ok) { document.getElementById('item-' + id).remove(); return; }
  const detalle = await r.json().catch(() => ({}));
  estado.textContent = 'error: ' + (detalle.detail || r.status);
}
function enviar(id) { accion(id, 'enviar', document.getElementById('texto-' + id).value); }
function descartar(id) { accion(id, 'descartar'); }
"""


def _item(b: dict) -> str:
    bid = b["id"]
    alta = b.get("prioridad") == "alta"
    quien = f"@{b['autor_usuario']}" if b.get("autor_usuario") else b["autor_id"]

    return f"""
<article class="item {'alta' if alta else ''}" id="item-{bid}">
  <div class="meta">
    <strong>{escape(quien)}</strong>
    <span class="tag">{escape(b['tipo'])}</span>
    <span class="tag">{escape(b['categoria'])}</span>
    {'<span class="tag alta">revisar</span>' if alta else ''}
    <span>confianza {float(b['confianza']):.0%}</span>
    <span>· {escape(b['creado_en'])}</span>
  </div>
  <blockquote>{escape(b['texto_entrante'])}</blockquote>
  <textarea id="texto-{bid}">{escape(b['respuesta'])}</textarea>
  <div class="acciones">
    <button class="enviar" onclick="enviar({bid})">Enviar</button>
    <button onclick="descartar({bid})">Descartar</button>
    <span class="estado" id="estado-{bid}">{escape(b['razon'])}</span>
  </div>
</article>"""


def render(borradores: list[dict], token: str) -> str:
    cuerpo = ("".join(_item(b) for b in borradores) if borradores
              else '<p class="vacio">Nada pendiente. Todo respondido.</p>')
    plural = "s" if len(borradores) != 1 else ""
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Borradores · Instagram</title><style>{ESTILOS}</style></head>
<body><main>
<h1>Borradores pendientes</h1>
<p class="sub">{len(borradores)} mensaje{plural} esperando tu visto bueno.</p>
{cuerpo}
</main>
<script>const TOKEN = {json.dumps(token)};{SCRIPT}</script>
</body></html>"""
