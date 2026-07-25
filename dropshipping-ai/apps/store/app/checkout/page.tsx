"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Promesas from "@/components/promesas";
import { clp } from "@/lib/api";
import { useCart } from "@/lib/cart";

type Paso = "formulario" | "verificando" | "pagando";

export default function Checkout() {
  const { items, total, vaciar } = useCart();
  const router = useRouter();
  const [paso, setPaso] = useState<Paso>("formulario");
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    nombre: "",
    email: "",
    telefono: "",
    direccion: "",
    payment_method: "contra_entrega" as "online" | "contra_entrega",
  });

  const listo =
    form.nombre.trim().length >= 2 && form.direccion.trim().length >= 5 && items.length > 0;

  async function comprar(e: React.FormEvent) {
    e.preventDefault();
    if (!listo) return;
    setError(null);
    setPaso("verificando");
    try {
      // 1. crear el pedido
      const creado = await fetch("/api/gw/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cliente: {
            nombre: form.nombre,
            email: form.email || undefined,
            telefono: form.telefono || undefined,
            direccion: form.direccion,
          },
          items: items.map((i) => ({ product_id: i.id, cantidad: i.cantidad })),
        }),
      }).then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))));

      // 2. checkout: el Agente B2B confirma stock antes de habilitar el pago
      const checkout = await fetch(`/api/gw/orders/${creado.order_id}/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ payment_method: form.payment_method }),
      }).then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))));

      if (checkout.status === "sin_stock") {
        setPaso("formulario");
        setError(
          "El proveedor no confirmó stock de todos los productos, así que no te cobramos nada. Quita el producto sin stock o inténtalo más tarde.",
        );
        return;
      }

      // 3. pago online (contra entrega ya quedó confirmado en el paso anterior)
      if (form.payment_method === "online") {
        setPaso("pagando");
        await fetch(`/api/gw/orders/${creado.order_id}/pay`, { method: "POST" }).then((r) =>
          r.ok ? r.json() : Promise.reject(new Error(String(r.status))),
        );
      }

      vaciar();
      router.push(`/pedido/${creado.order_id}`);
    } catch {
      setPaso("formulario");
      setError("Algo falló al procesar tu pedido. No se realizó ningún cobro; intenta de nuevo.");
    }
  }

  return (
    <main className="mx-auto max-w-3xl space-y-6 px-4 py-6">
      <h1 className="text-2xl font-semibold">Finalizar compra</h1>

      <section className="card space-y-1" aria-label="Resumen del pedido">
        {items.map((i) => (
          <p key={i.id} className="flex justify-between text-sm">
            <span>
              {i.nombre} × {i.cantidad}
            </span>
            <span className="tabular">{clp.format(i.precio * i.cantidad)}</span>
          </p>
        ))}
        <p className="flex justify-between border-t border-grid pt-2 font-semibold">
          <span>Total</span>
          <span className="tabular">{clp.format(total)}</span>
        </p>
        {items.length === 0 && (
          <p className="text-sm text-muted">Tu carrito está vacío: vuelve al catálogo.</p>
        )}
      </section>

      <form onSubmit={comprar} className="card space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="text-sm">
            Nombre*
            <input
              required
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              className="mt-1 w-full rounded-lg border border-grid bg-plane px-3 py-2"
            />
          </label>
          <label className="text-sm">
            Email
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="mt-1 w-full rounded-lg border border-grid bg-plane px-3 py-2"
            />
          </label>
          <label className="text-sm">
            Teléfono
            <input
              value={form.telefono}
              onChange={(e) => setForm({ ...form, telefono: e.target.value })}
              className="mt-1 w-full rounded-lg border border-grid bg-plane px-3 py-2"
            />
          </label>
          <label className="text-sm">
            Dirección de entrega*
            <input
              required
              value={form.direccion}
              onChange={(e) => setForm({ ...form, direccion: e.target.value })}
              className="mt-1 w-full rounded-lg border border-grid bg-plane px-3 py-2"
            />
          </label>
        </div>

        <fieldset className="space-y-2">
          <legend className="text-sm font-medium">¿Cómo prefieres pagar?</legend>
          <label className="flex items-start gap-2 text-sm">
            <input
              type="radio"
              name="pago"
              checked={form.payment_method === "contra_entrega"}
              onChange={() => setForm({ ...form, payment_method: "contra_entrega" })}
            />
            <span>
              <strong>Contra entrega</strong> — pagas en efectivo o tarjeta cuando
              recibas el producto.
            </span>
          </label>
          <label className="flex items-start gap-2 text-sm">
            <input
              type="radio"
              name="pago"
              checked={form.payment_method === "online"}
              onChange={() => setForm({ ...form, payment_method: "online" })}
            />
            <span>
              <strong>Pago online</strong> — solo se procesa después de confirmar
              stock con el proveedor.
            </span>
          </label>
        </fieldset>

        {error && (
          <p className="text-sm" style={{ color: "var(--status-critical)" }}>
            ⚠ {error}
          </p>
        )}

        <button className="btn-accent w-full" disabled={!listo || paso !== "formulario"}>
          {paso === "verificando"
            ? "Confirmando stock con el proveedor…"
            : paso === "pagando"
              ? "Procesando el pago…"
              : "Confirmar pedido"}
        </button>
        <Promesas compacto />
      </form>
    </main>
  );
}
