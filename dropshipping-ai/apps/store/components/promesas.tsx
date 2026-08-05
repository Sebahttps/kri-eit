// Las 5 promesas de venta, siempre visibles. No es marketing: cada una está
// codificada como regla dura en el backend.
//
// Cada promesa se presenta como una burbuja de chat con doble check verde —
// el elemento firma de CompAI. La lectura es deliberada: "esto ya está
// entregado", no "esto te prometemos".
const PROMESAS = [
  "Stock confirmado con el proveedor antes de cobrarte",
  // Acotada a RM a propósito: el contra entrega se sostiene con capital de
  // trabajo, y un rechazo en entrega a región cuesta flete doble. Fuera de RM
  // se ofrece abono + saldo. Ver docs/modo-artesanal.md §4.
  "Paga al recibir en la Región Metropolitana",
  "Seguimiento en tiempo real de tu despacho",
  "Garantía legal de 6 meses, gestión inmediata",
  "10 días para retractarte, sin preguntas",
];

/** Doble check de confirmación. Decorativo: el texto de la promesa ya lo dice. */
function DobleCheck({ tam = 18 }: { tam?: number }) {
  return (
    <svg
      className="doble-check"
      width={tam}
      height={(tam * 2) / 3}
      viewBox="0 0 24 16"
      fill="none"
      stroke="currentColor"
      strokeWidth={2.2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M1 8.5 L5 12.5 L12 4" />
      <path d="M10 8.5 L14 12.5 L21 4" />
    </svg>
  );
}

export default function Promesas({ compacto = false }: { compacto?: boolean }) {
  if (compacto) {
    return (
      <ul className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-ink-2">
        {PROMESAS.map((texto) => (
          <li key={texto} className="flex items-center gap-1.5">
            <DobleCheck tam={14} />
            {texto}
          </li>
        ))}
      </ul>
    );
  }
  return (
    <ul className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
      {PROMESAS.map((texto) => (
        <li key={texto} className="burbuja flex items-start gap-2 text-sm">
          <span className="pt-1">
            <DobleCheck />
          </span>
          <span className="text-ink-2">{texto}</span>
        </li>
      ))}
    </ul>
  );
}
