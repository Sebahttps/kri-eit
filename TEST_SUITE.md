# 🧪 TEST_SUITE — Validación del ecosistema multi-agente KRI-EIT

Suite de verificación de la estructura del repositorio: configuraciones de
agentes, prompts maestros y pipeline de orquestación.

## Cómo ejecutar

```bash
# Suite completa (igual que en CI)
python3 -m unittest discover -s tests -p "test_*.py"

# Dry-run del pipeline de agentes
./orchestrator.py --dry-run
```

## Agentes registrados (`.claude/agents/`)

| Agente | Rol |
|---|---|
| @kri-ai | Asistente creativo de negocios esenciales |
| @clainte | El Cliente del estudio (mirada crítica de usuario) |
| @gain | Gerente Comercial (veredictos GO / NO-GO) |
| @laier | Abogado estratega y analista de litigio (Chile) |
| @admain | Administración y Finanzas del estudio |
| @visuai | Director de Arte del estudio |
| @operai | Jefe de Operación del modo artesanal |
| @paiton | Ingeniero de Software Principal y Arquitecto de Soluciones |
| @juniar | Asistente junior de gestión (correo repetitivo, sin criterio comercial) |

## Qué valida la suite (`tests/test_agents_schema.py`)

1. **Configuraciones de agente**: hay al menos 6 archivos en
   `.claude/agents/`. Hoy son **9**; la suite no exige una lista cerrada, así
   que sumar un agente no rompe nada — pero sí hay que agregarlo a la tabla de
   arriba, que es la referencia legible del estudio.
2. **Frontmatter YAML**: cada configuración declara `name`, `description`
   y `tools`.
3. **Prompts maestros**: existen los 6 `asistente-*/PROMPT.md`, no están
   vacíos y contienen el bloque `<validation_checks>` de autocomprobación.
4. **Este archivo**: referencia a todos los agentes registrados.

## Pipeline de orquestación (`orchestrator.py`)

Etapas encadenadas: @kri-ai (creativo) → @clainte (cliente) → @gain
(comercial) → @laier (legal) → @admain (administrativo) → @visuai (visual).
El modo `--dry-run` genera artefactos mock para validación en CI/CD.
