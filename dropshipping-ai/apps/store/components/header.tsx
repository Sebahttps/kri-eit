"use client";

import Link from "next/link";
import { useCart } from "@/lib/cart";

export default function Header() {
  const { unidades, setAbierto } = useCart();
  return (
    <header className="sticky top-0 z-20 border-b border-grid bg-surface/95 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <Link href="/" className="text-lg font-semibold tracking-tight" aria-label="CompAI, ir al inicio">
          comp<span className="versalitas">ai</span>
        </Link>
        <button
          onClick={() => setAbierto(true)}
          className="btn-ghost relative"
          aria-label={`Abrir carrito (${unidades} unidades)`}
        >
          🛒 Carrito
          {unidades > 0 && (
            <span
              className="absolute -right-2 -top-2 flex h-5 min-w-5 items-center justify-center rounded-full px-1 text-xs font-semibold"
              style={{ backgroundColor: "var(--accent)", color: "var(--accent-ink)" }}
            >
              {unidades}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}
