# Modo artesanal — CompAI v0 sin infraestructura

Estado: **este es el modo operativo activo**. El stack (Shopify + agentes +
VPS) está terminado y **apagado** hasta que haya demanda probada y costo por
conversación medido. Ver `deploy-production.md` para reencenderlo.

El objetivo de este documento no es "vender online". Es responder una sola
pregunta con datos reales en vez de supuestos: **¿alguien paga por esto y a
qué costo de esfuerzo?** Todo lo demás se decide después de esa respuesta.

---

## 1. La restricción que define el diseño

Capital de trabajo disponible: **$0 de gasto nuevo**. La caja disponible es
colchón operativo, no inventario, y no se toca.

Eso elimina el modelo clásico de dropshipping chileno, donde compras al
mayorista y luego cobras. Aquí el orden se invierte: **el cliente financia la
compra al mayorista**.

De ahí sale la única fórmula que importa en este modo:

```
abono_mínimo_% = costo_mayorista / precio_venta
```

Con costo $30.000 y precio $40.000 → **75%**. Cualquier abono igual o mayor
al 75% paga la compra al mayorista sin tocar la caja. El 25% restante se cobra
contra entrega y es margen puro.

Consecuencias directas:

- **No se acepta pago 100% contra entrega.** Es la contradicción que se
  detectó en las promesas: exige comprar antes de cobrar, o sea capital que
  no existe. Por eso la promesa (b) cambia (§5).
- **No se usa Mercado Libre en el v0.** ML libera el dinero *después* de la
  entrega y cobra ~14% de comisión. Ambas cosas rompen la fórmula: tendrías
  que comprar al mayorista con caja propia y esperar. ML entra cuando haya
  colchón, no antes.
- Los canales válidos son los que permiten **cobro directo antes de
  despachar**: Facebook Marketplace, Yapo, Instagram, WhatsApp. Comisión 0%.

---

## 2. Criterios de selección de SKU

El margen objetivo subió de $3.000 a **$8.000–$12.000 por venta**, en pesos
absolutos, no en porcentaje. Un producto de $8.000 con 60% de margen deja
$4.800 y consume el mismo tiempo de atención que uno que deja $11.000.

Un SKU entra al catálogo solo si cumple **los seis** criterios:

| # | Criterio | Por qué |
|---|---|---|
| 1 | Margen bruto ≥ $8.000 absolutos | Bajo eso el tiempo por venta no se paga |
| 2 | Precio de venta $25.000–$70.000 | Bajo $25.000 no cabe el margen; sobre $70.000 nadie transfiere por adelantado a un desconocido |
| 3 | Abono mínimo ≤ 80% del precio | Si el costo es >80% del precio el margen es demasiado fino para absorber una devolución |
| 4 | Tasa de falla baja: sin electrónica compleja, sin motores, no frágil | La garantía legal de 6 meses (Ley 19.496, art. 20–21) la respondes **tú**. Una devolución te borra el margen de 4 ventas |
| 5 | Mayorista con retiro presencial en Santiago y stock verificable el mismo día | Retiro presencial = flete de entrada $0 y confirmación de stock real, que es la promesa (a) hecha a mano |
| 6 | Sin marca registrada ni réplicas | Vender réplicas te expone personalmente; no hay sociedad detrás |

### Lo que el criterio 4 descarta del catálogo actual

Los cuatro SKU de `db/seed.sql` son datos de prueba con proveedores
`.example`, pero como perfil de producto sirven de ejemplo:

- Freidora de aire, aspiradora robot, audífonos inalámbricos → **descartados
  por el criterio 4**. Electrónica con motor o batería: tasa de falla alta y
  garantía de 6 meses a tu costo.
- Lámpara LED $12.990 → **descartada por el criterio 1**: $6.490 de margen.

Familias que sí cumplen el perfil (**hipótesis a validar con cotización
real, no dato**): textil de hogar de gama media (ropa de cama, toallas),
mochilas y bolsos, camas y accesorios de mascotas, organización y almacenaje,
herramienta manual. Cero electrónica en el v0.

