# La vitrina Regalón se mudó

El `index.html` que vivía en esta carpeta **ya no está aquí**. Se movió el
2026-08-11 a un repositorio propio:

| | |
|---|---|
| **Repositorio** | https://github.com/Sebahttps/regalon |
| **En vivo** | https://regalon.compai.cl |
| **Local** | `C:\Users\sebas\regalon` |

## Por qué se movió

GitHub Pages aplica un dominio propio **a todo el repositorio, no a una
carpeta**. La raíz de `docs/` en `kri-eit` sirve la página del estudio KRI-EIT,
así que apuntar `regalon.compai.cl` aquí habría dejado el dominio mostrando el
estudio y la vitrina colgando de `/tienda-compai/`.

## Por qué no quedó una copia

Porque dos copias del mismo HTML se desincronizan, y la que está en vivo
siempre pierde: se edita la del repo cómodo y el cliente sigue viendo la otra.
**La única versión es la del repositorio `regalon`.** Si hay que cambiar la
vitrina, se cambia allá.

## Lo que sí sigue viviendo en `kri-eit`

Las decisiones que la sostienen, que son de negocio y no de código:

| Qué | Dónde |
|---|---|
| Nombre, arquitectura de marca, por qué Regalón no tiene logo | `asistente-visual/propuestas/dropshipping-por-encargo/arquitectura-de-marca.md` |
| Los 5 SKU con costo, código y piso de margen | `asistente-administrativo/gestion/dropshipping-por-encargo/catalogo-yollgo-verificado.md` |
| Guiones de venta y objeciones | `asistente-creativo/ideas/dropshipping-por-encargo/kit-de-venta.md` |
| Criterios del catálogo y del negocio | `dropshipping-ai/docs/modo-artesanal.md` |

## `docs/tienda/` ya no existe

Hasta el 22-ago-2026 este README decía *"no confundir con `docs/tienda/`, que
es la tienda operativa del estudio"*. **Era falso.** Esa carpeta tenía una copia
vieja de esta misma vitrina —11 KB contra los 31 KB de la buena— con precios
que ya no corrían ($16.990 y $10.300) y sin un solo botón de WhatsApp. Y estaba
**publicada**: `kri-eit` sirve Pages desde `/docs`, así que respondía 200 en
`sebahttps.github.io/kri-eit/tienda/`.

Sobrevivió a la mudanza del 11-ago por el nombre de la carpeta: el puntero
quedó en `docs/tienda-compai/` y el HTML viejo en `docs/tienda/`.

Se borró el 22-ago-2026, junto con el enlace que la página del estudio tenía en
su pie. **Ninguna de las dos vitrinas está en uso por ahora**; la buena sigue
existiendo en su repo y su dominio, sin tocar.
