#!/usr/bin/env node
/**
 * Maneja el business-api como lo harían la tienda y el dashboard: catálogo,
 * login, ruta protegida y una compra de punta a punta. No es la suite de
 * pruebas: le pega por HTTP al proceso realmente levantado.
 *
 *   node .claude/skills/run-business-api/driver.mjs --start   # lo levanta, lo maneja y lo baja
 *   node .claude/skills/run-business-api/driver.mjs           # contra uno ya corriendo
 *
 * Requiere la base arriba (local-db.mjs up). Sale con código 1 si algo que
 * debería funcionar no funcionó.
 */
import { spawn } from "node:child_process";
import net from "node:net";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const UNIDAD = path.resolve(AQUI, "../../..");
const requerir = createRequire(pathToFileURL(path.join(UNIDAD, "package.json")));

const PUERTO = Number(process.env.PORT ?? 4000);
const API = `http://127.0.0.1:${PUERTO}`;
const DSN =
  process.env.BUSINESS_DATABASE_URL ??
  "postgresql://dropship:dropship@127.0.0.1:5432/dropship";
const AGENTES = Number(process.env.AGENTS_PORT ?? 8000);

const CRED = { email: "supervisor@example.invalid", password: "clave-local-1234" };

let fallos = 0;
let saltados = 0;

function puertoAbierto(puerto) {
  return new Promise((res) => {
    const s = net.connect({ host: "127.0.0.1", port: puerto });
    s.on("connect", () => (s.destroy(), res(true)));
    s.on("error", () => res(false));
    s.setTimeout(1000, () => (s.destroy(), res(false)));
  });
}

