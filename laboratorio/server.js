// Laboratorio de consultas — estudio KRI-EIT
// Servidor mínimo: login con contraseña única + chat en vivo con los agentes.
// Variables de entorno requeridas: ANTHROPIC_API_KEY, LAB_PASSWORD.
// Opcional: SESSION_SECRET (si no, se genera al arrancar), PORT (3000).

const express = require("express");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const Anthropic = require("@anthropic-ai/sdk");

const PORT = process.env.PORT || 3000;
const LAB_PASSWORD = process.env.LAB_PASSWORD;
const SESSION_SECRET =
  process.env.SESSION_SECRET || crypto.randomBytes(32).toString("hex");
const MODEL = process.env.LAB_MODEL || "claude-opus-4-8";

if (!LAB_PASSWORD) {
  console.error("Falta la variable de entorno LAB_PASSWORD. Sin contraseña no hay laboratorio.");
  process.exit(1);
}
if (!process.env.ANTHROPIC_API_KEY) {
  console.error("Falta ANTHROPIC_API_KEY. Consíguela en platform.claude.com y cárgale crédito.");
  process.exit(1);
}

const anthropic = new Anthropic();

// ---- Los agentes del estudio: cada uno con su prompt maestro real ----
const REPO_ROOT = path.join(__dirname, "..");
const AGENT_DEFS = [
  { slug: "kri-ai",  nombre: "Kri-AI",   rol: "Creativo de negocios esenciales",        color: "#E8853C", dir: "asistente-creativo" },
  { slug: "gain",    nombre: "GAIn",     rol: "Gerente comercial · guardián de la caja", color: "#37D99A", dir: "asistente-comercial" },
  { slug: "admain",  nombre: "AdmAIn",   rol: "Administración y finanzas",               color: "#3E5C76", dir: "asistente-administrativo" },
  { slug: "laier",   nombre: "LAI-er",   rol: "Abogado estratega · Chile",               color: "#C9A24B", dir: "asistente-legal" },
  { slug: "visuai",  nombre: "VisuAI",   rol: "Director de arte",                        color: "#FF5EB1", dir: "asistente-visual" },
  { slug: "clainte", nombre: "ClAI-nte", rol: "El cliente · la mirada que paga",         color: "#C23B3B", dir: "asistente-cliente" },
];

const AGENTS = {};
for (const def of AGENT_DEFS) {
  const promptPath = path.join(REPO_ROOT, def.dir, "PROMPT.md");
  try {
    AGENTS[def.slug] = { ...def, system: fs.readFileSync(promptPath, "utf8") };
  } catch (err) {
    console.warn(`Aviso: no encontré ${promptPath}; el agente ${def.nombre} queda fuera.`);
  }
}
if (Object.keys(AGENTS).length === 0) {
  console.error("Ningún PROMPT.md encontrado. ¿Está el laboratorio dentro del repo kri-eit?");
  process.exit(1);
}

// ---- Sesión: cookie firmada con HMAC, un solo usuario ----
const sessionToken = crypto
  .createHmac("sha256", SESSION_SECRET)
  .update("kri-eit-laboratorio")
  .digest("hex");

function isAuthed(req) {
  const cookies = req.headers.cookie || "";
  const match = cookies.match(/(?:^|;\s*)lab=([^;]+)/);
  if (!match) return false;
  const token = Buffer.from(match[1]);
  const expected = Buffer.from(sessionToken);
  return token.length === expected.length && crypto.timingSafeEqual(token, expected);
}

const app = express();
app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

app.post("/api/login", (req, res) => {
  const given = Buffer.from(String(req.body?.password || ""));
  const expected = Buffer.from(LAB_PASSWORD);
  const ok =
    given.length === expected.length && crypto.timingSafeEqual(given, expected);
  if (!ok) return res.status(401).json({ error: "Contraseña incorrecta." });
  const secure = process.env.NODE_ENV === "production" ? "; Secure" : "";
  res.setHeader(
    "Set-Cookie",
    `lab=${sessionToken}; HttpOnly; SameSite=Lax; Path=/; Max-Age=2592000${secure}`
  );
  res.json({ ok: true });
});

app.post("/api/logout", (_req, res) => {
  res.setHeader("Set-Cookie", "lab=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0");
  res.json({ ok: true });
});

app.get("/api/session", (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ ok: false });
  res.json({
    ok: true,
    model: MODEL,
    agents: Object.values(AGENTS).map(({ slug, nombre, rol, color }) => ({
      slug, nombre, rol, color,
    })),
  });
});

// ---- El chat: streaming de texto plano hacia el navegador ----
app.post("/api/chat", async (req, res) => {
  if (!isAuthed(req)) return res.status(401).json({ error: "Sin sesión." });

  const agent = AGENTS[req.body?.agent];
  if (!agent) return res.status(400).json({ error: "Agente desconocido." });

  const raw = Array.isArray(req.body?.messages) ? req.body.messages : [];
  const messages = raw
    .filter(
      (m) =>
        m && (m.role === "user" || m.role === "assistant") &&
        typeof m.content === "string" && m.content.trim().length > 0
    )
    .slice(-40) // las últimas 40 vueltas bastan; controla costo y contexto
    .map((m) => ({ role: m.role, content: m.content }));

  if (messages.length === 0 || messages[messages.length - 1].role !== "user") {
    return res.status(400).json({ error: "La consulta viene vacía." });
  }

  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("X-Accel-Buffering", "no");

  try {
    const stream = anthropic.messages.stream({
      model: MODEL,
      max_tokens: 16000,
      thinking: { type: "adaptive" },
      system: agent.system,
      messages,
    });
    stream.on("text", (delta) => res.write(delta));
    await stream.finalMessage();
    res.end();
  } catch (err) {
    console.error("Error en /api/chat:", err.message);
    if (!res.headersSent) {
      res.status(502).json({ error: "El agente no pudo responder. Revisa el crédito de la API y reintenta." });
    } else {
      res.write("\n\n[Se cortó la respuesta — reintenta la consulta.]");
      res.end();
    }
  }
});

app.listen(PORT, () => {
  console.log(`Laboratorio KRI-EIT en http://localhost:${PORT}`);
  console.log(`Agentes cargados: ${Object.values(AGENTS).map((a) => a.nombre).join(", ")}`);
  console.log(`Modelo: ${MODEL}`);
});
