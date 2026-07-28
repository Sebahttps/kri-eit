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
        <h1 className="text-2xl font-semibold tracking-tight">
          Te confirmamos el stock antes de cobrarte
        </h1>
        <p className="text-sm text-ink-2">
          Cada promesa de CompAI está programada como regla dura en el sistema:
          no dependen de la buena voluntad de nadie.
        </p>
      </section>

      <Promesas />

      <p className="text-sm text-ink-2">
        Te confirmamos el stock, pagas al recibir y la garantía responde.{" "}
        <span className="font-medium text-ink">Palabra de CompAI.</span>
      </p>

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
