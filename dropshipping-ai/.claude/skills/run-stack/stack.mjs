#!/usr/bin/env node
/**
 * Levanta el stack local completo: Postgres -> agents-service -> dashboard.
 *
 *   node .claude/skills/run-stack/stack.mjs up      # deja los tres corriendo
 *   node .claude/skills/run-stack/stack.mjs status  # qué hay vivo y si la cadena responde
 *   node .claude/skills/run-stack/stack.mjs down    # baja los tres
 *
 * Todo vive fuera del repo: el clúster de Postgres y el entorno virtual de
 * Python quedan en el directorio temporal del sistema.
 */
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import net from "node:net";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const UNIDAD = path.resolve(AQUI, "../../.."); // dropshipping-ai
const LOCAL_DB = path.join(
  UNIDAD,
  "apps/business-api/.claude/skills/run-business-api/local-db.mjs",
);
const SEED_DEMO = path.join(UNIDAD, "db/seed-demo.sql");
const AGENTS = path.join(UNIDAD, "apps/agents-service");
const DASHBOARD = path.join(UNIDAD, "apps/dashboard");

const TMP = path.join(os.tmpdir(), "kri-eit-stack");
const VENV = path.join(os.tmpdir(), "kri-eit-agents-venv");
const ESTADO = path.join(TMP, "pids.json");
const WIN = process.platform === "win32";
const PY = WIN ? path.join(VENV, "Scripts", "python.exe") : path.join(VENV, "bin", "python");

const DSN = "postgresql://dropship:dropship@127.0.0.1:5432/dropship";
const PUERTOS = { postgres: 5432, agents: 8000, dashboard: 3000 };

const log = (m) => console.log(`[stack] ${m}`);

function puerto(p) {
  return new Promise((res) => {
    const s = net.connect({ host: "127.0.0.1", port: p });
    s.on("connect", () => (s.destroy(), res(true)));
    s.on("error", () => res(false));
    s.setTimeout(1000, () => (s.destroy(), res(false)));
  });
}

async function esperar(p, intentos = 60) {
  for (let i = 0; i < intentos; i++) {
    if (await puerto(p)) return true;
    await new Promise((r) => setTimeout(r, 700));
  }
  return false;
}

function leerPids() {
  try {
    return JSON.parse(fs.readFileSync(ESTADO, "utf8"));
  } catch {
    return {};
  }
}

function guardarPid(nombre, pid) {
  fs.mkdirSync(TMP, { recursive: true });
  fs.writeFileSync(ESTADO, JSON.stringify({ ...leerPids(), [nombre]: pid }, null, 1));
}

/**
 * Lanza un servicio de fondo que sobreviva a esta sesión y NO abra ventanas.
 *
 * En Windows hay que usar Start-Process -WindowStyle Hidden: da una consola
 * real pero oculta. El `detached` de Node deja al proceso SIN consola, y
 * entonces Windows le regala una ventana nueva a cada hijo que ese proceso
 * cree — el mismo problema que tenía Postgres (ver local-db.mjs).
 */
function lanzar(nombre, exe, args, cwd) {
  fs.mkdirSync(TMP, { recursive: true });
  const salida = path.join(TMP, `${nombre}.log`);
  const error = path.join(TMP, `${nombre}.err.log`);

  if (WIN) {
    // Dos cosas aprendidas a golpes, las dos necesarias:
    //
    // - `stdio: "ignore"` y NO capturar la salida de PowerShell. Si se captura,
    //   spawnSync se queda esperando un EOF que no llega aunque el servicio ya
    //   esté arriba.
    // - Sin `detached`. PowerShell lanzado detached queda sin consola y ahí
    //   Start-Process no llega a ejecutarse: no se crea el proceso ni el PID.
    //
    // Como no podemos leer stdout, el PID lo escribe PowerShell en un archivo.
    const pidFile = path.join(TMP, `${nombre}.pid`);
    fs.rmSync(pidFile, { force: true });
    const lista = args.map((a) => `'${a}'`).join(",");
    spawnSync(
      "powershell",
      [
        "-NoProfile",
        "-Command",
        `(Start-Process -FilePath '${exe}' -ArgumentList ${lista} -WorkingDirectory '${cwd}' ` +
          `-WindowStyle Hidden -PassThru -RedirectStandardOutput '${salida}' ` +
          `-RedirectStandardError '${error}').Id | Set-Content -Encoding ascii '${pidFile}'`,
      ],
      { stdio: "ignore", windowsHide: true },
    );
    const pid = parseInt(fs.readFileSync(pidFile, "utf8").trim(), 10);
    if (Number.isNaN(pid)) throw new Error(`no se pudo lanzar ${nombre} (sin PID)`);
    guardarPid(nombre, pid);
  } else {
    const fd = fs.openSync(salida, "a");
    const p = spawn(exe, args, { cwd, detached: true, stdio: ["ignore", fd, fd] });
    p.unref();
    guardarPid(nombre, p.pid);
  }
  log(`${nombre} lanzado (log: ${salida})`);
}

function matar(nombre, pid) {
  if (!pid) return;
  try {
    if (WIN) {
      // /T mata también a los hijos: `next dev` levanta procesos propios.
      spawnSync("taskkill", ["/PID", String(pid), "/T", "/F"], { stdio: "ignore" });
    } else {
      process.kill(-pid, "SIGTERM");
    }
    log(`${nombre} detenido`);
  } catch {
    // ya no estaba
  }
}

