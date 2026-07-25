import type { Metadata } from "next";
import CartDrawer from "@/components/cart-drawer";
import ChatWidget from "@/components/chat-widget";
import Header from "@/components/header";
import { CartProvider } from "@/lib/cart";
import "./globals.css";

export const metadata: Metadata = {
  title: "KRI·Tienda — productos en tendencia con garantías reales",
  description:
    "Stock confirmado antes de cobrarte, pago contra entrega, seguimiento en vivo, garantía de 6 meses y 10 días de retracto.",
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
