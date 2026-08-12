#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

AGENT_MAP = {
    "creativo": {"agent": "@kri-ai", "output": "propuesta_creativa.md", "prompt_file": "asistente-creativo/PROMPT.md"},
    "cliente": {"agent": "@clainte", "output": "evaluacion_cliente.md", "prompt_file": "asistente-cliente/PROMPT.md"},
    "comercial": {"agent": "@gain", "output": "propuesta_comercial.md", "prompt_file": "asistente-comercial/PROMPT.md"},
    "legal": {"agent": "@laier", "output": "dictamen_legal.md", "prompt_file": "asistente-legal/PROMPT.md"},
    "administrativo": {"agent": "@admain", "output": "reporte_financiero.md", "prompt_file": "asistente-administrativo/PROMPT.md"},
    "visual": {"agent": "@visuai", "output": "direccion_arte.md", "prompt_file": "asistente-visual/PROMPT.md"},
}

def validate_environment(repo_root):
    missing = []
    for stage, info in AGENT_MAP.items():
        p_path = os.path.join(repo_root, info["prompt_file"])
        if not os.path.exists(p_path):
            missing.append(p_path)
    if missing:
        print(f"[ERROR] Archivos de prompt faltantes: {missing}", file=sys.stderr)
        return False
    return True

def run_stage(stage_name, task_description, dry_run=False, repo_root="."):
    if stage_name not in AGENT_MAP:
        raise ValueError(f"Etapa desconocida: {stage_name}")

    stage_info = AGENT_MAP[stage_name]
    agent = stage_info["agent"]
    output_file = os.path.join(repo_root, stage_info["output"])

    cmd = ["claude", "-p", f"Usa el agente {agent} para {task_description}. Guarda el resultado en '{output_file}'."]

    print(f"\n[INFO] Ejecutando Etapa '{stage_name}' con Agente {agent}...")
    print(f"[CMD] {' '.join(cmd)}")

    if dry_run:
        print(f"[DRY-RUN] Simulación exitosa de la etapa '{stage_name}'. Generando artefacto mock...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Artefacto Generado por {agent}\n\nResumen de ejecución simulada para la tarea: {task_description}\n")
        return True

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Etapa '{stage_name}' completada.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al ejecutar etapa '{stage_name}': {e.stderr}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Orquestador del Pipeline de Agentes KRI-EIT")
    parser.add_argument("--dry-run", action="store_true", help="Simula la ejecución del pipeline para pruebas CI/CD")
    parser.add_argument("--initial-prompt", type=str, default="Conceptualizar un nuevo servicio de consultoría estratégica", help="Prompt inicial para la fase creativa")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.abspath(__file__))
    if not validate_environment(repo_root):
        sys.exit(1)

    print("=== INICIANDO PIPELINE DE AGENTES KRI-EIT ===")
    stages = [
        ("creativo", f"{args.initial_prompt} en 'propuesta_creativa.md'"),
        ("cliente", "auditar el archivo 'propuesta_creativa.md' y evaluar objeciones"),
        ("comercial", "ajustar la oferta comercial basándote en 'evaluacion_cliente.md'"),
        ("legal", "elaborar dictamen de riesgos contractuales para 'propuesta_comercial.md'"),
        ("administrativo", "calcular flujo de caja y proyección a 6 meses para 'propuesta_comercial.md'"),
        ("visual", "definir la dirección de arte y guía de diseño para 'propuesta_comercial.md'"),
    ]

    for stage_name, task in stages:
        success = run_stage(stage_name, task, dry_run=args.dry_run, repo_root=repo_root)
        if not success:
            print(f"[ABORT] Fallo en el pipeline en la etapa '{stage_name}'.")
            sys.exit(1)

    print("\n=== PIPELINE COMPLETADO CON ÉXITO ===")

if __name__ == "__main__":
    main()
