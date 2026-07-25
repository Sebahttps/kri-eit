# Dashboard del Supervisor (Paso 4)

Next.js 14 + Tailwind + shadcn/ui + Recharts. Se construye en el Paso 4 sobre
los contratos del servicio de agentes (`/openapi.json`):

- KPIs en tiempo real: vistas `kpi_ventas_diarias`, `kpi_conversion`, `kpi_tickets`.
- Tendencias de productos: vista `kpi_tendencias_productos`.
- Sugerencias de la IA: `GET /aprobaciones/pendientes` + botones Aprobar/Rechazar
  → `POST /aprobaciones/{id}/decision`.
