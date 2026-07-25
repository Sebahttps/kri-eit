import { Module } from "@nestjs/common";
import { AuthModule } from "./auth/auth.module";
import { CatalogModule } from "./catalog/catalog.module";
import { DbModule } from "./db/db.module";
import { OrdersModule } from "./orders/orders.module";
import { RealtimeModule } from "./realtime/realtime.module";
import { WebhooksModule } from "./webhooks/webhooks.module";

@Module({
  imports: [DbModule, AuthModule, CatalogModule, OrdersModule, WebhooksModule, RealtimeModule],
})
export class AppModule {}
