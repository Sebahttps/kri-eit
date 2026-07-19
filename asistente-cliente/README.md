# ClAI-nte — El Cliente del estudio KRI-EIT

ClAI-nte (cl-AI-nte) es la mirada crítica del estudio: actúa como el principal
cliente de cada proyecto. Encarna el perfil del cliente objetivo, se registra si es
necesario, prueba los flujos como usuario real — apurado, desconfiado, desde el
teléfono — y emite un informe de no más de una hoja con observaciones numeradas,
valoraciones de 1 a 5 estrellas y su veredicto: ¿lo usaría, pagaría, lo recomendaría?

## Contenido

| Archivo / carpeta | Qué es |
|---|---|
| `PROMPT.md` | El prompt maestro completo de ClAI-nte. |
| `plantillas/01-perfil-de-cliente.md` | El personaje que ClAI-nte encarna en cada prueba. |
| `plantillas/02-registro-de-prueba.md` | La bitácora del recorrido: qué vio, pensó y sintió en cada paso. |
| `plantillas/03-informe-de-cliente.md` | El informe final de UNA página, con estrellas y veredicto. |
| `informes/` | Aquí ClAI-nte guarda sus pruebas, una carpeta por proyecto. |

## Cómo usarlo

- **Dentro de Claude Code**: invoca el agente `clainte`. Dile qué probar (un sitio,
  un flujo, un mensaje de venta, incluso una idea contada) y qué perfil encarnar.
- **Con el resto del estudio**: es el control de calidad final — lo que Kri-AI idea,
  VisuAI diseña y GAIn aprueba, ClAI-nte lo enfrenta como cliente antes de salir al
  mundo.
- **Fuera del repositorio**: copia `PROMPT.md` como instrucciones de un Project en
  claude.ai.

## Advertencia

ClAI-nte es UNA voz de cliente simulada, no un estudio de mercado: sus informes son
la opinión de un perfil y así lo declaran. Las decisiones grandes se validan con
clientes reales (las preventas y pilotos que exige GAIn). En pruebas con registro
real usa solo datos autorizados por el dueño, jamás de terceros.
