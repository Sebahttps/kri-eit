import {
  Controller,
  Headers,
  Post,
  Req,
  UnauthorizedException,
} from "@nestjs/common";
import type { RawBodyRequest } from "@nestjs/common";
import type { Request } from "express";
import { ShopifyService } from "./shopify.service";

@Controller("webhooks")
export class ShopifyController {
  constructor(private readonly shopify: ShopifyService) {}

  /**
   * Webhook de Shopify (modo híbrido). Registrar en Shopify el topic
   * orders/create apuntando a POST /webhooks/shopify; la firma se valida
   * contra SHOPIFY_WEBHOOK_SECRET sobre el cuerpo crudo.
   */
  @Post("shopify")
  async shopifyWebhook(
    @Req() req: RawBodyRequest<Request>,
    @Headers("x-shopify-hmac-sha256") hmac?: string,
    @Headers("x-shopify-topic") topic?: string,
    @Headers("x-shopify-shop-domain") shopDomain?: string,
  ) {
    if (!this.shopify.verificarFirma(req.rawBody, hmac)) {
      throw new UnauthorizedException("Firma HMAC de Shopify inválida o secreto no configurado");
    }
    if (topic !== "orders/create") {
      return { ok: true, ignorado: topic ?? "sin topic" };
    }
    const payload = JSON.parse(req.rawBody!.toString("utf8"));
    return this.shopify.procesarPedido(payload, shopDomain ?? "desconocido");
  }
}
