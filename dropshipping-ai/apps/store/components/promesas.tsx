// Las 5 promesas de venta, siempre visibles. No es marketing: cada una está
// codificada como regla dura en el backend.
const PROMESAS = [
  { icono: "✔", texto: "Stock confirmado con el proveedor antes de cobrarte" },
  { icono: "💵", texto: "Paga al recibir si prefieres" },
  { icono: "📦", texto: "Seguimiento en tiempo real de tu despacho" },
  { icono: "🛡", texto: "Garantía legal de 6 meses, gestión inmediata" },
  { icono: "↩", texto: "10 días para retractarte, sin preguntas" },
];

export default function Promesas({ compacto = false }: { compacto?: boolean }) {
  if (compacto) {
    return (
      <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-ink-2">
        {PROMESAS.map((p) => (
          <li key={p.texto}>
            <span aria-hidden>{p.icono}</span> {p.texto}
          </li>
        ))}
      </ul>
    );
  }
  return (
    <div className="card">
      <ul className="grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-5">
        {PROMESAS.map((p) => (
          <li key={p.texto} className="flex items-start gap-2">
            <span aria-hidden className="text-base">{p.icono}</span>
            <span className="text-ink-2">{p.texto}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
