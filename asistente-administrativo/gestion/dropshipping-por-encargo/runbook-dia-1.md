# AdmAIn — Runbook del Día 1 (ejecutar y marcar)

**Fecha de ejecución:** ___ · **Reescrito 2026-08-08** para el modo artesanal y
el nicho mascotas. Todo el material ya existe; este es el orden.

> **Qué cambió.** La versión del 19-07 mandaba a registrarse en Dropi y publicar
> los 10 productos de hogar. Ese catálogo cae completo contra los criterios
> nuevos (`dropshipping-ai/docs/modo-artesanal.md` §2). El plan vigente es: un
> proveedor (**Mondo Mascota**), cinco SKU de mascotas, publicación de a uno.

## Antes de empezar: lo que este Día 1 NO es

No es un día de publicar. Es el día de **conseguir el producto en la mano**. Las
publicaciones necesitan fotos reales, y las fotos necesitan las muestras. El
orden importa: invertirlo produce anuncios con foto de catálogo, que es
exactamente lo que Marketplace penaliza y lo que hace que parezcas reventa.

## Mañana (1 hora — costo $0)

| ✔ | Paso | Material |
|---|---|---|
| ☐ | **Enviar el pedido a Mondo Mascota por WhatsApp** (+56 9 2092 9197) con los 5 pantallazos | §"El mensaje", abajo |
| ☑ | ~~Cotizar a los 4 proveedores del nicho~~ — **cerrado 11-08**: Mondo es el proveedor, sin compra mínima, precios de Yollgo | `catalogo-yollgo-verificado.md` |
| ☑ | WhatsApp Business — **ya existe**. Ajustar el nombre comercial a **"Sebastián — Al Tiro Store"** y cargar las respuestas rápidas | `kit-de-venta.md` §2-6 |
| ☐ | Crear las dos planillas en Google Sheets (ver abajo) | — |

### El mensaje para pedir las muestras

Adjuntar los **5 pantallazos** del producto y enviar:

```
Hola! Quiero hacer un pedido de 5 productos, 1 unidad de cada uno.
Le adjunto las capturas:

1161 · Transportador talla S — $4.500
1162 · Transportador talla M — $5.500
1163 · Transportador talla L — $6.500
X02062 · Cama de felpa 60 cm — $5.900
X02063 · Cama de felpa 70 cm — $7.500

Total: $29.900

¿Me confirma los precios y si están disponibles?
Paso a retirar a Sazié 2998.
```

Por qué está redactado así:

- **"1 unidad de cada uno" va primero.** Es el punto exacto donde aparece un
  mínimo si existe. Que salga en el mensaje y no en el mesón.
- **Los precios van explícitos.** Si su lista dice otra cosa, se sabe antes de
  pagar. Ya se comprobó que hay productos de nombre parecido al doble de precio
  en la misma categoría.
- **El código antes del nombre.** Pantallazo + código no deja margen a que
  preparen otro producto.

**Segundo mensaje — enviar recién cuando confirmen el pedido, no antes:**

```
Una consulta aparte: para pedidos futuros, ¿ustedes despachan
directo al cliente final o siempre hay que retirar?
```

Va separado a propósito: es la última pregunta abierta con el proveedor y decide
si hay que manipular producto en cada venta. Mezclarla con el primer pedido
expone a que contesten solo una de las dos.

**Las dos planillas, y por qué son dos:**

1. **Caja** — `fecha · SKU · canal · ingreso · costo · envío · margen`.
   Es la que dice si ganas plata.
2. **Conversaciones** — `fecha · canal · SKU · ¿cotizó? · ¿pagó? · forma de pago ·
   minutos de atención · margen · ¿rechazo en entrega? · ¿devolución? · motivo de
   caída`. Es la que decide el futuro del proyecto: sin ella no hay con qué
   comparar el costo por token cuando se encienda el stack
   (`modo-artesanal.md` §7).

## Mediodía (2-3 horas — costo $29.900)

Ir a Meiggs con la lista. **Retiro presencial: revisar calidad antes de pagar** —
es lo que hace sostenible la garantía de 6 meses que respondes tú.

| ✔ | SKU | Producto | **Código** | Costo |
|---|---|---|---|---|
| ☐ | X-BOLSO-S | Transportador talla S | `1161` | $4.500 |
| ☐ | X-BOLSO-M | Transportador talla M | `1162` | $5.500 |
| ☐ | X-BOLSO-L | Transportador talla L | `1163` | $6.500 |
| ☐ | F6711-60 | Cama de felpa 60 cm | `X02062` | $5.900 |
| ☐ | F6711-70 | Cama de felpa 70 cm | `X02063` | $7.500 |
| | | | **Total** | **$29.900** |

**Pedir por código, nunca por nombre.** "Arenero grande" son cuatro productos
distintos entre $6.300 y $14.500; el mismo riesgo existe en transportadores y
camas, donde hay más de 20 variantes por categoría.

| ✔ | Paso |
|---|---|
| ☐ | Guardar captura/boleta de cada compra en la carpeta `proveedores/` |
| ☐ | Anotar el costo REAL pagado (puede diferir del leído en Yollgo) |
| ☐ | **Verificar que no exijan mínimo al pedir una unidad.** Confirmaron que no hay, pero la planilla marca 50u/caja en transportadores y 30u/caja en camas. Si aparece un mínimo, **parar y recalcular** antes de comprar |

## Tarde (2 horas — costo $0)

| ✔ | Paso | Material |
|---|---|---|
| ☐ | Tomar las **5 fotos por producto**: producto solo, con escala, detalle de material, en uso, plegado | `publicaciones-mascotas-v0.md` §3 |
| ☐ | Publicar **UN** anuncio: el **transportador M** ($18.990, margen $13.490) | idem §2.4 |
| ☐ | Dejar los guiones a mano en atajos de WhatsApp Business | `kit-de-venta.md` §2-6 |

**Uno, no cinco.** Marketplace ordena por recencia: publicar de a uno durante
cinco días mantiene el perfil activo y te dice cuál genera consultas antes de
invertir tiempo en el resto.

## Días 2 a 5

Un SKU por día, en este orden: transportador **M** (día 1) → **L** → cama
**60 cm** → transportador **S** → cama **70 cm**.

Ojo con la cama de 70 cm: su precio de $19.990 es **interpolado, no observado**.
Si en una semana no genera consultas, bajar a $17.990 (margen $10.490, sigue
pasando el criterio).

## Todo el día, todos los días

- Responder en **<10 min** con los guiones.
- **Preguntar la comuna antes de ofrecer forma de pago.** Contra entrega solo RM.
- Confirmar stock ANTES de aceptar cualquier pago.
- Comprar al proveedor el MISMO día de cada pago.
- **No prometer boleta.** No hay inicio de actividades en el SII.

## Noche (10 minutos — sagrado)

| ✔ | Paso |
|---|---|
| ☐ | Anotar en la planilla: vistas, consultas, ventas, margen del día |
| ☐ | Anotar **minutos de atención** por conversación — es el número que más importa |
| ☐ | Reportar al estudio → GAIn decide el día siguiente |

## Meta y criterio de corte

La meta del mes 1 **no es un monto: son 10 ventas cerradas**. Ese es el dato que
permite decidir si el modelo da. Ver `modo-artesanal.md` §3 y §8.

Fechas y revisiones: `checklist-y-fechas.md`.
