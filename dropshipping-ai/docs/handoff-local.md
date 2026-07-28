# Traspaso a sesión local (Claude Code en el PC de Sebastián)

Contexto para la sesión de Claude Code corriendo localmente en Windows.
Este documento resume el estado del proyecto y las misiones pendientes que
requieren acceso de red o al PC del usuario (la sesión remota en la nube
tiene bloqueados los dominios de Shopify y Cloudflare).

## Estado actual (2026-07-28)

- **Sistema completo en `main`**: BD con triggers de las 5 promesas, agentes
  (FastAPI+LangGraph), gateway (NestJS), dashboard y tienda propia (Next.js),
  compose de producción endurecido + Caddy, cloud-init para VPS, y **conector
  Shopify** (webhook orders/create con HMAC, cancelación sin stock, sync de
  tracking) probado E2E 7/7. Ver `docs/shopify-hybrid.md` y
  `docs/deploy-production.md`.
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
- **Marca decidida**: **CompAI** (tienda B2C). Dominios `compai.cl` (principal)
  y `compay.cl` (redirect) — en proceso de inscripción en NIC Chile por el
  usuario. Tagline: "Te confirmamos el stock, pagas al recibir y la garantía
  responde. Palabra de CompAI." Identidad: base crema, verde confirmación,
  acento cobre; logotipo "comp" minúscula + "AI" versalitas cobre; elemento
  firma: burbuja-WhatsApp con doble check verde por promesa cumplida.
- **VPS**: aún no contratado. Plan recomendado: Vultr región Santiago,
  4 GB / 2 vCPU, Ubuntu 24.04, aprovisionado con `infra/cloud-init.yml`.

## Misiones para la sesión local (en orden)

1. **Configurar Shopify**: crear la app en `dev.shopify.com/dashboard` **desde
   la organización dueña de la tienda** (requisito del client credentials
   grant), instalarla, y ejecutar `dropshipping-ai/scripts/configure-shopify.ps1`
   (o hacer lo equivalente por API directamente). El usuario ingresa dominio,
   Client ID y Client Secret; verificar que los 4 productos quedaron creados
   (SKUs ME-001, ME-002, IS-101, IS-205 — deben coincidir con `db/seed.sql`).
   OMITIR el webhook hasta que el VPS exista.
2. **Cloudflare**: configurar la zona `compai.cl` con
   `scripts/configure-cloudflare.ps1` (requiere un API token del usuario con
   Zone:Edit + DNS:Edit). Ver `docs/dns-cloudflare.md`.
   **Corregido 2026-07-28**: `compai.cl` **NO está inscrito** en NIC Chile
   (WHOIS: "Nombre de dominio no existe"), pese a lo que decía este handoff.
   Como NIC Chile pide los nameservers durante la inscripción, el orden es:
   crear la zona en Cloudflare primero → inscribir en NIC Chile con esos NS →
   registros A al final. Los A (`tienda`, `panel`, `api` → IP del VPS) van en
   modo DNS-only/nube gris porque Caddy emite el TLS.
3. **Renombrar a CompAI**: ~~repo~~ **hecho 2026-07-28** — `apps/store` con
   identidad completa (crema/cobre/verde, logotipo `comp`+`ai` en versalitas,
   burbujas con doble check) y `apps/dashboard` con nombre y base crema,
   conservando la paleta de series de los gráficos. Contrastes verificados.
   **Pendiente del usuario**: nombre visible de la tienda Shopify
   (Configuración → General).
4. **Cuando el usuario contrate el VPS**: guiarlo con `infra/cloud-init.yml`
   (pegar como user-data), `dropship-setup` por SSH, variables `SHOPIFY_*`
   en `.env.prod` (webhook secret = Client Secret de la app del Dev
   Dashboard), crear el webhook (re-ejecutar el script del punto 1) y correr
   la prueba E2E de `docs/shopify-hybrid.md`.
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
