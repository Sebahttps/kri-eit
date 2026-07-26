import { Inject, Injectable, Logger } from "@nestjs/common";
import { createHmac, timingSafeEqual } from "crypto";
import { Pool } from "pg";
import { DB } from "../db/db.module";
import { OrdersService } from "../orders/orders.service";

const WEBHOOK_SECRET = () => process.env.SHOPIFY_WEBHOOK_SECRET ?? "";
const STORE_DOMAIN = () => process.env.SHOPIFY_STORE_DOMAIN ?? "";
const ADMIN_TOKEN = () => process.env.SHOPIFY_ADMIN_TOKEN ?? "";
const API_VERSION = "2024-01";

/**
 * Modo híbrido: Shopify es la vitrina y el checkout; los agentes siguen siendo
 * el back-office real. Un pedido creado en Shopify entra por webhook, se
 * registra como pedido interno y recorre el flujo existente (Agente B2B
 * verifica stock -> OC -> aprobación del Supervisor sobre el umbral).
 *
 * La promesa (a) queda degradada respecto de la tienda propia: Shopify cobra
 * antes de nuestra verificación, así que "nunca pagas sin stock" se convierte
 * en "cancelación y reembolso inmediatos si el proveedor no confirma stock".
 */
@Injectable()
export class ShopifyService {
  private readonly log = new Logger(ShopifyService.name);

  constructor(
    @Inject(DB) private readonly db: Pool,
    private readonly orders: OrdersService,
  ) {}

  /** Verifica la firma HMAC-SHA256 del webhook. Sin secreto configurado, rechaza. */
  verificarFirma(rawBody: Buffer | undefined, hmacHeader: string | undefined): boolean {
    const secret = WEBHOOK_SECRET();
    if (!secret || !rawBody || !hmacHeader) return false;
    const calculado = createHmac("sha256", secret).update(rawBody).digest("base64");
    const a = Buffer.from(calculado);
    const b = Buffer.from(hmacHeader);
    return a.length === b.length && timingSafeEqual(a, b);
  }

  /** Procesa orders/create: crea el pedido interno y dispara el flujo B2B. */
  async procesarPedido(payload: any, shopDomain: string) {
    const shopifyId: number = payload.id;

    // Shopify reintenta los webhooks: idempotencia por shopify_order_id.
    const existente = await this.db.query(
      "SELECT order_id FROM shopify_orders WHERE shopify_order_id = $1",
      [shopifyId],
    );
    if (existente.rows[0]) {
      return { ok: true, duplicado: true, order_id: existente.rows[0].order_id };
    }

    // Mapeo por SKU: el SKU de la variante en Shopify debe existir en products.
    const items: { product_id: string; cantidad: number }[] = [];
    const skusSinMapear: string[] = [];
    for (const li of payload.line_items ?? []) {
      const sku = li.sku?.trim();
      const producto = sku
        ? (await this.db.query("SELECT id FROM products WHERE sku = $1 AND activo", [sku])).rows[0]
        : undefined;
      if (!producto) {
        skusSinMapear.push(sku || `(sin SKU: ${li.title})`);
      } else {
        items.push({ product_id: producto.id, cantidad: li.quantity });
      }
    }
    if (skusSinMapear.length) {
      // 200 a propósito: un SKU mal mapeado no debe hacer reintentar a Shopify
      // eternamente. Queda en el log para corregir el mapeo y reprocesar a mano.
      this.log.warn(`Pedido Shopify ${shopifyId} sin mapear: ${skusSinMapear.join(", ")}`);
      return { ok: false, error: "skus_sin_mapear", skus: skusSinMapear };
    }

    const cliente = {
      nombre:
        [payload.customer?.first_name, payload.customer?.last_name].filter(Boolean).join(" ") ||
        payload.shipping_address?.name ||
        "Cliente Shopify",
      email: payload.customer?.email ?? payload.email ?? undefined,
      telefono: payload.customer?.phone ?? payload.shipping_address?.phone ?? undefined,
      direccion: payload.shipping_address
        ? [payload.shipping_address.address1, payload.shipping_address.city]
            .filter(Boolean)
            .join(", ")
        : undefined,
    };

    const pedido = await this.orders.crear(cliente, items);
    await this.db.query(
      `INSERT INTO shopify_orders (shopify_order_id, order_id, shop_domain)
       VALUES ($1, $2, $3)`,
      [shopifyId, pedido.order_id, shopDomain],
    );

    // COD (pago contra entrega, promesa b) vs. pago ya capturado por Shopify.
    const contraEntrega =
      (payload.payment_gateway_names ?? []).some((g: string) =>
        /cash on delivery|contra entrega|\bcod\b/i.test(g),
      ) || payload.financial_status === "pending";

    const resultado = await this.orders.checkout(
      pedido.order_id,
      contraEntrega ? "contra_entrega" : "online",
    );

    if (resultado.status === "sin_stock") {
      const cancelado = await this.cancelarEnShopify(shopifyId);
      return {
        ok: true,
        order_id: pedido.order_id,
        status: "sin_stock",
        productos_sin_stock: (resultado as any).productos_sin_stock,
        cancelado_en_shopify: cancelado,
      };
    }

    if (!contraEntrega) {
      // Shopify ya capturó el pago; se refleja internamente y se emite la OC.
      const pago = await this.orders.pagar(pedido.order_id);
      return { ok: true, order_id: pedido.order_id, ...pago };
    }
    return { ok: true, order_id: pedido.order_id, ...resultado };
  }

