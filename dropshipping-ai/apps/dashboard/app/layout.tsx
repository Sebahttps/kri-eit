import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CompAI · Panel del Supervisor",
  description: "Back-office de CompAI gestionado por Agentes IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
