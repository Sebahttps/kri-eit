# Marca CompAI — versión canónica

**Canónica: v1 · agosto 2026.** Cualquier archivo de marca fechado el 30-jul-2026
está obsoleto y vive archivado en `dropshipping-ai/brand/` (ver más abajo).

| | |
|---|---|
| Razón social | COMPAI GLOBAL SOLUTIONS SpA |
| Nombre de fantasía | CompAI SpA |
| RUT | 78.491.451-8 |
| Giro | Venta al por mayor de computadores y equipo periférico |
| Dominio | compai.cl |

---

## El logotipo

Tres piezas en un mismo lockup, sobre el sistema `viewBox="-38 -18 372 131"`:

| Pieza | Especificación | Día | Noche |
|---|---|---|---|
| `comp` | Helvetica / Arial · 600 · 56 · track −1,2 · x=4 y=58 | `#1A1D1B` | `#F5F0E4` |
| `AI` | Courier New · 700 · 53 · track 1,6 | `#A85F1B` | `#E0954F` |
| Doble tick | `translate(259 20) scale(1.5)` · stroke 2,2 · cap y join redondos | `#1F7A52` | `#4CC48B` |
| Brasa | blur 5 + blur 12 en `feMerge` · opacity 0,9 · **solo** `AI` y ticks | — | sí |

El contraste entre una grotesca pesada (`comp`) y una mecanográfica (`AI`) es lo
que distingue esta versión de la anterior: `AI` deja de ser un sufijo decorativo
y pasa a leerse como una etiqueta de máquina. Ese contraste es el activo de la
marca — no se toca sin recalcular el cuerpo (ver *Riesgos conocidos*).

### Aire y tamaños

- **Espacio libre:** la altura de x de `comp` (≈30 unidades) por los cuatro
  lados. Los archivos ya traen 42 unidades incorporadas para que el halo no se
  corte, así que en maqueta se colocan sin margen adicional.
- **Mínimo digital:** 110 px de ancho de lockup. **Mínimo impreso:** 30 mm.
- **Doble tick solo:** desde 24 px. Bajo eso los dos ticks se funden en uno.

### Paleta

| Hex | Rol | Contraste |
|---|---|---|
| `#F5F0E4` | Blanco marca · `comp` sobre oscuro | 17,46:1 sobre `#080A09` |
| `#E0954F` | Ámbar · `AI` sobre oscuro | 8,11:1 sobre `#080A09` |
| `#4CC48B` | Verde tick sobre oscuro | 9,05:1 sobre `#080A09` |
| `#1A1D1B` | Tinta · `comp` sobre claro | 17,00:1 sobre blanco |
| `#A85F1B` | Ámbar impreso · `AI` sobre claro | 4,86:1 sobre blanco |
| `#1F7A52` | Verde tick impreso | 5,30:1 sobre blanco |
| `#080A09` | Fondo base · `#0D100E` superficie card | — |
| `#8FF0B4` | Acento de interfaz (**no** es el verde del tick) | 14,46:1 sobre `#080A09` |
| `#FFB25C` | Precios en interfaz | 11,13:1 sobre `#080A09` |

`#A85F1B` cumple AA (4,5:1) sobre blanco puro con **4,86:1** de margen estrecho:
sirve como color de marca, pero **no** como color de texto corrido sobre fondos
crema o beige, donde cae a 4,35:1 y deja de cumplir.

### Tipografía de interfaz

Space Grotesk (display y cuerpo) e IBM Plex Mono (precios, metadatos, kickers).
El logotipo no usa ninguna de las dos: es Helvetica 600 + Courier New 700, ambas
de sistema, para que el SVG se vea igual sin cargar webfonts.

---

## Archivos

### `svg/` — vectoriales

| Archivo | Uso |
|---|---|
| `compai-logotipo.svg` | Nocturno con brasa. Pantalla y fondos oscuros |
| `compai-logotipo-dia.svg` | Diurno, tinta plana. Papel y fondos claros |
| `compai-logotipo-mono.svg` | Una sola tinta `#1A1D1B`. Timbres, grabado, fax, fotocopia |
| `compai-letras.svg` | Solo el lockup tipográfico, sin ticks |
| `compai-ticks.svg` / `-dia.svg` | Solo el doble tick |
| **`compai-logotipo-curvas.svg`** | Nocturno **con el texto convertido a curvas** |
| **`compai-logotipo-dia-curvas.svg`** | Diurno en curvas |
| **`compai-logotipo-mono-curvas.svg`** | Monocromo en curvas |
| **`compai-favicon.svg`** | Doble tick sobre `#080A09`, esquinas 14/64. Pestaña y avatar |
| **`compai-favicon-dia.svg`** | Mismo, sobre blanco, para fondos claros |

**Los cuatro archivos en negrita se generaron aquí; no venían en el kit.**

Las versiones **en curvas** existen porque los archivos originales usan texto en
vivo: se dibujan con la fuente de cada equipo. Helvetica y Courier New están en
Windows y macOS, pero **no** en un servidor Linux ni en un contenedor de CI, donde
el navegador cae a Liberation Mono o DejaVu Sans Mono y el `AI` cambia de forma.
**Para imprenta, PDF de oferta, INAPI y cualquier render en servidor se usan las
versiones en curvas.** Las de texto vivo quedan para edición.

### `png/` — mapa de bits, fondo transparente, 3×

Los mismos seis lockups, para Word, correo y presentaciones.

