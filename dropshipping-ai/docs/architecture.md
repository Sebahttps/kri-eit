# Arquitectura — Sistema de Dropshipping Autónomo

## Stack (decidido en Paso 1)

| Capa | Tecnología | Por qué |
|---|---|---|
| Dashboard | Next.js 14 + TypeScript + Tailwind + shadcn/ui + Recharts | Dashboard moderno, SSR de KPIs, tiempo real vía WS |
| Gateway de negocio | NestJS (TypeScript) | Auth, pedidos, pagos, WebSocket hacia el dashboard |
| Agentes IA | Python + FastAPI + **LangGraph** | `interrupt()`/checkpoints nativos = human-in-the-loop real |
| LLM | Claude (langchain-anthropic) | Ya es el estándar del estudio (laboratorio/) |
| Base de datos | PostgreSQL 16 (+ pgvector opcional) | Transaccional; promesas como triggers; RAG sin motor extra |
| Caché / colas | Redis | Stock en ms, colas de scraping, pub/sub tiempo real |
| Infra | Docker Compose | Local primero; K8s solo si el volumen lo exige |

**LangGraph sobre CrewAI**: el requisito central es que el Supervisor apruebe
decisiones críticas sin frenar la operación. LangGraph pausa un grafo con
`interrupt()`, persiste el estado en Postgres y lo reanuda días después con
`Command(resume=...)`. CrewAI no ofrece ese control fino de pausa/reanudación.

## Human-in-the-loop: ciclo de una Sugerencia IA

```
Agente B2B detecta decisión sobre umbral
  └─ interrupt() → fila en ai_suggestions (status=pendiente, thread_id=checkpoint)
       └─ Dashboard muestra la tarjeta [Aprobar/Rechazar]
            └─ POST /aprobaciones/{id}/decision
                 └─ Command(resume='aprobar'|'rechazar') → el grafo continúa
                      └─ OC emitida o rechazada + auditoría en agent_actions
```

Umbrales configurables por entorno (`AGENTS_UMBRAL_*` en `app/config.py`):
- `umbral_costo_oc`: OC sobre este monto requieren aprobación.
- `umbral_margen_pct`: cambios de margen sobre este % requieren aprobación.

## Auditoría

`agent_actions` registra cada acción de agente (stock verificado, OC emitida,
garantía activada, sugerencia decidida). Es la evidencia operativa para la
garantía legal automatizada y para depurar decisiones de los agentes.

## Contratos de API

FastAPI publica el OpenAPI en `/docs` y `/openapi.json`; de ahí se generan los
tipos TypeScript de `packages/shared-types` para el dashboard y el gateway
(`openapi-typescript` en el Paso 4).

## Pendiente (Paso 4)

- `apps/business-api`: NestJS — auth de supervisores, pagos, WS de KPIs.
- `apps/dashboard`: Next.js — KPIs en vivo, tendencias, bandeja de Sugerencias.
- Checkpointer Postgres (`langgraph-checkpoint-postgres`) en producción en vez
  del `MemorySaver` por defecto (ya está en requirements; se inyecta en
  `construir_grafo(checkpointer=...)` desde `main.py`).
