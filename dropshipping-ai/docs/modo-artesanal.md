# Modo artesanal — CompAI v0 sin infraestructura

Estado: **este es el modo operativo activo**. El stack (Shopify + agentes +
VPS) está terminado y **apagado** hasta que haya demanda probada y costo por
conversación medido. Ver `deploy-production.md` para reencenderlo.

El objetivo de este documento no es "vender online". Es responder una sola
pregunta con datos reales en vez de supuestos: **¿alguien paga por esto y a
qué costo de esfuerzo?** Todo lo demás se decide después de esa respuesta.

Este documento define **qué** es el negocio. El orden de ejecución y las puertas
de decisión del mes 1 están en `hoja-de-ruta-mes-1.md`.

Base de proveedores: `asistente-administrativo/gestion/dropshipping-por-encargo/directorio-proveedores.md`
(~95 mayoristas reales, eje Meiggs / Estación Central, muchos en Yollgo).
Operación desde **Santiago**, con retiro presencial disponible.

---

## 1. Capital de trabajo y exposición máxima

Hay capital de trabajo acotado, **sin tomar crédito nuevo**. Eso cambia el
diseño respecto de la versión anterior de este documento: el cliente ya no
tiene que financiar la compra al mayorista, así que **el pago contra entrega
vuelve a estar disponible** (§4). Era la única razón por la que se había
eliminado.

Pero capital acotado no es capital libre. Dos reglas lo gobiernan.

**Regla de unidades en tránsito.** El capital fija cuántos pedidos puedes
tener comprados y no cobrados al mismo tiempo:

```
unidades_en_tránsito_máx = capital_de_trabajo / costo_unitario_promedio
```

Ese número es el techo real de ventas simultáneas. Si es 20 y vendes 25 en una
semana, las últimas 5 esperan — o se ofrecen con abono, que libera caja de
inmediato.

**Regla de exposición por SKU.** Comprar en profundidad antes de vender es
como se pierde el capital. La escalera:

| Paso | Compra | Cuándo |
|---|---|---|
| 1. Muestra | 1 unidad | Antes de publicar. Para fotos reales y para **verificar calidad con el producto en la mano** |
| 2. Por encargo | 1 unidad por pedido | Desde la publicación hasta la primera venta cerrada |
| 3. Profundidad | 3–5 unidades | Solo después de **2 ventas cerradas** del mismo SKU |

Ningún SKU salta pasos, y ninguno concentra más de **1/4 del capital**. Un SKU
que se veía obvio y no rota es exactamente lo que inmoviliza la caja.

La muestra del paso 1 no es un gasto opcional: en Marketplace la foto real es
lo que convierte, y tener la unidad en la mano es lo único que te dice si el
producto aguanta los 6 meses de garantía legal que respondes tú.

---

## 2. Criterios de selección de SKU

El margen objetivo subió de $3.000 a **$8.000–$12.000 por venta**, en pesos
absolutos, no en porcentaje. Un producto de $8.000 con 60% de margen deja
$4.800 y consume el mismo tiempo de atención que uno que deja $11.000.

Un SKU entra al catálogo solo si cumple **los seis** criterios:

| # | Criterio | Por qué |
|---|---|---|
| 1 | Margen neto ≥ $8.000 absolutos | Bajo eso el tiempo por venta no se paga |
| 2 | ~~Precio de venta $25.000–$70.000~~ **Sin piso de precio. Techo $70.000** | **Corregido 2026-08-05 con datos reales.** El piso salía de asumir costo ≈ 50-60% del precio. En los mayoristas del directorio el costo real es **25-30%** del precio de calle, así que un ticket de $17.000 deja $12.000 de margen. Manda el criterio 1, no el precio |
| 3 | Rota: producto con demanda visible en Marketplace hoy | La rotación es lo que protege el capital inmovilizado (§1) |
| 4 | Sin electrónica ni productos eléctricos | La garantía legal de 6 meses (Ley 19.496, art. 20–21) la respondes tú; y los eléctricos requieren **certificación SEC**, según la opinión legal de LAI-er |
| 5 | Mayorista con despacho directo al cliente final, **o** retiro presencial en Meiggs | El despacho directo elimina manipuleo; el retiro presencial te deja revisar calidad antes de despachar. Ambos sirven, por razones distintas |
| 6 | Sin marca registrada ni réplicas | Vender réplicas te expone personalmente; no hay sociedad detrás |

