"use client";

import useSWR from "swr";
import ProductCard from "@/components/product-card";
import Promesas from "@/components/promesas";
import { fetcher, type Producto } from "@/lib/api";

export default function Catalogo() {
  const { data, error } = useSWR<Producto[]>("/api/gw/products", fetcher);

  return (
    <main className="mx-auto max-w-5xl space-y-6 px-4 py-6">
      <section className="space-y-2">
        <h1 className="text-2xl font-semibold">
          Productos en tendencia, promesas que se cumplen solas
        </h1>
        <p className="text-sm text-ink-2">
          Cada promesa de esta tienda está programada en el sistema: no dependemos
          de la buena voluntad de nadie.
        </p>
      </section>

      <Promesas />

      {error && (
        <p className="card text-sm" style={{ color: "var(--status-critical)" }}>
          ⚠ No pudimos cargar el catálogo. Intenta de nuevo en unos segundos.
        </p>
      )}

      <section
        className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        aria-label="Catálogo de productos"
      >
        {(data ?? []).map((p) => (
          <ProductCard key={p.id} producto={p} />
        ))}
      </section>
    </main>
  );
}
