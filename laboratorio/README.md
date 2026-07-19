# Laboratorio de consultas — estudio KRI-EIT

La aplicación web del estudio: una página con **login** (contraseña única) y un
**laboratorio de chat en vivo** con los seis agentes — Kri-AI, GAIn, AdmAIn, LAI-er,
VisuAI y ClAI-nte. Cada agente responde con su prompt maestro real, leído
directamente desde las carpetas del repositorio, así que mejorar un PROMPT.md mejora
al agente del laboratorio sin tocar código.

## Qué necesitas (una sola vez)

1. **Una API key de Anthropic** — se crea en [platform.claude.com](https://platform.claude.com)
   y se le carga crédito. El laboratorio cobra por uso: con el modelo por defecto
   (Claude Opus) una consulta típica cuesta entre 2 y 5 centavos de dólar.
   *Tu suscripción de claude.ai no incluye crédito de API: son cuentas separadas.*
2. **Una contraseña para el laboratorio** — la que tú quieras (variable `LAB_PASSWORD`).
3. **Node.js 18 o superior** (solo para correrlo local) o una cuenta en un hosting
   con plan gratuito (Render, Railway, Fly.io).

## Probarlo en tu computador

```bash
cd laboratorio
npm install
ANTHROPIC_API_KEY=sk-ant-... LAB_PASSWORD=tu-clave npm start
# abre http://localhost:3000
```

## Publicarlo en internet (Render, plan gratuito)

1. Crea una cuenta en [render.com](https://render.com) y conéctala a tu GitHub.
2. **New → Web Service** → elige el repositorio `kri-eit`.
3. Configuración:
   - **Root Directory**: `laboratorio`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
4. En **Environment**, agrega las variables:
   - `ANTHROPIC_API_KEY` = tu key de platform.claude.com
   - `LAB_PASSWORD` = tu contraseña de acceso
   - `SESSION_SECRET` = cualquier texto largo y aleatorio
   - `NODE_ENV` = `production`
5. Deploy. Render te da una URL tipo `https://kri-eit.onrender.com` — esa es tu
   página: entras, pones tu contraseña y se abre el laboratorio.

> El plan gratuito de Render "duerme" el servidor tras 15 minutos sin uso; la primera
> visita después de eso tarda ~30 segundos en despertar. Para uso personal, funciona.

## Variables de entorno

| Variable | Obligatoria | Qué es |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | La key de la API (empieza con `sk-ant-`). |
| `LAB_PASSWORD` | ✅ | La contraseña del login. |
| `SESSION_SECRET` | recomendada | Firma de la cookie de sesión; sin ella se genera una al azar y las sesiones se cierran en cada reinicio. |
| `LAB_MODEL` | opcional | Modelo a usar (por defecto `claude-opus-4-8`; para abaratar, `claude-sonnet-5`). |
| `PORT` | opcional | Puerto del servidor (3000). |

## Seguridad, en simple

- La contraseña viaja una vez y queda una cookie firmada (HttpOnly): suficiente para
  un laboratorio personal de un solo usuario.
- La API key vive **solo en el servidor** — el navegador jamás la ve.
- No compartas la URL con la contraseña: quien entra, consume tu crédito.
- Las conversaciones viven en la memoria del navegador (se pierden al recargar); el
  servidor no guarda historial.

## Costos, en simple

Pagas por lo que consultas. Referencia con Claude Opus ($5 entrada / $25 salida por
millón de tokens): una consulta con respuesta extensa ≈ US$0,02–0,05. Cien consultas
≈ US$3–5. Si quieres abaratar, `LAB_MODEL=claude-sonnet-5` baja el costo a menos de
la mitad con excelente calidad.