### El catálogo anterior no pasa estos criterios

`asistente-comercial/veredictos/dropshipping-por-encargo/01-tabla-margenes.md`
tiene 10 productos armados bajo la regla vieja de $3.000, con tickets de
$9.990 a $19.990. Contra los criterios de arriba **caen los 10**: el mejor es
la mopa giratoria, con ~$8.000 estimados sobre un ticket de $19.990 — bajo el
piso de precio del criterio 2 y sin holgura en el 1.

No hay que recotizarlos. Hay que **reemplazarlos** por SKU de otro nicho y
otro ticket. Los cinco de la tabla que sí siguen sirviendo son las reglas de
envío, no los productos.

### Nichos candidatos, con proveedores ya identificados

Hipótesis a validar con cotización real, no dato. Los proveedores salen del
directorio:

| Nicho | Por qué encaja | Proveedores del directorio |
|---|---|---|
| Bolsos, carteras y mochilas | Ticket alto, cero electrónica, no frágil | Yonglong, Baodelai, Amanda Fashion, Carteras Colorina |
| Textil de hogar | Ticket medio-alto, tasa de falla casi nula | Ilahui, Mundo Toallas, Super Linda, Doral |
| Mascotas | **Nicho de recompra** — el mismo cliente vuelve | Pet Baby, Huanyu, Mondo Mascotas, Duo Mai |
| Accesorios de tecnología **no eléctricos** | Ticket alto, sin exposición SEC | Munditel, Andoom, Supermak *(solo no eléctricos)* |

Mascotas merece atención especial: es el único con recompra natural, y la
recompra es lo que hace que el costo de conseguir al cliente se pague dos
veces. GAIn ya lo había marcado como candidato futuro; con ticket más alto
pasa a ser candidato inmediato.

### Primer dato real: PETBABY, bolsos de transporte (2026-08-05)

Costos leídos en Yollgo (tienda 5151, categoría `042_00E`) contra precios
observados en Mercado Libre el mismo día:

| Producto | SKU | Medida | Costo | Precio de mercado | Margen |
|---|---|---|---|---|---|
| Bolso de viaje S | PBB-54420 | 24×34 cm | $4.990 | $14.990–$16.990 | $10.000–$12.000 |
| Bolso de viaje M | PBB-54419 | 26×42 cm | $5.500 | $17.989–$19.890 | $12.500–$14.400 |
| Bolso de viaje L | PBB-54418 | 28×49 cm | $5.990 | $19.890–$21.548 | $13.900–$15.600 |
| Bolso reforzado | PBB-54416+ | — | $8.990 | $24.990 | ~$16.000 |

Los cuatro pasan el criterio 1 con holgura, y **ninguno alcanzaba el piso de
precio del criterio 2 original** — de ahí la corrección.

Dos hallazgos que cambian la operación:

1. **Se vende por caja, no por unidad.** El listado marca `10u/c` y la
   etiqueta `20/CAJA`. No se puede comprar 1, así que la escalera del §1 no se
   puede recorrer: se entra directo al paso 3. Lo que la hace tolerable es el
   monto — una caja de 10 del M son $55.000, una fracción del capital.
   **Confirmar la mínima real con el proveedor antes de comprometer.**
2. **El volumen no es problema en esta categoría.** Son bolsos blandos y
   plegables de 24 a 49 cm. El riesgo de flete que motivaba pedir medidas
   aplica a cuchas y rascadores, no a esto.

Advertencia sobre el canal: sobre estos precios, la comisión de Mercado Libre
(~14%) más el envío gratis obligatorio dejan el margen cerca de **$7.000**,
bajo el objetivo. En Facebook Marketplace con envío por pagar el margen queda
íntegro. **Marketplace primero; ML solo con el precio ajustado al alza.**

