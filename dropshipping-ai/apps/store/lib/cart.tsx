"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { Producto } from "./api";

export type ItemCarrito = {
  id: string;
  nombre: string;
  precio: number;
  cantidad: number;
};

type CartCtx = {
  items: ItemCarrito[];
  total: number;
  unidades: number;
  abierto: boolean;
  setAbierto: (v: boolean) => void;
  agregar: (p: Producto) => void;
  quitar: (id: string) => void;
  cambiarCantidad: (id: string, cantidad: number) => void;
  vaciar: () => void;
};

const Ctx = createContext<CartCtx | null>(null);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ItemCarrito[]>([]);
  const [abierto, setAbierto] = useState(false);

  useEffect(() => {
    try {
      const guardado = localStorage.getItem("carrito");
      if (guardado) setItems(JSON.parse(guardado));
    } catch {
      /* carrito corrupto: se parte de cero */
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("carrito", JSON.stringify(items));
  }, [items]);

  const agregar = useCallback((p: Producto) => {
    setItems((prev) => {
      const existente = prev.find((i) => i.id === p.id);
      if (existente) {
        return prev.map((i) => (i.id === p.id ? { ...i, cantidad: i.cantidad + 1 } : i));
      }
      return [...prev, { id: p.id, nombre: p.nombre, precio: Number(p.precio_venta), cantidad: 1 }];
    });
    setAbierto(true);
  }, []);

  const quitar = useCallback(
    (id: string) => setItems((prev) => prev.filter((i) => i.id !== id)),
    [],
  );

  const cambiarCantidad = useCallback(
    (id: string, cantidad: number) =>
      setItems((prev) =>
        cantidad < 1
          ? prev.filter((i) => i.id !== id)
          : prev.map((i) => (i.id === id ? { ...i, cantidad } : i)),
      ),
    [],
  );

  const vaciar = useCallback(() => setItems([]), []);

  const value = useMemo(
    () => ({
      items,
      total: items.reduce((s, i) => s + i.precio * i.cantidad, 0),
      unidades: items.reduce((s, i) => s + i.cantidad, 0),
      abierto,
      setAbierto,
      agregar,
      quitar,
      cambiarCantidad,
      vaciar,
    }),
    [items, abierto, agregar, quitar, cambiarCantidad, vaciar],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useCart(): CartCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useCart debe usarse dentro de <CartProvider>");
  return ctx;
}
