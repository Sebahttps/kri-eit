#!/usr/bin/env node
/**
 * Postgres local y desechable para correr el business-api sin Docker.
 *
 * Por qué existe: el API no arranca sin una base en 5432 (RealtimeGateway abre
 * un cliente pg en onModuleInit y su rechazo tumba el proceso). En una máquina
 * con Docker eso lo resuelve infra/docker-compose.yml. Este script es para la
 * máquina que no lo tiene: baja los binarios de Postgres vía npm, crea un
 * clúster en el directorio temporal del sistema y le aplica el esquema.
 *
 *   node .claude/skills/run-business-api/local-db.mjs up      # deja la base lista
 *   node .claude/skills/run-business-api/local-db.mjs down    # la detiene
 *   node .claude/skills/run-business-api/local-db.mjs reset   # borra datos y reaplica
 *   node .claude/skills/run-business-api/local-db.mjs nuke    # borra el clúster entero
 *
 * Nada de esto toca el repo: el clúster vive fuera del árbol de trabajo.
 */
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const UNIDAD = path.resolve(AQUI, "../../.."); // apps/business-api
const REPO_DB = path.resolve(UNIDAD, "../../db"); // dropshipping-ai/db

// pg vive en las dependencias del propio API; no se instala nada en el repo.
const requerir = createRequire(pathToFileURL(path.join(UNIDAD, "package.json")));

const BASE = path.join(os.tmpdir(), "kri-eit-business-api-db");
const DATA = path.join(BASE, "data");
const LOG = path.join(BASE, "pg.log");
const EXE = process.platform === "win32" ? ".exe" : "";
const PUERTO = 5432;
const USUARIO = "dropship";
const CLAVE = "dropship";
const BASE_DATOS = "dropship";

// 127.0.0.1 y no localhost: en Windows localhost resuelve a ::1 primero y el
// clúster solo escucha en IPv4.
export const DSN = `postgresql://${USUARIO}:${CLAVE}@127.0.0.1:${PUERTO}/${BASE_DATOS}`;

const log = (m) => console.log(`[db] ${m}`);

function binarios() {
  const raiz = path.join(BASE, "node_modules", "@embedded-postgres");
  if (!fs.existsSync(raiz)) return null;
  // El paquete instala solo el subpaquete de la plataforma actual.
  for (const d of fs.readdirSync(raiz)) {
    const bin = path.join(raiz, d, "native", "bin");
    if (fs.existsSync(path.join(bin, `postgres${EXE}`))) return bin;
  }
  return null;
}

function asegurarBinarios() {
  let bin = binarios();
  if (bin) return bin;
  log("descargando binarios de Postgres (una sola vez, ~200 MB)…");
  fs.mkdirSync(BASE, { recursive: true });
  // package.json propio para que npm no escale hasta el package.json del repo.
  fs.writeFileSync(
    path.join(BASE, "package.json"),
    JSON.stringify({ name: "business-api-local-db", private: true, version: "1.0.0" }),
  );
  const r = spawnSync("npm", ["install", "embedded-postgres", "--no-audit", "--no-fund"], {
    cwd: BASE,
    shell: true,
    stdio: "inherit",
  });
  if (r.status !== 0) throw new Error("npm install de embedded-postgres falló");
  bin = binarios();
  // npm >= 11 no ejecuta el postinstall del paquete (allow-scripts). En Windows
  // ese postinstall solo rehace symlinks y los .exe ya vienen usables.
  if (!bin) throw new Error("no aparecieron los binarios de Postgres tras el install");
  return bin;
}

function asegurarCluster(bin) {
  if (fs.existsSync(path.join(DATA, "PG_VERSION"))) return;
  log("creando el clúster…");
  const pw = path.join(BASE, "pw.txt");
  fs.writeFileSync(pw, CLAVE);
  try {
    const r = spawnSync(
      path.join(bin, `initdb${EXE}`),
      ["-D", DATA, "-U", USUARIO, `--pwfile=${pw}`, "-E", "UTF8", "--locale=C", "-A", "md5"],
      { stdio: "inherit" },
    );
    if (r.status !== 0) throw new Error("initdb falló");
  } finally {
    fs.rmSync(pw, { force: true });
  }
}