### Comparación de los cuatro proveedores, mismo producto (2026-08-05)

Transportador blando de mascota, leído en Yollgo:

| Proveedor | Rango de precio | Empaque | Mínimo real en $ |
|---|---|---|---|
| **Mondo Mascota** (3183) | $3.900 – $57.000 (30 modelos) | **1u/c — por unidad** | **$3.900** |
| PETBABY (5151) | $4.990 – $8.990 | 10u/c | $49.900 |
| HUANYU / PETSHOW (2625) | $4.000 – $20.000; coches $39.000–$49.990 | 6, 10 o 12u/c según modelo | $24.000 – $66.000 |
| DUO MAI (2577) | no cargó | — | pedidos por WeChat |

El mismo transportador talla M cuesta **$5.500 en los tres**. Lo que cambia no
es el precio, es el mínimo: en Mondo compras 1 por $5.500; en PETBABY compras
10 por $55.000; en Huanyu 12 por $66.000.

**Mondo Mascota es el proveedor de arranque**, por dos razones independientes:

1. **Vende por unidad.** Es el único que permite recorrer la escalera del §1
   —muestra, por encargo, profundidad— en vez de saltar directo al paso 3.
2. **Tiene los consumibles.** Su catálogo (60+ categorías, con traducción al
   español) incluye bolsas para fecas, arena, antipulgas, higiene y snacks.
   Es el único que sostiene la tesis de recompra por sí solo.

PETBABY y Huanyu quedan para **profundidad**: cuando un SKU ya vendió y se
justifica comprar la caja, ahí su precio por unidad es competitivo y el
mínimo deja de ser un problema. Huanyu además tiene coches de paseo a
$39.000–$49.990 por unidad, una categoría de ticket alto que los otros no
tienen.

Notas de terreno: PETBABY está en Bascuñán Guerrero 260 local 1 y Huanyu en
Conferencia 265 — ambos con retiro presencial en el eje Meiggs. Mondo y Duo
Mai toman pedidos por WeChat, no por la app. Huanyu avisa que el descuento
por efectivo vale solo dentro del mes. La app muestra los precios de Huanyu
con símbolo `€`; son pesos.

### Mondo Mascota: camas y consumibles (2026-08-05)

Todo `1u/c`. Costos leídos en Yollgo, tienda 3183.

**Camas** (categoría `007`) — $3.000 a $23.000. La línea de felpa escala
limpio por tamaño y es la más fácil de publicar como familia:

| Producto | Costo |
|---|---|
| Cama de felpa 40 cm | $3.000 |
| Cama de felpa 50 cm | $4.400 |
| Cama de felpa 60 cm (F6711) | $5.900 |
| Cama de felpa 70 cm (F6711) | $7.500 |
| Cama de felpa 80 cm (F6711) | $9.000 |
| Cama de felpa 100 cm (F6711) | $13.900 |
| Cama redonda grande 70 cm | $10.000 |
| Cama sofá con respaldo L 60×40 | $11.500 |
| Cama iglú | $17.000 |
| Cama cuadrada peluda M/L | $18.900 |
| Set de 3 camas cuadradas | $23.000 |

**Consumibles** (categoría `024`, bolsas y palas) — el ticket es bajo, como
estaba previsto:

| Producto | Costo | Empaque |
|---|---|---|
| Bolsas para fecas 4 un. | $420 | 12u/c |
| Bolsas para fecas 6 un. | $610 | 12u/c |
| Bolsas para fecas 10 un. | $1.150 | 12u/c |
| Dispensador + rollo | $380 | 12u/c |
| Porta bolsas | $950 – $1.650 | 6–12u/c |
| Bolsas biodegradables, 5 rollos | $2.990 | 3u/c |
| Pala recoge fecas plegable 45–80 cm | $2.150 – $5.600 | 1–3u/c |
| Baño ecológico perro chico | $5.500 | 1u/c |
| Baño ecológico perro mediano/grande | $12.000 | 1u/c |

