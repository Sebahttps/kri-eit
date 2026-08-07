#!/bin/bash
# Uso: ./run-agent.sh <nombre_agente> "<tarea>"
# Ejemplo: ./run-agent.sh gain "Auditar la estrategia de precios en asistente-comercial/"

AGENT=$1
PROMPT=$2

if [ -f ".claude/agents/${AGENT}.md" ]; then
  echo "🚀 Ejecutando agente [${AGENT}]..."
  claude -p "Carga y asume el rol del agente en .claude/agents/${AGENT}.md y ejecuta la siguiente tarea: ${PROMPT}"
else
  echo "❌ El agente '${AGENT}' no existe en .claude/agents/"
fi
