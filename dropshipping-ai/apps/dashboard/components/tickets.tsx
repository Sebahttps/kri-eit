"use client";

import useSWR from "swr";
import { fetcher, type Ticket } from "@/lib/api";

const PRIORIDAD: Record<number, { label: string; color: string }> = {
  1: { label: "P1 crítica", color: "var(--status-critical)" },
  2: { label: "P2 alta", color: "var(--status-serious)" },
  3: { label: "P3 media", color: "var(--status-warning)" },
  4: { label: "P4 baja", color: "var(--status-good)" },
  5: { label: "P5 mínima", color: "var(--status-good)" },
};

export default function Tickets() {
  const { data } = useSWR<Ticket[]>("/api/agents/kpis/tickets", fetcher, {
    refreshInterval: 10000,
  });
  const tickets = data ?? [];

  return (
    <div className="card">
      <h3 className="text-sm font-medium text-ink-2">Tickets abiertos</h3>
      <ul className="mt-3 space-y-2">
        {tickets.map((t) => {
          const p = PRIORIDAD[t.prioridad] ?? PRIORIDAD[3];
          return (
            <li
              key={t.numero}
              className="flex items-center justify-between gap-3 rounded-lg px-3 py-2"
              style={{ border: "1px solid rgb(var(--grid))" }}
            >
              <div className="min-w-0">
                <p className="truncate text-sm">
                  #{t.numero} · {t.asunto}
                </p>
                <p className="text-xs text-muted">
                  {t.cliente ?? "Cliente sin identificar"} · {t.status.replace("_", " ")}
                </p>
              </div>
              <span
                className="flex shrink-0 items-center gap-1 text-xs font-medium"
                style={{ color: p.color }}
              >
                <span aria-hidden>●</span> {p.label}
              </span>
            </li>
          );
        })}
        {tickets.length === 0 && (
          <li className="text-sm text-muted">
            Sin tickets abiertos: el Agente Front-Office está al día.
          </li>
        )}
      </ul>
    </div>
  );
}
