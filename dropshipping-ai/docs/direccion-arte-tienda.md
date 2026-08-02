# Dirección de arte — tienda CompAI (Shopify Horizon 4.1.3)

Dirección de arte SOBRE la identidad ya decidida (crema `#f7f2e6`, tinta
`#1c1917`, cobre `#a2551f` en botones, verde `#15734a` solo en el doble check,
tarjetas `#fdfbf4`, bordes `#e5dcc8`, Inter). Aquí no se cambia la base: varía
composición, fotografía, tono del copy y ritmo de página.

**Mensajes clave (máx. 3):** 1) te confirmamos el stock antes de cobrarte,
2) puedes pagar al recibir, 3) si algo falla, CompAI responde (garantía 6 meses,
retracto 10 días). **Emoción objetivo: alivio** — la sensación de "aquí no me
van a dejar botado". Todo lo visual se juzga contra eso.

---

## 1. Tres direcciones visuales

### A. «Palabra en grande» — la promesa es el hero

**Concepto:** la tienda abre con texto, no con foto. La promesa en tipografía
grande sobre crema; el producto aparece después, ya con el terreno de confianza
ganado. **Emoción:** seriedad que tranquiliza.

- **Hero:** sección *Texto enriquecido* (o banner sin imagen) a ancho completo
  sobre `#f7f2e6`. Título en Inter semibold, 2 líneas máximo, ~clamp 2.2–3.5rem;
  subtítulo 1 línea; un solo botón cobre. Nada más arriba del pliegue en móvil.
- **Orden de secciones:** hero tipográfico → **las cinco promesas** (burbujas
  `.compai-promesas`, inmediatamente bajo el hero: son el segundo pantallazo en
  móvil) → colección destacada (4 productos, tarjetas `#fdfbf4`) → sección
  *media con texto* explicando "cómo funciona la confirmación" en 3 pasos →
  FAQ en filas contraíbles (COD, plazos, garantía) → pie.
- **Página de producto:** galería sobria a la izquierda, columna de compra a la
  derecha; bajo el botón, microcopy de confianza (ver §3). Las promesas
  completas se repiten como sección al final de la PDP.
- **Jerarquía:** texto > promesas > producto. Fotografía de apoyo, no
  protagonista: bodegones simples sobre crema.
- **Gana para:** lanzar YA, sin fotos propias todavía — funciona con fotos de
  proveedor retocadas. **Riesgo:** si el copy no es excelente, la home se
  siente vacía; y una tienda sin producto arriba vende menos por impulso.

### B. «El mesón de la casa» — el producto viviendo en un hogar chileno

**Concepto:** fotografía cálida de los productos en uso sobre superficies
reales (mesón de cocina, escritorio, piso de la casa), luz de ventana, tonos
que conviven con el crema. La confianza se muestra, no solo se declara.
**Emoción:** pertenencia — "esto podría estar en mi casa".

- **Hero:** *banner de imagen* con una foto horizontal (freidora o lámpara en
  contexto doméstico, luz cálida lateral), texto sobre placa `#fdfbf4` al 92%
  de opacidad para garantizar contraste, botón cobre. En móvil, versión
  recortada vertical del mismo escenario.