**Confirmado el diagnóstico del nicho:** ningún consumible pasa el filtro de
$8.000 por sí solo. Una bolsa de $420 vendida a $1.500 deja $1.080. Sirven
únicamente como **segunda compra del mismo cliente** —sin costo de
adquisición— y conviene venderlos en pack, no sueltos.

La excepción son los baños ecológicos: a $12.000 de costo son durables de
ticket alto, no consumibles, y entran al catálogo principal.

#### Camas: el margen baja cuando sube el tamaño

Precios de mercado leídos en Mercado Libre el 2026-08-05: 60 cm
$16.990–$29.980 · 80 cm $12.984 · 90 cm $15.972 · 100 cm $16.983 · 110 cm
$18.700–$29.680.

**El precio de mercado casi no escala con el tamaño, pero el costo sí.**
Cruzado con los costos de Mondo, el resultado es contraintuitivo:

| Cama de felpa | Costo | Mercado | Margen | Veredicto |
|---|---|---|---|---|
| 60 cm | $5.900 | $16.990 | $11.090 | **PASA** |
| 70 cm | $7.500 | ~$17.000 | $9.500 | **PASA** |
| 80 cm | $9.000 | $12.984 | $3.984 | FUERA |
| 100 cm | $13.900 | $16.983 | $3.083 | FUERA |

Las camas grandes son lo peor del catálogo: cuestan casi el triple y se venden
casi al mismo precio. Y las que sí sirven —60 y 70 cm— son además las que no
dan problema de flete. Los dos criterios apuntan al mismo lado.

**Hallazgo de posicionamiento:** lo que sostiene el precio no es el tamaño,
es la palabra **"antiestrés"**. Una cama de 60 cm publicada así se vende entre
$16.990 y $29.980; la misma superficie publicada como "cama de felpa" cae a
$10.300. Es el mismo producto de Mondo: cambia el título de la publicación,
no el costo. Esto vale para todo el catálogo — el título es una variable de
margen, no de estética.

**Pendiente:** las categorías de snacks y antipulgas de Mondo, que se
cortaron por inestabilidad de la app.

### Medio de pago para el contra entrega: Klap

Evaluado el 2026-08-05. Tarifas publicadas, vigentes desde el 12-01-2026:

| Medio | Comisión | Sobre una venta de $19.900 |
|---|---|---|
| Débito | $78 + 0,62% + IVA | **~$239** |
| Prepago | $78 + 1,06% + IVA | ~$322 |
| Crédito | $78 + 1,39% + IVA | ~$422 |

Abono en 1 día hábil. Tarjetas internacionales 2,88% + 0,0083 UF + IVA.

Encaja exactamente con el contra entrega en RM del §4: cobras con tarjeta al
entregar, el dinero llega al día siguiente, y el costo es **~2% del margen**
—contra el ~14% de Mercado Libre, que son $2.786 sobre la misma venta—.
Además elimina el manejo de efectivo y desarma la objeción de estafa mejor
que cualquier argumento, porque el cliente paga cuando tiene el producto en la
mano y con su propia tarjeta.

#### Resuelto el 2026-08-05: el bloqueante no es Klap, es el SII

No se pudo preguntar a Klap directamente —su sitio devuelve errores de
plantilla, la FAQ da 404 y la página de comercios responde 403— pero la
respuesta está documentada públicamente:

1. **Klap por sí solo no exige inicio de actividades.** Afilia a persona
   natural mayor de 18 años con cédula vigente, además de personas jurídicas.
2. **La normativa sí lo exige.** Desde el **2 de enero de 2026**, los
   comercios que venden a través de plataformas de pago electrónico deben
   tener inicio de actividades formalizado.
3. **Toda venta con tarjeta se informa al SII.** Klap y el resto de las
   empresas de medios de pago están obligadas a reportar las ventas con
   débito, crédito y prepago.

