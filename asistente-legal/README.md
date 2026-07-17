# LAIer — Abogado Estratega y Analista de Litigio (Chile)

LAIer es el asistente legal de este repositorio, hermano de Kri-ai (el asistente
creativo de negocios). Es un abogado estratega chileno experto en Derecho Civil,
Derecho Procesal Civil y Derecho Constitucional a nivel de cédulas, con un módulo
psicoanalítico para perfilar a los participantes de un conflicto y un método de
"doble tesis" que le permite probar y defender cualquier posición dentro de la ley.

## Contenido

| Archivo / carpeta | Qué es |
|---|---|
| `PROMPT.md` | El prompt maestro completo de LAIer. Se puede copiar como instrucciones de sistema en cualquier asistente (Claude, un Project de claude.ai, la API). |
| `plantillas/01-ficha-del-caso.md` | Ficha de ingreso de un caso: hechos, objetivo, prueba, debilidades. |
| `plantillas/02-perfil-participante.md` | Perfil psicoanalítico de trabajo de un participante. |
| `plantillas/03-frente-estrategico.md` | Un frente de litigio en doble tesis: cómo probar / cómo refutan / cómo neutralizar. |
| `casos/` | Aquí LAIer guarda los expedientes de trabajo, una carpeta por caso. |

## Cómo usarlo

- **Dentro de Claude Code**: invoca el agente `laier` (definido en
  `.claude/agents/laier.md`). Cuéntale tu caso y pídele el análisis; si quieres
  conservarlo, pídele que guarde el expediente en `casos/<nombre-caso>/`.
- **Fuera del repositorio**: copia `PROMPT.md` como instrucciones personalizadas de un
  Project en claude.ai, o pégalo al inicio de una conversación.
- **Consola visual**: existe además un artefacto publicado (consola LITIS) que arma el
  expediente de forma interactiva y genera el prompt con el caso ya cargado.

## Advertencia

LAIer entrega análisis estratégico y educativo con citas verificables. No constituye
asesoría legal formal ni reemplaza el patrocinio de un abogado habilitado (Ley
18.120), y sus perfiles psicológicos son hipótesis de trabajo, no diagnósticos.
