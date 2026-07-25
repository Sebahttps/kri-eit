"use client";

import { useEffect, useRef, useState } from "react";

type Mensaje = { rol: "cliente" | "agente"; texto: string };

/** Chat flotante con el Agente Front-Office (ventas y post-venta). */
export default function ChatWidget() {
  const [abierto, setAbierto] = useState(false);
  const [mensajes, setMensajes] = useState<Mensaje[]>([
    {
      rol: "agente",
      texto:
        "¡Hola! Soy el asistente de la tienda. Puedo verificar stock, buscar productos, revisar tu pedido, gestionar garantías o retractos. ¿En qué te ayudo?",
    },
  ]);
  const [texto, setTexto] = useState("");
  const [enviando, setEnviando] = useState(false);
  const conversationId = useRef<string | null>(null);
  const listaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listaRef.current?.scrollTo({ top: listaRef.current.scrollHeight });
  }, [mensajes, abierto]);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    const mensaje = texto.trim();
    if (!mensaje || enviando) return;
    setTexto("");
    setMensajes((m) => [...m, { rol: "cliente", texto: mensaje }]);
    setEnviando(true);
    try {
      const res = await fetch("/api/agents/front-office/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mensaje,
          conversation_id: conversationId.current,
        }),
      });
      if (!res.ok) throw new Error(String(res.status));
      const data = await res.json();
      conversationId.current = data.conversation_id;
      setMensajes((m) => [...m, { rol: "agente", texto: data.respuesta }]);
    } catch {
      setMensajes((m) => [
        ...m,
        {
          rol: "agente",
          texto:
            "No puedo responder en este momento. Escríbenos de nuevo en unos minutos o revisa tu pedido desde el link de confirmación.",
        },
      ]);
    } finally {
      setEnviando(false);
    }
  }

  if (!abierto) {
    return (
      <button
        onClick={() => setAbierto(true)}
        className="fixed bottom-5 right-5 z-20 flex h-14 w-14 items-center justify-center rounded-full text-2xl shadow-lg"
        style={{ backgroundColor: "var(--accent)", color: "var(--accent-ink)" }}
        aria-label="Abrir chat de ayuda"
      >
        💬
      </button>
    );
  }

  return (
    <div className="fixed bottom-5 right-5 z-20 flex h-[28rem] w-80 flex-col overflow-hidden rounded-xl bg-surface shadow-2xl"
         style={{ border: "1px solid rgb(var(--grid))" }}>
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{ backgroundColor: "var(--accent)", color: "var(--accent-ink)" }}
      >
        <span className="text-sm font-medium">Asistente de la tienda</span>
        <button onClick={() => setAbierto(false)} aria-label="Cerrar chat">✕</button>
      </div>

      <div ref={listaRef} className="flex-1 space-y-2 overflow-y-auto p-3">
        {mensajes.map((m, i) => (
          <p
            key={i}
            className={`max-w-[85%] whitespace-pre-wrap rounded-lg px-3 py-2 text-sm ${
              m.rol === "cliente" ? "ml-auto" : ""
            }`}
            style={
              m.rol === "cliente"
                ? { backgroundColor: "var(--series-1)", color: "#fff" }
                : { backgroundColor: "rgb(var(--grid) / 0.5)" }
            }
          >
            {m.texto}
          </p>
        ))}
        {enviando && <p className="text-xs text-muted">El asistente está escribiendo…</p>}
      </div>

      <form onSubmit={enviar} className="flex gap-2 border-t border-grid p-3">
        <input
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Escribe tu consulta…"
          className="min-w-0 flex-1 rounded-lg border border-grid bg-plane px-3 py-2 text-sm outline-none"
        />
        <button className="btn-accent" disabled={enviando || !texto.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
}