- **Orden:** hero fotográfico → cinta fina de confianza (una línea: "Stock
  confirmado antes de cobrar · Paga al recibir · Garantía 6 meses") → colección
  destacada con fotos en contexto → **las cinco promesas** en burbujas, a mitad
  de página → *media con texto* con la foto "honesta" (producto + caja + lo que
  trae) → FAQ → pie.
- **PDP:** primera imagen SIEMPRE en contexto, segunda sobre fondo crema
  limpio, tercera el detalle honesto (puertos, filtro, costuras).
- **Jerarquía:** foto > promesa > texto largo.
- **Gana para:** diferenciarse de inmediato del dropshipping de fondo blanco;
  es la dirección con más carácter. **Riesgo:** exige comprar unidades de
  muestra y hacer fotos decentes; con fotos malas, el efecto se invierte.

### C. «Conversación abierta» — la página como un chat que responde

**Concepto:** la estructura de la home imita un hilo de conversación: cada
duda del cliente escéptico ("¿y si no llega?", "¿y si sale malo?") recibe su
respuesta en burbuja con doble check. Extiende el elemento firma (burbuja
WhatsApp) a sistema de página. **Emoción:** sorpresa que desarma la
desconfianza nombrándola.

- **Hero:** título + dos burbujas en diálogo: una gris-papel con la duda
  ("¿Otra tienda que cobra y desaparece?") y la respuesta CompAI con doble
  check verde ("Aquí te confirmamos el stock antes de cobrarte."). Botón cobre
  debajo.
- **Orden:** hero-diálogo → productos (tarjetas con una mini-burbuja de dato
  útil por producto) → **las cinco promesas** (aquí son el clímax, no un
  bloque de apoyo) → sección "así trabaja el agente" → FAQ escrita como chat →
  pie.
- **PDP:** bajo el botón de compra, una burbuja única con doble check y el
  microcopy de confirmación; el resto sobrio para no saturar.
- **Jerarquía:** diálogo > producto > detalle.
- **Gana para:** memorabilidad y coherencia total con el isotipo. **Riesgo:**
  a un paso del gimmick; si cada sección es burbuja, el doble check se
  devalúa (la restricción del verde existe por algo). Exige disciplina.

### Recomendación

**Empezar con A («Palabra en grande») y migrar el hero a B cuando existan
fotos propias.** A es la única ejecutable hoy con fotos de proveedor
retocadas, pone la promesa —el único diferenciador real— arriba de todo, y no
depende de recursos que aún no existen. B queda como evolución natural: mismo
esqueleto de secciones, se reemplaza el hero tipográfico por el fotográfico.
C se reserva como campaña o landing puntual, no como sistema permanente.

---

## 2. Guía de fotografía de producto (para el dueño)

### Setup base (sirve para los 4 SKUs)

- **Fondo:** cartulina o papel kraft claro / lino en tono crema-arena, lo más
  cercano a `#f7f2e6`–`#e5dcc8`. En retoque se empuja al crema exacto. Nunca
  blanco puro: el blanco `#ffffff` "flota" recortado sobre la página crema y
  grita AliExpress.
- **Luz:** una ventana lateral con luz de día + un rebotador blanco (plumavit
  o cartón forrado) al lado opuesto. Sin flash directo. Sombras suaves y
  visibles: la sombra de contacto es lo que hace que el objeto "pese" y se lea
  real.
- **Cámara:** el teléfono basta. Limpiar el lente, HDR desactivado si satura,
  apoyar el teléfono o usar trípode barato. Disparar en horizontal Y vertical
  (Horizon usa ambas: banner horizontal, tarjeta ~cuadrada).
- **Cantidad por SKU:** mínimo 5 tomas — 3/4 general, frontal, detalle,
  escala (con una mano o un objeto común), y la "foto honesta" (producto +
  caja + accesorios reales que trae).

### Ángulos por producto

1. **Freidora de aire 5L ($42.000):** principal en 3/4 a la altura del mesón,
   levemente desde abajo (se ve sólida, no juguete). Segunda: canasto abierto
   mostrando el interior. Escala: junto a un plato o una mano poniendo
   papas. Detalle: panel de control encendido. Contexto (fase B): mesón de
   cocina con azulejos o madera clara.
2. **Aspiradora robot compacta ($79.900):** principal a ras de piso (ángulo
   bajo, piso de madera o flotante — es donde vivirá). Cenital para la forma.
   **Foto honesta obligatoria:** la parte de abajo con cepillos y ruedas — es
   lo que nadie muestra y lo que más confianza da a este precio. Detalle:
   depósito de polvo extraído. Escala: junto a la pata de una silla.
3. **Audífonos inalámbricos Pro ($21.990):** macro sobre papel `#fdfbf4`
   (la superficie de tarjeta). Estuche abierto en 3/4 con un
   audífono fuera. Escala: uno en la palma. Detalle: bisagra y puerto de
   carga (los puntos donde los clones fallan). Evitar el "audífono flotando
   con partículas": es el cliché número uno del rubro.
4. **Lámpara de escritorio LED ($12.990):** el producto ES la luz — la
   principal va **encendida**, atardecer o pieza en penumbra, mostrando el
   cono de luz cálida sobre un escritorio con un cuaderno. Secundaria apagada
   sobre crema para la forma. Detalle: articulación del brazo en 2 posiciones.
   Escala: junto a un libro.

### Si se parte de fotos de proveedor (retoque)

- Elegir SOLO fotos reales del proveedor (no renders). Señales de render:
  reflejos imposibles, cero polvo, sombra idéntica en todas las tomas.
- Recortar el objeto, ponerlo sobre `#f7f2e6`, y **agregar sombra de contacto
  suave** (elipse difuminada bajo el objeto, opacidad ~20%). Sin esa sombra el
  recorte se nota siempre.
- Igualar temperatura de color hacia cálido (+ ligero) para que conviva con
  el crema. Nunca dejar el fondo blanco original.
- Verificar que no queden restos de watermark ni texto en otros idiomas.

### Qué NO hacer (los gatillos de desconfianza)

- Fondo blanco genérico de marketplace, recorte duro sin sombra.
- Watermarks, logos de terceros, texto chino/inglés incrustado en la imagen.
- Renders 3D irreales o imágenes generadas con manos/reflejos raros.
- Flechas rojas, círculos amarillos, "50% OFF" pegado en la foto.
- Fotos de estilo de vida de banco de imágenes con casas evidentemente no
  chilenas. Mejor bodegón simple y honesto que lifestyle falso.
- Mezclar estilos entre los 4 SKUs: mismo fondo, misma luz, misma dirección
  de sombra en todo el catálogo. La consistencia ES la señal de que hay
  alguien serio detrás.

---

## 3. Copy clave (chileno neutro)

- **Hero — título:** `Te confirmamos el stock antes de cobrarte.`
- **Hero — subtítulo:** `Tecnología y hogar para tu casa, con entrega
  verificada en Chile. Y si prefieres, pagas al recibir.`
- **Botón principal:** `Ver los productos` (claridad sobre astucia; nada de
  "Shop now").
- **Microcopy de confianza en la página de producto** (bajo el botón de
  compra, en burbuja con doble check verde — una sola burbuja, tres líneas):
  - `Stock confirmado con el proveedor antes de cobrarte.`
  - `Paga al recibir, si prefieres. Seguimiento real de tu despacho.`
  - `Garantía legal de 6 meses y 10 días para retractarte.`
- **Cierre de la burbuja / sello:** `Compra confirmada. CompAI responde.`
- **Estado de disponibilidad en PDP:** en vez del "In stock" por defecto,
  `Disponible — confirmamos con el proveedor antes de cobrar.`
- Tono general: segunda persona singular, frases cortas, cero anglicismos
  innecesarios (no "shipping", sí "despacho"; no "refund", sí "devolución").

---

## 4. Logo para la solicitud de marca mixta en INAPI

**Presentar como etiqueta: `logo-compai.svg` completo (versión día) — el
logotipo "comp + AI" con el doble check verde — NO el isotipo solo.**

Razones de protección, no de estética:

1. **La raíz "comp-" está saturada en clase 35** (ya detectado en el
   handoff). En una mixta, la distintividad se evalúa por el conjunto: las
   versalitas cobre de "AI" + el doble check verde son justamente lo que
   aporta carácter registrable y ayuda a superar observaciones por semejanza
   con otras "comp…".
2. **El isotipo solo es débil como marca:** una burbuja de chat con dos
   checks se parece a iconografía de mensajería de uso común; defenderlo
   aislado sería cuesta arriba. Dentro del conjunto, en cambio, queda
   protegido como parte de la etiqueta.
3. **Una sola solicitud cubre denominación + gráfica:** la mixta protege el
   conjunto tal como se presenta. Si más adelante hay presupuesto, una
   segunda solicitud denominativa pura de "COMPAI" reforzaría la palabra por
   separado — pero la prioritaria es esta mixta.

**Especificaciones de la etiqueta:**

- **En color**, tal como se usa: "comp" en `#1c1917`, "AI" en `#a2551f`,
  doble check en `#15734a`. El color es parte del distintivo (el verde de
  confirmación significa algo); presentarla en blanco y negro regalaría ese
  elemento.
- **Fondo blanco** (o transparente aplanado a blanco), no crema: el crema es
  la superficie del sitio, no parte del signo; incluirlo limitaría la marca a
  usarse sobre ese fondo.
- **Formato:** exportar el SVG a PNG o JPG de alta resolución — mínimo
  1500 px de ancho (equivalente a ~300 dpi en el tamaño de etiqueta que pide
  el formulario en línea de INAPI), sin bordes ni marcos.
- **Antes de exportar, convertir el texto a curvas** (mismo requisito que
  para Shopify, ver `brand/README.md`): el SVG usa texto vivo y en otra
  máquina cambiaría de forma. La etiqueta debe ser exactamente la marca que
  se usa en la tienda — la coherencia entre lo registrado y lo usado importa
  si algún día hay que probar uso.
- La versión nocturna (`logo-compai-noche.svg`) NO se presenta: el degradado
  del muro y el resplandor son tratamiento escénico, no el signo. Queda
  cubierta como variante de uso de la misma marca.