async function esperarPuerto(puerto, { intentos = 60, muerto = () => false } = {}) {
  for (let i = 0; i < intentos; i++) {
    if (await puertoAbierto(puerto)) return true;
    if (muerto()) return false; // el proceso ya cayó: no tiene sentido seguir esperando
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

async function pedir(metodo, ruta, { body, token, espera, nota } = {}) {
  const r = await fetch(API + ruta, {
    method: metodo,
    headers: {
      ...(body ? { "content-type": "application/json" } : {}),
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const texto = await r.text();
  let cuerpo;
  try {
    cuerpo = JSON.parse(texto);
  } catch {
    cuerpo = texto;
  }
  const ok = espera === undefined || (Array.isArray(espera) ? espera : [espera]).includes(r.status);
  if (!ok) fallos++;
  const marca = espera === undefined ? "    " : ok ? " ok " : "FALLA";
  console.log(`[${marca}] ${r.status} ${metodo} ${ruta}${nota ? `  (${nota})` : ""}`);
  console.log("          " + JSON.stringify(cuerpo).slice(0, 220));
  return { status: r.status, body: cuerpo };
}

/**
 * El seed deja al supervisor con password_hash = 'BLOQUEADO-…' a propósito, así
 * que ninguna clave entra. Se le pone una utilizable solo en la base local.
 */
async function sembrarClaveSupervisor() {
  const { Client } = requerir("pg");
  const { hash } = requerir("bcryptjs");
  const c = new Client({ connectionString: DSN });
  await c.connect();
  const r = await c.query("UPDATE supervisors SET password_hash = $1 WHERE email = $2", [
    await hash(CRED.password, 10),
    CRED.email,
  ]);
  await c.end();
  if (r.rowCount !== 1) throw new Error("no se encontró el supervisor del seed; ¿falta el seed?");
  console.log(`[ ok ] clave local puesta a ${CRED.email}`);
}

async function manejar() {
  await sembrarClaveSupervisor();

  console.log("\n=== 1. Salud y catálogo (público) ===");
  const salud = await pedir("GET", "/health", { espera: 200 });
  if (salud.body?.db !== true) {
    fallos++;
    console.log("[FALLA] el health no reporta db:true");
  }
  await pedir("GET", "/products/categorias", { espera: 200 });
  const productos = await pedir("GET", "/products?limite=3", { espera: 200 });

  console.log("\n=== 2. Autenticación ===");
  await pedir("POST", "/auth/login", {
    body: { email: "no-es-un-email", password: "corta" },
    espera: 400,
    nota: "ValidationPipe",
  });
  await pedir("POST", "/auth/login", {
    body: { ...CRED, password: "clave-equivocada" },
    espera: 401,
  });
  const login = await pedir("POST", "/auth/login", { body: CRED, espera: 201 });
  const token = login.body?.access_token;
  if (!token) throw new Error("el login no devolvió access_token");

  console.log("\n=== 3. Ruta protegida ===");
  await pedir("GET", "/orders?limite=3", { espera: 401, nota: "sin token" });
  await pedir("GET", "/orders?limite=3", { token, espera: 200, nota: "con token" });

  console.log("\n=== 4. Compra de punta a punta ===");
  const lista = Array.isArray(productos.body) ? productos.body : [];
  if (!lista.length) throw new Error("catálogo vacío; ¿se aplicó el seed?");
  const prod = lista[0];
  console.log(`          producto: ${prod.nombre} (${prod.precio_venta})`);
  const pedido = await pedir("POST", "/orders", {
    body: {
      cliente: { nombre: "Cliente de prueba", email: "prueba@example.invalid" },
      items: [{ product_id: prod.id, cantidad: 2 }],
    },
    espera: 201,
  });
  const id = pedido.body?.order_id;
  if (!id) throw new Error("POST /orders no devolvió order_id");

  await pedir("POST", `/orders/${id}/pay`, {
    espera: 422,
    nota: "pagar antes del checkout debe rechazarse",
  });

  // El checkout llama al agents-service para confirmar stock con el proveedor.
  if (await puertoAbierto(AGENTES)) {
    await pedir("POST", `/orders/${id}/checkout`, {
      body: { payment_method: "contra_entrega" },
      espera: [200, 201],
    });
    await pedir("POST", `/orders/${id}/pay`, { espera: [200, 201] });
  } else {
    saltados++;
    console.log(`\n[SALTO] agents-service no está en :${AGENTES}: el checkout no puede completarse.`);
    const r = await pedir("POST", `/orders/${id}/checkout`, {
      body: { payment_method: "contra_entrega" },
      nota: "sin agents-service",
    });
    if (r.status === 500) {
      console.log(
        "          conocido: el fetch al agents-service lanza y sale un 500 pelado,\n" +
          "          mientras que un error HTTP del mismo servicio sí da 422 (orders.service.ts:87).",
      );
    }
  }

  await pedir("GET", `/orders/${id}`, { espera: 200, nota: "detalle del pedido" });
  await pedir("GET", "/orders?limite=3", { token, espera: 200, nota: "el supervisor lo ve" });
}

(async () => {
  let api = null;
  if (process.argv.includes("--start")) {
    console.log(`[api] levantando node dist/main.js en :${PUERTO}…`);
    api = spawn(process.execPath, ["dist/main.js"], {
      cwd: UNIDAD,
      env: { ...process.env, PORT: String(PUERTO), BUSINESS_DATABASE_URL: DSN },
      stdio: ["ignore", "inherit", "inherit"],
    });
    let cayo = false;
    api.on("exit", (c) => {
      cayo = true;
      if (c !== null && c !== 0) console.log(`[api] el proceso murió con código ${c}`);
    });
    if (!(await esperarPuerto(PUERTO, { muerto: () => cayo }))) {
      throw new Error(
        `el API no abrió :${PUERTO}. Sin base en 5432 el proceso muere en el arranque ` +
          "(RealtimeGateway.onModuleInit); corre local-db.mjs up primero.",
      );
    }
  } else if (!(await puertoAbierto(PUERTO))) {
    throw new Error(`no hay nada escuchando en :${PUERTO}; usa --start o levántalo aparte`);
  }

  try {
    await manejar();
  } finally {
    if (api) api.kill();
  }

  console.log(
    `\n=== ${fallos === 0 ? "TODO OK" : `${fallos} FALLO(S)`}` +
      `${saltados ? `, ${saltados} salto(s)` : ""} ===`,
  );
  process.exit(fallos === 0 ? 0 : 1);
})().catch((e) => {
  console.error(`\n[driver] ERROR: ${e.message}`);
  process.exit(1);
});
