# compai.cl — resuelto el 2026-08-20

**`https://compai.cl` está en línea**, sirviendo la página de servicio desde
GitHub Pages. El repo es `Sebahttps/CompAI` (público, rama `main`, raíz), y la
fuente de la página vive en `kri-eit/sitio-compai/`.

## Qué se cambió en Cloudflare

Los valores anteriores quedan escritos por si alguna vez hay que volver atrás.

| Registro | Antes | Ahora |
|---|---|---|
| `compai.cl` A | `23.227.38.65` (Shopify) | **cuatro registros**: `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
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

**Los cuatro A, no uno.** Al principio se dejó solo `185.199.108.153` y GitHub
no emitía el certificado. La documentación de GitHub Pages exige los cuatro para
un dominio raíz; con uno solo la verificación queda a medias. **Y los cuatro en
Solo DNS**: uno quedó por error con el proxy naranja encendido, que es
exactamente lo que impide a GitHub validar el dominio.

## Pendiente: el certificado HTTPS

**`http://compai.cl` responde 200 y sirve la página.** Lo que falta es el
certificado: GitHub sigue presentando su comodín `*.github.io`, que no cubre
`compai.cl`, así que `https://` da error de confianza. La API reporta
`https_certificate: null`.

No queda nada que arreglar en el DNS — ya está en la configuración documentada.
**GitHub declara hasta 24 horas** para emitir el certificado de un dominio
propio, y el reloj partió cuando el DNS quedó correcto. Se forzó dos veces la
reverificación reescribiendo el dominio por API.

Si persiste: en *Settings → Pages* del repo, borrar el dominio personalizado,
guardar, volver a escribirlo y guardar. Eso fuerza a GitHub a re-verificar el
DNS y pedir un certificado nuevo que cubra ápice y `www`.

**Cuando el certificado aparezca**, activar *Enforce HTTPS* en *Settings →
Pages*. Hasta entonces la página se ve por `http://` sin problema; lo único que
no se debe hacer es forzar HTTPS antes de que el certificado exista, porque eso
deja el sitio inaccesible en vez de solo sin cifrar.

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
