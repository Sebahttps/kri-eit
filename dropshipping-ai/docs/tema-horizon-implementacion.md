# Implementación en Horizon 4.1.3 — dirección A con el ADN de C

Ejecuta primero `docs/shopify-tema-compai.md` (colores globales, logotipo en
curvas, CSS propia, mecánica de las burbujas): este documento no lo repite.
Las direcciones, la fotografía y el copy base están en
`docs/direccion-arte-tienda.md`.

**Para el dueño, en corto:** C no está descartada — está sembrada. La idea de
que la página SEA el agente es correcta, y justamente por eso no puede ser un
disfraz: el día que la página hable como agente, tiene que haber un agente
real respondiendo detrás (y ya lo tienes: los agentes de verificación son
munición honesta). Hoy A instala la voz de CompAI en tres puntos exactos
(§2); la hoja de ruta (§3) dice qué debe ser verdad antes de que C sea la
casa entera. La personificación se gana con hechos, no se decora.

Los nombres de sección pueden variar levemente según idioma o subversión del
editor; usa el equivalente más cercano. Todo lo que va entre comillas es
texto exacto para pegar.

---

## 1. Home, sección por sección (orden de arriba abajo)

### 1.1 Hero — sección **Texto enriquecido**

- Ajustes: esquema principal (crema), sin imagen, ancho de página, contenido
  centrado; espaciado superior e inferior amplios (el mayor que ofrezca el
  control, ~64 px). En móvil, nada más que esto arriba del pliegue.
- **Título (H1):** "Te confirmamos el stock antes de cobrarte."
- **Subtítulo:** "Tecnología y hogar para tu casa, con entrega verificada en
  Chile. Y si prefieres, pagas al recibir."
- **Botón (sólido, cobre):** "Ver los productos" → enlace a la colección
  principal (`/collections/all`). Un solo botón; sin botón secundario.

### 1.2 Las cinco promesas — sección **Texto enriquecido** con lista

- Montaje y clase `.compai-promesas`: seguir `shopify-tema-compai.md` §4 tal
  cual, con sus cinco textos exactos. Esquema principal; sin título de
  sección (las burbujas se explican solas); espaciado superior reducido para
  que en móvil sea el segundo pantallazo.

### 1.3 Catálogo — sección **Colección destacada**

- Ajustes: la colección con los 4 productos; 4 columnas en escritorio, 2 en
  móvil; esquema secundario si existe (tarjetas `#fdfbf4`); relación de
  imagen cuadrada; mostrar título y precio, sin insignias extra.
- **Título de sección:** "Lo que tenemos hoy" (honesto con un catálogo
  chico: comunica curaduría, no bodega infinita).
- El **dato útil por producto** no va en la tarjeta (Horizon no lo muestra):
  va como primera línea de la descripción de cada producto, y así aparece en
  la PDP y en la vista rápida. Textos (completar corchetes con la ficha real
  del proveedor antes de publicar; no inventar cifras):
  - Freidora de aire 5L: "5 litros: porciones para toda la familia, sin
    aceite."
  - Aspiradora robot compacta: "Compacta: pasa donde la aspiradora grande no
    llega, y vuelve sola a su base."
  - Audífonos inalámbricos Pro: "Con estuche de carga: batería para el día
    [confirmar horas reales con el proveedor]."
  - Lámpara de escritorio LED: "Luz cálida para estudiar de noche [confirmar
    con la ficha: ¿intensidad regulable?]."

### 1.4 Cómo funciona la confirmación — sección **Medios con texto** (o **Iconos con texto** / multicolumna si la versión la ofrece, en 3 columnas)

- Ajustes: esquema principal, imagen opcional (si hay, un bodegón sobre
  crema; jamás una ilustración genérica de "robot").
- **Título de sección:** "Cómo funciona la confirmación"
- **Paso 1 — Eliges.** "Agregas tu producto y dejas tu pedido."
- **Paso 2 — Confirmamos.** "Un agente verifica el stock directamente con el
  proveedor antes de cobrarte. Si no hay stock, no se te cobra. Así de
  simple."
- **Paso 3 — Recibes.** "Sigues tu despacho en tiempo real y, si así lo
  elegiste, pagas al recibir."

### 1.5 FAQ — sección **Contenido desplegable / filas contraíbles**

- Ajustes: esquema principal, una pregunta por fila, todas cerradas por
  defecto. **Título de sección:** "Pregúntale a CompAI"
- **"¿Y si pago y no llega?"** → "No pasa: confirmamos el stock con el
  proveedor antes de cobrarte y te damos el seguimiento real del despacho.
  Y si aun así algo falla, te devolvemos la plata. Compra confirmada.
  CompAI responde."
- **"¿Puedo pagar cuando me llegue?"** → "Sí. Al finalizar tu compra elige
  pago contra entrega y pagas al recibir tu pedido." *(Requiere COD activo:
  Configuración → Pagos → Métodos de pago manuales.)*
- **"¿Cuánto demora el despacho?"** → "Entre [X] y [Y] días hábiles según tu
  comuna. Te lo decimos antes de confirmar tu compra y te enviamos el
  seguimiento apenas sale." *(Completar con los plazos reales del proveedor;
  publicar esta fila solo cuando estén confirmados.)*
- **"¿Y si sale malo?"** → "Tienes garantía legal de 6 meses. Nos escribes y
  la gestionamos de inmediato: cambio, reparación o devolución de tu plata,
  como manda la ley."
