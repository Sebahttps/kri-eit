# Traspaso a sesión local (Claude Code en el PC de Sebastián)

Contexto para la sesión de Claude Code corriendo localmente en Windows.
Este documento resume el estado del proyecto y las misiones pendientes que
requieren acceso de red o al PC del usuario (la sesión remota en la nube
tiene bloqueados los dominios de Shopify y Cloudflare).

## Estado actual (2026-07-31)

- **Sistema completo en `main`**: BD con triggers de las 5 promesas, agentes
  (FastAPI+LangGraph), gateway (NestJS), dashboard y tienda propia (Next.js),
  compose de producción endurecido + Caddy, cloud-init para VPS, y **conector
  Shopify** (webhook orders/create con HMAC, cancelación sin stock, sync de
  tracking) probado E2E 7/7. Ver `docs/shopify-hybrid.md` y
  `docs/deploy-production.md`.
  **Ojo**: el arreglo de la llave SSH en el cloud-init (`8ad86ac`) está en la
  rama de trabajo, **no en `main`**. Hasta que se mergee, un servidor nuevo
  creado desde `main` volvería a nacer sin llave.
- **Modo elegido**: híbrido — Shopify como vitrina/checkout, agentes como
  back-office.
- **PR #14 abierto** (borrador): `scripts/configure-shopify.ps1` — el usuario
  intentó ejecutarlo pegándolo por partes en la consola y falló por inputs
  (dominio incompleto, token mal pegado). El script en sí no tiene errores
  conocidos; falta una ejecución limpia como archivo.
- **Tienda Shopify**: creada, plan Básico (promo US$1/mes x3 meses). Falta la
  app del Dev Dashboard; scopes necesarios: read/write de orders, fulfillments
  **y products** (products lo usa el script que crea el catálogo).
  **Corregido 2026-07-28**: no existe token `shpat_` para apps nuevas — la app
  entrega Client ID + Client Secret y el gateway los canjea por un token de
  24 h. El código, el script y `docs/shopify-hybrid.md` ya reflejan esto.
- **Marca decidida**: **CompAI** (tienda B2C). `compai.cl` (principal) ya está
  inscrito en NIC Chile y delegado a Cloudflare; `compay.cl` (redirect) sigue
  sin inscribir. Tagline: "Te confirmamos el stock, pagas al recibir y la garantía
  responde. Palabra de CompAI." Identidad: base crema, verde confirmación,
  acento cobre; logotipo "comp" minúscula + "AI" versalitas cobre; elemento
  firma: burbuja-WhatsApp con doble check verde por promesa cumplida.
- **VPS**: **desplegado y accesible**. Vultr Santiago, 2 vCPU / 4 GB,
  `64.176.23.118`, Ubuntu 24.04.4, aprovisionado con `infra/cloud-init.yml`.
  Se entra con `ssh -i C:\Users\sebas\.ssh\id_ed25519 root@64.176.23.118`.
  Falta solo correr `dropship-setup` (detalle en el punto 4).
- **DNS**: `compai.cl` inscrito en NIC Chile y delegado a Cloudflare. Los tres
  registros A del VPS creados y propagados. Detalle en el punto 2.

## Misiones para la sesión local (en orden)

1. **Configurar Shopify**: crear la app en `dev.shopify.com/dashboard` **desde
   la organización dueña de la tienda** (requisito del client credentials
   grant), instalarla, y ejecutar `dropshipping-ai/scripts/configure-shopify.ps1`
   (o hacer lo equivalente por API directamente). El usuario ingresa dominio,
   Client ID y Client Secret; verificar que los 4 productos quedaron creados
   (SKUs ME-001, ME-002, IS-101, IS-205 — deben coincidir con `db/seed.sql`).
   El webhook ya **no** hay que omitirlo: el VPS existe y `api.compai.cl`
   resuelve. Pero apunta a él solo después de `dropship-setup`, o los primeros
   envíos de Shopify llegarán a un puerto cerrado.
2. **Cloudflare: HECHO 2026-07-31.** La zona `compai.cl` está activa y el
   dominio quedó inscrito en NIC Chile y delegado (`aarav` y
   `sierra.ns.cloudflare.com`). Estado de los 7 registros, todos en
   **DNS-only / nube gris**:

   | Nombre | Tipo | Contenido | Para qué |
   |---|---|---|---|
   | `compai.cl` | A | `23.227.38.65` | Shopify |
   | `compai.cl` | AAAA | `2620:127:f00f:5::` | Shopify (IPv6) |
   | `www` | CNAME | `shops.myshopify.com` | Shopify |
   | `0c6208a9-…` | CNAME | `dns-verification.shop…` | verificación de Shopify |
   | `hola` | A | `64.176.23.118` | VPS — tienda propia |
   | `panel` | A | `64.176.23.118` | VPS — dashboard |
   | `api` | A | `64.176.23.118` | VPS — gateway |

   Los subdominios del VPS son `hola`, `panel` y `api` — **no `tienda`**, que
   es como los nombraba antes este documento: la tienda real vive en la raíz
   (Shopify) y `tienda.` para el canal secundario confunde. Los tres deben
   quedar en nube gris o Caddy no puede completar el desafío HTTP-01.

   El AAAA de la raíz existe aunque `docs/dns-cloudflare.md` lo da por omitido
   por defecto; la dirección es la de Shopify, así que se dejó como está.

   Se hizo por el panel, no con `scripts/configure-cloudflare.ps1`. El script
   sigue siendo válido y es idempotente; sirve para `compay.cl`.
