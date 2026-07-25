import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "KRI-EIT · Panel del Supervisor",
  description: "Dropshipping autónomo gestionado por Agentes IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
