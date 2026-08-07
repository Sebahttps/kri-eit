# 🤖 KRI-EIT: Directrices de Operación y Arquitectura Multi-Agente

## 🎯 Visión General
Este repositorio (`kri-eit`) es una plataforma multi-agente para desarrollo, automatización y proyectos de e-commerce / dropshipping AI. Claude Code actúa como el **Orquestador Principal**, coordinando agentes especializados y ejecutando tareas en la terminal con alta autonomía.

---

## 🏛️ Mapa de Agentes y Roles (`.claude/agents/`)
Cuando se solicite una tarea específica, debes asumir o invocar las directrices del agente correspondiente almacenado en las carpetas de los asistentes:

* **AdmAIn** (`/asistente-administrativo`): Gestión de proveedores, logística, archivos e inventario.
* **VisuAI** (`/asistente-visual`): UI/UX, rediseño de tienda, CSS/HTML, estética de marca.
* **ClAI-nte** (`/asistente-cliente`): Atención, soporte, redacción de interacciones y experiencia de usuario.
* **ComerciAI** (`/asistente-comercial`): Estrategias de ventas, ofertas, catálogo y precios.
* **LegAI** (`/asistente-legal`): Políticas, cumplimiento normativo y contratos.
* **CreativAI** (`/asistente-creativo`): Copywriting, campañas y generación de ideas.

---

## 🛠️ Normas de Ejecución para Claude Code

### 1. Comandos Frecuentes del Entorno
- **Web App / Laboratorio:** `cd laboratorio && npm run dev` o `python app.py` (según subproyecto).
- **Verificación / Linter:** Validar sintaxis antes de confirmar cambios en código TypeScript/Python.
- **Git Flow:** Crear ramas de características (`feature/nombre`) antes de realizar cambios mayoritarios.

### 2. Principios de Independencia Operativa
1. **Verificación Autónoma:** Antes de dar por finalizada una tarea, ejecuta las pruebas locales o verifica los archivos modificados.
2. **Ediciones Mínimas y Precisas:** Modifica solo los archivos relevantes. No alteres archivos de directivas globales sin autorización explícita.
3. **Pases de Contexto:** Si una tarea requiere coordinación (ej. Comercial + Visual), resume el resultado del primer agente antes de pasar al segundo.

### 3. Formato y Lenguaje
- **Idioma principal:** Español.
- **Estilo de Respuesta:** Directo, conciso, orientado a la acción y scannable (tablas, bloques de código, listas).