function nodeBin() {
  return process.execPath;
}

async function up() {
  // 1. Postgres, con esquema y seed. Reutiliza el script del business-api en vez
  //    de duplicar la lógica del clúster.
  log("Postgres…");
  const db = spawnSync(nodeBin(), [LOCAL_DB, "up"], { encoding: "utf8" });
  process.stdout.write(db.stdout ?? "");
  if (db.status !== 0) throw new Error("no se pudo levantar Postgres");

  // 2. Datos de demostración: sin esto el dashboard sale correcto pero en cero,
  //    porque el seed base no trae ventas ni tickets.
  await sembrarDemo();

  // 3. agents-service. No necesita Redis ni clave de Anthropic: ambos son
  //    perezosos y solo se tocan en el chat y en la verificación de stock, que
  //    el dashboard nunca llama. Lo único que exige al arrancar es Postgres.
  if (!(await puerto(PUERTOS.agents))) {
    asegurarVenv();
    log("agents-service…");
    lanzar("agents", PY, ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], AGENTS);
    if (!(await esperar(PUERTOS.agents))) throw new Error("el agents-service no abrió :8000");
  } else log("agents-service ya estaba arriba");

  // 4. Dashboard.
  if (!(await puerto(PUERTOS.dashboard))) {
    log("dashboard…");
    lanzar("dashboard", nodeBin(), ["node_modules/next/dist/bin/next", "dev"], DASHBOARD);
    if (!(await esperar(PUERTOS.dashboard))) throw new Error("el dashboard no abrió :3000");
  } else log("dashboard ya estaba arriba");

  await status();
}

async function sembrarDemo() {
  const { Client } = await import(
    "file://" + path.join(UNIDAD, "apps/business-api/node_modules/pg/lib/index.js").replace(/\\/g, "/")
  ).then((m) => m.default ?? m);
  const c = new Client({ connectionString: DSN });
  await c.connect();
  try {
    const { rows } = await c.query("SELECT count(*)::int AS n FROM orders");
    if (rows[0].n > 0) {
      log(`datos de demo ya presentes (${rows[0].n} pedidos)`);
      return;
    }
    await c.query(fs.readFileSync(SEED_DEMO, "utf8"));
    log("seed-demo.sql aplicado");
  } finally {
    await c.end();
  }
}

function asegurarVenv() {
  if (fs.existsSync(PY)) return;
  log("creando entorno virtual de Python e instalando dependencias (una sola vez)…");
  const py = spawnSync(WIN ? "python" : "python3", ["-m", "venv", VENV], { stdio: "inherit" });
  if (py.status !== 0) throw new Error("no se pudo crear el entorno virtual");
  const pip = spawnSync(
    PY,
    ["-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", "requirements.txt"],
    { cwd: AGENTS, stdio: "inherit" },
  );
  if (pip.status !== 0) throw new Error("falló el pip install del agents-service");
}

async function status() {
  console.log("");
  for (const [nombre, p] of Object.entries(PUERTOS)) {
    console.log(`  ${(await puerto(p)) ? "✓" : "✗"}  ${nombre.padEnd(10)} :${p}`);
  }
  // La prueba que importa: una sola petición que atraviesa los tres.
  try {
    const r = await fetch("http://127.0.0.1:3000/api/agents/kpis/resumen");
    const j = await r.json();
    console.log(
      `\n  cadena dashboard -> agents -> postgres: ${r.status}\n` +
        `  ventas_hoy=${j.ventas_hoy}  tickets=${j.tickets_abiertos}  sugerencias=${j.sugerencias_pendientes}`,
    );
    console.log("\n  → http://localhost:3000");
  } catch (e) {
    console.log(`\n  cadena rota: ${e.message}`);
  }
}

/** Quién está escuchando en un puerto. Respaldo para cuando no hay PID anotado. */
function pidPorPuerto(p) {
  if (!WIN) return null;
  const r = spawnSync(
    "powershell",
    [
      "-NoProfile",
      "-Command",
      `(Get-NetTCPConnection -LocalPort ${p} -State Listen -ErrorAction SilentlyContinue | ` +
        `Select-Object -First 1).OwningProcess`,
    ],
    { encoding: "utf8", windowsHide: true },
  );
  const n = parseInt((r.stdout ?? "").trim(), 10);
  return Number.isNaN(n) ? null : n;
}

async function down() {
  const pids = leerPids();
  matar("dashboard", pids.dashboard);
  matar("agents", pids.agents);

  // Si un `up` se interrumpió antes de anotar el PID, el servicio queda vivo y
  // huérfano. Se le busca por el puerto, que es lo que sí sabemos con certeza.
  for (const [nombre, p] of [
    ["dashboard", PUERTOS.dashboard],
    ["agents", PUERTOS.agents],
  ]) {
    if (await puerto(p)) matar(`${nombre} (huérfano en :${p})`, pidPorPuerto(p));
  }

  fs.rmSync(ESTADO, { force: true });
  spawnSync(nodeBin(), [LOCAL_DB, "down"], { stdio: "inherit" });
}

const acciones = { up, down, status };
const accion = process.argv[2] ?? "up";
if (!acciones[accion]) {
  console.error(`uso: stack.mjs [${Object.keys(acciones).join("|")}]`);
  process.exit(2);
}
acciones[accion]().catch((e) => {
  console.error(`[stack] ERROR: ${e.message}`);
  process.exit(1);
});
