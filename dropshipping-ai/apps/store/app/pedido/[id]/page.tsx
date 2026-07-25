"use client";

import useSWR from "swr";
import {
  clp,
  ESTADO_LEGIBLE,
  fetcher,
  type EventoSeguimiento,
  type PedidoDetalle,
} from "@/lib/api";

const PASOS = [
  "stock_confirmado",
  "oc_emitida",
  "despachado",
  "en_transito",
  "entregado",
] as const;

const AVANCE: Record<string, number> = {
  carrito: -1,
  verificando_stock: -1,
  stock_confirmado: 0,
  pago_pendiente: 0,
  pagado: 0,
  contra_entrega_confirmado: 0,
  oc_emitida: 1,
  despachado: 2,
  en_transito: 3,
  entregado: 4,
  completado: 4,
};

export default function Pedido({ params }: { params: { id: string } }) {
  const { data: pedido, error } = useSWR<PedidoDetalle>(
    `/api/gw/orders/${params.id}`,
    fetcher,
    { refreshInterval: 10000 },
  );
  const { data: seguimiento } = useSWR<{ eventos: EventoSeguimiento[] }>(
    `/api/agents/front-office/pedidos/${params.id}/seguimiento`,
    fetcher,
    { refreshInterval: 10000 },
  );

  if (error) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-6">
        <p className="card text-sm" style={{ color: "var(--status-critical)" }}>
          ⚠ No encontramos ese pedido.
        </p>
      </main>
    );
  }
  if (!pedido) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-6">
        <p className="text-sm text-muted">Cargando tu pedido…</p>
      </main>
    );
  }

  const avance = AVANCE[pedido.status] ?? -1;
  const retractoVigente =
    pedido.limite_retracto_at && new Date(pedido.limite_retracto_at) > new Date();

  return (
    <main className="mx-auto max-w-3xl space-y-6 px-4 py-6">
      <header>
        <h1 className="text-2xl font-semibold">Pedido #{pedido.numero}</h1>
        <p className="text-sm text-ink-2">
          Estado: <strong>{ESTADO_LEGIBLE[pedido.status] ?? pedido.status}</strong>
          {pedido.payment_method === "contra_entrega" && " · pagas al recibir"}
        </p>
      </header>

      <section className="card" aria-label="Progreso del pedido">
        <ol className="grid grid-cols-5 gap-1 text-center text-xs">
          {PASOS.map((paso, i) => (
            <li key={paso} className="space-y-1">
              <div
                className="mx-auto flex h-7 w-7 items-center justify-center rounded-full font-semibold"
                style={
                  i <= avance
                    ? { backgroundColor: "var(--status-good)", color: "#fff" }
                    : { backgroundColor: "rgb(var(--grid))", color: "rgb(var(--muted))" }
                }
              >
                {i <= avance ? "✓" : i + 1}
              </div>
              <p className={i <= avance ? "" : "text-muted"}>{ESTADO_LEGIBLE[paso]}</p>
            </li>
          ))}
        </ol>
        {pedido.stock_confirmado_at && (
          <p className="mt-3 text-xs" style={{ color: "var(--delta-good)" }}>
            ✔ Stock confirmado con el proveedor el{" "}
            {new Date(pedido.stock_confirmado_at).toLocaleString("es-CL")} — recién
            entonces se habilitó tu pago.
          </p>
        )}
      </section>

      <section className="card space-y-1" aria-label="Detalle de productos">
        {pedido.items.map((i, idx) => (
          <p key={idx} className="flex justify-between text-sm">
            <span>
              {i.nombre} × {i.cantidad}
            </span>
            <span className="tabular">{clp.format(Number(i.precio_unitario) * i.cantidad)}</span>
          </p>
        ))}
        <p className="flex justify-between border-t border-grid pt-2 font-semibold">
          <span>Total</span>
          <span className="tabular">{clp.format(Number(pedido.total))}</span>
        </p>
      </section>

      <section className="card" aria-label="Seguimiento del despacho">
        <h2 className="text-sm font-medium text-ink-2">Seguimiento en tiempo real</h2>
        {pedido.tracking_number ? (
          <>
            <p className="mt-1 text-sm">
              {pedido.carrier} · {pedido.tracking_number}
              {pedido.tracking_url && (
                <>
                  {" · "}
                  <a
                    className="underline"
                    style={{ color: "var(--series-1)" }}
                    href={pedido.tracking_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    ver en el courier
                  </a>
                </>
              )}
            </p>
            <ul className="mt-3 space-y-2 text-sm">
              {(seguimiento?.eventos ?? []).map((e, i) => (
                <li key={i} className="flex gap-3">
                  <span className="tabular shrink-0 text-xs text-muted">
                    {new Date(e.ocurrido_at).toLocaleString("es-CL")}
                  </span>
                  <span>
                    {e.descripcion}
                    {e.ubicacion && <span className="text-muted"> · {e.ubicacion}</span>}
                  </span>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p className="mt-1 text-sm text-muted">
            Tu número de seguimiento aparecerá aquí apenas el proveedor despache.
            Esta página se actualiza sola.
          </p>
        )}
      </section>

      <section className="card text-sm" aria-label="Garantías y retracto">
        <h2 className="text-sm font-medium text-ink-2">Tus garantías</h2>
        <ul className="mt-2 space-y-1 text-ink-2">
          <li>
            🛡 Garantía legal de <strong>6 meses</strong>
            {pedido.entregado_at
              ? ` — activa desde el ${new Date(pedido.entregado_at).toLocaleDateString("es-CL")}`
              : " — se activa automáticamente al recibir"}
            .
          </li>
          <li>
            ↩ Derecho a retracto de <strong>10 días</strong>
            {pedido.limite_retracto_at
              ? retractoVigente
                ? ` — vigente hasta el ${new Date(pedido.limite_retracto_at).toLocaleDateString("es-CL")}`
                : " — plazo vencido"
              : " — corre desde la entrega"}
            .
          </li>
        </ul>
        <p className="mt-2 text-xs text-muted">
          Para ejercer garantía o retracto, escríbenos por el chat de la esquina:
          el asistente lo gestiona al instante.
        </p>
      </section>
    </main>
  );
}
