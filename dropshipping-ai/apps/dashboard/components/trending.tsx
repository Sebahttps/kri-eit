"use client";

import useSWR from "swr";
import { fetcher, type Tendencia } from "@/lib/api";

// Barras horizontales por producto: magnitud (trending_score) en una sola
// serie — un solo tono, etiqueta directa del valor, sin leyenda.
export default function Trending() {
  const { data } = useSWR<Tendencia[]>("/api/agents/kpis/tendencias", fetcher, {
    refreshInterval: 30000,
  });
  const items = data ?? [];
  const max = Math.max(1, ...items.map((t) => t.trending_score));

  return (
    <div className="card">
      <h3 className="text-sm font-medium text-ink-2">Tendencias de productos</h3>
      <ul className="mt-3 space-y-3">
        {items.map((t) => (
          <li key={t.id}>
            <div className="flex items-baseline justify-between gap-2 text-sm">
              <span className="truncate">
                {t.nombre}
                <span className="ml-2 text-xs text-muted">{t.categoria}</span>
              </span>
              <span className="tabular shrink-0 text-xs text-ink-2">
                {t.ventas_7d} ventas 7d · margen {t.margen_pct.toFixed(0)}%
              </span>
            </div>
            <div className="mt-1 flex items-center gap-2">
              <div className="h-2 flex-1 overflow-hidden rounded-full bg-grid">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${(t.trending_score / max) * 100}%`,
                    backgroundColor: "var(--series-1)",
                  }}
                />
              </div>
              <span className="tabular w-10 text-right text-xs text-ink-2">
                {t.trending_score.toFixed(0)}
              </span>
            </div>
          </li>
        ))}
        {items.length === 0 && (
          <li className="text-sm text-muted">Aún no hay datos de tendencia.</li>
        )}
      </ul>
    </div>
  );
}
