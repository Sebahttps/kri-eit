# Dashboard del Supervisor

Panel de control del humano supervisor: Next.js 14 + Tailwind + Recharts + SWR.

- **KPIs en tiempo real** (refresco 5 s): ventas de hoy, tasa de conversión,
  tickets de soporte, latencia de verificaciones de stock.
- **Gráficos de tendencia**: ventas y conversión de los últimos 30 días
  (dos gráficos con un eje cada uno — nunca doble eje).
- **Tendencias de productos**: ranking por `trending_score` con ventas 7d y margen.
- **Sugerencias de la IA**: decisiones críticas escaladas por los agentes con
  botones Aprobar/Rechazar; la decisión reanuda el grafo LangGraph pausado.
- Modo claro/oscuro automático (`prefers-color-scheme`), paleta validada por
  contraste y daltonismo.

## Desarrollo

```bash
npm install
AGENTS_API_URL=http://localhost:8000 npm run dev   # http://localhost:3000
```

El dashboard habla solo con `/api/agents/*`, que Next.js reescribe hacia el
servicio de agentes (sin CORS). `NEXT_PUBLIC_SUPERVISOR_ID` identifica al
supervisor mientras el gateway (business-api) no implemente auth; por defecto
usa el UUID fijo del seed.

## Tiempo real

Hoy: polling SWR (5–30 s según el panel). Ruta de mejora: el gateway NestJS
expone WebSocket y estos hooks pasan de `refreshInterval` a suscripción.
