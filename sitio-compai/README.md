# sitio-compai

La página de servicio de `compai.cl`. Una sola página, un solo archivo.

`index.html` **se genera**: no editarlo a mano, se pisa. Editar `_construir.py`
y correrlo:

```
python sitio-compai/_construir.py
```

## Por qué una página y no un sitio

El dominio ya sale impreso en la carátula de oferta, la ficha de empresa, las
tres plantillas comerciales, la firma de correo y las tarjetas. Lo único que
esta página tiene que lograr es que **el comprador público que lea `compai.cl`
al pie de una cotización y escriba la dirección encuentre lo que esperaba
encontrar**. Nada más. Un dominio sin página se lee como empresa nueva; uno que
lleva a otro negocio se lee como que algo raro pasa.

## Cero dependencias externas

Ni webfonts, ni CDN, ni imágenes sueltas: el logotipo va incrustado como SVG en
curvas y las tipografías son de sistema. Son 13 KB en un archivo. Carga igual de
rápido en la red de un municipio que en fibra, y no hay nada que se pueda caer.

Va en la paleta **nocturna**, que es donde el logotipo nació. Es el único
soporte donde puede ir así: los documentos que se imprimen usan la diurna,
porque el comprador público imprime en blanco y negro.

## El teléfono no se versiona

`TELEFONO` está vacío en `_construir.py` a propósito — este repo es público. Se
completa antes de construir y se deja en blanco al guardar. Si queda vacío, el
pie sale solo con el correo, que es una degradación aceptable.

## Lo que falta para que esté en línea

1. **La raíz de `compai.cl` la ocupa Shopify hoy** (`23.227.38.65`), y `www`
   apunta a `shops.myshopify.com`. Hay que moverlos.
2. Publicar por **GitHub Pages**, igual que `regalon.compai.cl`. Es gratis y no
   depende del VPS — eso importa, porque el VPS se está apagando.
3. En Cloudflare, apuntar la raíz a GitHub Pages. Cloudflare aplana CNAME en el
   ápice, así que no hace falta poner las cuatro IP a mano.

**Quitar el dominio de Shopify no cancela el plan de Shopify.** Son dos cosas
distintas y la facturación sigue corriendo por su lado.
