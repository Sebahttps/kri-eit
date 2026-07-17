# GAIn — Gerente Comercial del estudio KRI-EIT

GAIn (G-AI-n: *gain*, ganancia) es el gerente comercial del estudio y el contrapeso
de Kri-AI: el que pone los peros, cuestiona cada idea antes de gastar un peso y da la
visión más amplia de cómo ganar dinero de verdad — qué hacer y, sobre todo, qué NO
hacer. Su palabra favorita es "no"; por eso su GO vale oro.

## Contenido

| Archivo / carpeta | Qué es |
|---|---|
| `PROMPT.md` | El prompt maestro completo de GAIn. Se puede copiar como instrucciones de sistema en cualquier asistente (Claude, un Project de claude.ai, la API). |
| `plantillas/01-interrogatorio.md` | Los peros de GAIn: las 8 preguntas que toda idea debe responder, con la evidencia que las levanta. |
| `plantillas/02-mapa-de-ingresos.md` | Rutas de monetización ordenadas por esfuerzo, retorno y riesgo, con qué hacer y qué no. |
| `plantillas/03-veredicto.md` | El veredicto GO / NO-GO / GO condicionado, con condiciones medibles y lista negra del caso. |
| `veredictos/` | Aquí GAIn guarda sus revisiones, una carpeta por idea o negocio evaluado. |

## Cómo usarlo

- **Dentro de Claude Code**: invoca el agente `gain` (definido en
  `.claude/agents/gain.md`). Preséntale una idea — tuya o una propuesta de Kri-AI —
  y pídele el interrogatorio, el mapa de ingresos o el veredicto.
- **El dúo con Kri-AI**: el flujo natural del estudio es Kri-AI propone → GAIn
  cuestiona → la idea se fortalece o se descarta. Pídele a GAIn que revise cualquier
  propuesta guardada en `asistente-creativo/ideas/`.
- **Fuera del repositorio**: copia `PROMPT.md` como instrucciones personalizadas de un
  Project en claude.ai, o pégalo al inicio de una conversación.

## Advertencia

GAIn entrega análisis estratégico y educativo con números explícitos y supuestos
declarados. No constituye asesoría financiera, tributaria ni de inversiones regulada;
para decisiones tributarias o societarias, validar con un contador o abogado.
