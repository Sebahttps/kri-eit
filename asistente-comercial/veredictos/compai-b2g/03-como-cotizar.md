# Cómo elegir qué cotizar

Operativo. Sale de los datos del 4-ago-2026, no de teoría.

## La demanda es amplia y delgada

**168 órdenes del rubro en un día, repartidas entre 145 unidades compradoras
distintas.** Solo 19 unidades compraron más de una vez el mismo día.

**Consecuencia táctica: no hay clientes que cultivar.** No existe el municipio
que compre tóner todas las semanas y al que convenga visitar. Hay 145 compradores
distintos que aparecen una vez y desaparecen. La única forma de agarrar esa
demanda es que el sistema avise — por eso los 85 rubros cargados en la unidad de
venta son la infraestructura del negocio, no un trámite.

## Los tres filtros, antes de mirar el precio

| # | Filtro | Por qué |
|---|---|---|
| 1 | **Máximo 3 líneas** | La orden de Reicol tenía 39 líneas por $197.753: **$5.071 netos por línea**. Cotizar 39 ítems y comprarlos en 39 lugares es margen negativo con cualquier valoración de la hora propia |
| 2 | **Comprador en la RM, o producto sin bulto** | 12 de 15 compradores de la muestra están fuera de la RM. El flete se come el margen de una orden chica |
| 3 | **Especificación con marca y modelo** | Si dice "según anexo adjunto" o describe un servicio, no se puede calcular el costo. Y donde no se puede calcular, se pierde plata |

Una orden que pasa los tres se cotiza en 15 minutos. Una que no, no se cotiza.
No es pereza: es que el tiempo por cotización es el costo real del negocio.

## Antes de poner un precio: mirar qué se adjudicó antes

Esto es lo que separa adivinar de cotizar. **Los precios adjudicados son
públicos** y se consultan sin registrarse:

```
https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json
    ?fecha=DDMMAAAA&ticket=<TICKET>
```

Devuelve todas las órdenes del día. Las de Compra Ágil terminan en **`-AG26`**.
Con el código de una orden se pide el detalle:

```
    ?codigo=1057439-4227-AG26&ticket=<TICKET>
```

y ahí viene lo que importa: `Items.Listado[].PrecioNeto` es el **precio unitario
neto adjudicado**, junto con `EspecificacionComprador`, el proveedor que ganó y
el organismo que compró.

**Buscar dos o tres adjudicaciones del mismo producto antes de ofertar** dice a
qué precio se está ganando. Es la diferencia entre ofertar con dato y ofertar con
esperanza.

*Ojo:* la API pública limita las peticiones por minuto y devuelve **429** si se
la apura. Bajar el listado del día una vez, guardarlo, y trabajar sobre el
archivo.

## Dónde está el margen, según los datos

**Sí:** licencias de software y consumibles con código de parte. Cero flete, cero
bulto, especificación exacta, y el cálculo del costo es una búsqueda.

**No:**

- **Órdenes de picking** — muchas líneas de artículos baratos y distintos.
- **Arriendo de equipos** — es comprar inventario y financiarlo a 12 meses.
- **Reventa de equipamiento de marca** — el caso del All-in-One: se adjudicó
  31 % bajo el precio de vitrina **con licencias incluidas**. Ahí el margen sale
  de importar, no de vender.
- **Servicio técnico fuera de la RM** — quien gana está en la ciudad. Es un
  negocio de radio de 30 km.

## La regla que ordena todo

**No se cotiza lo que no se puede costear.** Si no se sabe a cuánto se compra,
no hay oferta: hay una apuesta. Y una oferta en Mercado Público **obliga** — si
se adjudica y no se puede entregar, el problema no es el margen, es la sanción
en el Registro de Proveedores.
