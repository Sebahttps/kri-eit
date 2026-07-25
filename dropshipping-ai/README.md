# Sistema de Dropshipping Autónomo · Agentes IA

Sistema de dropshipping gestionado por dos Agentes IA con un humano Supervisor
que solo aprueba decisiones críticas.

## Las 5 promesas de venta (hard-coded)

| Promesa | Dónde vive la regla |
|---|---|
| (a) Stock confirmado antes de pagar | Trigger `trg_pago_requiere_stock` + endpoint `POST /back-office/pedidos/{id}/confirmar-stock` |
| (b) Pago contra entrega | Enum `payment_method` + estado `contra_entrega_confirmado` |
| (c) Seguimiento en tiempo real | Tablas `shipments` / `shipment_events` + `GET /front-office/pedidos/{id}/seguimiento` |
| (d) Garantía legal 6 meses automática | Trigger `trg_entrega_activa_garantia` (se activa sola al entregar) |
| (e) Retracto 10 días sin fricción | Trigger `trg_retracto_dentro_de_plazo` (auto-aprueba dentro del plazo) |

## Arquitectura

```
apps/
  agents-service/   FastAPI + LangGraph (Python)  — los dos agentes + KPIs
  business-api/     NestJS                        — catálogo, auth, pedidos, webhooks, WS
  dashboard/        Next.js                       — panel del Supervisor
  store/            Next.js                       — tienda B2C con chat del agente
db/                 schema.sql + seeds + migrations (PostgreSQL 16)
infra/              docker-compose (postgres, redis, agents-service)
packages/
  shared-types/     contratos compartidos (se generan del OpenAPI del servicio)
```

- **Agente Front-Office (B2C)**: agente ReAct (Claude vía LangGraph) con
  herramientas de catálogo, verificación de stock, seguimiento, garantías,
  retracto y tickets. Las promesas están en su system prompt Y en las
  herramientas: no puede ofrecer pago sin pasar por `verificar_disponibilidad`.
- **Agente Back-Office (B2B)**: grafo LangGraph con *human-in-the-loop*.
  Verifica stock (API o scraping, con caché Redis), y emite órdenes de compra:
  bajo el umbral de autonomía actúa solo; sobre él, hace `interrupt()`, crea
  una **Sugerencia IA** y espera la decisión del Supervisor, que reanuda el
  grafo con `Command(resume=...)`.

## Correr en local

```bash
cd infra
ANTHROPIC_API_KEY=sk-... docker compose up --build
# Dashboard del Supervisor:                http://localhost:3000
# Tienda B2C:                              http://localhost:3001
# Gateway de negocio (REST + WebSocket):   http://localhost:4000
# API de agentes + OpenAPI interactivo:    http://localhost:8000/docs
```

Para ver el dashboard con datos de ejemplo, aplica además `db/seed-demo.sql`
(30 días de pedidos, tickets y una sugerencia pendiente).

## Correr en producción

Hay un compose endurecido (`infra/docker-compose.prod.yml`): secretos
obligatorios vía `.env.prod`, servicios internos sin puertos publicados y
Caddy como único punto de entrada con HTTPS automático.

```bash
cd infra
cp .env.prod.example .env.prod   # completar secretos y dominios
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

Guía completa (DNS, backups, contraseña del Supervisor, webhooks de
carriers): [`docs/deploy-production.md`](docs/deploy-production.md).

## Modo híbrido con Shopify

Opcionalmente, Shopify puede ser la vitrina y el checkout mientras los
agentes siguen siendo el back-office (verificación de stock, OC, aprobación
del Supervisor, garantías y retracto). Configuración y trade-offs:
[`docs/shopify-hybrid.md`](docs/shopify-hybrid.md).

## Flujo de un pedido

```
carrito → verificando_stock → stock_confirmado → pagado | contra_entrega_confirmado
        → oc_emitida → despachado → en_transito → entregado → completado
   (entregado activa garantía 6m y ventana de retracto 10d automáticamente)
```