  /**
   * Cancela (con reembolso y email al cliente) un pedido sin stock confirmado.
   * Best-effort: sin credenciales de Admin API queda para gestión manual.
   */
  private async cancelarEnShopify(shopifyId: number): Promise<boolean> {
    if (!STORE_DOMAIN() || !ADMIN_TOKEN()) {
      this.log.warn(
        `Pedido Shopify ${shopifyId} sin stock: cancelar y reembolsar MANUALMENTE ` +
          "(SHOPIFY_STORE_DOMAIN/SHOPIFY_ADMIN_TOKEN no configurados)",
      );
      return false;
    }
    try {
      const resp = await fetch(
        `https://${STORE_DOMAIN()}/admin/api/${API_VERSION}/orders/${shopifyId}/cancel.json`,
        {
          method: "POST",
          headers: {
            "X-Shopify-Access-Token": ADMIN_TOKEN(),
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: true, reason: "inventory", refund: null }),
        },
      );
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      return true;
    } catch (e) {
      this.log.error(`No se pudo cancelar el pedido Shopify ${shopifyId}: ${e}`);
      return false;
    }
  }

  /**
   * Al primer 'despachado' del carrier, crea el fulfillment en Shopify con el
   * tracking, para que el cliente vea el seguimiento donde compró. Best-effort.
   */
  async sincronizarSeguimiento(
    orderId: string,
    evento: { status: string; carrier: string; tracking_number: string },
  ): Promise<void> {
    if (evento.status !== "despachado") return;
    if (!STORE_DOMAIN() || !ADMIN_TOKEN()) return;

    const { rows } = await this.db.query(
      "SELECT shopify_order_id FROM shopify_orders WHERE order_id = $1",
      [orderId],
    );
    const shopifyId = rows[0]?.shopify_order_id;
    if (!shopifyId) return; // pedido de la tienda propia, no de Shopify

    try {
      const headers = {
        "X-Shopify-Access-Token": ADMIN_TOKEN(),
        "Content-Type": "application/json",
      };
      const foResp = await fetch(
        `https://${STORE_DOMAIN()}/admin/api/${API_VERSION}/orders/${shopifyId}/fulfillment_orders.json`,
        { headers },
      );
      if (!foResp.ok) throw new Error(`fulfillment_orders HTTP ${foResp.status}`);
      const abiertas = ((await foResp.json()).fulfillment_orders ?? []).filter(
        (fo: any) => fo.status === "open" || fo.status === "in_progress",
      );
      if (!abiertas.length) return; // ya tiene fulfillment (reintento del carrier)

      const tracking = (
        await this.db.query(
          "SELECT tracking_url FROM shipments WHERE order_id = $1 AND tracking_number = $2",
          [orderId, evento.tracking_number],
        )
      ).rows[0];

      const resp = await fetch(
        `https://${STORE_DOMAIN()}/admin/api/${API_VERSION}/fulfillments.json`,
        {
          method: "POST",
          headers,
          body: JSON.stringify({
            fulfillment: {
              notify_customer: true,
              tracking_info: {
                number: evento.tracking_number,
                company: evento.carrier,
                url: tracking?.tracking_url ?? undefined,
              },
              line_items_by_fulfillment_order: abiertas.map((fo: any) => ({
                fulfillment_order_id: fo.id,
              })),
            },
          }),
        },
      );
      if (!resp.ok) throw new Error(`fulfillments HTTP ${resp.status}`);
      this.log.log(`Tracking ${evento.tracking_number} sincronizado al pedido Shopify ${shopifyId}`);
    } catch (e) {
      this.log.error(`No se pudo sincronizar tracking del pedido Shopify ${shopifyId}: ${e}`);
    }
  }
}
