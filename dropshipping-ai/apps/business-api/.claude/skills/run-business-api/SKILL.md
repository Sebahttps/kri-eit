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

Para comprobar el modo degradado —que sin base el API sigue en pie y lo dice con
503 en todas las rutas, sin volverse goloso con las que no la tocan:

```powershell
node .claude/skills/run-business-api/local-db.mjs down
node .claude/skills/run-business-api/driver.mjs --start --sin-base
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

- **Sin base, el API arranca igual y lo dice.** `/health` contesta
  `503 {estado:"degradado", db:false}` y `RealtimeGateway` reintenta el `LISTEN`
  cada 5 s hasta que Postgres aparece; cuando aparece, se engancha solo, sin
  reiniciar nada. Lo mismo al revés: si matas Postgres con el API corriendo, el
  proceso sobrevive y el health vuelve a 503. Hasta el 12-ago-2026 no era así —
  el `await` del gateway tumbaba el arranque y el 503 nunca llegaba a
  contestarse. Si ves ese comportamiento, estás corriendo un `dist/` viejo:
  recompila.
- **Todas las rutas lo reportan igual, no solo `/health`.** Un filtro global
  (`src/db/db-unavailable.filter.ts`) traduce los fallos de conexión de Postgres
  a `503 {estado:"degradado", db:false, mensaje:…}` en cualquier ruta. Distingue
  por código (`ECONNREFUSED`, `57P0x`, `08xxx`) y por mensaje para los fallos del
  pool, que llegan sin código. Un error de SQL de verdad (`42601`, `23505`) no
  entra ahí a propósito: ese sigue saliendo como 500, que es lo correcto.
  Verificable con `driver.mjs --sin-base`.
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
  confirmar stock con el proveedor. Sin él devuelve `503` ("El Agente B2B no está
  disponible…"); si el agents-service *responde* con error, es un `422`. Dos
  fallos distintos, dos códigos distintos — hasta el 12-ago-2026 el primero salía
  como `500` pelado. El detalle con la URL interna va al log, no a la respuesta.
  El driver exige ese 503 y marca el paso como `[SALTO]` porque el flujo no puede
  completarse, no porque tolere el error.
- **`emitirOrdenCompra` nunca lanza, a propósito.** Corre *después* de que el
  pago quedó registrado; si lanzara, un agents-service caído le diría al cliente
  que su pago falló cuando sí se cobró. Devuelve
  `{status:"error", detalle:"…la OC queda pendiente"}` dentro de una respuesta
  200.
- **El correlativo `numero` de los pedidos es una secuencia que no se reinicia.**
  Tras varias corridas verás `numero: 34`; `local-db.mjs reset` lo vuelve a 1.
- **Puertos vecinos:** 3000 es el dashboard y 3001 la tienda — son los orígenes
  que `src/main.ts:9` permite por CORS por defecto. El API es el 4000.

## Troubleshooting

| Síntoma | Causa y arreglo |
|---|---|
| `WARN [RealtimeGateway] sin eventos en vivo (ECONNREFUSED …:5432)` cada 5 s | No hay base. El API funciona a medias a propósito; `local-db.mjs up` y se engancha solo. |
| `/health` responde `503 {estado:"degradado"}` | Igual que arriba: el API está vivo, la base no. |
| El proceso muere al arrancar con `ECONNREFUSED 5432` | Es el comportamiento viejo: estás corriendo un `dist/` anterior al 12-ago-2026. `npm run build`. |
| `no se encontró el supervisor del seed` | La base existe sin seed. `local-db.mjs reset`. |
| `catálogo vacío; ¿se aplicó el seed?` | Igual que el anterior. |
| `EADDRINUSE :4000` | Quedó una instancia viva de una corrida anterior. `Get-Process node \| Stop-Process -Force`. |
| `npm install de embedded-postgres falló` | Descarga de ~200 MB; reintenta con red estable. |
| El shell se queda colgado tras lanzar Postgres | Estás lanzándolo a mano. Usa `local-db.mjs up`, que lo hace `detached`. |
