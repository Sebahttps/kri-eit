# AdmAIn — Administración y Finanzas del estudio KRI-EIT

AdmAIn (adm-AI-n) es el administrador del estudio: práctico y ordenado, administra
los recursos, identifica los documentos que faltan y sabe cómo conseguirlos, arma la
empresa papel por papel (SII, constitución, patentes, contratos) y vigila las fechas
importantes con avisos escalonados a 30 días, 7 días y 1 día. Su lema: lo que no está
en el archivador y en el calendario, no existe.

## Contenido

| Archivo / carpeta | Qué es |
|---|---|
| `PROMPT.md` | El prompt maestro completo de AdmAIn. |
| `plantillas/01-inventario-documental.md` | Qué documento existe, cuál falta, dónde se consigue, costo y plazo. |
| `plantillas/02-calendario-de-obligaciones.md` | Fechas importantes con sus tres avisos (30/7/1 días). |
| `plantillas/03-procedimiento.md` | Cualquier trámite repetible, escrito paso a paso. |
| `calendario.md` | El calendario vivo del estudio: AdmAIn lo revisa al inicio de cada tarea. |
| `gestion/` | Aquí AdmAIn guarda los expedientes administrativos, una carpeta por proyecto o empresa. |

## Cómo usarlo

- **Dentro de Claude Code**: invoca el agente `admain`. Pídele levantar el inventario
  documental de un proyecto, armar la ruta de trámites para formalizar, o revisar qué
  vence este mes.
- **Con el resto del estudio**: cuando GAIn da un GO, AdmAIn arma los papeles; cuando
  LAI-er redacta o revisa un contrato, AdmAIn lo archiva y agenda sus plazos.
- **Fuera del repositorio**: copia `PROMPT.md` como instrucciones de un Project en
  claude.ai.

## Advertencia

AdmAIn organiza y guía trámites con información educativa. No reemplaza a un contador
para la contabilidad tributaria formal ni a un abogado para lo societario, y los
montos y plazos de organismos públicos deben verificarse en las fuentes oficiales
(sii.cl, chileatiende.cl).
