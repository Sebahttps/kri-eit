# Asistente Creativo — Ideas de primera necesidad, comercialización y gestión

Este directorio contiene todo lo necesario para usar el **Asistente Creativo**: un
asistente de IA especializado en generar y desarrollar ideas de negocio basadas en
**necesidades reales** (productos y servicios de primera necesidad), con vocación de
**prevalecer en el tiempo**, y con una mirada experta en **comercialización y
administración**.

## ¿Qué hace?

Dado un contexto (una zona, un público, un problema, un presupuesto), el asistente:

1. **Detecta necesidades reales** — prioriza alimentación, salud, vivienda, agua,
   energía, transporte, cuidado de personas, educación básica y seguridad.
2. **Genera ideas duraderas** — soluciones a problemas comunes o nunca antes
   resueltos, filtrando modas pasajeras.
3. **Entrega la propuesta completa** — no solo la idea: cómo venderla (propuesta de
   valor, cliente, precio, canales, marca) y cómo administrarla (operación, costos,
   equipo, finanzas, riesgos, indicadores).

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `PROMPT.md` | Prompt maestro del asistente. Cópialo como system prompt en Claude, un Proyecto de claude.ai, o cualquier LLM. |
| `plantillas/01-ficha-de-idea.md` | Plantilla para capturar y evaluar cada idea generada. |
| `plantillas/02-plan-comercial.md` | Plantilla del plan de comercialización (venta, precio, canales, marca). |
| `plantillas/03-plan-administrativo.md` | Plantilla del plan de operación y administración (costos, equipo, finanzas, riesgos). |

Además, el asistente queda registrado como **subagente de Claude Code** en
`.claude/agents/asistente-creativo.md`: dentro de este repositorio puedes pedirle a
Claude Code que use el agente `asistente-creativo` para generar propuestas.

## Cómo usarlo

### Opción A — En Claude Code (este repo)

> Usa el agente asistente-creativo: necesito una idea de negocio para un barrio
> residencial con poca oferta de alimentos frescos, presupuesto inicial bajo.

### Opción B — En claude.ai u otra herramienta

1. Copia el contenido de `PROMPT.md` como instrucciones del sistema (o de un Proyecto).
2. Describe tu contexto: lugar, público, presupuesto, habilidades, restricciones.
3. Pide una o varias propuestas. Guarda los resultados usando las plantillas de
   `plantillas/` para comparar ideas de forma ordenada.

## Criterios que el asistente siempre aplica

- **Necesidad real primero**: si la gente puede vivir sin el producto, la idea baja de prioridad.
- **Prevalencia**: la demanda debe existir hoy y en 10 años.
- **Comercialización concreta**: nada de "hacer marketing"; el asistente dice qué vender, a quién, a qué precio, por qué canal y con qué mensaje.
- **Administrable**: la propuesta incluye cómo operarla día a día con recursos realistas.
- **Honestidad**: si una idea es débil, lo dice y explica por qué.
