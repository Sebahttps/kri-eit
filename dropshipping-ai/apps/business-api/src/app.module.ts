import { Module } from "@nestjs/common";
import { AuthModule } from "./auth/auth.module";
import { CatalogModule } from "./catalog/catalog.module";
import { DbModule } from "./db/db.module";
import { HealthModule } from "./health/health.module";
import { OrdersModule } from "./orders/orders.module";
import { RealtimeModule } from "./realtime/realtime.module";
import { ShopifyModule } from "./shopify/shopify.module";
import { WebhooksModule } from "./webhooks/webhooks.module";

@Module({
  imports: [
    DbModule,
    HealthModule,
    AuthModule,
    CatalogModule,
    OrdersModule,
    ShopifyModule,
    WebhooksModule,
    RealtimeModule,
  ],
})
export class AppModule {}
