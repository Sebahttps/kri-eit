import { Inject, Injectable, Logger } from "@nestjs/common";
import { createHmac, timingSafeEqual } from "crypto";
import { Pool } from "pg";
import { DB } from "../db/db.module";
import { OrdersService } from "../orders/orders.service";

const WEBHOOK_SECRET = () => process.env.SHOPIFY_WEBHOOK_SECRET ?? "";
const STORE_DOMAIN = () => process.env.SHOPIFY_STORE_DOMAIN ?? "";
const CLIENT_ID = () => process.env.SHOPIFY_CLIENT_ID ?? "";
const CLIENT_SECRET = () => process.env.SHOPIFY_CLIENT_SECRET ?? "";
/**
 * Solo para apps personalizadas creadas en el admin ANTES del 1-ene-2026:
 * ésas sí tienen un `shpat_` permanente. Las apps nuevas (Dev Dashboard) no
 * exponen token y deben usar SHOPIFY_CLIENT_ID/SHOPIFY_CLIENT_SECRET.
 */
const LEGACY_TOKEN = () => process.env.SHOPIFY_ADMIN_TOKEN ?? "";
// `||` y no `??`: el compose exporta la variable vacía cuando no se define,
// y "" produciría una URL inválida (/admin/api//graphql.json).
const API_VERSION = () => process.env.SHOPIFY_API_VERSION || "2026-04";

/** El token dura 24 h; lo renovamos con holgura para no usarlo recién vencido. */
const MARGEN_RENOVACION_MS = 5 * 60 * 1000;

/** El proyecto compila sin `lib: DOM`; el tipo Response sale del fetch de Node. */
type RespuestaFetch = Awaited<ReturnType<typeof fetch>>;

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

  /** Token de Admin API vigente (client credentials) y su vencimiento. */
  private token: { valor: string; venceEn: number } | null = null;
  /** Renovación en curso, para no pedir N tokens ante N pedidos simultáneos. */
  private renovacion: Promise<string | null> | null = null;

  constructor(
    @Inject(DB) private readonly db: Pool,
    private readonly orders: OrdersService,
  ) {}

  /**
   * Devuelve un token de Admin API, o null si no hay credenciales.
   *
   * Desde el 1-ene-2026 las apps del Dev Dashboard no exponen un `shpat_`
   * permanente: se intercambian Client ID + Client Secret por un token de
   * 24 h (client credentials grant). Requiere que la app y la tienda estén
   * en la MISMA organización de Shopify.
   */
  private async obtenerToken(): Promise<string | null> {
    if (LEGACY_TOKEN()) return LEGACY_TOKEN();
    if (!STORE_DOMAIN() || !CLIENT_ID() || !CLIENT_SECRET()) return null;
    if (this.token && Date.now() < this.token.venceEn) return this.token.valor;

    if (!this.renovacion) {
      this.renovacion = this.renovarToken().finally(() => {
        this.renovacion = null;
      });
    }
    return this.renovacion;
  }

  private async renovarToken(): Promise<string | null> {
    try {
      const resp = await fetch(`https://${STORE_DOMAIN()}/admin/oauth/access_token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "client_credentials",
          client_id: CLIENT_ID(),
          client_secret: CLIENT_SECRET(),
        }),
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status} ${await resp.text()}`);
      const datos = (await resp.json()) as { access_token?: string; expires_in?: number };
      if (!datos.access_token) throw new Error("respuesta sin access_token");

      const duracionMs = (datos.expires_in ?? 86399) * 1000;
      this.token = {
        valor: datos.access_token,
        venceEn: Date.now() + Math.max(duracionMs - MARGEN_RENOVACION_MS, 60_000),
      };
      this.log.log("Token de Admin API renovado (client credentials)");
      return this.token.valor;
    } catch (e) {
      // No cacheamos el fallo: el siguiente pedido vuelve a intentarlo.
      this.token = null;
      this.log.error(`No se pudo obtener el token de Admin API: ${e}`);
      return null;
    }
  }

  /** Llama a la Admin API REST con el token vigente. Null si no hay credenciales. */
  private async llamarAdminApi(
    ruta: string,
    init: { method?: string; body?: string } = {},
  ): Promise<RespuestaFetch | null> {
    const token = await this.obtenerToken();
    if (!token) return null;
    return fetch(`https://${STORE_DOMAIN()}/admin/api/${API_VERSION()}/${ruta}`, {
      method: init.method ?? "GET",
      headers: {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
      },
      body: init.body,
    });
  }

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
    try {
      const resp = await this.llamarAdminApi(`orders/${shopifyId}/cancel.json`, {
        method: "POST",
        body: JSON.stringify({ email: true, reason: "inventory", refund: null }),
      });
      if (!resp) {
        this.log.warn(
          `Pedido Shopify ${shopifyId} sin stock: cancelar y reembolsar MANUALMENTE ` +
            "(sin token de Admin API: revisa SHOPIFY_STORE_DOMAIN / SHOPIFY_CLIENT_ID / " +
            "SHOPIFY_CLIENT_SECRET, o el error de renovación en el log)",
        );
        return false;
      }
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

    const { rows } = await this.db.query(
      "SELECT shopify_order_id FROM shopify_orders WHERE order_id = $1",
      [orderId],
    );
    const shopifyId = rows[0]?.shopify_order_id;
    if (!shopifyId) return; // pedido de la tienda propia, no de Shopify

    try {
      const foResp = await this.llamarAdminApi(
        `orders/${shopifyId}/fulfillment_orders.json`,
      );
      if (!foResp) return; // sin credenciales: el tracking vive igual en la tienda propia
      if (!foResp.ok) throw new Error(`fulfillment_orders HTTP ${foResp.status}`);
      const cuerpo = (await foResp.json()) as { fulfillment_orders?: any[] };
      const abiertas = (cuerpo.fulfillment_orders ?? []).filter(
        (fo: any) => fo.status === "open" || fo.status === "in_progress",
      );
      if (!abiertas.length) return; // ya tiene fulfillment (reintento del carrier)

      const tracking = (
        await this.db.query(
          "SELECT tracking_url FROM shipments WHERE order_id = $1 AND tracking_number = $2",
          [orderId, evento.tracking_number],
        )
      ).rows[0];

      const resp = await this.llamarAdminApi("fulfillments.json", {
        method: "POST",
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
      });
      if (!resp) return;
      if (!resp.ok) throw new Error(`fulfillments HTTP ${resp.status}`);
      this.log.log(`Tracking ${evento.tracking_number} sincronizado al pedido Shopify ${shopifyId}`);
    } catch (e) {
      this.log.error(`No se pudo sincronizar tracking del pedido Shopify ${shopifyId}: ${e}`);
    }
  }
}
