"use client";

import Link from "next/link";
import { clp } from "@/lib/api";
import { useCart } from "@/lib/cart";

export default function CartDrawer() {
  const { items, total, abierto, setAbierto, quitar, cambiarCantidad } = useCart();
  if (!abierto) return null;

  return (
    <div className="fixed inset-0 z-30" role="dialog" aria-label="Carrito de compras">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={() => setAbierto(false)}
        aria-hidden
      />
      <aside className="absolute right-0 top-0 flex h-full w-full max-w-sm flex-col bg-surface p-5 shadow-xl">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Tu carrito</h2>
          <button className="btn-ghost" onClick={() => setAbierto(false)}>
            Cerrar
          </button>
        </div>

        <ul className="mt-4 flex-1 space-y-3 overflow-y-auto">
          {items.map((i) => (
            <li key={i.id} className="flex items-center justify-between gap-2 text-sm">
              <div className="min-w-0 flex-1">
                <p className="truncate">{i.nombre}</p>
                <p className="tabular text-xs text-muted">{clp.format(i.precio)} c/u</p>
              </div>
              <div className="flex items-center gap-1">
                <button
                  className="btn-ghost px-2 py-1"
                  aria-label={`Quitar una unidad de ${i.nombre}`}
                  onClick={() => cambiarCantidad(i.id, i.cantidad - 1)}
                >
                  −
                </button>
                <span className="tabular w-6 text-center">{i.cantidad}</span>
                <button
                  className="btn-ghost px-2 py-1"
                  aria-label={`Agregar una unidad de ${i.nombre}`}
                  onClick={() => cambiarCantidad(i.id, i.cantidad + 1)}
                >
                  +
                </button>
              </div>
              <button
                className="text-xs text-muted underline"
                onClick={() => quitar(i.id)}
              >
                quitar
              </button>
            </li>
          ))}
          {items.length === 0 && (
            <li className="text-sm text-muted">Tu carrito está vacío.</li>
          )}
        </ul>

        <div className="border-t border-grid pt-4">
          <p className="flex justify-between text-sm">
            <span>Total</span>
            <span className="tabular text-lg font-semibold">{clp.format(total)}</span>
          </p>
          <Link
            href="/checkout"
            onClick={() => setAbierto(false)}
            className={`btn-accent mt-3 block text-center ${items.length === 0 ? "pointer-events-none opacity-50" : ""}`}
          >
            Ir a pagar
          </Link>
          <p className="mt-2 text-center text-xs text-muted">
            Verificamos stock con el proveedor antes de cobrarte.
          </p>
        </div>
      </aside>
    </div>
  );
}