- **"Me arrepentí. ¿Puedo devolverlo?"** → "Tienes 10 días desde que lo
  recibes para retractarte, sin preguntas. Coordinamos el retiro y te
  devolvemos lo pagado."

### 1.6 Pie de página

- Menú con las políticas (garantía, cambios y retracto, despacho y pago
  contra entrega, privacidad) — las respuestas de la FAQ deben calzar con lo
  que digan esas políticas, no prometer de más.
- Texto del pie: "Compra confirmada. CompAI responde."

## 1.7 Página de producto (plantilla de producto)

- **Burbuja de confianza bajo el botón de compra:** en la plantilla de
  producto, agrega un bloque de **texto** (o HTML personalizado) justo bajo
  los botones, dentro de una sección o bloque con la clase
  `.compai-promesas` (misma mecánica de `shopify-tema-compai.md` §4). El
  contenido es UNA lista con UNA sola viñeta, con saltos de línea internos:
  - "Stock confirmado con el proveedor antes de cobrarte.
    Paga al recibir, si prefieres. Seguimiento real de tu despacho.
    Garantía legal de 6 meses y 10 días para retractarte.
    **Compra confirmada. CompAI responde.**"
- **Estado de disponibilidad:** Temas → ⋯ → *Editar contenido del tema
  predeterminado*, buscar el texto de "Disponible / In stock" y reemplazar
  por: "Disponible — confirmamos con el proveedor antes de cobrar."
- **Al final de la plantilla:** repetir la sección de las cinco promesas
  (idéntica a 1.2). Nada más entre la galería y la FAQ del pie: la PDP de A
  es sobria a propósito.
- Orden de imágenes por producto: ver la guía de fotografía
  (`direccion-arte-tienda.md` §2); mientras solo haya fotos de proveedor,
  publicarlas ya retocadas sobre crema, nunca el recorte blanco original.

---

## 2. La dosis de C dentro de A (desde el día uno)

El ADN de «Conversación abierta» vive exactamente en tres lugares:

1. **Las cinco promesas en burbujas** (home 1.2 + final de PDP) — burbuja
   con doble check verde.
2. **La burbuja única de la PDP** (1.7) — burbuja con doble check, pegada a
   la decisión de compra.
3. **La FAQ en primera persona de CompAI** (1.5) — la única aparición
   conversacional extra: CompAI habla ("te devolvemos la plata"), pero en
   filas contraíbles normales, **sin** burbujas ni doble check. La voz sí;
   el disfraz no.

**Regla de la voz** (para cualquier sección futura): CompAI habla en primera
persona SOLO cuando responde una preocupación del cliente con un compromiso
verificable. Nunca para vender, describir productos, saludar ni celebrar.

**Regla del doble check:** acompaña únicamente compromisos cumplibles (las
promesas y el cierre de la burbuja PDP). Jamás en títulos, ofertas,
decoración ni iconografía de secciones. **Máximo un elemento con doble check
visible por pantalla.** Si una idea nueva pide burbuja "porque se ve bonito",
la respuesta es no: cada uso decorativo le roba significado al que está al
lado del botón de compra.

---

## 3. Hoja de ruta hacia C completa: "la página como un gran agente"

C madura = la página no *parece* un agente: *es la interfaz* de los agentes
que ya existen en el sistema. Para eso, hitos en orden:

1. **Fotos propias de los 4 SKUs** (guía §2 del doc de dirección). Al
   cumplirse, migrar el hero de A al de B («El mesón de la casa») — mismo
   esqueleto, cambia el hero. Este es el paso intermedio ya aprobado.
2. **Canal conversacional real y respondido**: WhatsApp del negocio con
   respuesta garantizada (humano u agente) en horario declarado. Sin esto,
   cualquier "pregúntame" en la página es la peor traición posible a la
   marca: prometer conversación y no contestar.
3. **Datos de confirmación expuestos**: que el gateway publique señales
   reales de los agentes de verificación (p. ej. "última confirmación de
   stock de este producto: hoy 10:42"). Es la munición honesta de C — datos
   vivos reales. Si el dato no existe o falla, la sección no se muestra;
   nunca se simula. Un contador inventado convertiría a CompAI exactamente
   en lo que promete no ser.
4. **Prueba social real**: ~50 ventas entregadas con seguimiento cumplido y
   permiso escrito de clientes para citar sus mensajes.

**Cuándo:** estrenar C primero como landing de campaña (lanzamiento oficial
o hito de ventas), medible contra la home A/B — señal de éxito definida
antes: tasa de conversión y de rebote de la landing vs. la home actual. Solo
si gana, se convierte en home.

**La home C madura, sección a sección:**
- Hero-diálogo: burbuja del cliente escéptico ("¿Otra tienda que cobra y
  desaparece?") y respuesta CompAI con doble check; botón "Pregúntame" que
  abre el WhatsApp real.
- Cinta de datos vivos del sistema (confirmaciones de stock del día), solo
  con datos reales.
- Productos con foto propia en contexto y su dato útil verificado.
- Las cinco promesas, intactas: siguen siendo el clímax.
- Testimonios reales presentados como hilos de chat, con permiso.
- FAQ conversacional que desemboca en el canal real.

**Riesgos que siguen vigentes** (los mismos de la propuesta original): si
todo es burbuja, el doble check se devalúa — las reglas de §2 aplican
también en C; y un chat visible sin respuesta detrás, o un dato vivo
simulado, destruyen el único activo de la marca. C se gana con los hitos 2 y
3; sin ellos, es gimmick.
