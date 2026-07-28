import type { Metadata } from "next";
import CartDrawer from "@/components/cart-drawer";
import ChatWidget from "@/components/chat-widget";
import Header from "@/components/header";
import { CartProvider } from "@/lib/cart";
import "./globals.css";

export const metadata: Metadata = {
  title: "CompAI — te confirmamos el stock antes de cobrarte",
  description:
    "Te confirmamos el stock, pagas al recibir y la garantía responde. Palabra de CompAI.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <CartProvider>
          <Header />
          {children}
          <CartDrawer />
          <ChatWidget />
        </CartProvider>
      </body>
    </html>
  );
}
