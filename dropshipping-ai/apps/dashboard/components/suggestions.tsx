"use client";

import { useState } from "react";
import useSWR from "swr";
import { decidirSugerencia, fetcher, type Sugerencia } from "@/lib/api";

const SUPERVISOR_ID =
  process.env.NEXT_PUBLIC_SUPERVISOR_ID ?? "00000000-0000-0000-0000-000000000001";

// Módulo "Sugerencias de la IA": las decisiones críticas que los agentes
// escalan. Aprobar/Rechazar reanuda el grafo LangGraph pausado.
export default function Suggestions() {
  const { data, mutate } = useSWR<Sugerencia[]>(
    "/api/agents/aprobaciones/pendientes",
    fetcher,
    { refreshInterval: 5000 },
  );
  const [ocupada, setOcupada] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function decidir(id: string, decision: "aprobar" | "rechazar") {
    setOcupada(id);
    setError(null);
    try {
      await decidirSugerencia(id, decision, SUPERVISOR_ID);
      await mutate();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al enviar la decisión");
    } finally {
      setOcupada(null);
    }
  }

  const pendientes = data ?? [];

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-ink-2">Sugerencias de la IA</h3>
        {pendientes.length > 0 && (
          <span
            className="rounded-full px-2 py-0.5 text-xs font-medium text-white"
            style={{ backgroundColor: "var(--status-warning)", color: "#0b0b0b" }}
          >
            {pendientes.length} pendiente{pendientes.length !== 1 && "s"}
          </span>
        )}
      </div>

      {error && (
        <p className="mt-2 text-xs" style={{ color: "var(--status-critical)" }}>
          ⚠ {error}
        </p>
      )}

      <ul className="mt-3 space-y-3">
        {pendientes.map((s) => (
          <li
            key={s.id}
            className="rounded-lg p-3"
            style={{ border: "1px solid rgb(var(--grid))" }}
          >
            <p className="text-sm">{s.titulo}</p>
            <p className="mt-1 text-xs text-muted">
              {s.agente === "back_office" ? "Agente Back-Office" : "Agente Front-Office"} ·{" "}
              {s.tipo} · {new Date(s.created_at).toLocaleString("es-CL")}
            </p>
            <div className="mt-3 flex gap-2">
              <button
                onClick={() => decidir(s.id, "aprobar")}
                disabled={ocupada === s.id}
                className="rounded-lg px-3 py-1.5 text-sm font-medium text-white disabled:opacity-50"
                style={{ backgroundColor: "var(--status-good)" }}
              >
                ✓ Aprobar
              </button>
              <button
                onClick={() => decidir(s.id, "rechazar")}
                disabled={ocupada === s.id}
                className="rounded-lg px-3 py-1.5 text-sm font-medium text-white disabled:opacity-50"
                style={{ backgroundColor: "var(--status-critical)" }}
              >
                ✕ Rechazar
              </button>
            </div>
          </li>
        ))}
        {pendientes.length === 0 && (
          <li className="text-sm text-muted">
            Sin decisiones pendientes: los agentes están operando dentro de sus umbrales
            de autonomía.
          </li>
        )}
      </ul>
    </div>
  );
}
