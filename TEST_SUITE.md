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
| @instagrai | Encargado de los mensajes de Instagram (cola de borradores y tono) |

## Qué valida la suite (`tests/test_agents_schema.py`)

1. **Configuraciones de agente**: los 8 agentes registrados existen en
   `.claude/agents/`, sin faltantes ni sobrantes.
2. **Frontmatter YAML**: cada configuración declara `name`, `description`
   y `tools`.
3. **Prompts maestros**: existen los 6 `asistente-*/PROMPT.md`, no están
   vacíos y contienen el bloque `<validation_checks>` de autocomprobación.
4. **Este archivo**: referencia a todos los agentes registrados.

## Suite del agente de Instagram (`instagram-agent/tests/`)

Suite propia, fuera de la de CI porque depende de paquetes externos:

```bash
cd instagram-agent && python3 -m unittest discover -s tests -p "test_*.py"
```

`test_seguridad.py` (firma HMAC de los webhooks de Meta) y `test_politica.py`
(qué se responde solo y qué espera aprobación) corren sin instalar nada.
`test_esquemas.py` y `test_flujo.py` requieren `pip install -r requirements.txt`;
usan dobles, así que ningún test toca la red ni la cuenta real.

## Pipeline de orquestación (`orchestrator.py`)

Etapas encadenadas: @kri-ai (creativo) → @clainte (cliente) → @gain
(comercial) → @laier (legal) → @admain (administrativo) → @visuai (visual).
El modo `--dry-run` genera artefactos mock para validación en CI/CD.
