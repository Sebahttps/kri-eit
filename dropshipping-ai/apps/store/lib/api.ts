export type Producto = {
  id: string;
  nombre: string;
  descripcion: string | null;
  categoria: string;
  precio_venta: string | number;
  trending_score: string | number;
};

export type PedidoDetalle = {
  id: string;
  numero: number;
  status: string;
  payment_method: string | null;
  payment_status: string;
  total: string | number;
  stock_confirmado_at: string | null;
  entregado_at: string | null;
  limite_retracto_at: string | null;
  created_at: string;
  cliente: string;
  carrier: string | null;
  tracking_number: string | null;
  tracking_url: string | null;
  envio_status: string | null;
  items: { cantidad: number; precio_unitario: string; nombre: string }[];
};

export type EventoSeguimiento = {
  status: string;
  descripcion: string;
  ubicacion: string | null;
  ocurrido_at: string;
};

export const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} en ${url}`);
  return res.json();
};

export const clp = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
  maximumFractionDigits: 0,
});

export const ESTADO_LEGIBLE: Record<string, string> = {
  carrito: "En carrito",
  verificando_stock: "Verificando stock con el proveedor…",
  stock_confirmado: "Stock confirmado",
  pago_pendiente: "Esperando pago",
  pagado: "Pago recibido",
  contra_entrega_confirmado: "Confirmado — pagas al recibir",
  oc_emitida: "Comprado al proveedor",
  despachado: "Despachado",
  en_transito: "En camino",
  entregado: "Entregado",
  completado: "Completado",
  cancelado: "Cancelado",
  retractado: "Retracto ejercido",
};
