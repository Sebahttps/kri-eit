"use client";

import useSWR from "swr";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { clp, fetcher, type PuntoVenta } from "@/lib/api";

// Ventas (CLP) y conversión (%) son escalas distintas: dos gráficos
// (small multiples), nunca doble eje.

const tooltipStyle = {
  backgroundColor: "rgb(var(--surface))",
  border: "1px solid rgb(var(--grid))",
  borderRadius: 8,
  fontSize: 12,
  color: "rgb(var(--ink))",
};

function diaCorto(d: string) {
  return d.slice(5); // 'MM-DD'
}

export default function SalesCharts() {
  const { data } = useSWR<PuntoVenta[]>("/api/agents/kpis/ventas?dias=30", fetcher, {
    refreshInterval: 15000,
  });
  const serie = data ?? [];

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="card">
        <h3 className="text-sm font-medium text-ink-2">Ventas · últimos 30 días</h3>
        <div className="mt-3 h-56">
          <ResponsiveContainer>
            <AreaChart data={serie} margin={{ top: 4, right: 4, bottom: 0, left: 4 }}>
              <defs>
                <linearGradient id="ventasFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--series-1)" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="var(--series-1)" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="rgb(var(--grid))" vertical={false} />
              <XAxis
                dataKey="dia"
                tickFormatter={diaCorto}
                tick={{ fill: "rgb(var(--muted))", fontSize: 11 }}
                tickLine={false}
                axisLine={{ stroke: "rgb(var(--grid))" }}
                minTickGap={24}
              />
              <YAxis
                tickFormatter={(v: number) => (v >= 1000 ? `${Math.round(v / 1000)}k` : String(v))}
                tick={{ fill: "rgb(var(--muted))", fontSize: 11 }}
                tickLine={false}
                axisLine={false}
                width={40}
              />
              <Tooltip
                contentStyle={tooltipStyle}
                formatter={(v) => [clp.format(Number(v)), "Ventas"]}
                labelFormatter={(l) => `Día ${l}`}
              />
              <Area
                type="monotone"
                dataKey="ventas"
                stroke="var(--series-1)"
                strokeWidth={2}
                fill="url(#ventasFill)"
                dot={false}
                activeDot={{ r: 4 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h3 className="text-sm font-medium text-ink-2">Tasa de conversión · últimos 30 días</h3>
        <div className="mt-3 h-56">
          <ResponsiveContainer>
            <LineChart data={serie} margin={{ top: 4, right: 4, bottom: 0, left: 4 }}>
              <CartesianGrid stroke="rgb(var(--grid))" vertical={false} />
              <XAxis
                dataKey="dia"
                tickFormatter={diaCorto}
                tick={{ fill: "rgb(var(--muted))", fontSize: 11 }}
                tickLine={false}
                axisLine={{ stroke: "rgb(var(--grid))" }}
                minTickGap={24}
              />
              <YAxis
                domain={[0, 100]}
                tickFormatter={(v: number) => `${v}%`}
                tick={{ fill: "rgb(var(--muted))", fontSize: 11 }}
                tickLine={false}
                axisLine={false}
                width={40}
              />
              <Tooltip
                contentStyle={tooltipStyle}
                formatter={(v) => [`${Number(v).toFixed(1)}%`, "Conversión"]}
                labelFormatter={(l) => `Día ${l}`}
              />
              <Line
                type="monotone"
                dataKey="conversion_pct"
                stroke="var(--series-2)"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
