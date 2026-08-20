# sitio-compai

La página de servicio de `compai.cl`. Una sola página, un solo archivo.

`index.html` **se genera**: no editarlo a mano, se pisa. Editar `_construir.py`
y correrlo:

```
python sitio-compai/_construir.py
```

## Por qué una página y no un sitio

El dominio ya sale impreso en la carátula de oferta, la ficha de empresa, las
tres plantillas comerciales, la firma de correo y las tarjetas. Lo único que
esta página tiene que lograr es que **el comprador público que lea `compai.cl`
al pie de una cotización y escriba la dirección encuentre lo que esperaba
encontrar**. Nada más. Un dominio sin página se lee como empresa nueva; uno que
lleva a otro negocio se lee como que algo raro pasa.

## Dirección de arte: "ficha técnica iluminada"

El público no es una startup ni un inversionista: es un encargado de
adquisiciones que rinde cuentas a Contraloría. **Demasiado efecto lo espanta y
lo plano también.** El punto justo es sobrio con oficio: que se note trabajo, no
efectos.

Cómo se resuelve eso en la página:

- **Retícula de plano** de fondo (paso 34 px, paso mayor 170 px), hecha con
  `repeating-linear-gradient`. Textura sin ruido y sin un solo byte de red.
- **Una sola fuente de luz.** El filtro `brasa` del logotipo se extiende a la
  página como un halo en registro exacto detrás del lockup, y todos los
  reflejos internos de las tarjetas caen del mismo lado. Ningún resplandor
  suelto: si se despega del logotipo, deja de tener razón física y se lee como
  adorno.
- **Espina vertical continua** entre la columna de rótulos y el cuerpo. Es lo
  que convierte cuatro bloques en un documento.
- **Secciones numeradas** (`01`…`04`), rótulos y datos duros en monoespaciada.
- **Cero animación.** Nada se mueve solo; solo hay transiciones de estado, y se
  apagan con `prefers-reduced-motion`.

## Cero dependencias externas

Ni webfonts, ni CDN, ni imágenes sueltas, ni JavaScript: los logotipos van
incrustados como SVG en curvas y las tipografías son de sistema. Son **32 KB en
un archivo (8,5 KB comprimido)** y **cero peticiones externas**. Carga igual de
rápido en la red de un municipio que en fibra, y no hay nada que se pueda caer.

## En pantalla es nocturna; impresa, diurna

En pantalla va en la paleta **nocturna**, que es donde el logotipo nació. Pero
el comprador público imprime, y a menudo en blanco y negro: el bloque
`@media print` da vuelta la página entera a la paleta **diurna** del manual
—fondo blanco, tinta `#1A1D1B`, ámbar `#A85F1B`, verde `#1F7A52`— y cambia el
logotipo nocturno por el de tinta plana, que también viaja incrustado. Impresa
sale una ficha, no una captura oscura.

## Contrastes medidos

| Uso | Color | Sobre | Ratio |
|---|---|---|---|
| Titulares y texto fuerte | `#F5F0E4` | `#080A09` | 17,46:1 |
| Texto secundario (cuerpo) | `#A6AFA8` | `#080A09` | 8,81:1 |
| Rótulos cortos en mono | `#8A938D` | `#080A09` | 6,28:1 |
| Enlaces y confirmación | `#4CC48B` | `#080A09` | 9,05:1 |
| Números de sección | `#E0954F` | `#080A09` | 8,11:1 |
| Impresión, texto secundario | `#46504A` | blanco | 8,38:1 |

Todo por sobre AA. `#A85F1B` (4,86:1) queda solo como filete y borde en
impresión, nunca como texto corrido — el manual de marca ya advierte que sobre
crema cae a 4,35:1 y deja de cumplir.

## El teléfono no se versiona

`TELEFONO` está vacío en `_construir.py` a propósito — este repo es público. Se
completa antes de construir y se deja en blanco al guardar. Si queda vacío, el
pie sale solo con el correo, que es una degradación aceptable.

## Cómo revisarla antes de publicar

`file://` está bloqueado. Hay que servirla:

```
python sitio-compai/_construir.py
cd sitio-compai && python -m http.server 8777
```

y abrir `http://127.0.0.1:8777`. Para ver la versión impresa, Ctrl+P y mirar la
vista previa.

## Lo que falta para que esté en línea

1. **La raíz de `compai.cl` la ocupa Shopify hoy** (`23.227.38.65`), y `www`
   apunta a `shops.myshopify.com`. Hay que moverlos.
2. Publicar por **GitHub Pages**, igual que `regalon.compai.cl`. Es gratis y no
   depende del VPS — eso importa, porque el VPS se está apagando.
3. En Cloudflare, apuntar la raíz a GitHub Pages. Cloudflare aplana CNAME en el
   ápice, así que no hace falta poner las cuatro IP a mano.

**Quitar el dominio de Shopify no cancela el plan de Shopify.** Son dos cosas
distintas y la facturación sigue corriendo por su lado.
