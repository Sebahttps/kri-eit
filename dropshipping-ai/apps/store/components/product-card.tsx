"use client";

import { clp, type Producto } from "@/lib/api";
import { useCart } from "@/lib/cart";

// Sin catálogo de imágenes aún: un monograma por categoría mantiene la
// tarjeta visual sin inventar fotos.
const EMOJI_CATEGORIA: Record<string, string> = {
  hogar: "🏠",
  tecnología: "🎧",
  iluminación: "💡",
};

export default function ProductCard({ producto }: { producto: Producto }) {
  const { agregar } = useCart();
  const enTendencia = Number(producto.trending_score) >= 80;

  return (
    <article className="card flex flex-col gap-3">
      <div
        className="flex h-28 items-center justify-center rounded-lg text-5xl"
        style={{ backgroundColor: "rgb(var(--grid) / 0.4)" }}
        aria-hidden
      >
        {EMOJI_CATEGORIA[producto.categoria] ?? "📦"}
      </div>
      <div className="flex-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-medium leading-snug">{producto.nombre}</h3>
          {enTendencia && (
            <span
              className="shrink-0 rounded-full px-2 py-0.5 text-xs font-medium"
              style={{ backgroundColor: "var(--accent)", color: "var(--accent-ink)" }}
            >
              🔥 tendencia
            </span>
          )}
        </div>
        <p className="mt-1 text-xs text-muted">{producto.categoria}</p>
        {producto.descripcion && (
          <p className="mt-2 text-sm text-ink-2">{producto.descripcion}</p>
        )}
      </div>
      <div className="flex items-center justify-between">
        <span className="tabular text-lg font-semibold">
          {clp.format(Number(producto.precio_venta))}
        </span>
        <button className="btn-accent" onClick={() => agregar(producto)}>
          Agregar
        </button>
      </div>
    </article>
  );
}
