---
name: run-business-api
description: Compila, levanta y maneja el business-api de CompAI (NestJS, puerto 4000) en una máquina sin Docker, incluyendo un Postgres local desechable con el esquema y el seed aplicados. Úsala cuando pidan correr, arrancar, levantar, probar, smoke-testear o depurar el business-api, verificar un cambio contra el API real, o pegarle a /health, /products, /auth/login o /orders.
---

# Correr el business-api

API NestJS en `:4000`. Se maneja con `driver.mjs`, que le pega por HTTP como lo
harían la tienda y el dashboard: catálogo, login, ruta protegida y una compra de
punta a punta.

**Todas las rutas de este documento son relativas a `apps/business-api/`.**
Verificado en Windows 10 con PowerShell, Node 24.18 y npm 11.16.

## Requisitos

Solo Node y npm. No hace falta Docker ni instalar Postgres: `local-db.mjs` baja
los binarios de PostgreSQL vía npm (~200 MB, la primera vez) y arma un clúster
desechable en el directorio temporal del sistema, fuera del repo.

En una máquina *con* Docker existe `infra/docker-compose.yml` como alternativa —
no verificado desde esta skill.

## Compilar

```powershell
npm install          # solo la primera vez
npm run build        # nest build -> dist/
```

## Correr y manejar (ruta del agente)

Dos comandos. El primero deja la base lista; el segundo levanta el API, lo
maneja de punta a punta y lo baja.

```powershell
node .claude/skills/run-business-api/local-db.mjs up
node .claude/skills/run-business-api/driver.mjs --start
```

Salida esperada al final: `=== TODO OK, 1 salto(s) ===` y código de salida 0.
El salto es el checkout, que necesita el agents-service (ver Gotchas).

El driver ejerce, en orden: `GET /health` (exige `db:true`), `/products/categorias`,
`/products`, el `ValidationPipe` del login (400), credenciales malas (401), login
correcto (201 + JWT), `/orders` sin token (401) y con token (200), `POST /orders`
(201), pagar antes del checkout (422), el detalle del pedido y su aparición en la
lista del supervisor. Cualquier desviación es un `[FALLA]` y salida 1.

Contra un API que ya está corriendo, sin `--start`:

```powershell
node .claude/skills/run-business-api/driver.mjs
```

Manejo de la base:

```powershell
node .claude/skills/run-business-api/local-db.mjs down    # detener
node .claude/skills/run-business-api/local-db.mjs reset   # datos limpios + seed
node .claude/skills/run-business-api/local-db.mjs nuke    # borrar el clúster entero
```

## Correr a mano (ruta humana)

```powershell
$env:BUSINESS_DATABASE_URL="postgresql://dropship:dropship@127.0.0.1:5432/dropship"
npm run start:dev
```

Queda en watch. Sirve para iterar sobre el código; para verificar comportamiento,
el driver contra esta instancia es más rápido que pegarle a mano.

## Pruebas

`package.json` no define script `test`. No hay suite en este paquete; el driver
es la verificación disponible.

## Gotchas

- **Sin base, el API no se degrada: se muere.** `RealtimeGateway.onModuleInit`
  (`src/realtime/realtime.gateway.ts:23`) abre su propio cliente `pg` para el
  `LISTEN eventos`; ese `await` rechaza, `bootstrap()` no captura nada y el
  proceso cae *después* de mapear las 12 rutas y *antes* de que `listen()`
  termine. El puerto 4000 nunca se abre. El `HealthController` está escrito para
  contestar `503 {estado:"degradado", db:false}` en ese caso, pero nunca alcanza
  a contestarlo.
- **`localhost` no sirve en el DSN.** Resuelve a `::1` primero y el clúster local
  solo escucha en IPv4. Usa `127.0.0.1` en `BUSINESS_DATABASE_URL`.
- **`embedded-postgres` no trae `psql` ni `createdb`** — solo `initdb`, `pg_ctl` y
  `postgres`. Por eso `local-db.mjs` aplica el SQL con `pg` desde Node.
- **Cada `.sql` se manda como una sola query.** Partirlo por `;` rompe los cuerpos
  `$$` de las funciones de `001_notify_events.sql`.
- **Lanzar `postgres` heredando los handles del shell cuelga el shell.** El
  script lo lanza `detached` con la salida a `pg.log`. Lo mismo pasa con
  `pg_ctl start` desde PowerShell.
- **npm ≥ 11 no ejecuta el postinstall de `@embedded-postgres`** (avisa
  `allow-scripts`). En Windows da igual: ese script solo rehace symlinks y los
  `.exe` ya vienen usables.
- **El seed bloquea al supervisor a propósito:** `password_hash` queda en
  `'BLOQUEADO-sin-contrasena-ver-docs-deploy-production'`, que no es un hash
  bcrypt, así que ninguna clave entra. El driver le escribe una clave local
  (`clave-local-1234`) antes de probar el login. Eso vive solo en el clúster
  desechable.
- **`POST /orders/:id/checkout` necesita el agents-service en `:8000`** para
  confirmar stock con el proveedor. Sin él devuelve `500 Internal server error`
  con `fetch failed` en el log — mientras que si el agents-service *responde* con
  error, `src/orders/orders.service.ts:87` lo traduce a un 422 explicativo. La
  misma indisponibilidad se reporta de dos formas distintas según dónde falle.
  El driver detecta el puerto cerrado y lo marca `[SALTO]` en vez de `[FALLA]`.
- **El correlativo `numero` de los pedidos es una secuencia que no se reinicia.**
  Tras varias corridas verás `numero: 34`; `local-db.mjs reset` lo vuelve a 1.
- **Puertos vecinos:** 3000 es el dashboard y 3001 la tienda — son los orígenes
  que `src/main.ts:9` permite por CORS por defecto. El API es el 4000.

## Troubleshooting

| Síntoma | Causa y arreglo |
|---|---|
| `AggregateError [ECONNREFUSED] ::1:5432` y el proceso muere | No hay base. `local-db.mjs up`. |
| `[driver] ERROR: el API no abrió :4000` | Lo mismo; el driver lo detecta en ~2 s y lo dice. |
| `no se encontró el supervisor del seed` | La base existe sin seed. `local-db.mjs reset`. |
| `catálogo vacío; ¿se aplicó el seed?` | Igual que el anterior. |
| `EADDRINUSE :4000` | Quedó una instancia viva de una corrida anterior. `Get-Process node \| Stop-Process -Force`. |
| `npm install de embedded-postgres falló` | Descarga de ~200 MB; reintenta con red estable. |
| El shell se queda colgado tras lanzar Postgres | Estás lanzándolo a mano. Usa `local-db.mjs up`, que lo hace `detached`. |
