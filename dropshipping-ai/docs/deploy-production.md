# Despliegue en producción

Guía para levantar el sistema completo en un VPS con Docker Compose y HTTPS
automático (Caddy + Let's Encrypt). Todo lo que se usa aquí vive en `infra/`:
`docker-compose.prod.yml`, `Caddyfile` y `.env.prod.example`.

## Requisitos

- VPS Linux con **4 GB de RAM** o más, con los puertos **80 y 443** abiertos.
  Recomendado: **Vultr región Santiago** (`vhp-2c-4gb-amd`, ~US$24/mes) — para
  una tienda chilena la latencia local es la diferencia más grande, y ni
  DigitalOcean ni Hetzner tienen presencia en Sudamérica.

  > **Memoria durante el build**: en runtime el stack completo ronda 1 GB, pero
  > `up -d --build` compila cuatro imágenes en paralelo y cada build de Next.js
  > puede pedir 1–2 GB. En 4 GB sin swap el despliegue puede morir con un OOM
  > poco descriptivo. [`infra/cloud-init.yml`](../infra/cloud-init.yml) crea 4 GB
  > de swap (con `vm.swappiness=10`, para que sea red de seguridad y no lastre
  > el runtime). **Si instalas el VPS a mano, crea el swap antes del primer
  > build** o usa un plan de 8 GB.
- **Docker Engine + Docker Compose v2** instalados
  (`curl -fsSL https://get.docker.com | sh`).
- Un dominio con **tres registros A** apuntando a la IP del servidor, p. ej.:
  - `hola.tudominio.cl` → tienda propia (canal secundario; en modo híbrido la
    vitrina pública vive en la raíz del dominio, servida por Shopify)
  - `panel.tudominio.cl` → dashboard del Supervisor
  - `api.tudominio.cl` → gateway de negocio (webhooks de carriers y WebSocket)
- Una clave de la API de Anthropic (para los dos agentes IA).

## Vía rápida: aprovisionamiento automático con cloud-init

Si el VPS aún no existe, la forma más simple es dejar que el propio proveedor
lo configure al crearlo:

1. Al crear el servidor (Ubuntu 24.04), pegar el contenido completo de
   [`infra/cloud-init.yml`](../infra/cloud-init.yml) en el campo
   **User Data / Cloud-Init** del panel del proveedor.
2. Apuntar los 3 registros DNS a la IP asignada.
3. Entrar una única vez por SSH y ejecutar:

   ```bash
   dropship-setup
   ```

   Pide la clave de Anthropic, los 3 dominios y el email ACME; el resto
   (Docker, repo clonado en `/opt/kri-eit`, secretos de Postgres/JWT
   generados, firewall UFW, stack levantado y cron de backups) ya quedó
   hecho por cloud-init.

Con eso el despliegue está completo — las secciones 1 y 2 siguientes son la
alternativa manual, y la sección 3 ("Endurecer") aplica igual en ambos casos.

## 1. Clonar y configurar

```bash
git clone https://github.com/Sebahttps/kri-eit.git
cd kri-eit/dropshipping-ai/infra
cp .env.prod.example .env.prod
```

Editar `.env.prod` y completar todas las variables. Los tres secretos son
obligatorios — el compose se niega a arrancar si falta alguno:

| Variable | Cómo generarla |
|---|---|
| `POSTGRES_PASSWORD` | `openssl rand -hex 24` |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com |
| `BUSINESS_JWT_SECRET` | `openssl rand -hex 32` |
| `STORE_DOMAIN` / `DASHBOARD_DOMAIN` / `API_DOMAIN` | tus subdominios (sin `https://`) |
| `ACME_EMAIL` | email para avisos de Let's Encrypt |

## 2. Levantar

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

La primera vez tarda unos minutos: construye las 4 imágenes, inicializa
PostgreSQL (schema + triggers de las 5 promesas + seeds) y Caddy emite los
certificados HTTPS. Verificar:

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod ps    # todo "Up"
curl -I https://hola.tudominio.cl                                     # 200 con TLS
```

Diferencias con el compose de desarrollo: los secretos no tienen valores por
defecto, y **ningún servicio interno publica puertos** — postgres, redis, la
API de agentes (8000), el gateway (4000) y las dos apps Next solo son
accesibles dentro de la red de Docker; el único punto de entrada es Caddy
(80/443).

## 3. Endurecer antes de recibir tráfico real

### Cambiar la contraseña del Supervisor

El seed crea el supervisor con una contraseña que no está en el repo (solo su
hash bcrypt). Aun así conviene rotarla al desplegar. No hay endpoint de cambio
de contraseña, así que se actualiza directo en la base de datos:

> **El seed deja al Supervisor bloqueado a propósito.** Este repositorio es
> público, y publicar un hash bcrypt real permite descifrarlo sin conexión: sin
> límite de intentos, sin bloqueo y sin dejar rastro. `dropship-setup` pide el
> correo y la contraseña y los aplica, así que **en el camino con cloud-init no
> hay que hacer nada de lo de abajo**. Esto es solo para la instalación manual o
> para rotar la clave más adelante.

```bash
cd kri-eit/dropshipping-ai/infra
DC="docker compose -f docker-compose.prod.yml --env-file .env.prod"

# 1. Generar el hash. La clave va por entorno y no por argumentos: argv es
#    visible en la lista de procesos del host, el entorno del contenedor no.
read -rsp "Nueva contraseña: " PW; echo
HASH=$($DC exec -T -e PW="$PW" business-api \
  node -e "console.log(require('bcryptjs').hashSync(process.env.PW,10))" | tr -d '\r')
unset PW

# 2. Aplicarlo (el id del Supervisor es fijo; el correo puede cambiarse aquí)
$DC exec -T postgres psql -U dropship -d dropship -v ON_ERROR_STOP=1 \
  -c "UPDATE supervisors SET email='tu@correo', password_hash='$HASH'
      WHERE id='00000000-0000-0000-0000-000000000001';"
unset HASH
```

### Backups diarios de PostgreSQL

La base de datos es el corazón del sistema (pedidos, garantías, retractos,
auditoría de los agentes). Programar un dump diario:

```bash
crontab -e
# Todos los días a las 03:30, conservando 14 días:
30 3 * * * cd /ruta/a/kri-eit/dropshipping-ai/infra && docker compose -f docker-compose.prod.yml --env-file .env.prod exec -T postgres pg_dump -U dropship dropship | gzip > /var/backups/dropship-$(date +\%F).sql.gz && find /var/backups -name 'dropship-*.sql.gz' -mtime +14 -delete
```

Idealmente, copiar además los dumps fuera del servidor (rclone a S3/Backblaze).

### Datos reales en vez de seeds

- **No aplicar `db/seed-demo.sql`** en producción: son 30 días de datos
  ficticios solo para probar el dashboard.
- Cargar los **proveedores B2B reales** (tabla `suppliers`): el Agente
  Back-Office verifica stock contra la URL/API configurada en cada proveedor.
- Revisar el **umbral de autonomía** del agente (monto sobre el cual pide
  aprobación al Supervisor en vez de emitir la OC solo).

### Webhooks de carriers

Configurar en el courier (Chilexpress, Starken, etc.) la URL
`https://api.tudominio.cl/webhooks/carrier` para que el seguimiento en tiempo
real (promesa c) y la activación automática de garantía y retracto al entregar
(promesas d y e) funcionen con envíos reales.

## 4. Operación

```bash
# Actualizar a una nueva versión del código
git pull && docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Logs de un servicio
docker compose -f docker-compose.prod.yml --env-file .env.prod logs -f agents-service

# Restaurar un backup (con el stack detenido salvo postgres)
gunzip -c dropship-2026-07-25.sql.gz | docker compose -f docker-compose.prod.yml --env-file .env.prod exec -T postgres psql -U dropship dropship
```

Los servicios tienen `restart: unless-stopped`, así que sobreviven reinicios
del servidor. Los certificados HTTPS se renuevan solos.

## Alternativa: plataformas gestionadas

Si prefieres no administrar un VPS: dashboard y tienda en **Vercel**, y
agentes + gateway + Postgres + Redis en **Railway/Render**. Requiere ajustar
`AGENTS_API_URL` / `BUSINESS_API_URL` / `BUSINESS_CORS_ORIGIN` a las URLs
públicas entre plataformas. El VPS con este compose es la vía con menos
fricción porque replica exactamente la topología con la que el sistema fue
probado de punta a punta.