### Entregable de esta sección

Una planilla con **5 a 8 SKU** y estas columnas, llenada con cotizaciones
reales de mayoristas (Patronato, Meiggs, Franklin):

```
SKU | Producto | Mayorista | Costo | Precio venta | Margen $ | Abono mín % | Flete salida | Margen neto
```

`Margen neto = Precio − Costo − Flete salida`. Si el margen neto de un SKU
baja de $8.000, sale de la lista. Sin excepciones: la excepción es
exactamente cómo se llega otra vez a $3.000 por venta.

---

## 3. Aritmética honesta del mes

El primer mes hay una tentación aritmética que hay que nombrar para
descartarla: dividir la meta de ingresos por el margen unitario y tomar el
resultado como plan. A $10.000 de margen neto, una meta de $700.000 son 70
ventas — 2,6 al día, todos los días, partiendo de cero reputación. **No
ocurre en el mes 1.** Ningún canal sin reseñas convierte a ese ritmo.

La meta del mes 1 no es un monto. Es **cerrar 10 ventas**. Diez ventas dan el
único dato que se necesita para decidir: costo de esfuerzo por venta, tasa de
respuesta a la objeción del abono, y tasa de devolución. Con eso se sabe si
escalar a 40 tiene sentido, o si el modelo no da.

Corolario importante: **este proyecto no es la solución de caja de corto
plazo**, y tratarlo como tal lleva a la peor decisión posible — bajar el
margen para vender más rápido, que es exactamente cómo se vuelve a $3.000 por
venta y a un negocio que no existe.

---

## 4. La objeción real: pedir transferencia anticipada

Es el patrón exacto de la estafa de Marketplace. La objeción no es un detalle
de copy, es **el producto**. Mitigaciones que cuestan $0:

1. **Perfil personal con historial**, no una página recién creada. La
   antigüedad de la cuenta es la señal más barata que tienes.
2. **Videollamada de 30 segundos** si el cliente la pide. Convierte a un
   desconocido en una persona.
3. **Entrega presencial en punto público** para Santiago. El abono cubre la
   compra al mayorista; el saldo se paga en la mano. El cliente arriesga solo
   el abono, no el total.
4. **Comprobante de compra al mayorista** enviado por WhatsApp el mismo día,
   con el plazo por escrito.
5. **Garantía de 6 meses por escrito** en el chat. Es obligación legal de
   todas formas: decirlo explícito es gratis y desarma la objeción.

Limitación que hay que declarar y no esconder: **mientras no haya inicio de
actividades en el SII, no hay boleta**. Si un cliente la pide, la respuesta es
que no se emite y se le ofrece devolver el abono. Prometer una boleta que no
existe es lo único de esta lista que sí destruye el negocio.

---

## 5. Cambio en las promesas

La promesa (b) pasa de **"pago contra entrega"** a **abono + saldo**:

| Antes | Ahora |
|---|---|
| "Paga al recibir si prefieres" | "Reservas con un abono y pagas el saldo al recibir" |

Las otras cuatro promesas se mantienen intactas y **siguen siendo reglas
duras en la base** (`trg_pago_requiere_stock`, `trg_entrega_activa_garantia`,
`trg_retracto_dentro_de_plazo`). En modo artesanal se cumplen a mano:

- (a) Stock confirmado antes de cobrar → llamas al mayorista **antes** de
  pedir el abono. No después.
- (c) Seguimiento → número de seguimiento de Starken/Chilexpress por WhatsApp
  el mismo día del despacho.
- (d) Garantía 6 meses → declarada por escrito en el chat.
- (e) Retracto 10 días → si lo pide dentro de plazo, se devuelve. Contabiliza
  la devolución en la planilla; es el dato que dice si el SKU sirve.

Reintroducir el contra entrega puro requiere colchón de capital de trabajo, no
una decisión de copy.

---

## 6. Guion de WhatsApp

