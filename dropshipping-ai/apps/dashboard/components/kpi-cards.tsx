"use client";

import useSWR from "swr";
import { clp, fetcher, type Resumen } from "@/lib/api";

function Tile({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail?: string;
}) {
  return (
    <div className="card">
      <p className="text-sm text-ink-2">{label}</p>
      <p className="mt-1 text-3xl font-semibold">{value}</p>
      {detail && <p className="mt-1 text-xs text-muted">{detail}</p>}
    </div>
  );
}

export default function KpiCards() {
  const { data, error } = useSWR<Resumen>("/api/agents/kpis/resumen", fetcher, {
    refreshInterval: 5000,
  });

  if (error)
    return (
      <div className="card text-sm" style={{ color: "var(--status-critical)" }}>
        ⚠ Sin conexión con el servicio de agentes
      </div>
    );

  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      <Tile
        label="Ventas de hoy"
        value={data ? clp.format(data.ventas_hoy) : "—"}
        detail={data ? `${data.pedidos_hoy} pedidos` : undefined}
      />
      <Tile
        label="Tasa de conversión"
        value={data ? `${data.conversion_hoy_pct.toFixed(1)}%` : "—"}
        detail="pedidos confirmados / iniciados hoy"
      />
      <Tile
        label="Tickets de soporte"
        value={data ? String(data.tickets_abiertos) : "—"}
        detail={
          data
            ? `${data.tickets_resueltos_24h} resueltos en 24 h · ${data.horas_promedio_resolucion} h promedio`
            : undefined
        }
      />
      <Tile
        label="Verificaciones de stock"
        value={data ? `${data.stock_latencia_media_ms} ms` : "—"}
        detail={data ? `${data.stock_checks_24h} consultas en 24 h` : undefined}
      />
    </div>
  );
}