Consecuencia: **el bloqueante deja de ser Klap y pasa a ser la consulta a la
AFC** sobre si iniciar actividades afecta el seguro de cesantía. Y no aplica
solo a Klap: alcanza a cualquier plataforma de pago electrónico, Mercado Pago
incluido.

Fuera de ese perímetro quedan el **efectivo** y la **transferencia bancaria
directa**, que son justamente los dos medios con los que opera el v0. El
catálogo y las publicaciones no dependen de esta consulta; solo depende de
ella la mejora de cobrar con tarjeta.

Confianza: media-alta. Son fuentes secundarias, no la página oficial de Klap,
que no fue accesible. Confirmar en el contact center **600 363 2020** con una
pregunta concreta: *"¿pueden afiliar a una persona natural sin inicio de
actividades, y qué informan al SII?"*

### Entregable de esta sección

Planilla con **5 a 8 SKU** cotizados de verdad:

```
SKU | Producto | Mayorista | ¿Despacha directo? | Costo | Precio venta |
Margen neto | Paso de compra (1/2/3)
```

`Margen neto = Precio − Costo` cuando el envío va **por pagar** (el cliente lo
paga al recibir, que es el default y no toca tu margen). Si asumes el envío,
réstalo. Bajo $8.000 el SKU sale de la lista, sin excepciones: la excepción es
exactamente cómo se vuelve a $3.000 por venta.

---

## 3. Aritmética del mes 1

Hay una tentación aritmética que conviene nombrar para descartarla: dividir la
meta de ingresos por el margen unitario y tomar el resultado como plan. A
$10.000 de margen, una meta de $700.000 son 70 ventas — 2,6 al día, todos los
días, partiendo de cero reseñas. **No ocurre en el mes 1.**

La meta del mes 1 no es un monto. Es **cerrar 10 ventas**. Diez ventas dan el
único dato que se necesita para decidir: costo de esfuerzo por venta, tasa de
rechazo en contra entrega, y tasa de devolución. Con eso se sabe si escalar a
40 tiene sentido, o si el modelo no da.

Corolario: **este proyecto no es la solución de caja de corto plazo**, y
tratarlo como tal lleva a la peor decisión posible — bajar el margen para
vender más rápido, que es cómo se vuelve a $3.000 por venta y a un negocio que
no existe.

---

## 4. Forma de pago: contra entrega en RM, abono fuera de RM

El contra entrega es la palanca de conversión más fuerte del Marketplace
chileno, y con capital de trabajo es viable. Pero no es gratis: un pedido
rechazado en la entrega te cuesta el flete de ida y vuelta más el capital
inmovilizado, y con $10.000 de margen eso se lleva el margen de dos ventas
buenas. Por eso se ofrece con criterio, no como default universal:

| Destino | Forma de pago | Por qué |
|---|---|---|
| Región Metropolitana | **Contra entrega**, incluso en mano | Puedes entregar tú y verificar. Riesgo de rechazo bajo y recuperable |
| Regiones | **Abono + saldo al recibir** | Un rechazo a región es flete doble y el producto vuelve en días |

El abono para regiones se calcula así:

```
abono_mínimo_% = costo_mayorista / precio_venta
```

Con costo $30.000 y precio $40.000 → 75%. Cualquier abono igual o mayor cubre
la compra al proveedor sin tocar el capital, que queda libre para los pedidos
de RM en contra entrega.

**Mercado Libre vuelve a ser viable.** Se había descartado por su ciclo de
pago diferido, que solo era problema sin colchón. Con capital, su comisión
(~14%) es el costo real a evaluar: sobre un ticket de $40.000 son $5.600, que
se come más de la mitad del margen objetivo. Entra solo con SKU cuyo margen
neto lo aguante, o con precio ajustado al alza para ese canal.

### La objeción de siempre

"¿Cómo sé que no es estafa?" es el producto, no un detalle de copy. En RM la
respuesta es directa y desarma sola: **contra entrega, pagas cuando lo tienes
en la mano**. Fuera de RM hay que trabajarla — perfil con historial,
comprobante de compra al mayorista por WhatsApp, videollamada si la piden, y
la garantía de 6 meses por escrito.

