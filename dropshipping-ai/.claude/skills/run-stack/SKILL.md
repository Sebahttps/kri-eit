---
name: run-stack
description: Levanta el stack local completo de CompAI en una máquina sin Docker — Postgres, agents-service (FastAPI) y dashboard (Next.js) — con datos de demostración, en un comando. Úsala cuando pidan correr, levantar, arrancar o probar el dashboard, el panel del supervisor, el agents-service o "el stack completo"; para ver KPIs, gráficos, tickets o sugerencias con datos reales; o para apagarlo todo.
---

# Correr el stack local

Tres servicios encadenados: **dashboard (`:3000`) → agents-service (`:8000`) → Postgres (`:5432`)**.
El dashboard no consulta la base directamente ni pasa por el business-api: todo lo
que muestra viene del agents-service, vía el proxy `/api/agents/*` de
`apps/dashboard/next.config.mjs`.

**Las rutas de este documento son relativas a `dropshipping-ai/`.**
Verificado en Windows 10 con PowerShell, Node 24.18 y Python 3.13.14.

## Requisitos

Node y Python. **No hace falta Docker, ni Redis, ni una clave de Anthropic** (ver
Gotchas). La primera corrida baja los binarios de Postgres y crea un entorno
virtual de Python; ambos quedan en el directorio temporal del sistema, fuera del
repo.

## Levantarlo

```powershell
node .claude/skills/run-stack/stack.mjs up
```

Un solo comando: arranca Postgres con esquema y seed, aplica `db/seed-demo.sql`
si la base está vacía, instala las dependencias de Python la primera vez, y
levanta los otros dos. Termina imprimiendo el estado y una petición que atraviesa
los tres:

```
  ✓  postgres   :5432
  ✓  agents     :8000
  ✓  dashboard  :3000

  cadena dashboard -> agents -> postgres: 200
  ventas_hoy=63990  tickets=3  sugerencias=1

  → http://localhost:3000
```

En frío tarda ~27 s (más la instalación de dependencias la primera vez). Es
idempotente: lo que ya esté arriba lo deja como está.

```powershell
node .claude/skills/run-stack/stack.mjs status   # qué vive y si la cadena responde
node .claude/skills/run-stack/stack.mjs down     # baja los tres
```

## Verificarlo

`status` es la prueba: una sola petición a `/api/agents/kpis/resumen` **por el
puerto del dashboard** recorre los tres servicios. Si devuelve 200 con números,
la cadena entera está sana. Para mirarlo con ojos, `http://localhost:3000`.

El business-api (`:4000`) no participa de esta cadena; tiene su propia skill en
`apps/business-api/.claude/skills/run-business-api/`.

## Gotchas

- **El agents-service NO necesita Redis ni clave de Anthropic**, pese a lo que
  sugiere su `requirements.txt`. Ambos son perezosos: el cliente de Redis se crea
  sin conectar y cada uso está en un `try/except` que se traga el fallo
  (`app/tools/proveedores.py:25-29`), y el modelo solo se instancia cuando llega
  una petición al chat (`app/graphs/front_office/graph.py:126-129`). Lo único
  que exige al arrancar es Postgres (`app/main.py:20`). Los cinco endpoints que
  el dashboard consume tocan solo Postgres; sin Redis se pierde el caché de
  proveedores y sin clave falla `/front-office/chat`, y el dashboard no llama a
  ninguno de los dos.
- **`langgraph-checkpoint-postgres` no se importa en ningún archivo.** Está en
  `requirements.txt` pero es dependencia muerta hoy. Si su instalación falla en
  Windows, se puede comentar sin consecuencias.
- **Sin `seed-demo.sql` el dashboard sale correcto pero en cero.** El seed base
  no trae ventas ni tickets, así que todo aparece en `—` y parece roto sin
  estarlo. El script lo aplica solo si `orders` está vacía.
- **En Windows, lanzar los servicios con el `detached` de Node no sirve, por dos
  motivos distintos.** Uno: deja al proceso sin consola, y entonces Windows le
  da una ventana nueva a cada hijo que ese proceso cree (por eso Postgres
  llenaba la pantalla de ventanas negras; ver los Gotchas de `run-business-api`).
  Dos: PowerShell lanzado detached se queda sin consola y `Start-Process` ni
  siquiera llega a ejecutarse — no se crea el proceso. Lo que funciona es
  `spawnSync` de PowerShell **sin** detached, con `Start-Process -WindowStyle
  Hidden`.
- **Y no captures la salida de ese PowerShell.** Con `encoding`/pipe, `spawnSync`
  espera un EOF que nunca llega y el script se cuelga indefinidamente aunque el
  servicio ya esté arriba. Por eso el PID va por archivo y el stdio en
  `"ignore"`.
- **Los servicios sobreviven a la sesión.** Es deliberado: así no se caen cuando
  termina la tarea que los lanzó. Hay que bajarlos con `down` a propósito.
- **`down` también caza huérfanos.** Si un `up` se interrumpió antes de anotar el
  PID, el servicio queda vivo sin registro; `down` lo busca por el puerto.

## Troubleshooting

| Síntoma | Causa y arreglo |
|---|---|
| El dashboard muestra "Sin conexión con el servicio de agentes" | El agents-service no está en `:8000`. `stack.mjs status` y, si falta, `up`. |
| KPIs en `—` o gráficos vacíos, sin banner rojo | La cadena funciona pero la base no tiene datos. `local-db.mjs reset` y luego `stack.mjs up`, que reaplica el demo. |
| `no se pudo lanzar agents (sin PID)` | PowerShell no ejecutó `Start-Process`. Revisa que no se le haya añadido `detached` al spawn. |
| El script se queda colgado tras "agents-service…" | Alguien volvió a capturar la salida de PowerShell. Debe ir con `stdio: "ignore"`. |
| Ventanas negras apareciendo solas | Postgres lanzado sin consola oculta. Ver los Gotchas de `run-business-api`. |
| `falló el pip install del agents-service` | Borra `%TEMP%\kri-eit-agents-venv` y repite; se recrea entero. |
