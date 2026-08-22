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

## Cómo está publicada

En línea desde el 21-ago-2026 y verificado desde fuera ese mismo día.

| | |
|---|---|
| Dominio | `https://compai.cl` (y `www` redirige 301 al ápice) |
| Repositorio publicador | `github.com/Sebahttps/CompAI` — solo `CNAME`, `README.md`, `index.html`, `404.html` |
| Origen | GitHub Pages, rama `main`, raíz |
| DNS | Cloudflare, registro **DNS-only**: la respuesta trae `Server: GitHub.com`, no pasa por el proxy naranja |
| Certificado | Let's Encrypt emitido por Pages, renovación automática |
| Peso | 34 KB en un archivo, ~8,5 KB con gzip, cero peticiones externas |

El VPS ya no participa: se destruyó el 20-ago y los subdominios `hola`, `panel`
y `api` se eliminaron de Cloudflare para no dejar *dangling DNS*.

## Cómo se actualiza

```
python sitio-compai/_construir.py        # genera index.html y 404.html
cd sitio-compai && python -m http.server 8777   # revisar en 127.0.0.1:8777
```

Cuando esté bueno, copiar **los dos archivos** al repo publicador
(`CompAI/`), commit y push. GitHub Pages sirve con `Cache-Control: max-age=600`,
así que el cambio puede tardar hasta diez minutos en verse.

**No editar `index.html` ni `404.html` a mano**, en ninguno de los dos repos: se
generan y se pisan.

## La 404

`404.html` se construye del mismo script y reusa encabezado y pie. Sin ella,
un enlace mal copiado desde un PDF aterriza en la página de error de GitHub con
el octocat, que descubre el andamio justo delante del comprador. Lleva
`noindex` y una sola salida: volver a la portada.

## Los datos de contacto, y por qué sí van

`TELEFONO`, `DOMICILIO` y `FICHA_PROVEEDOR` están completos desde el
21-ago-2026. Antes iban vacíos "porque el repo es público", y **esa razón era
falsa**: `index.html` se publica en la web abierta y es tan público como el
repo, e indexable. Iban vacíos porque eran una decisión pendiente.

- **Teléfono**: va. Ya estaba impreso en la cotización, en la firma de correo y
  en la ficha de Mercado Público.
- **Domicilio**: va a nivel de ciudad y región, sin calle. El domicilio
  tributario es particular y la dirección exacta no le aporta al comprador lo
  suficiente como para justificarlo.
- **Ficha de proveedor**: `https://proveedor.mercadopublico.cl/ficha/<RUT>`.
  Convierte "Inscrita y hábil" de afirmación propia en dato verificable de un
  clic. **Sin comprobar todavía si esa URL se ve sin sesión iniciada** — si
  pidiera login hay que quitar el enlace y dejar solo la fecha.
- **`ACREDITADO_HASTA`**: 19 de agosto de 2027, tomado de la propia ficha. La
  habilidad es un estado que caduca; afirmarla sin fecha deja expuesta a la
  empresa el día que deje de estarlo.

## Coherencia entre fuentes

Un comprador que verifica cruza tres fuentes: esta página, la ficha de Mercado
Público y el estatuto. Tienen que decir lo mismo.

**Domicilio — resuelto el 21-ago-2026.** El estatuto decía *Carmen 668, depto
825, Santiago* y Mercado Público *CARRION 1507 DP 1930 P19, INDEPENDENCIA*. Se
actualizó el RES a **Carrion 1507, block B, depto 1930, Independencia**, con lo
que las dos fuentes coinciden en cuanto se firme el trámite. La página muestra
solo *Santiago, Región Metropolitana*, por decisión: la calle no aporta lo
suficiente como para publicar un domicilio particular.

**Correo — abierto.** La ficha de Mercado Público trae `stapiamena@gmail.com`
como correo laboral, mientras la página y las cotizaciones usan
`stapiamena@compai.cl`. Al comprador que verifica le aparecen dos correos para
la misma empresa. Se corrige en el escritorio de ChileCompra, no acá.

## Lo que la página todavía no contesta

- **Despacho a regiones: sí o no.** Primera pregunta de cualquier comprador
  fuera de la RM.
- **Boletas de garantía y de seriedad de la oferta: si se pueden tomar.** Sobre
  cierto monto, no poder tomarlas es no poder ofertar.

**Los plazos se dejan como están.** La sección `02` dice que no se compromete
una fecha que no esté respaldada; poner plazos genéricos rompería lo más
creíble que tiene la página.