Cinco momentos. El tiempo de respuesta al primer mensaje es lo que decide la
venta en Marketplace: bajo 5 minutos o se pierde.

### 6.1 Primer contacto

> Hola, sí, tengo disponible. Te confirmo con mi proveedor el stock exacto y
> te aviso en unos minutos — no te pido nada hasta tenerlo confirmado.
> ¿Es para Santiago o despacho a región?

Nunca cotizar antes de confirmar stock. Es la promesa (a) y además evita
prometer algo que no puedes cumplir.

### 6.2 Stock confirmado — la cotización

> Listo, confirmado: queda stock. El total es $XX.XXX
> [+ $X.XXX de despacho a <comuna>].
>
> Cómo funciona: reservas con $XX.XXX (que es lo que pago yo al proveedor hoy
> mismo) y el saldo de $XX.XXX lo pagas al recibirlo. Te mando el comprobante
> de la compra apenas la hago.

El abono se justifica solo, sin pedir confianza: es transparente sobre para
qué es la plata.

### 6.3 La objeción (aparecerá en la mayoría de los chats)

> Te entiendo perfecto, es lo que yo también preguntaría. Mira:
> — Mi perfil tiene <N> años, puedes revisar mi historial.
> — Si estás en Santiago, te lo entrego en persona en <punto público> y ahí
>   pagas el saldo.
> — Apenas hago la compra te mando la foto del comprobante.
> — Y tienes 6 meses de garantía legal y 10 días para arrepentirte.
>
> Si aun así prefieres no arriesgar, lo entiendo y no hay problema.

La última línea importa. Cerrar a presión a alguien que desconfía produce la
devolución que te borra el margen de cuatro ventas.

### 6.4 Post-abono, mismo día

> Recibido, gracias. Acá va el comprobante de la compra al proveedor.
> Lo retiro el <día> y te llega el <fecha>. Te mando el seguimiento apenas lo
> despache.

Plazo por escrito, siempre. Un plazo incumplido y no avisado es la causa #1
de reclamo en SERNAC.

### 6.5 Post-entrega

> ¿Todo bien con el pedido? Recuerda que tiene 6 meses de garantía; si algo
> falla me escribes directo a mí y lo resuelvo.
>
> Si quedaste conforme, ¿me dejarías una reseña en mi perfil? Es lo que me
> permite seguir vendiendo.

La reseña es el activo que hace que el próximo cliente no discuta el abono.
Es el único "marketing" del v0.

---

## 7. Qué se mide (y por qué esto conecta con el stack apagado)

Una planilla, una fila por conversación:

```
Fecha | Canal | SKU | ¿Cotizó? | ¿Abonó? | Minutos de atención |
Margen neto | ¿Devolución? | Motivo de caída
```

Dos números salen de ahí y son los que deciden el futuro del proyecto:

- **Minutos de atención por venta cerrada.** Es el equivalente artesanal del
  costo por token del agents-service. Si cerrar una venta cuesta 90 minutos,
  ningún agente de IA la va a cerrar barato tampoco: el problema no es la
  automatización, es la fricción del pago anticipado.
- **Motivo de caída más frecuente.** Si la mayoría cae en la objeción del
  abono, el problema es el modelo de pago y automatizarlo no lo arregla. Si
  cae en precio, el problema es la selección de SKU.

Cuando se encienda el stack, esa planilla es la línea base contra la que se
compara el costo por token en `agent_actions`. Sin ella, el número de los
agentes no significa nada porque no hay con qué compararlo.

---

## 8. Criterio de reencendido

El stack Shopify + agentes se reenciende (~$52.000/mes de costo fijo) solo
cuando se cumplan **las tres**:

1. 10 ventas cerradas en modo artesanal.
2. Margen neto promedio ≥ $8.000.
3. Ingreso mensual ≥ $500.000 sostenido, que es también el umbral acordado
   para reevaluar INAPI.

Antes de eso, cada peso de infraestructura sale de una caja que no lo tiene.
