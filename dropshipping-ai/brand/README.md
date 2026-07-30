# Marca CompAI

Cuatro piezas en SVG. El **doble check** es el eje de la identidad: aparece en
el logotipo, en el isotipo y en las cinco promesas de la tienda. Repetir la
misma forma en los tres sitios es lo que la vuelve reconocible.

| Archivo | Uso | Tamaño mínimo |
|---|---|---|
| `logo-compai.svg` | Encabezado, facturas, firma de correo | 120 px de ancho |
| `logo-compai-noche.svg` | Redes, portadas, fondos oscuros | 120 px de ancho |
| `isotipo-compai.svg` | Avatar, app, sello | 24 px |
| `favicon.svg` | Pestaña del navegador | 16 px |

`favicon.svg` está copiado como `app/icon.svg` en la tienda y en el dashboard;
Next.js lo publica solo, sin configuración.

## Paleta

| Color | Hex | Rol | Contraste sobre papel |
|---|---|---|---|
| Cobre | `#a2551f` | Acento de marca, las versalitas | 5,26:1 |
| Verde confirmación | `#15734a` | **Solo** el doble check | 5,66:1 |
| Tinta | `#1c1917` | Texto principal | 15,65:1 |
| Crema | `#f7f2e6` | Plano de página | — |
| Papel | `#fdfbf4` | Tarjetas y superficies | — |
| Cobre nocturno | `#d98a4e` | Acento sobre fondo oscuro | 6,09:1 |

El verde está reservado al doble check y no se usa como color decorativo. Esa
restricción es la que hace que, cuando aparece, signifique algo.

## Por qué el resplandor es cobre y no neón

La versión nocturna usa **cobre incandescente, no neón frío**. Un cian o un
magenta traerían la estética que usan las tiendas de dropshipping fraudulentas,
que es exactamente aquello de lo que esta marca se diferencia: su único
argumento es que al cliente no lo van a estafar. El cobre caliente lee como
metal y brasa — llamativo sin sonar a estafa.

## Decisiones técnicas

- **Las versalitas de `AI` se resuelven con mayúscula a menor tamaño**, no con
  `font-variant-caps`. El soporte de esa propiedad es irregular en visores SVG y
  en el editor de temas de Shopify; así el resultado es idéntico en todas partes.
- **La burbuja del isotipo va rellena, no perfilada.** A tamaños chicos un
  contorno fino se rompe; el relleno mantiene legible el significado.
- **El favicon no es el isotipo reescalado.** La burbuja ocupa casi todo el
  lienzo y el trazo es más grueso: a 16 px el margen generoso del isotipo se
  pierde. Se cambia elegancia por legibilidad.
- **El centrado del check está calculado, no ajustado a ojo** (desviación de
  0,01 unidades sobre un lienzo de 64).

## ⚠️ Antes de subir los logotipos a Shopify

Los dos logotipos usan **texto en vivo** con la tipografía del sistema, la misma
que la tienda. Eso los mantiene nítidos y editables, pero se dibujan con la
fuente de cada dispositivo: en un equipo sin esa familia, la marca cambia de
forma.

Para el archivo definitivo hay que **convertir el texto a curvas** en Figma,
Illustrator o Inkscape (*Texto → Contornear*) y guardar como SVG.

El isotipo y el favicon no tienen ese problema: son geometría pura y sirven
tal cual.
