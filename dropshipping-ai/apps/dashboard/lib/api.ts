// Cliente de la API de agentes (proxy /api/agents → agents-service, ver next.config.mjs)

export type Resumen = {
  ventas_hoy: number;
  pedidos_hoy: number;
  conversion_hoy_pct: number;
  tickets_abiertos: number;
  tickets_resueltos_24h: number;
  horas_promedio_resolucion: number;
  sugerencias_pendientes: number;
  stock_latencia_media_ms: number;
  stock_checks_24h: number;
};

export type PuntoVenta = { dia: string; ventas: number; pedidos: number; conversion_pct: number };

export type Tendencia = {
  id: string;
  nombre: string;
  categoria: string;
  trending_score: number;
  margen_pct: number;
  ventas_7d: number;
  ventas_30d: number;
};

export type Ticket = {
  numero: number;
  asunto: string;
  status: string;
  prioridad: number;
  created_at: string;
  cliente: string | null;
};

export type Sugerencia = {
  id: string;
  agente: string;
  tipo: string;
  titulo: string;
  detalle: Record<string, unknown>;
  status: string;
  created_at: string;
};

export const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} en ${url}`);
  return res.json();
};

export async function decidirSugerencia(
  id: string,
  decision: "aprobar" | "rechazar",
  supervisorId: string,
) {
  const res = await fetch(`/api/agents/aprobaciones/${id}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, supervisor_id: supervisorId }),
  });
  if (!res.ok) throw new Error(`Error ${res.status} al decidir la sugerencia`);
  return res.json();
}

export const clp = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  maximumFractionDigits: 0,
});