### `inapi/` — etiqueta para la solicitud de marca

| Archivo | Qué es |
|---|---|
| `etiqueta-inapi-compai.png` / `.jpg` / `.svg` | **Etiqueta en color, 2100 × 636 px.** La recomendada |
| `etiqueta-inapi-compai-bn.png` / `.jpg` / `.svg` | Misma etiqueta en negro puro, alternativa de mayor cobertura |

Construida sobre el lockup en curvas, encuadre = caja del arte + 30 unidades de
aire por lado (la regla de espacio libre de la propia marca), fondo blanco sólido,
sin canal alfa. El PNG está en RGB de 8 bits; el JPG es respaldo para el
formulario en línea si rechaza PNG.

**Color o blanco y negro es decisión de LegAI/AdmAIn, no de diseño.** El criterio
visual: la combinación ámbar + verde es el activo distintivo real de la marca y
vale reivindicarla; el B/N cubre más combinaciones cromáticas pero renuncia a
proteger el par de color. Ambos archivos están listos, la decisión no cuesta
tiempo.

### `propuestas/` — no presentar, no publicar

`lockup-v1.1-espaciado` corrige dos defectos métricos del lockup v1 (ver
*Riesgos conocidos*). **No es la marca vigente.** Nada de esta carpeta se adjunta
a INAPI ni se usa en producción hasta que se apruebe.

---

## Riesgos conocidos del lockup v1

Se documentan porque son medibles, no opiniones. Ninguno impide usar la marca.

1. **`p` y `A` se tocan.** Con Arial Bold 56 y Courier New Bold 53, la caja de
   `comp` termina en x=147,67 y la de `AI` empieza en x=147,36: se solapan 0,31
   unidades. A 110 px de lockup eso son 0,12 px — invisible. Importa solo en
   impresión pobre, donde la tinta puede puentear las dos letras.
2. **El hueco entre `AI` y los ticks es de 49,4 unidades**, o sea 1,66 veces la
   altura de x. El propio manual fija el espacio libre *exterior* en 30 unidades:
   hoy el aire *interno* del lockup es mayor que el externo, que es justo al revés
   de como se sostiene un conjunto. Por eso los ticks se leen como un objeto
   suelto y no como parte de la marca.
3. **El cuerpo 53 de `AI` no iguala la altura de x de `comp`**, como afirma la
   especificación: la altura de mayúsculas de Courier New Bold a 53 es 31,39 y la
   altura de x de Arial Bold a 56 es 29,70. Para igualarlas el cuerpo sería 50,15.
   La diferencia de 5,7 % es pequeña y el lockup se lee parejo igual — pero la
   especificación dice que está calculado y no lo está.
4. **El doble tick no sobrevive a 16 px.** A ese tamaño los dos ticks se funden en
   un trazo único y se pierde la idea de "doble confirmación". El manual declara
   24 px como mínimo y es correcto. El kit anterior resolvía la pestaña con una
   burbuja rellena, que a 16 px sí leía; el kit actual no tiene equivalente.

`propuestas/lockup-v1.1-espaciado` resuelve 1 y 2: +4 unidades entre `p` y `A`, y
ticks a `translate(235.06 20)` para un aire interno de 21,5 unidades (0,72 × la
altura de x). La proporción pasa de 6,39:1 a 5,86:1 y el conjunto se lee como una
sola pieza.

---

## Lo que NO vive en este repositorio

`kri-eit` es un **repositorio público**. Los logotipos son marca y su difusión es
deseable; los **timbres no**.

Los tres timbres (`timbre-gerente-general`, `timbre-recepcion`, `timbre-pdf`)
quedan **solo en local**, en `compai_workspace/`, que `.gitignore` ya bloquea.

El motivo no es privacidad sino control: un timbre es un facsímil de
autorización. El de PDF está diseñado precisamente para pegarse sobre un
documento digital, y el de Gerente General valida contratos y poderes. Publicar
esos archivos equivale a repartir el sello de la empresa: cualquiera podría
descargarlo y timbrar un documento a nombre de CompAI. Que un timbre no tenga
valor legal por sí solo no evita el daño — evita el pleito, no la confusión del
tercero que lo recibe. El `.gitignore` de esta carpeta bloquea `timbre-*` como
segunda barrera, por si alguien copia el kit completo aquí sin mirar.

---

## Relación con `dropshipping-ai/brand/`

Aquella carpeta es la marca del **30-jul-2026**, hecha para la tienda Shopify de
mascotas. Se archiva, no se fusiona: pertenece a un negocio que se cierra y su
`shopify-custom.css` no aplica a nada vigente. Lo que allí es distinto:

| | 30-jul-2026 (archivado) | ago-2026 (canónico) |
|---|---|---|
| `comp` | `system-ui` 600 — Segoe UI en Windows, SF en macOS | Helvetica / Arial 600 |
| `AI` | Misma familia, cuerpo 41 (versalitas) | **Courier New 700, cuerpo 53** |
| Ticks | `translate(232 20)` | `translate(259 20)` |
| Tinta / ámbar / verde | `#1c1917` `#a2551f` `#15734a` | `#1A1D1B` `#A85F1B` `#1F7A52` |
| Nocturno | Placa oscura incorporada al archivo | Sin placa, fondo transparente |
| Isotipo | Burbuja de chat verde con tick | Eliminado |
| Lienzo | `0 0 300 84`, sin aire | `-38 -18 372 131`, 42 u de aire |
