# Auditoría de márgenes B2G — datos duros

**Fecha:** 2026-08-20 · **Fuente:** API pública de Mercado Público
(`api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json`), órdenes de
compra del **4 de agosto de 2026**. Todo lo de acá es dato publicado, no
estimación.

## 1. El tamaño del canal

| | |
|---|---|
| Órdenes de compra ese día | **12.684** |
| De ellas, Compra Ágil (`-AG26`) | **4.691 · 36 %** |
| Del rubro de CompAI (computación, oficina, educativo) | **180 · 3,84 %** de las ágiles |
| Proyección mensual del rubro (22 días hábiles) | **~3.960 Compras Ágiles** |

Desglose del rubro: computación 95, educativo 46, oficina 39.

**El canal no es el problema.** Hay volumen de sobra.

## 2. El ticket

Sobre 15 órdenes con detalle, 99 líneas de producto:

| | |
|---|---|
| Total por orden — mediana | **$609.161** |
| Rango | $77.091 – $3.000.000 |

Calza con el modelo de GAIn: tickets de $150.000 a $600.000 son el grueso, y un
fondo de $2–4 millones aguanta cuatro a seis órdenes simultáneas.

## 3. El hallazgo que cambia el modelo: buena parte de "computación" NO es venta

De las Compras Ágiles de computación revisadas, la mayoría **no son venta de
equipos**:

| Adjudicado | Qué era realmente |
|---|---|
| $189.000 | Reparación de impresora HP LaserJet 500 M525 + cambio de film y rodillo |
| $142.000 | Reparación de HP 1536dnf MFP + mantención completa |
| $17.500 | Revisión de HP 1102W + actualización de firmware |
| $1.020.000 | **Arriendo** de multifuncional monocromática, 12 meses |
| $39.599 × 12 | **Arriendo** de multifuncional Canon MAXIFY GX6010 |

Eso es **servicio y arriendo, no reventa**. Márgenes muy superiores, pero exige
capacidad técnica y presencia local — no se resuelve con un proveedor mayorista.
El ganador recurrente de las reparaciones es ML COMPUTACIÓN Y TECNOLOGÍA LTDA.

## 4. El margen de la reventa pura: el caso que se pudo verificar

Única línea de la muestra con especificación suficiente para comparar contra
mercado:

> **"COMPUTADOR DE ESCRITORIO ALL IN ONE, procesador i5, disco SSD 500 GB, RAM
> 16 GB, debe incluir licencia Office y Windows Professional"**
> Adjudicado a **$511.900 netos** = **$609.161 con IVA**
> (Logística Integral Express SpA)

Precio de vitrina de un equipo equivalente en Chile, agosto 2026:

| Fuente | Equipo | Precio con IVA |
|---|---|---|
| Pulga | Lenovo AIO i5 / 16 GB / 512 GB (sin teclado ni mouse) | $529.200 |
| Retail de marca (Falabella, Paris, SP Digital) | AIO i5 / 16 GB / 512 GB nuevo | **$700.000 – $880.000** |

**El adjudicatario vendió a $609.161 IVA incluido un equipo cuyo equivalente de
marca cuesta entre $700.000 y $880.000 en vitrina — y encima incluyó licencia de
Office y de Windows Professional**, que por separado suman otros $100.000 o más.

### Qué significa

El margen **no sale de vender bien: sale de comprar barato**. El ganador o
importa, o tiene cuenta de distribuidor con precios muy por debajo del retail, o
usa marca genérica. Un proveedor nuevo que compre en un distribuidor chileno a
precio de lista **pierde plata en esta orden**.

Esto confirma la aritmética del IVA que ya había advertido GAIn: comprar sin
factura es margen negativo, y comprar con factura al 80–90 % del precio de calle
deja un margen de un dígito.

## 5. Quiénes ganan hoy

Nombres que se repiten en la muestra: ML Computación y Tecnología Ltda.,
Servicios Computacionales Global, PCInbox SpA, Importaciones y Servicios
Advanced, Comercial Escarta SpA, Comercializadora Reicol SpA, Logística Integral
Express SpA.

Son **revendedores establecidos y especializados**, varios con "Importaciones" en
la razón social. Ninguno es un recién llegado.

## Lo que esta auditoría NO resolvió

- **Una sola línea comparable.** El resto de las especificaciones remite a
  "anexo adjunto" o describe servicios, que no tienen precio de vitrina.
- **Muestra de un solo día** (4-ago-2026) y 15 órdenes con detalle. La API
  pública limita las peticiones por minuto.
- **No se pudo medir el margen mediano** que pedía la condición de corte. Lo que
  sí se pudo es verificar un caso concreto, y ese caso es desfavorable.

## Nota de método

Se usó el ticket público de pruebas de ChileCompra. Los códigos terminados en
`-AG26` identifican órdenes de Compra Ágil. Datos crudos cacheados durante la
sesión; reproducible con `fecha=DDMMAAAA` y `codigo=` en la misma API.