async function conectar(db, reintentos = 1) {
  const { Client } = requerir("pg");
  for (let i = 0; i < reintentos; i++) {
    const c = new Client({
      connectionString: `postgresql://${USUARIO}:${CLAVE}@127.0.0.1:${PUERTO}/${db}`,
    });
    try {
      await c.connect();
      return c;
    } catch (e) {
      await c.end().catch(() => {});
      if (i === reintentos - 1) throw e;
      await new Promise((r) => setTimeout(r, 500));
    }
  }
}

async function vivo() {
  try {
    const c = await conectar("postgres");
    await c.end();
    return true;
  } catch {
    return false;
  }
}

async function arrancar(bin) {
  if (await vivo()) {
    log("ya estaba corriendo");
    return;
  }
  // Detached y con la salida a un archivo: si el proceso hereda los handles del
  // shell, el shell se queda colgado esperando a que el demonio termine.
  const salida = fs.openSync(LOG, "a");
  const p = spawn(
    path.join(bin, `postgres${EXE}`),
    ["-D", DATA, "-p", String(PUERTO), "-c", "listen_addresses=127.0.0.1"],
    { detached: true, stdio: ["ignore", salida, salida] },
  );
  p.unref();
  const c = await conectar("postgres", 60);
  await c.end();
  log(`Postgres escuchando en 127.0.0.1:${PUERTO} (log: ${LOG})`);
}

async function asegurarBaseDatos() {
  const c = await conectar("postgres");
  try {
    await c.query(`CREATE DATABASE ${BASE_DATOS}`);
    log(`base '${BASE_DATOS}' creada`);
    return true; // recién creada -> hay que aplicar el esquema
  } catch (e) {
    if (e.code !== "42P04") throw e; // duplicate_database
    return false;
  } finally {
    await c.end();
  }
}

function archivosSql() {
  const migraciones = fs
    .readdirSync(path.join(REPO_DB, "migrations"))
    .filter((f) => f.endsWith(".sql"))
    .sort()
    .map((f) => path.join(REPO_DB, "migrations", f));
  return [path.join(REPO_DB, "schema.sql"), ...migraciones, path.join(REPO_DB, "seed.sql")];
}

async function aplicarEsquema() {
  const c = await conectar(BASE_DATOS);
  try {
    for (const f of archivosSql()) {
      // El archivo entero como una sola query: pg lo manda en modo simple, que
      // acepta varias sentencias y no se traga los cuerpos $$ de las funciones.
      await c.query(fs.readFileSync(f, "utf8"));
      log(`aplicado ${path.basename(f)}`);
    }
  } finally {
    await c.end();
  }
}

async function up() {
  const bin = asegurarBinarios();
  asegurarCluster(bin);
  await arrancar(bin);
  const nueva = await asegurarBaseDatos();
  if (nueva) await aplicarEsquema();
  else log("la base ya tenía esquema (usa 'reset' para rehacerla)");
  console.log(`\nBUSINESS_DATABASE_URL=${DSN}`);
}

async function down() {
  const bin = binarios();
  if (!bin || !fs.existsSync(DATA)) return log("no hay clúster que detener");
  spawnSync(path.join(bin, `pg_ctl${EXE}`), ["-D", DATA, "-m", "fast", "stop"], {
    stdio: "inherit",
  });
}

async function reset() {
  const bin = asegurarBinarios();
  asegurarCluster(bin);
  await arrancar(bin);
  const c = await conectar("postgres");
  try {
    await c.query(
      `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = $1`,
      [BASE_DATOS],
    );
    await c.query(`DROP DATABASE IF EXISTS ${BASE_DATOS}`);
    await c.query(`CREATE DATABASE ${BASE_DATOS}`);
  } finally {
    await c.end();
  }
  await aplicarEsquema();
  console.log(`\nBUSINESS_DATABASE_URL=${DSN}`);
}

async function nuke() {
  await down();
  fs.rmSync(BASE, { recursive: true, force: true });
  log(`borrado ${BASE}`);
}

const acciones = { up, down, reset, nuke };
const accion = process.argv[2] ?? "up";
if (!acciones[accion]) {
  console.error(`uso: local-db.mjs [${Object.keys(acciones).join("|")}]`);
  process.exit(2);
}
acciones[accion]().catch((e) => {
  console.error(`[db] ERROR: ${e.message}`);
  process.exit(1);
});