3. **Renombrar a CompAI**: ~~repo~~ **hecho 2026-07-28** — `apps/store` con
   identidad completa (crema/cobre/verde, logotipo `comp`+`ai` en versalitas,
   burbujas con doble check) y `apps/dashboard` con nombre y base crema,
   conservando la paleta de series de los gráficos. Contrastes verificados.
   **Pendiente del usuario**: nombre visible de la tienda Shopify
   (Configuración → General) y aplicar `docs/shopify-tema-compai.md` en el
   editor del tema (Horizon 4.1.3): colores, logotipo y `brand/shopify-custom.css`.
   Los assets de marca están en `brand/` (ver su README).
4. **VPS: APROVISIONADO 2026-07-31.** Falta un solo paso: `dropship-setup`.
   - IP `64.176.23.118`, Vultr **Santiago**, Cloud Compute 2 vCPU / 4 GB,
     Ubuntu 24.04.4. Latencia desde Chile: **7 ms**.
   - Acceso: `ssh -i C:\Users\sebas\.ssh\id_ed25519 root@64.176.23.118`.
   - Verificado tras el aprovisionamiento: cloud-init `done` sin errores,
     Docker 29.7.1 + Compose v5.3.1, repo en `/opt/kri-eit` (`main`), swap de
     4 GB con `swappiness=10`, `.env.prod` en `600 root` con `POSTGRES_PASSWORD`
     y `BUSINESS_JWT_SECRET` generados, y `ufw` activo con 22/80/443.

   **Por qué estuvo bloqueado un día** (vale la pena no repetirlo): el campo
   Cloud-Init User-Data del panel contenía solo el texto `compai.prod` — el
   `cloud-init.yml` nunca se pegó ahí. Y ese archivo tampoco instalaba ninguna
   llave. Los dos intentos con la contraseña de root habrían fallado igual.
   Corregido en `infra/cloud-init.yml` (commit `8ad86ac`), que ahora instala la
   llave como primer paso de `runcmd`.

   **Lección sobre Vultr**: las llaves SSH solo se inyectan al desplegar.
   Después, toda vía del panel para añadirlas —incluida *Reinstall SSH Keys*—
   **borra el disco**. La llave tiene que ir en el cloud-init desde el inicio.
   El desbloqueo fue: pegar el cloud-init completo en User-Data → Settings →
   Change OS → Ubuntu 24.04, que consume el user-data al arrancar. La IP se
   conserva.

   **Siguiente paso — lo corre el usuario**, porque pide secretos:

   ```
   ssh -i C:\Users\sebas\.ssh\id_ed25519 root@64.176.23.118 -t dropship-setup
   ```

   El `-t` es necesario: el script usa `read -rsp` y sin TTY no funciona.
   Respuestas: clave de Anthropic, `hola.compai.cl`, `panel.compai.cl`,
   `api.compai.cl`, ACME `stapiamena@gmail.com`, más el correo y la contraseña
   del Supervisor (mínimo 12 caracteres). **No reutilizar la contraseña del
   seed**: su hash está publicado en el repo (ver `docs/deploy-production.md`).
   Tarda varios minutos —construye cuatro imágenes— y para eso está el swap.

   - Luego: variables `SHOPIFY_*` en `.env.prod` (`SHOPIFY_CLIENT_ID`,
     `SHOPIFY_CLIENT_SECRET`, webhook secret = el mismo Client Secret), crear
     el webhook re-ejecutando el script del punto 1, y la prueba E2E de
     `docs/shopify-hybrid.md`.
   - Mantención de Vultr: lunes 2026-08-03, 15:00 UTC (11:00 en Chile).
5. Pendientes manuales del usuario que conviene recordarle: activar COD
   (Configuración → Pagos → Métodos de pago manuales), fotos/tema de la
   tienda, y solicitud de marca mixta CompAI en INAPI (la raíz "comp-" está
   saturada en clase 35).

## Reglas de trabajo

- Secretos (tokens Shopify/Cloudflare, contraseñas): el usuario los ingresa
  localmente; NUNCA commitearlos ni pegarlos en chats. `.env*` está en
  `.gitignore`.
- Desarrollar en la rama `claude/dropshipping-ai-agents-system-cqtygt`
  (recrearla desde `main` si su PR fue mergeado), commits descriptivos, PR
  para revisión del usuario.
- La contraseña del Supervisor del dashboard no está en el repo (solo su
  hash en `db/seed.sql`); el usuario la tiene.
