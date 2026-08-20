# compai.cl — resuelto el 2026-08-20

**`https://compai.cl` está en línea**, sirviendo la página de servicio desde
GitHub Pages. El repo es `Sebahttps/CompAI` (público, rama `main`, raíz), y la
fuente de la página vive en `kri-eit/sitio-compai/`.

## Qué se cambió en Cloudflare

Los valores anteriores quedan escritos por si alguna vez hay que volver atrás.

| Registro | Antes | Ahora |
|---|---|---|
| `compai.cl` A | `23.227.38.65` (Shopify) | `185.199.108.153` (GitHub Pages) |
| `compai.cl` AAAA | `2620:127:f00f:5::` (Shopify) | `2606:50c0:8000::153` (GitHub Pages) |
| `www.compai.cl` CNAME | `shops.myshopify.com` | `sebahttps.github.io` |

**Lo que NO se tocó, a propósito:** el registro `MX → smtp.google.com` y los
tres `TXT` (SPF, DMARC y verificación de Google). Ese MX es lo que hace existir
`stapiamena@compai.cl`, que está impreso en la carátula de oferta, la ficha de
empresa, las plantillas comerciales y la firma de correo. Tocarlo por descuido
deja a la empresa sin correo el mismo día que lo repartió en todos lados.

Todo quedó en **Solo DNS** (nube gris), igual que `regalon`. Con el proxy
naranja activo desde el principio, GitHub a veces no logra emitir su
certificado y el sitio queda con error de TLS sin causa aparente.

## Pendiente menor: el certificado de `www`

`https://compai.cl` responde 200. `https://www.compai.cl` todavía falla el TLS
porque GitHub aún no emite el certificado que cubre el subdominio — al 20-ago la
API reporta `https_certificate: null`. Suele resolverse solo en menos de una
hora desde que el DNS apunta bien.

Si persiste: en *Settings → Pages* del repo, borrar el dominio personalizado,
guardar, volver a escribirlo y guardar. Eso fuerza a GitHub a re-verificar el
DNS y pedir un certificado nuevo que cubra ápice y `www`.

**No es urgente.** El dominio impreso en todos los documentos es `compai.cl`,
sin `www`.

## ⚠️ Lo que hay que hacer el día que se destruya el VPS

`api.compai.cl`, `hola.compai.cl` y `panel.compai.cl` siguen apuntando a
**`64.176.23.118`**. Cuando la instancia se destruya, Vultr libera esa IP y se
la asigna a otro cliente.

**Esos tres registros se borran en el mismo momento en que se destruya la
instancia, no después.** Si quedan, apuntan a un servidor ajeno: quien reciba
esa IP puede levantar lo que quiera y para el mundo sería un subdominio de
CompAI, con su certificado y todo. Es un secuestro de subdominio por *dangling
DNS*, y el costo de evitarlo son tres clics.

## Lo que esta página no resuelve

**Quitarle el dominio a Shopify no cancela el plan de Shopify.** La tienda dejó
de ser alcanzable desde `compai.cl`, pero la facturación sigue corriendo por su
lado — y la promo de US$1/mes se acaba alrededor del 1-nov, cuando el plan
Básico salta a ~US$39. Eso se cierra en el panel de Shopify, no acá.
