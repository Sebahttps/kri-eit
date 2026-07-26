import { Module } from "@nestjs/common";
import { ShopifyModule } from "../shopify/shopify.module";
import { WebhooksController } from "./webhooks.controller";

@Module({ imports: [ShopifyModule], controllers: [WebhooksController] })
export class WebhooksModule {}