Limitación que se declara y no se esconde: mientras no haya inicio de
actividades en el SII, **no hay boleta**. Si un cliente la pide, se le dice que
no se emite y se le ofrece devolver el abono. Prometer una boleta que no existe
es lo único de esta lista que sí destruye el negocio.

---

## 5. Estado de las cinco promesas

Las cinco siguen siendo reglas duras de la base
(`trg_pago_requiere_stock`, `trg_entrega_activa_garantia`,
`trg_retracto_dentro_de_plazo`). En modo artesanal se cumplen a mano:

| | Promesa | Cómo se cumple sin infraestructura |
|---|---|---|
| (a) | Stock confirmado antes de cobrar | Llamas al mayorista **antes** de pedir el pago. No después |
| (b) | Pago al recibir | Contra entrega en RM; abono + saldo a regiones (§4) |
| (c) | Seguimiento en tiempo real | Código de Starken/Chilexpress por WhatsApp el mismo día del despacho |
| (d) | Garantía legal 6 meses | Declarada por escrito en el chat. El criterio 4 de SKU es lo que la hace sostenible |
| (e) | Retracto 10 días | Si lo pide en plazo, se devuelve. Se anota en la planilla: es el dato que dice si el SKU sirve |

La promesa (b) se enuncia como **"Paga al recibir en la Región
Metropolitana"**. Precisa y cumplible: prometer contra entrega a todo Chile es
prometer algo que el capital no aguanta.

---

## 6. Guion de WhatsApp

El kit palabra por palabra está en
`asistente-creativo/ideas/dropshipping-por-encargo/kit-de-venta.md` y sigue
vigente, incluida su regla de oro: **responder en menos de 10 minutos**. En
Marketplace la velocidad es la venta.

Tres ajustes sobre ese kit:

1. **§2, primer mensaje:** ofrecer contra entrega solo si la comuna es de RM.
   Preguntar la comuna *antes* de ofrecer la forma de pago, no después.
2. **§3, confirmación de stock:** para regiones, reemplazar "si prefieres
   transferencia" por el abono con su monto explícito y la frase que lo
   justifica — *"es lo que le pago al proveedor hoy mismo"*.
3. **§1, mensaje al proveedor:** la lista de 10 productos de hogar quedó
   obsoleta (§2). Reemplazarla por los nichos y el rango de precio nuevos, y
   mantener las dos preguntas que sí importan: **¿despachan directo al cliente
   final?** y **¿puedo usar sus fotos?**

---

## 7. Qué se mide (y por qué conecta con el stack apagado)

Una planilla, una fila por conversación:

```
Fecha | Canal | SKU | ¿Cotizó? | ¿Pagó? | Forma de pago | Minutos de atención |
Margen neto | ¿Rechazo en entrega? | ¿Devolución? | Motivo de caída
```

Tres números salen de ahí y deciden el futuro del proyecto:

- **Minutos de atención por venta cerrada.** Es el equivalente artesanal del
  costo por token del agents-service. Si cerrar una venta cuesta 90 minutos,
  ningún agente de IA la va a cerrar barato tampoco: el problema no sería la
  automatización sino la fricción del proceso.
- **Tasa de rechazo en contra entrega.** Es el costo real de la promesa (b) y
  lo que dice si el contra entrega se extiende a regiones o no.
- **Motivo de caída más frecuente.** Si cae en precio, el problema es la
  selección de SKU. Si cae en confianza, el problema es el canal.

Cuando se encienda el stack, esa planilla es la línea base contra la que se
compara el costo por token en `agent_actions`. Sin ella el número de los
agentes no significa nada, porque no hay con qué compararlo.

---

## 8. Criterio de reencendido

El stack Shopify + agentes se reenciende (~$52.000/mes de costo fijo) solo
cuando se cumplan **las tres**:

1. 10 ventas cerradas en modo artesanal.
2. Margen neto promedio ≥ $8.000.
3. Ingreso mensual ≥ $500.000 sostenido, que es también el umbral acordado
   para reevaluar INAPI.
